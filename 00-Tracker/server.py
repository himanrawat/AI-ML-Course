#!/usr/bin/env python3
"""AI/ML course learning tracker - local server and command-line tool.

The course folders are the source of truth: every request rescans them, so new,
renamed and deleted topic files are picked up automatically. Progress is stored
in 00-Tracker/progress.json, keyed by each topic's stable "# ID:" header.

Usage (from the AI-ML-Course folder; standard library only, any Python 3.10+):
    python3 00-Tracker/server.py                 start the dashboard (http://127.0.0.1:8765)
    python3 00-Tracker/server.py status          print a progress summary
    python3 00-Tracker/server.py sync            rescan, then regenerate PROGRESS.md and COURSE-MAP.md
    python3 00-Tracker/server.py check-links     verify every topic can be opened in the editor
    python3 00-Tracker/server.py open <topic>    open a topic file in the editor
    python3 00-Tracker/server.py mark <topic> <requirement> [--undo]

<topic> is a topic ID (python.variables.basics) or a path (01-Python/01-Variables/01-basics.py).
Set TRACKER_EDITOR (code, cursor, windsurf, codium) to choose the editor command.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import webbrowser
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import quote

TRACKER_DIR = Path(__file__).resolve().parent
COURSE_ROOT = TRACKER_DIR.parent
REQUIREMENTS = ("theory", "beginner", "intermediate", "advanced", "assessment")
EXERCISES = ("beginner", "intermediate", "advanced")
MODULE_DIR = re.compile(r"^\d{2}-.+$")
TOPIC_FILE = re.compile(r"^\d{2}-.+\.py$")
QUESTION_LINE = re.compile(r"^# QUESTION \d+:\s*(BEGINNER|INTERMEDIATE|ADVANCED)\s*$")
STATIC_FILES = {"/": "index.html", "/index.html": "index.html",
                "/tracker.css": "tracker.css", "/tracker.js": "tracker.js"}
CONTENT_TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
                 ".js": "text/javascript; charset=utf-8"}

TITLE_WORDS = {
    "API": "API", "AI": "AI", "ML": "ML", "LLM": "LLM", "LLMS": "LLMs", "RAG": "RAG", "MCP": "MCP",
    "SQL": "SQL", "CSV": "CSV", "JSON": "JSON", "HTTP": "HTTP", "PCA": "PCA", "CNNS": "CNNs", "GPT": "GPT",
    "GIT": "Git", "LORA": "LoRA", "FASTAPI": "FastAPI", "PYTORCH": "PyTorch", "NUMPY": "NumPy",
    "PANDAS": "pandas", "PYTEST": "pytest", "PATHLIB": "pathlib", "PYPROJECT": "pyproject",
    "DTYPES": "dtypes", "DATAFRAMES": "DataFrames", "DATALOADERS": "DataLoaders", "NN.MODULE": "nn.Module",
    "REACT": "ReAct", "CI/CD": "CI/CD", "A/B": "A/B", "IF": "if", "ELIF": "elif", "ELSE": "else",
    "TRY": "try", "EXCEPT": "except", "BREAK": "break", "CONTINUE": "continue", "PASS": "pass",
    "ASYNC": "async", "AWAIT": "await", "MATCH-CASE": "match-case", "VS": "vs",
    "TRAIN/VALIDATION/TEST": "Train/Validation/Test",
}
SMALL_WORDS = {"a", "an", "and", "as", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with"}


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def pretty_title(raw):
    words = []
    for index, word in enumerate(raw.split()):
        stripped = word.lstrip("(\"'")
        lead = word[:len(word) - len(stripped)]
        core = stripped.rstrip("),:.\"'")
        trail = stripped[len(core):]
        if core.upper() in TITLE_WORDS:
            core = TITLE_WORDS[core.upper()]
        elif index > 0 and core.lower() in SMALL_WORDS:
            core = core.lower()
        else:
            core = "-".join(part[:1].upper() + part[1:].lower() for part in core.split("-"))
        words.append(lead + core + trail)
    return " ".join(words)


def display_name(folder_name):
    return re.sub(r"^\d{2}-", "", folder_name).replace("-", " ")


def parse_topic(path):
    """Read a topic file's header and exercise areas. Returns None if it has no TOPIC/ID header."""
    text = path.read_text(encoding="utf-8", errors="replace")
    title = re.search(r"^# TOPIC:(.+)$", text, re.M)
    topic_id = re.search(r"^# ID:\s*(\S+)\s*$", text, re.M)
    if not (title and topic_id):
        return None
    level = re.search(r"^# LEVEL:\s*(\w+)", text, re.M)
    lines = text.splitlines()
    questions = [(i, m.group(1).lower()) for i, line in enumerate(lines) if (m := QUESTION_LINE.match(line))]
    exercises = {}
    for n, (start, name) in enumerate(questions):
        end = questions[n + 1][0] if n + 1 < len(questions) else len(lines)
        code_at = next((j for j in range(start, end) if lines[j].strip() == "# YOUR CODE:"), None)
        has_code = code_at is not None and any(
            line.strip() and not line.lstrip().startswith("#") for line in lines[code_at + 1:end])
        exercises[name] = {"line": start + 1, "codeLine": (code_at + 1) if code_at is not None else None,
                           "hasCode": has_code}
    return {"id": topic_id.group(1), "title": pretty_title(title.group(1).strip()),
            "level": level.group(1).lower() if level else "unknown", "exercises": exercises}


class TrackerError(Exception):
    def __init__(self, message, status=HTTPStatus.BAD_REQUEST):
        super().__init__(message)
        self.status = status


class Tracker:
    def __init__(self, root=COURSE_ROOT, tracker_dir=None):
        self.root = Path(root).resolve()
        self.tracker_dir = Path(tracker_dir).resolve() if tracker_dir else self.root / "00-Tracker"
        self.progress_path = self.tracker_dir / "progress.json"
        self.path_file = self.tracker_dir / "learning-path.json"
        self.lock = threading.RLock()

    # ---------- storage ----------
    def load_progress(self):
        if not self.progress_path.exists():
            return {"schemaVersion": 1, "updatedAt": None, "topics": {}}
        try:
            data = json.loads(self.progress_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise TrackerError(f"progress.json is not valid JSON ({error}). Fix or restore it; "
                               "the tracker will not overwrite it.", HTTPStatus.INTERNAL_SERVER_ERROR)
        data.setdefault("schemaVersion", 1)
        data.setdefault("topics", {})
        return data

    def save_progress(self, data):
        data["updatedAt"] = now_iso()
        temp = self.progress_path.with_suffix(".json.tmp")
        temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(temp, self.progress_path)

    # ---------- scanning ----------
    def scan(self):
        topics, issues, seen = [], [], {}
        for module_dir in sorted(p for p in self.root.iterdir() if p.is_dir()):
            if not MODULE_DIR.match(module_dir.name) or module_dir.resolve() == self.tracker_dir:
                continue
            for path in sorted(module_dir.rglob("*.py")):
                relative = path.relative_to(self.root)
                if not TOPIC_FILE.match(path.name) or any(
                        part.startswith(".") or part == "__pycache__" for part in relative.parts):
                    continue
                meta = parse_topic(path)
                if meta is None:
                    issues.append({"type": "invalid", "path": relative.as_posix(),
                                   "message": "Topic file has no '# TOPIC:' / '# ID:' header, so it can't be tracked."})
                    continue
                if meta["id"] in seen:
                    issues.append({"type": "duplicate", "path": relative.as_posix(),
                                   "message": f"ID '{meta['id']}' is already used by {seen[meta['id']]}; "
                                              "this file is ignored until its ID is changed."})
                    continue
                seen[meta["id"]] = relative.as_posix()
                section_parts = relative.parts[1:-1]
                meta.update({
                    "path": relative.as_posix(),
                    "module": module_dir.name,
                    "moduleName": display_name(module_dir.name),
                    "section": "/".join(section_parts),
                    "sectionName": " / ".join(display_name(p) for p in section_parts) or "General",
                })
                topics.append(meta)
        return topics, issues

    def learning_order(self, topics):
        """Topic IDs in recommended order: learning-path.json entries first, then folder order."""
        by_path = {t["path"]: t["id"] for t in topics}
        order, placed, unknown = [], set(), []
        entries = json.loads(self.path_file.read_text(encoding="utf-8"))["order"] if self.path_file.exists() else []
        for entry in entries:
            entry = entry.strip("/")
            matched = [t["id"] for t in topics if t["path"] == entry or t["path"].startswith(entry + "/")]
            if not matched:
                unknown.append(entry)
            for topic_id in matched:
                if topic_id not in placed:
                    order.append(topic_id)
                    placed.add(topic_id)
        order += [t["id"] for t in topics if t["id"] not in placed]
        return order, unknown, by_path

    def reconcile(self, topics, data):
        """Align progress.json with the files on disk. Returns (changed, events)."""
        events = []
        stored = data["topics"]
        scanned = {t["id"]: t for t in topics}
        new_ids = [i for i in scanned if i not in stored]
        for topic_id, entry in list(stored.items()):
            if topic_id in scanned or entry.get("missingSince"):
                continue
            # ID edited but the file stayed at the same path: carry progress over to the new ID.
            successor = next((n for n in new_ids if scanned[n]["path"] == entry.get("path")), None)
            if successor:
                stored[successor] = {**entry, "title": scanned[successor]["title"]}
                new_ids.remove(successor)
                entry["missingSince"] = "migrated"
                events.append({"type": "id-changed", "from": topic_id, "to": successor, "path": entry.get("path")})
        for topic_id in [i for i, e in stored.items() if e.get("missingSince") == "migrated"]:
            del stored[topic_id]
        for topic_id, topic in scanned.items():
            entry = stored.get(topic_id)
            if entry is None:
                stored[topic_id] = {"path": topic["path"], "title": topic["title"],
                                    "requirements": {r: None for r in REQUIREMENTS},
                                    "lastOpenedAt": None, "missingSince": None}
                events.append({"type": "new", "id": topic_id, "path": topic["path"]})
                continue
            entry.setdefault("requirements", {})
            for requirement in REQUIREMENTS:
                entry["requirements"].setdefault(requirement, None)
            if entry.get("path") != topic["path"]:
                events.append({"type": "moved", "id": topic_id, "from": entry.get("path"), "to": topic["path"]})
                entry["path"] = topic["path"]
            if entry.get("missingSince"):
                events.append({"type": "restored", "id": topic_id, "path": topic["path"]})
                entry["missingSince"] = None
            entry["title"] = topic["title"]
        for topic_id, entry in stored.items():
            if topic_id not in scanned and not entry.get("missingSince"):
                entry["missingSince"] = now_iso()
                events.append({"type": "missing", "id": topic_id, "path": entry.get("path")})
        return bool(events), events

    # ---------- state ----------
    @staticmethod
    def topic_status(entry, topic):
        done = [r for r in REQUIREMENTS if entry["requirements"].get(r)]
        if len(done) == len(REQUIREMENTS):
            return "completed"
        if done or any(e["hasCode"] for e in topic["exercises"].values()):
            return "in_progress"
        return "not_started"

    def build_state(self, topics, data, scan_issues, events):
        order, unknown_entries, _ = self.learning_order(topics)
        position = {topic_id: n + 1 for n, topic_id in enumerate(order)}
        stored = data["topics"]
        enriched = []
        for topic in topics:
            entry = stored[topic["id"]]
            absolute = (self.root / topic["path"]).resolve()
            enriched.append({
                **topic,
                "requirements": entry["requirements"],
                "lastOpenedAt": entry.get("lastOpenedAt"),
                "status": self.topic_status(entry, topic),
                "pathOrder": position[topic["id"]],
                "editorUrl": f"vscode://file{quote(str(absolute))}:1",
            })
        by_id = {t["id"]: t for t in enriched}

        modules = []
        for module in dict.fromkeys(t["module"] for t in enriched):
            module_topics = [t for t in enriched if t["module"] == module]
            sections = []
            for section in dict.fromkeys(t["section"] for t in module_topics):
                section_topics = [t for t in module_topics if t["section"] == section]
                sections.append({"section": section, "name": section_topics[0]["sectionName"],
                                 **self.summarise(section_topics), "topicIds": [t["id"] for t in section_topics]})
            modules.append({"module": module, "name": module_topics[0]["moduleName"],
                            **self.summarise(module_topics), "sections": sections})

        def activity(topic):
            stamps = [topic["lastOpenedAt"]] + list(topic["requirements"].values())
            return max((s for s in stamps if s), default=None)

        active = [t for t in enriched if t["status"] != "completed" and activity(t)]
        current = max(active, key=activity, default=None)
        upcoming = [by_id[i] for i in order if by_id[i]["status"] != "completed"]
        next_topic = next((t for t in upcoming if not current or t["id"] != current["id"]), None)

        issues = list(scan_issues)
        for topic_id, entry in stored.items():
            if entry.get("missingSince"):
                done = sum(1 for v in entry["requirements"].values() if v)
                issues.append({"type": "missing", "id": topic_id, "path": entry.get("path"),
                               "message": f"File not found (last seen at {entry.get('path')}). "
                                          f"{done} saved requirement(s) are kept until you restore the file "
                                          "with the same ID or forget this entry."})
        for entry in unknown_entries:
            issues.append({"type": "learning-path", "path": entry,
                           "message": "learning-path.json refers to a file or folder that no longer exists."})

        overall = self.summarise(enriched)
        return {
            "generatedAt": now_iso(),
            "courseRoot": str(self.root),
            "requirements": list(REQUIREMENTS),
            "summary": {**overall,
                        "totalModules": len(modules),
                        "completedModules": sum(1 for m in modules if m["topics"] and m["completedTopics"] == m["topics"])},
            "currentTopic": current["id"] if current else None,
            "nextTopic": next_topic["id"] if next_topic else None,
            "learningPath": order,
            "modules": modules,
            "topics": enriched,
            "issues": issues,
            "events": events,
            "editor": self.editor_label(),
        }

    @staticmethod
    def summarise(topics):
        total_requirements = len(topics) * len(REQUIREMENTS)
        done = sum(1 for t in topics for r in REQUIREMENTS if t["requirements"].get(r))
        exercises_done = sum(1 for t in topics for r in EXERCISES if t["requirements"].get(r))
        completed = sum(1 for t in topics if t["status"] == "completed")
        in_progress = sum(1 for t in topics if t["status"] == "in_progress")
        return {
            "topics": len(topics), "completedTopics": completed, "inProgressTopics": in_progress,
            "remainingTopics": len(topics) - completed,
            "requirementsDone": done, "requirementsTotal": total_requirements,
            "exercisesDone": exercises_done, "exercisesTotal": len(topics) * len(EXERCISES),
            "percent": round(100 * done / total_requirements, 1) if total_requirements else 0.0,
        }

    def state(self):
        with self.lock:
            topics, issues = self.scan()
            data = self.load_progress()
            changed, events = self.reconcile(topics, data)
            if changed:
                self.save_progress(data)
            state = self.build_state(topics, data, issues, events)
            self.write_reports(state)
            return state

    # ---------- actions ----------
    def resolve(self, key, topics=None):
        topics = topics if topics is not None else self.scan()[0]
        key = key.strip().removeprefix("./")
        for topic in topics:
            if key in (topic["id"], topic["path"]):
                return topic
        raise TrackerError(f"Unknown topic '{key}'. Use a topic ID or a path relative to the course folder.",
                           HTTPStatus.NOT_FOUND)

    def set_requirement(self, key, requirement, done):
        if requirement not in REQUIREMENTS:
            raise TrackerError(f"Unknown requirement '{requirement}'. Use one of: {', '.join(REQUIREMENTS)}.")
        with self.lock:
            topics, _ = self.scan()
            topic = self.resolve(key, topics)
            data = self.load_progress()
            self.reconcile(topics, data)
            requirements = data["topics"][topic["id"]]["requirements"]
            if done:
                if requirement in EXERCISES and not topic["exercises"].get(requirement, {}).get("hasCode"):
                    raise TrackerError(f"Write your {requirement} solution under its '# YOUR CODE:' line in "
                                       f"{topic['path']} first - an empty exercise can't be marked complete.",
                                       HTTPStatus.CONFLICT)
                if requirement == "assessment":
                    missing = [r for r in REQUIREMENTS[:-1] if not requirements.get(r)]
                    if missing:
                        raise TrackerError(f"Complete {', '.join(missing)} before the final assessment.",
                                           HTTPStatus.CONFLICT)
                requirements[requirement] = requirements.get(requirement) or now_iso()
            else:
                requirements[requirement] = None
                if requirement != "assessment":
                    requirements["assessment"] = None
            self.save_progress(data)
        return self.state()

    def editor_command(self, absolute, line=1):
        preferred = os.environ.get("TRACKER_EDITOR")
        for name in ([preferred] if preferred else ["code", "cursor", "windsurf", "codium"]):
            executable = shutil.which(name)
            if executable:
                return [executable, "--reuse-window", "--goto", f"{absolute}:{line}"]
        if preferred:
            raise TrackerError(f"TRACKER_EDITOR='{preferred}' was not found on PATH.", HTTPStatus.INTERNAL_SERVER_ERROR)
        if sys.platform == "darwin" and Path("/Applications/Visual Studio Code.app").exists():
            return ["open", "-a", "Visual Studio Code", str(absolute)]
        return None

    def editor_label(self):
        try:
            command = self.editor_command(self.root, 1)
        except TrackerError as error:
            return {"available": False, "message": str(error)}
        if not command:
            return {"available": False, "message": "No editor command found; links fall back to vscode:// URLs."}
        return {"available": True, "command": Path(command[0]).name}

    def open_topic(self, key, exercise=None, dry_run=False):
        with self.lock:
            topics, _ = self.scan()
            topic = self.resolve(key, topics)
            absolute = (self.root / topic["path"]).resolve()
            if not absolute.is_file() or self.root not in absolute.parents:
                raise TrackerError(f"{topic['path']} is not a file inside the course folder.", HTTPStatus.NOT_FOUND)
            line = 1
            if exercise:
                if exercise not in topic["exercises"]:
                    raise TrackerError(f"{topic['path']} has no {exercise} exercise.", HTTPStatus.NOT_FOUND)
                line = topic["exercises"][exercise]["codeLine"] or topic["exercises"][exercise]["line"]
            command = self.editor_command(absolute, line)
            url = f"vscode://file{quote(str(absolute))}:{line}"
            result = {"id": topic["id"], "path": topic["path"], "line": line, "url": url,
                      "command": command, "opened": False, "dryRun": dry_run}
            if not dry_run:
                if not command:
                    raise TrackerError("No editor command available; open the vscode:// link instead.",
                                       HTTPStatus.SERVICE_UNAVAILABLE)
                completed = subprocess.run(command, capture_output=True, text=True, timeout=20)
                if completed.returncode != 0:
                    raise TrackerError(f"Editor command failed: {completed.stderr.strip() or completed.returncode}",
                                       HTTPStatus.INTERNAL_SERVER_ERROR)
                result["opened"] = True
                data = self.load_progress()
                self.reconcile(topics, data)
                data["topics"][topic["id"]]["lastOpenedAt"] = now_iso()
                self.save_progress(data)
            return result

    def forget(self, topic_id):
        with self.lock:
            data = self.load_progress()
            entry = data["topics"].get(topic_id)
            if not entry or not entry.get("missingSince"):
                raise TrackerError("Only entries whose file is missing can be forgotten.", HTTPStatus.CONFLICT)
            del data["topics"][topic_id]
            self.save_progress(data)
        return self.state()

    # ---------- generated Markdown ----------
    def write_reports(self, state):
        self._write_if_changed(self.root / "PROGRESS.md", self.render_progress(state))
        self._write_if_changed(self.root / "COURSE-MAP.md", self.render_course_map(state))

    @staticmethod
    def _write_if_changed(path, content):
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            path.write_text(content, encoding="utf-8")

    @staticmethod
    def render_progress(state):
        by_id = {t["id"]: t for t in state["topics"]}
        s = state["summary"]
        tick = lambda value: "✓" if value else "·"
        lines = ["# Progress", "",
                 "<!-- Generated by 00-Tracker/server.py from progress.json. Do not edit by hand. -->", "",
                 f"**Overall:** {s['percent']}% of requirements · {s['completedTopics']}/{s['topics']} topics completed · "
                 f"{s['inProgressTopics']} in progress · {s['completedModules']}/{s['totalModules']} modules completed", ""]
        for label, key in (("Current topic", "currentTopic"), ("Next recommended", "nextTopic")):
            topic = by_id.get(state[key])
            lines.append(f"- **{label}:** " + (f"[{topic['title']}]({topic['path']})" if topic else "none"))
        lines += ["", "Columns: Theory · Beginner · Intermediate · Advanced · Assessment (✓ done, · not yet)", ""]
        for module in state["modules"]:
            lines += [f"## {module['name']} — {module['percent']}% ({module['completedTopics']}/{module['topics']} topics)", "",
                      "| Topic | T | B | I | A | Assess |", "|---|---|---|---|---|---|"]
            for section in module["sections"]:
                for topic_id in section["topicIds"]:
                    topic = by_id[topic_id]
                    r = topic["requirements"]
                    lines.append(f"| [{topic['title']}]({topic['path']}) | " +
                                 " | ".join(tick(r[k]) for k in REQUIREMENTS) + " |")
            lines.append("")
        return "\n".join(lines)

    @staticmethod
    def render_course_map(state):
        by_id = {t["id"]: t for t in state["topics"]}
        lines = ["# Course Map", "",
                 "<!-- Generated by 00-Tracker/server.py from the course folders. Do not edit by hand. -->", "",
                 f"{state['summary']['topics']} topics in {state['summary']['totalModules']} modules. "
                 "The **#** column is the recommended learning order: maths topics are interleaved just before "
                 "the ML topics that use them (configured in `00-Tracker/learning-path.json`).", ""]
        for module in state["modules"]:
            lines += [f"## {module['name']}", ""]
            for section in module["sections"]:
                lines += [f"### {section['name']}", "", "| # | Topic | Level | File |", "|---|---|---|---|"]
                for topic_id in section["topicIds"]:
                    t = by_id[topic_id]
                    lines.append(f"| {t['pathOrder']} | {t['title']} | {t['level']} | [{t['path']}]({t['path']}) |")
                lines.append("")
        return "\n".join(lines)


# ---------- HTTP server ----------
class Handler(BaseHTTPRequestHandler):
    tracker = None

    def log_message(self, fmt, *args):
        if os.environ.get("TRACKER_VERBOSE"):
            super().log_message(fmt, *args)

    def _allowed_origin(self):
        port = self.server.server_port
        allowed_hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        if self.headers.get("Host") not in allowed_hosts:
            return False
        origin = self.headers.get("Origin")
        return origin is None or origin in {f"http://{h}" for h in allowed_hosts}

    def _send(self, status, body, content_type="application/json; charset=utf-8"):
        payload = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(payload)

    def _guard(self):
        if not self._allowed_origin():
            self._send(HTTPStatus.FORBIDDEN, {"error": "Requests are only accepted from this local tracker page."})
            return False
        return True

    def do_GET(self):
        if not self._guard():
            return
        path = self.path.split("?", 1)[0]
        try:
            if path == "/api/state":
                return self._send(HTTPStatus.OK, self.tracker.state())
            if path in STATIC_FILES:
                file = TRACKER_DIR / STATIC_FILES[path]
                return self._send(HTTPStatus.OK, file.read_bytes(), CONTENT_TYPES[file.suffix])
            self._send(HTTPStatus.NOT_FOUND, {"error": "Not found"})
        except TrackerError as error:
            self._send(error.status, {"error": str(error)})

    def do_POST(self):
        if not self._guard():
            return
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            return self._send(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "Use Content-Type: application/json."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(min(length, 65536)) or b"{}")
            if self.path == "/api/progress":
                return self._send(HTTPStatus.OK, self.tracker.set_requirement(
                    str(body["id"]), str(body["requirement"]), bool(body["done"])))
            if self.path == "/api/open":
                dry_run = bool(body.get("dryRun")) or os.environ.get("TRACKER_DRY_RUN") == "1"
                return self._send(HTTPStatus.OK, self.tracker.open_topic(
                    str(body["id"]), body.get("exercise"), dry_run=dry_run))
            if self.path == "/api/forget":
                return self._send(HTTPStatus.OK, self.tracker.forget(str(body["id"])))
            self._send(HTTPStatus.NOT_FOUND, {"error": "Not found"})
        except TrackerError as error:
            self._send(error.status, {"error": str(error)})
        except (KeyError, ValueError) as error:
            self._send(HTTPStatus.BAD_REQUEST, {"error": f"Bad request: {error}"})


def make_server(tracker, port=8765, host="127.0.0.1"):
    handler = type("TrackerHandler", (Handler,), {"tracker": tracker})
    return ThreadingHTTPServer((host, port), handler)


# ---------- command line ----------
def print_status(state):
    s = state["summary"]
    by_id = {t["id"]: t for t in state["topics"]}
    print(f"Overall {s['percent']}% | topics {s['completedTopics']}/{s['topics']} completed, "
          f"{s['inProgressTopics']} in progress, {s['remainingTopics']} remaining | "
          f"modules {s['completedModules']}/{s['totalModules']} | exercises {s['exercisesDone']}/{s['exercisesTotal']}")
    for module in state["modules"]:
        bar = "#" * round(module["percent"] / 5)
        print(f"  {module['name']:<22} [{bar:<20}] {module['percent']:5.1f}%  "
              f"{module['completedTopics']}/{module['topics']} topics")
    for label, key in (("Current", "currentTopic"), ("Next", "nextTopic")):
        topic = by_id.get(state[key])
        print(f"{label}: " + (f"{topic['title']} ({topic['path']})" if topic else "none"))
    for issue in state["issues"]:
        print(f"! {issue['type']}: {issue.get('path')} - {issue['message']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description="AI/ML course learning tracker")
    sub = parser.add_subparsers(dest="command")
    serve = sub.add_parser("serve", help="start the dashboard (default)")
    serve.add_argument("--port", type=int, default=8765)
    serve.add_argument("--no-browser", action="store_true")
    sub.add_parser("status", help="print a progress summary")
    sub.add_parser("sync", help="rescan folders and regenerate PROGRESS.md and COURSE-MAP.md")
    sub.add_parser("check-links", help="verify every topic resolves to a file the editor can open")
    open_cmd = sub.add_parser("open", help="open a topic in the editor")
    open_cmd.add_argument("topic")
    open_cmd.add_argument("--exercise", choices=EXERCISES)
    mark = sub.add_parser("mark", help="mark a requirement complete (or --undo)")
    mark.add_argument("topic")
    mark.add_argument("requirement", choices=REQUIREMENTS)
    mark.add_argument("--undo", action="store_true")
    args = parser.parse_args(argv)
    tracker = Tracker()

    try:
        if args.command in (None, "serve"):
            port = getattr(args, "port", 8765)
            try:
                server = make_server(tracker, port)
            except OSError:
                sys.exit(f"Port {port} is busy. Try: python3 00-Tracker/server.py serve --port {port + 1}")
            tracker.state()
            url = f"http://127.0.0.1:{server.server_port}"
            print(f"Learning tracker running at {url}  (Ctrl+C to stop)")
            if not getattr(args, "no_browser", False):
                webbrowser.open(url)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("\nStopped.")
        elif args.command in ("status", "sync"):
            state = tracker.state()
            if args.command == "sync":
                for event in state["events"]:
                    print(f"{event['type']}: {event.get('id') or event.get('to')} {event.get('path', '')}")
                print("PROGRESS.md and COURSE-MAP.md are up to date.")
            print_status(state)
        elif args.command == "check-links":
            state = tracker.state()
            failures = []
            for topic in state["topics"]:
                try:
                    result = tracker.open_topic(topic["id"], dry_run=True)
                    if not result["command"] and not result["url"].startswith("vscode://file/"):
                        failures.append((topic["path"], "no editor command or URL"))
                    for exercise in topic["exercises"]:
                        tracker.open_topic(topic["id"], exercise, dry_run=True)
                except TrackerError as error:
                    failures.append((topic["path"], str(error)))
            print(f"Checked {len(state['topics'])} topic links (+ exercise links) using "
                  f"{state['editor'].get('command', 'vscode:// URLs')}.")
            for path, message in failures:
                print(f"  FAIL {path}: {message}")
            print("All links OK." if not failures else f"{len(failures)} problem(s).")
            sys.exit(1 if failures else 0)
        elif args.command == "open":
            result = tracker.open_topic(args.topic, args.exercise)
            print(f"Opened {result['path']}:{result['line']}")
        elif args.command == "mark":
            state = tracker.set_requirement(args.topic, args.requirement, not args.undo)
            topic = tracker.resolve(args.topic)
            entry = next(t for t in state["topics"] if t["id"] == topic["id"])
            print(f"{topic['path']}: {args.requirement} {'cleared' if args.undo else 'done'} -> status {entry['status']}")
    except TrackerError as error:
        sys.exit(f"Error: {error}")


if __name__ == "__main__":
    main()
