"""Tests for the learning tracker. Run: python3 -m unittest 00-Tracker/test_tracker.py -v"""

import http.client
import json
import shutil
import sys
import tempfile
import threading
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from server import Tracker, TrackerError, make_server, parse_topic  # noqa: E402

TEMPLATE = """# ======================================
# TOPIC: {title}
# LEVEL: BEGINNER
# ID: {topic_id}
# ======================================

# THEORY
x = 1

# ======================================
# QUESTION 1: BEGINNER
# ======================================
# Task.

# YOUR CODE:
{beginner}

# ======================================
# QUESTION 2: INTERMEDIATE
# ======================================
# Task.

# YOUR CODE:
{intermediate}

# ======================================
# QUESTION 3: ADVANCED
# ======================================
# Task.

# YOUR CODE:
{advanced}
"""


def write_topic(path, topic_id, title="SAMPLE TOPIC", beginner="", intermediate="", advanced=""):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE.format(topic_id=topic_id, title=title, beginner=beginner,
                                    intermediate=intermediate, advanced=advanced))


class TrackerTestCase(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "00-Tracker").mkdir()
        write_topic(self.root / "01-Python/01-Variables/01-basics.py", "py.basics", "PYTHON VARIABLES")
        write_topic(self.root / "01-Python/01-Variables/02-types.py", "py.types")
        write_topic(self.root / "02-Mathematics/01-Algebra/01-vectors.py", "math.vectors")
        write_topic(self.root / "03-ML/01-Intro/01-intro.py", "ml.intro")
        (self.root / "01-Python/helper.py").write_text("# not a topic\n")
        (self.root / "01-Python/01-Variables/03-no-header.py").write_text("print('no header')\n")
        self.tracker = Tracker(self.root)

    def tearDown(self):
        shutil.rmtree(self.root)

    def topic(self, state, topic_id):
        return next(t for t in state["topics"] if t["id"] == topic_id)

    def fill(self, relative, topic_id, **code):
        write_topic(self.root / relative, topic_id, **code)


class ScanningTests(TrackerTestCase):
    def test_scans_topics_ignores_helpers_and_reports_invalid_files(self):
        state = self.tracker.state()
        self.assertEqual({t["id"] for t in state["topics"]}, {"py.basics", "py.types", "math.vectors", "ml.intro"})
        self.assertEqual(state["summary"]["totalModules"], 3)
        self.assertTrue(any(i["type"] == "invalid" and i["path"].endswith("03-no-header.py") for i in state["issues"]))
        self.assertEqual(self.topic(state, "py.basics")["title"], "Python Variables")

    def test_new_topic_appears_on_next_scan(self):
        self.tracker.state()
        self.fill("01-Python/02-Loops/01-for.py", "py.for")
        state = self.tracker.state()
        self.assertIn("py.for", {t["id"] for t in state["topics"]})
        self.assertIn({"type": "new", "id": "py.for", "path": "01-Python/02-Loops/01-for.py"}, state["events"])

    def test_duplicate_ids_are_reported(self):
        self.fill("03-ML/01-Intro/02-copy.py", "ml.intro")
        state = self.tracker.state()
        self.assertTrue(any(i["type"] == "duplicate" for i in state["issues"]))
        self.assertEqual(sum(t["id"] == "ml.intro" for t in state["topics"]), 1)

    def test_exercise_code_detection(self):
        path = self.root / "01-Python/01-Variables/01-basics.py"
        write_topic(path, "py.basics", beginner="print('hi')", advanced="# only a comment")
        exercises = parse_topic(path)["exercises"]
        self.assertTrue(exercises["beginner"]["hasCode"])
        self.assertFalse(exercises["intermediate"]["hasCode"])
        self.assertFalse(exercises["advanced"]["hasCode"])


class ProgressTests(TrackerTestCase):
    def test_exercise_cannot_be_marked_without_code(self):
        with self.assertRaises(TrackerError) as ctx:
            self.tracker.set_requirement("py.basics", "beginner", True)
        self.assertIn("YOUR CODE", str(ctx.exception))

    def test_full_completion_flow_and_assessment_gate(self):
        self.fill("01-Python/01-Variables/01-basics.py", "py.basics",
                  beginner="a = 1", intermediate="b = 2", advanced="c = 3")
        self.tracker.set_requirement("py.basics", "theory", True)
        with self.assertRaises(TrackerError):
            self.tracker.set_requirement("py.basics", "assessment", True)
        for requirement in ("beginner", "intermediate"):
            state = self.tracker.set_requirement("py.basics", requirement, True)
        self.assertEqual(self.topic(state, "py.basics")["status"], "in_progress")
        self.tracker.set_requirement("py.basics", "advanced", True)
        state = self.tracker.set_requirement("01-Python/01-Variables/01-basics.py", "assessment", True)
        self.assertEqual(self.topic(state, "py.basics")["status"], "completed")
        self.assertEqual(state["summary"]["completedTopics"], 1)
        self.assertEqual(state["summary"]["percent"], round(100 * 5 / 20, 1))
        state = self.tracker.set_requirement("py.basics", "theory", False)
        self.assertIsNone(self.topic(state, "py.basics")["requirements"]["assessment"])
        self.assertEqual(self.topic(state, "py.basics")["status"], "in_progress")

    def test_opening_does_not_complete_or_start_a_topic(self):
        self.tracker.state()
        data = self.tracker.load_progress()
        data["topics"]["py.types"]["lastOpenedAt"] = "2026-11-01T10:00:00+00:00"
        self.tracker.save_progress(data)
        state = self.tracker.state()
        topic = self.topic(state, "py.types")
        self.assertEqual(topic["status"], "not_started")
        self.assertEqual(state["summary"]["completedTopics"], 0)
        self.assertEqual(state["currentTopic"], "py.types")

    def test_progress_persists_across_restarts(self):
        self.tracker.set_requirement("math.vectors", "theory", True)
        restarted = Tracker(self.root)
        self.assertTrue(self.topic(restarted.state(), "math.vectors")["requirements"]["theory"])

    def test_corrupt_progress_file_is_never_overwritten(self):
        self.tracker.state()
        self.tracker.progress_path.write_text("{ broken")
        with self.assertRaises(TrackerError):
            self.tracker.state()
        self.assertEqual(self.tracker.progress_path.read_text(), "{ broken")

    def test_unknown_topic_and_requirement_are_rejected(self):
        with self.assertRaises(TrackerError):
            self.tracker.set_requirement("nope", "theory", True)
        with self.assertRaises(TrackerError):
            self.tracker.set_requirement("py.basics", "homework", True)


class SyncTests(TrackerTestCase):
    def test_moved_file_keeps_progress(self):
        self.tracker.set_requirement("ml.intro", "theory", True)
        new_path = self.root / "03-ML/02-Basics/01-intro-renamed.py"
        new_path.parent.mkdir(parents=True)
        (self.root / "03-ML/01-Intro/01-intro.py").rename(new_path)
        state = self.tracker.state()
        topic = self.topic(state, "ml.intro")
        self.assertEqual(topic["path"], "03-ML/02-Basics/01-intro-renamed.py")
        self.assertTrue(topic["requirements"]["theory"])
        self.assertTrue(any(e["type"] == "moved" for e in state["events"]))

    def test_missing_file_is_reported_kept_restored_and_forgettable(self):
        self.tracker.set_requirement("py.types", "theory", True)
        file = self.root / "01-Python/01-Variables/02-types.py"
        backup = file.read_text()
        file.unlink()
        state = self.tracker.state()
        self.assertTrue(any(i["type"] == "missing" and i["id"] == "py.types" for i in state["issues"]))
        self.assertTrue(self.tracker.load_progress()["topics"]["py.types"]["requirements"]["theory"])
        file.write_text(backup)
        state = self.tracker.state()
        self.assertFalse(any(i["type"] == "missing" for i in state["issues"]))
        self.assertTrue(self.topic(state, "py.types")["requirements"]["theory"])
        file.unlink()
        self.tracker.state()
        self.tracker.forget("py.types")
        self.assertNotIn("py.types", self.tracker.load_progress()["topics"])

    def test_changed_id_at_same_path_migrates_progress(self):
        self.tracker.set_requirement("math.vectors", "theory", True)
        self.fill("02-Mathematics/01-Algebra/01-vectors.py", "math.linear-algebra.vectors")
        state = self.tracker.state()
        self.assertTrue(self.topic(state, "math.linear-algebra.vectors")["requirements"]["theory"])
        self.assertNotIn("math.vectors", self.tracker.load_progress()["topics"])

    def test_reports_are_generated(self):
        self.tracker.state()
        self.assertIn("Python Variables", (self.root / "PROGRESS.md").read_text())
        self.assertIn("01-Python/01-Variables/01-basics.py", (self.root / "COURSE-MAP.md").read_text())


class PositionTests(TrackerTestCase):
    def test_learning_path_orders_recommendations(self):
        (self.root / "00-Tracker/learning-path.json").write_text(json.dumps(
            {"order": ["02-Mathematics", "01-Python/01-Variables/02-types.py", "01-Python", "does/not-exist"]}))
        state = self.tracker.state()
        self.assertEqual(state["learningPath"], ["math.vectors", "py.types", "py.basics", "ml.intro"])
        self.assertEqual(state["nextTopic"], "math.vectors")
        self.assertTrue(any(i["type"] == "learning-path" for i in state["issues"]))

    def test_current_and_next(self):
        self.tracker.set_requirement("py.types", "theory", True)
        state = self.tracker.state()
        self.assertEqual(state["currentTopic"], "py.types")
        self.assertEqual(state["nextTopic"], "py.basics")


class OpenTests(TrackerTestCase):
    def test_dry_run_builds_command_and_url(self):
        self.tracker.state()
        result = self.tracker.open_topic("py.basics", dry_run=True)
        self.assertEqual(result["path"], "01-Python/01-Variables/01-basics.py")
        self.assertTrue(result["url"].startswith("vscode://file/"))
        self.assertTrue(result["url"].endswith("01-basics.py:1"))
        if result["command"]:
            self.assertIn(f"{(self.root / result['path']).resolve()}:1", result["command"][-1])
        exercise = self.tracker.open_topic("py.basics", "advanced", dry_run=True)
        self.assertGreater(exercise["line"], 1)
        self.assertIsNone(self.tracker.load_progress()["topics"]["py.basics"]["lastOpenedAt"])

    def test_unknown_and_traversal_paths_are_rejected(self):
        for key in ("../../etc/passwd", "missing.id"):
            with self.assertRaises(TrackerError):
                self.tracker.open_topic(key, dry_run=True)


class HttpTests(TrackerTestCase):
    def setUp(self):
        super().setUp()
        self.server = make_server(self.tracker, port=0)
        self.port = self.server.server_port
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        super().tearDown()

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        payload = json.dumps(body).encode() if body is not None else None
        connection.request(method, path, body=payload, headers=headers or {})
        response = connection.getresponse()
        data = response.read()
        connection.close()
        return response.status, data

    def test_state_page_and_assets(self):
        status, data = self.request("GET", "/api/state")
        self.assertEqual(status, 200)
        self.assertEqual(len(json.loads(data)["topics"]), 4)
        for path in ("/", "/tracker.css", "/tracker.js"):
            self.assertEqual(self.request("GET", path)[0], 200)
        self.assertEqual(self.request("GET", "/server.py")[0], 404)
        self.assertEqual(self.request("GET", "/progress.json")[0], 404)

    def test_progress_post_and_validation(self):
        json_headers = {"Content-Type": "application/json"}
        status, data = self.request("POST", "/api/progress", {"id": "py.basics", "requirement": "theory", "done": True},
                                    json_headers)
        self.assertEqual(status, 200)
        self.assertTrue(self.topic(json.loads(data), "py.basics")["requirements"]["theory"])
        status, data = self.request("POST", "/api/progress",
                                    {"id": "py.basics", "requirement": "beginner", "done": True}, json_headers)
        self.assertEqual(status, 409)
        status, _ = self.request("POST", "/api/progress", {"id": "py.basics"}, json_headers)
        self.assertEqual(status, 400)

    def test_security_checks(self):
        body = {"id": "py.basics", "requirement": "theory", "done": True}
        self.assertEqual(self.request("POST", "/api/progress", body, {"Content-Type": "text/plain"})[0], 415)
        self.assertEqual(self.request("POST", "/api/progress", body,
                                      {"Content-Type": "application/json", "Origin": "https://evil.example"})[0], 403)
        self.assertEqual(self.request("GET", "/api/state", headers={"Host": "evil.example"})[0], 403)

    def test_open_endpoint_dry_run(self):
        status, data = self.request("POST", "/api/open", {"id": "ml.intro", "dryRun": True},
                                    {"Content-Type": "application/json"})
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(data)["path"], "03-ML/01-Intro/01-intro.py")
        status, _ = self.request("POST", "/api/open", {"id": "nope", "dryRun": True},
                                 {"Content-Type": "application/json"})
        self.assertEqual(status, 404)


if __name__ == "__main__":
    unittest.main()
