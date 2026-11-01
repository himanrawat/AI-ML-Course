"use strict";

const REQUIREMENT_LABELS = {
  theory: "Theory",
  beginner: "Beginner",
  intermediate: "Intermediate",
  advanced: "Advanced",
  assessment: "Assessment",
};
const EXERCISES = ["beginner", "intermediate", "advanced"];
const STATUS_LABELS = { not_started: "Not started", in_progress: "In progress", completed: "Completed" };
const POLL_MS = 5000;

const ui = loadUiState();
let state = null;
let lastFingerprint = "";
let toastTimer = null;

function loadUiState() {
  const defaults = { view: "modules", filter: "all", openModules: [] };
  try {
    return { ...defaults, ...JSON.parse(localStorage.getItem("ai-ml-tracker-ui") || "{}") };
  } catch {
    return defaults;
  }
}

function saveUiState() {
  try {
    localStorage.setItem("ai-ml-tracker-ui", JSON.stringify(ui));
  } catch {
    /* storage unavailable: UI state simply isn't remembered */
  }
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

async function api(path, body) {
  const options = body === undefined
    ? { cache: "no-store" }
    : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const response = await fetch(path, options);
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
  return data;
}

function showToast(message, isError = false) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.className = isError ? "toast error" : "toast";
  toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.hidden = true; }, isError ? 7000 : 3500);
}

// ---------- rendering ----------
function requirementState(topic, requirement) {
  if (topic.requirements[requirement]) return "done";
  if (EXERCISES.includes(requirement) && !topic.exercises[requirement]?.hasCode) return "locked";
  if (requirement === "assessment" && ["theory", ...EXERCISES].some((r) => !topic.requirements[r])) return "locked";
  return "ready";
}

function requirementTitle(topic, requirement, chipState) {
  if (chipState === "done") return `${REQUIREMENT_LABELS[requirement]} done on ${topic.requirements[requirement].slice(0, 10)}. Click to undo.`;
  if (chipState === "locked" && requirement === "assessment") return "Unlocks after Theory and all three exercises are done.";
  if (chipState === "locked") return "Write your solution under this exercise's '# YOUR CODE:' line first.";
  if (EXERCISES.includes(requirement)) return "Code detected. Click to mark this exercise complete after review.";
  return `Mark ${REQUIREMENT_LABELS[requirement]} complete.`;
}

function renderRequirements(topic) {
  const chips = state.requirements.map((requirement) => {
    const chipState = requirementState(topic, requirement);
    const hasCode = EXERCISES.includes(requirement) && topic.exercises[requirement]?.hasCode;
    return `<button type="button" class="req" data-id="${escapeHtml(topic.id)}" data-req="${requirement}"
      data-state="${chipState}" data-code="${hasCode}" aria-pressed="${chipState === "done"}"
      title="${escapeHtml(requirementTitle(topic, requirement, chipState))}">${REQUIREMENT_LABELS[requirement]}</button>`;
  });
  return `<div class="reqs" role="group" aria-label="Requirements for ${escapeHtml(topic.title)}">${chips.join("")}</div>`;
}

function topicLink(topic) {
  return `<a class="topic-link" href="${escapeHtml(topic.editorUrl)}" data-open="${escapeHtml(topic.id)}"
    title="Open ${escapeHtml(topic.path)} in your editor">${escapeHtml(topic.title)}</a>`;
}

function renderTopic(topic, withModule = false) {
  const moduleBadge = withModule ? `<span class="badge badge-module">${escapeHtml(topic.moduleName)}</span>` : "";
  return `<li class="topic status-${topic.status}" data-topic="${escapeHtml(topic.id)}">
    <span class="status-dot" title="${STATUS_LABELS[topic.status]}" aria-label="${STATUS_LABELS[topic.status]}"></span>
    <div>
      ${topicLink(topic)}
      <div class="topic-meta">
        <span class="badge">${escapeHtml(topic.level)}</span>${moduleBadge}
        <code>${escapeHtml(topic.path)}</code>
        <span>#${topic.pathOrder} in learning path</span>
      </div>
    </div>
    ${renderRequirements(topic)}
  </li>`;
}

function progressBar(percent) {
  return `<div class="bar ${percent >= 100 ? "complete" : ""}" role="progressbar" aria-valuemin="0" aria-valuemax="100"
    aria-valuenow="${percent}"><span style="width:${percent}%"></span></div>`;
}

function matches(topic) {
  if (ui.filter !== "all" && topic.status !== ui.filter) return false;
  const query = document.getElementById("search").value.trim().toLowerCase();
  return !query || [topic.title, topic.path, topic.id, topic.moduleName].some((v) => v.toLowerCase().includes(query));
}

function renderModules(byId) {
  const parts = state.modules.map((module) => {
    const sections = module.sections.map((section) => {
      const topics = section.topicIds.map((id) => byId[id]).filter(matches);
      if (!topics.length) return "";
      return `<div class="section-head"><h3>${escapeHtml(section.name)}</h3>
          <span class="muted small">${section.completedTopics}/${section.topics} · ${section.percent}%</span>
          ${progressBar(section.percent)}</div>
        <ul class="topic-list">${topics.map((t) => renderTopic(t)).join("")}</ul>`;
    }).join("");
    if (!sections) return "";
    const isOpen = ui.openModules.includes(module.module) || ui.filter !== "all" || document.getElementById("search").value;
    return `<details class="module" data-module="${escapeHtml(module.module)}" ${isOpen ? "open" : ""}>
      <summary>
        <span class="module-name">${escapeHtml(module.name)}</span>
        ${progressBar(module.percent)}
        <span class="module-counts">${module.percent}% · ${module.completedTopics}/${module.topics} topics ·
          ${module.inProgressTopics} in progress</span>
      </summary>
      <div class="module-body">${sections}</div>
    </details>`;
  }).join("");
  return parts || `<p class="empty">No topics match the current filter.</p>`;
}

function renderPath(byId) {
  const topics = state.learningPath.map((id) => byId[id]).filter(matches);
  if (!topics.length) return `<p class="empty">No topics match the current filter.</p>`;
  return `<div class="module"><div class="module-body">
    <p class="muted small">Recommended order. Maths topics sit just before the machine-learning topics that use them.</p>
    <ul class="topic-list">${topics.map((t) => renderTopic(t, true)).join("")}</ul></div></div>`;
}

function renderPositionCard(elementId, topic, emptyText) {
  const element = document.getElementById(elementId);
  if (!topic) {
    element.innerHTML = `<p class="muted">${emptyText}</p>`;
    return;
  }
  const doneCount = state.requirements.filter((r) => topic.requirements[r]).length;
  element.innerHTML = `<div class="title-row">${topicLink(topic)}</div>
    <div class="meta muted small">${escapeHtml(topic.moduleName)} › ${escapeHtml(topic.sectionName)} ·
      <code>${escapeHtml(topic.path)}</code> · ${doneCount}/5 requirements</div>
    ${renderRequirements(topic)}`;
}

function renderStats() {
  const s = state.summary;
  const tiles = [
    [`${s.percent}%`, "Overall completion"],
    [s.totalModules, "Total modules"],
    [`${s.completedModules}/${s.totalModules}`, "Completed modules"],
    [`${s.completedTopics}/${s.topics}`, "Completed topics"],
    [s.inProgressTopics, "In-progress topics"],
    [s.remainingTopics, "Remaining topics"],
  ];
  document.getElementById("stats").innerHTML = tiles
    .map(([value, label]) => `<div class="stat"><div class="stat-value">${value}</div><div class="stat-label">${label}</div></div>`)
    .join("");
}

function renderIssues() {
  const section = document.getElementById("issues");
  if (!state.issues.length) {
    section.hidden = true;
    section.innerHTML = "";
    return;
  }
  section.hidden = false;
  section.innerHTML = `<h2>Sync issues (${state.issues.length})</h2><ul>${state.issues.map((issue) => `
    <li><strong>${escapeHtml(issue.type)}</strong> · <code>${escapeHtml(issue.path || issue.id)}</code> — ${escapeHtml(issue.message)}
      ${issue.type === "missing" ? `<button type="button" data-forget="${escapeHtml(issue.id)}">Forget entry</button>` : ""}</li>`).join("")}</ul>`;
}

function render() {
  const byId = Object.fromEntries(state.topics.map((t) => [t.id, t]));
  const s = state.summary;
  if (!ui.initialized) {
    const focus = byId[state.currentTopic] || byId[state.nextTopic];
    if (focus && !ui.openModules.length) ui.openModules = [focus.module];
    ui.initialized = true;
    saveUiState();
  }
  document.getElementById("course-root").textContent = state.courseRoot;
  document.getElementById("overall-percent").textContent = s.percent;
  document.getElementById("overall-bar").style.width = `${s.percent}%`;
  document.getElementById("overall-caption").textContent =
    `${s.requirementsDone}/${s.requirementsTotal} requirements · ${s.exercisesDone}/${s.exercisesTotal} exercises done`;
  renderPositionCard("current-topic", byId[state.currentTopic], "Open a topic or complete a requirement to set your position.");
  renderPositionCard("next-topic", byId[state.nextTopic], "Everything is complete. Congratulations!");
  renderStats();
  renderIssues();
  const editor = state.editor;
  document.getElementById("editor-status").textContent = editor.available
    ? `Links open with: ${editor.command}` : editor.message;
  document.getElementById("content").innerHTML = ui.view === "path" ? renderPath(byId) : renderModules(byId);
  document.querySelectorAll("[data-view]").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.view === ui.view)));
  document.getElementById("filter").value = ui.filter;
}

function announceEvents(events) {
  if (!events?.length) return;
  const counts = events.reduce((acc, e) => ({ ...acc, [e.type]: (acc[e.type] || 0) + 1 }), {});
  const text = Object.entries(counts).map(([type, n]) => `${n} ${type}`).join(", ");
  showToast(`Course folders changed: ${text} topic(s).`);
}

async function refresh(force = false) {
  try {
    const next = await api("/api/state");
    document.getElementById("offline").hidden = true;
    const fingerprint = JSON.stringify([next.topics, next.issues, next.summary, next.currentTopic, next.nextTopic, next.editor]);
    if (force || fingerprint !== lastFingerprint) {
      state = next;
      lastFingerprint = fingerprint;
      render();
    }
    if (state) announceEvents(next.events);
  } catch (error) {
    document.getElementById("offline").hidden = false;
  }
}

function applyState(next) {
  state = next;
  lastFingerprint = JSON.stringify([next.topics, next.issues, next.summary, next.currentTopic, next.nextTopic, next.editor]);
  render();
}

// ---------- interactions ----------
document.addEventListener("click", async (event) => {
  const link = event.target.closest("[data-open]");
  if (link) {
    event.preventDefault();
    try {
      const result = await api("/api/open", { id: link.dataset.open });
      showToast(`Opened ${result.path} in your editor.`);
      refresh();
    } catch (error) {
      showToast(`${error.message} Trying the vscode:// link instead.`, true);
      window.location.href = link.getAttribute("href");
    }
    return;
  }
  const chip = event.target.closest(".req");
  if (chip) {
    const done = chip.dataset.state !== "done";
    try {
      applyState(await api("/api/progress", { id: chip.dataset.id, requirement: chip.dataset.req, done }));
      showToast(`${REQUIREMENT_LABELS[chip.dataset.req]} ${done ? "marked complete" : "cleared"}.`);
    } catch (error) {
      showToast(error.message, true);
    }
    return;
  }
  const forget = event.target.closest("[data-forget]");
  if (forget) {
    if (!window.confirm(`Forget saved progress for ${forget.dataset.forget}? This can't be undone.`)) return;
    try {
      applyState(await api("/api/forget", { id: forget.dataset.forget }));
    } catch (error) {
      showToast(error.message, true);
    }
    return;
  }
  const tab = event.target.closest("[data-view]");
  if (tab) {
    ui.view = tab.dataset.view;
    saveUiState();
    render();
  }
});

document.addEventListener("toggle", (event) => {
  const module = event.target.closest?.("details.module");
  if (!module || ui.filter !== "all" || document.getElementById("search").value) return;
  const id = module.dataset.module;
  ui.openModules = module.open ? [...new Set([...ui.openModules, id])] : ui.openModules.filter((m) => m !== id);
  saveUiState();
}, true);

document.getElementById("filter").addEventListener("change", (event) => {
  ui.filter = event.target.value;
  saveUiState();
  render();
});
document.getElementById("search").addEventListener("input", () => render());
window.addEventListener("focus", () => refresh());
setInterval(() => { if (document.visibilityState === "visible") refresh(); }, POLL_MS);

refresh(true);
