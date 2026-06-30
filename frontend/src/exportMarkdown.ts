import type { DebateResponse } from "./types";

const APP_NAME = "AI Debate Arena";
const TAGLINE = "Structured disagreement for better decisions.";

export function buildDebateMarkdownReport(result: DebateResponse, generatedAt = new Date()): string {
  const generated = formatTimestamp(generatedAt);

  return [
    `# ${APP_NAME} Report`,
    "",
    `> ${TAGLINE}`,
    "",
    `Generated: ${generated}`,
    `App: ${APP_NAME}`,
    `Debate Mode: ${safeText(result.debate_mode)}`,
    `Question: ${safeText(result.question)}`,
    "",
    "## Roles",
    "",
    `- Debater A: ${safeText(result.debater_a_role)}`,
    `- Debater B: ${safeText(result.debater_b_role)}`,
    "",
    "## Models Used",
    "",
    `- Debater A: ${safeText(result.models_used?.debater_a?.provider)} / ${safeText(result.models_used?.debater_a?.model)}`,
    `- Debater B: ${safeText(result.models_used?.debater_b?.provider)} / ${safeText(result.models_used?.debater_b?.model)}`,
    `- Judge: ${safeText(result.models_used?.judge?.provider)} / ${safeText(result.models_used?.judge?.model)}`,
    "",
    "## Judge Summary",
    "",
    safeText(result.judge_summary),
    "",
    "## Strongest Arguments",
    "",
    "### Debater A",
    "",
    safeText(result.strongest_argument_a),
    "",
    "### Debater B",
    "",
    safeText(result.strongest_argument_b),
    "",
    "## Weakest Assumptions",
    "",
    "### Debater A",
    "",
    safeText(result.weakest_assumption_a),
    "",
    "### Debater B",
    "",
    safeText(result.weakest_assumption_b),
    "",
    "## Unresolved Questions",
    "",
    renderMarkdownList(result.unresolved_questions),
    "",
    "## Recommended Next Steps",
    "",
    renderMarkdownList(result.recommended_next_steps),
    "",
    "## Suggested Follow-up Debates",
    "",
    renderMarkdownList(result.suggested_follow_up_debates),
    "",
    "## Full Debate Transcript",
    "",
    "### Debater A Opening",
    "",
    safeText(result.debater_a_opening),
    "",
    "### Debater B Opening",
    "",
    safeText(result.debater_b_opening),
    "",
    "### Debater A Rebuttal",
    "",
    safeText(result.debater_a_rebuttal),
    "",
    "### Debater B Rebuttal",
    "",
    safeText(result.debater_b_rebuttal),
    "",
    "## Limitations",
    "",
    "This report is generated from an AI debate workflow. It is structured disagreement, not guaranteed truth. The app does not browse the web, verify current facts, or generate real citations unless such source material is explicitly provided by the user and included in the debate input.",
    "",
  ].join("\n");
}

export function downloadMarkdownReport(markdown: string, filename = buildMarkdownFilename()): void {
  const safeFilename = filename.endsWith(".md") ? filename : `${filename}.md`;
  const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");

  link.href = url;
  link.download = safeFilename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

export function buildMarkdownFilename(now = new Date()): string {
  const date = now.toISOString().slice(0, 10);
  const time = now
    .toTimeString()
    .slice(0, 8)
    .replace(/:/g, "");

  return `ai-debate-arena-report-${date}-${time}.md`;
}

function formatTimestamp(date: Date): string {
  const pad = (value: number) => value.toString().padStart(2, "0");
  return [
    date.getFullYear(),
    "-",
    pad(date.getMonth() + 1),
    "-",
    pad(date.getDate()),
    " ",
    pad(date.getHours()),
    ":",
    pad(date.getMinutes()),
    ":",
    pad(date.getSeconds()),
  ].join("");
}

function renderMarkdownList(items: string[] | null | undefined): string {
  if (!items || items.length === 0) {
    return "- None returned.";
  }

  const renderedItems = items
    .map((item) => safeText(item, ""))
    .filter(Boolean)
    .map((item) => `- ${item}`);

  return renderedItems.length > 0 ? renderedItems.join("\n") : "- None returned.";
}

function safeText(value: unknown, fallback = "Not returned."): string {
  if (typeof value !== "string") {
    return fallback;
  }

  const trimmed = value.trim();
  return trimmed ? trimmed : fallback;
}
