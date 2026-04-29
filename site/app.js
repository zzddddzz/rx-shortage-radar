const state = {
  payload: null,
  query: "",
  status: "All",
  sort: "name",
  selectedId: null,
  rxnorm: {
    lastQuery: "",
    loading: false,
    candidates: [],
    error: "",
  },
};

const statusColors = {
  Current: "#1e7c5b",
  Resolved: "#295f9e",
  "To Be Discontinued": "#a45d16",
};

const statusClasses = {
  Current: "pill-current",
  Resolved: "pill-resolved",
  "To Be Discontinued": "pill-discontinued",
};

const elements = {
  totalRecords: document.querySelector("#total-records"),
  sourceUpdated: document.querySelector("#source-updated"),
  generatedAt: document.querySelector("#generated-at"),
  statusChart: document.querySelector("#status-chart"),
  statusTabs: document.querySelector("#status-tabs"),
  rxnormPanel: document.querySelector("#rxnorm-panel"),
  rxnormStatus: document.querySelector("#rxnorm-status"),
  rxnormButton: document.querySelector("#rxnorm-button"),
  rxnormResults: document.querySelector("#rxnorm-results"),
  searchInput: document.querySelector("#search-input"),
  sortSelect: document.querySelector("#sort-select"),
  resultCount: document.querySelector("#result-count"),
  resultsList: document.querySelector("#results-list"),
  detailContent: document.querySelector("#detail-content"),
  sourceDisclaimer: document.querySelector("#source-disclaimer"),
};

function normalizeText(value) {
  return String(value || "")
    .toLowerCase()
    .match(/[a-z0-9]+/g)
    ?.join(" ") || "";
}

function formatDate(value) {
  if (!value) return "Unknown";
  const date = new Date(`${value}T00:00:00Z`);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("en", {
    year: "numeric",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  }).format(date);
}

function formatGenerated(value) {
  if (!value) return "Unknown";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(date);
}

function makeElement(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function pillClass(status) {
  return `pill ${statusClasses[status] || "pill-other"}`;
}

function allStatuses() {
  const counts = state.payload?.summary?.status_counts || {};
  return ["All", ...Object.keys(counts)];
}

function filteredRecords() {
  const terms = normalizeText(state.query).split(" ").filter(Boolean);
  let records = state.payload?.records || [];
  
  if (state.status !== "All") {
    records = records.filter((record) => record.status === state.status);
  }
  if (terms.length) {
    records = records.filter((record) => terms.every((term) => record.search_text?.includes(term)));
  }

  const groups = new Map();
  for (const record of records) {
    const key = `${record.generic_name || "Unnamed"}|${record.status}`;
    
    if (!groups.has(key)) {
      groups.set(key, {
        ...record,
        id: key, 
        _packageCount: 1,
        _ndcSet: new Set(record.package_ndc ? [record.package_ndc] : [])
      });
    } else {
      const group = groups.get(key);
      group._packageCount++;
      if (record.package_ndc) group._ndcSet.add(record.package_ndc);
      
      if (record.update_date && (!group.update_date || record.update_date > group.update_date)) {
        group.update_date = record.update_date;
      }
    }
  }

  
  const groupedRecords = Array.from(groups.values()).map(g => ({
    ...g,
    package_ndc: Array.from(g._ndcSet) 
  }));

  const sorted = [...groupedRecords];
  sorted.sort((a, b) => {
    if (state.sort === "updated") {
      return String(b.update_date || "").localeCompare(String(a.update_date || ""));
    }
    if (state.sort === "status") {
      return String(a.status || "").localeCompare(String(b.status || ""));
    }
    return String(a.generic_name || "").localeCompare(String(b.generic_name || ""));
  });
  return sorted;
}

function setQuery(value) {
  state.query = value;
  state.selectedId = null;
  elements.searchInput.value = value;
  const url = new URL(window.location.href);
  if (value) {
    url.searchParams.set("q", value);
  } else {
    url.searchParams.delete("q");
  }
  window.history.replaceState({}, "", url);
}

function resetRxNormState() {
  state.rxnorm.error = "";
  state.rxnorm.candidates = [];
}

function isEditableTarget(target) {
  if (!(target instanceof HTMLElement)) return false;
  const tagName = target.tagName.toLowerCase();
  return target.isContentEditable || tagName === "input" || tagName === "textarea" || tagName === "select";
}

function clearSearch() {
  if (!state.query) return;
  setQuery("");
  resetRxNormState();
  render();
}

function handleKeyboardShortcuts(event) {
  if (event.defaultPrevented || event.metaKey || event.ctrlKey || event.altKey) return;

  if (event.key === "/" && !isEditableTarget(event.target)) {
    event.preventDefault();
    elements.searchInput.focus();
    elements.searchInput.select();
    return;
  }

  if (event.key === "Escape") {
    if (event.target === elements.sortSelect) return;
    if (state.query) {
      event.preventDefault();
      clearSearch();
    }
  }
}

function renderSummary() {
  const summary = state.payload.summary || {};
  const source = state.payload.source || {};
  elements.totalRecords.textContent = new Intl.NumberFormat().format(summary.total_records || 0);
  elements.sourceUpdated.textContent = formatDate(source.last_updated);
  elements.generatedAt.textContent = formatGenerated(state.payload.generated_at);
  if (source.disclaimer) {
    elements.sourceDisclaimer.textContent = source.disclaimer;
  }

  const counts = summary.status_counts || {};
  const maxCount = Math.max(1, ...Object.values(counts));
  elements.statusChart.replaceChildren(
    ...Object.entries(counts).map(([status, count]) => {
      const row = makeElement("div", "chart-row");
      const label = makeElement("div", "chart-label", status);
      const track = makeElement("div", "chart-track");
      const fill = makeElement("div", "chart-fill");
      fill.style.setProperty("--width", `${Math.max(3, (count / maxCount) * 100)}%`);
      fill.style.setProperty("--color", statusColors[status] || "#b33a3a");
      track.append(fill);
      const value = makeElement("strong", "", new Intl.NumberFormat().format(count));
      row.append(label, track, value);
      return row;
    }),
  );
}

function renderTabs() {
  const counts = state.payload.summary?.status_counts || {};
  const tabs = allStatuses().map((status) => {
    const label = status === "All" ? `All (${state.payload.summary.total_records})` : `${status} (${counts[status] || 0})`;
    const button = makeElement("button", "status-tab", label);
    button.type = "button";
    button.setAttribute("role", "tab");
    button.setAttribute("aria-selected", String(state.status === status));
    button.addEventListener("click", () => {
      state.status = status;
      state.selectedId = null;
      render();
    });
    return button;
  });
  elements.statusTabs.replaceChildren(...tabs);
}

function renderRxNormPanel(records) {
  const query = state.query.trim();
  if (query.length < 3) {
    elements.rxnormPanel.hidden = true;
    return;
  }
  elements.rxnormPanel.hidden = false;
  elements.rxnormButton.disabled = state.rxnorm.loading;
  elements.rxnormButton.textContent = state.rxnorm.loading ? "Resolving" : "Resolve";

  if (state.rxnorm.error) {
    elements.rxnormStatus.textContent = state.rxnorm.error;
  } else if (state.rxnorm.candidates.length && state.rxnorm.lastQuery === query) {
    elements.rxnormStatus.textContent = "Select a normalized RxNorm candidate to search shortage records.";
  } else if (records.length === 0) {
    elements.rxnormStatus.textContent = "No direct shortage match. Try RxNorm approximate matching.";
  } else {
    elements.rxnormStatus.textContent = "Optional RxNorm normalization for misspellings and free-text drug names.";
  }

  const candidateNodes = state.rxnorm.candidates.map((candidate) => {
    const button = makeElement("button", "rxnorm-choice", candidate.name || `RxCUI ${candidate.rxcui}`);
    button.type = "button";
    const meta = makeElement("span", "", `RxCUI ${candidate.rxcui} · score ${candidate.score}`);
    button.append(meta);
    button.addEventListener("click", () => {
      setQuery(candidate.name || candidate.rxcui);
      state.rxnorm.candidates = [];
      state.rxnorm.error = "";
      render();
    });
    return button;
  });
  elements.rxnormResults.replaceChildren(...candidateNodes);
}

async function resolveRxNorm() {
  const query = state.query.trim();
  if (query.length < 3 || state.rxnorm.loading) return;

  state.rxnorm = { lastQuery: query, loading: true, candidates: [], error: "" };
  render();
  const url = new URL("https://rxnav.nlm.nih.gov/REST/approximateTerm.json");
  url.searchParams.set("term", query);
  url.searchParams.set("maxEntries", "8");

  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`RxNorm HTTP ${response.status}`);
    const payload = await response.json();
    const candidates = payload.approximateGroup?.candidate || [];
    const seen = new Set();
    state.rxnorm.candidates = candidates
      .filter((candidate) => {
        if (!candidate.rxcui || seen.has(candidate.rxcui)) return false;
        seen.add(candidate.rxcui);
        return true;
      })
      .map((candidate) => ({
        rxcui: candidate.rxcui,
        name: candidate.name || "",
        score: Number.parseFloat(candidate.score || "0").toPrecision(3),
        rank: candidate.rank || "",
      }));
    if (!state.rxnorm.candidates.length) {
      state.rxnorm.error = "RxNorm returned no candidates for this term.";
    }
  } catch (error) {
    state.rxnorm.error = `RxNorm lookup failed: ${error.message}`;
  } finally {
    state.rxnorm.loading = false;
    render();
  }
}

function renderResults(records) {
  elements.resultCount.textContent = `${new Intl.NumberFormat().format(records.length)} shown`;
  if (!records.length) {
    elements.resultsList.replaceChildren(makeElement("div", "empty-state", "No records match this search."));
    renderDetail(null);
    return;
  }

  if (!state.selectedId || !records.some((record) => record.id === state.selectedId)) {
    state.selectedId = records[0].id;
  }

  const nodes = records.slice(0, 250).map((record) => {
    const button = makeElement("button", "result-item");
    button.type = "button";
    button.setAttribute("aria-pressed", String(record.id === state.selectedId));
    button.addEventListener("click", () => {
      state.selectedId = record.id;
      render();
    });

    const body = makeElement("div");
    body.append(
      makeElement("div", "result-title", record.generic_name || "Unnamed drug"),
      makeElement(
        "div",
        "result-meta",
        `${record.brand_names?.join(", ") || "No brand listed"} · ${record._packageCount} package(s) · Updated ${formatDate(record.update_date)}`,
      ),
    );
    button.append(body, makeElement("span", pillClass(record.status), record.status || "Unknown"));
    return button;
  });

  if (records.length > 250) {
    nodes.push(makeElement("div", "empty-state", `Showing first 250 of ${records.length} matches. Refine search to narrow results.`));
  }
  elements.resultsList.replaceChildren(...nodes);
  renderDetail(records.find((record) => record.id === state.selectedId));
}

function field(label, value) {
  const row = makeElement("div", "field");
  const term = makeElement("dt", "", label);
  const description = makeElement("dd", "", Array.isArray(value) ? value.join(", ") || "None listed" : value || "None listed");
  row.append(term, description);
  return row;
}

function renderDetail(record) {
  if (!record) {
    elements.detailContent.className = "detail-empty";
    elements.detailContent.textContent = "Select a record to inspect FDA fields.";
    return;
  }
  const content = makeElement("div");
  content.append(
    makeElement("h2", "detail-title", record.generic_name || "Unnamed drug"),
    makeElement("p", "detail-subtitle", record.presentation || record.related_info || "FDA shortage record"),
    makeElement("span", pillClass(record.status), record.status || "Unknown"),
  );

  const fields = makeElement("dl", "field-list");
  fields.append(
    field("Brand names", record.brand_names),
    field("RxCUIs", record.rxcuis),
    field("Package NDC", record.package_ndc),
    field("Product NDCs", record.product_ndcs),
    field("Therapeutic categories", record.therapeutic_categories),
    field("Company", record.company_name),
    field("Dosage form", record.dosage_form),
    field("Route", record.routes),
    field("Updated", formatDate(record.update_date)),
    field("Initial posting", formatDate(record.initial_posting_date)),
    field("Related information", record.related_info),
  );
  content.append(fields);
  elements.detailContent.className = "";
  elements.detailContent.replaceChildren(content);
}

function render() {
  if (!state.payload) return;
  const records = filteredRecords();
  renderSummary();
  renderTabs();
  renderRxNormPanel(records);
  renderResults(records);
}

async function init() {
  const params = new URLSearchParams(window.location.search);
  const initialQuery = params.get("q") || "";
  if (initialQuery) {
    setQuery(initialQuery);
  }
  elements.searchInput.addEventListener("input", (event) => {
    setQuery(event.target.value);
    resetRxNormState();
    render();
  });
  elements.sortSelect.addEventListener("change", (event) => {
    state.sort = event.target.value;
    render();
  });
  elements.rxnormButton.addEventListener("click", resolveRxNorm);
  document.addEventListener("keydown", handleKeyboardShortcuts);

  try {
    const response = await fetch("data/shortages.json", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    state.payload = await response.json();
    render();
  } catch (error) {
    elements.totalRecords.textContent = "Unavailable";
    elements.sourceUpdated.textContent = "Unavailable";
    elements.generatedAt.textContent = "Unavailable";
    elements.resultCount.textContent = "Could not load data";
    elements.resultsList.replaceChildren(makeElement("div", "empty-state", `Could not load data/shortages.json: ${error.message}`));
  }
}

init();
