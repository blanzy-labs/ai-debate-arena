import { FormEvent, useEffect, useMemo, useState } from "react";

import { fetchHealth, runDebate } from "./api";
import { DEBATE_MODES, getDebateMode } from "./debateModes";
import { buildDebateMarkdownReport, downloadMarkdownReport } from "./exportMarkdown";
import type { DebateModeSlug, DebateResponse, HealthResponse, ProviderName } from "./types";

const PROVIDERS: Array<{ value: ProviderName; label: string }> = [
  { value: "openai", label: "OpenAI" },
  { value: "gemini", label: "Gemini" },
];

const PROGRESS_STAGES = [
  "Debater A opening",
  "Debater B opening",
  "Debater A rebuttal",
  "Debater B rebuttal",
  "Judge summary",
];

const DEFAULT_TOPIC = "";

function yesNo(value: boolean | undefined) {
  return value ? "yes" : "no";
}

function renderList(items: string[]) {
  if (items.length === 0) {
    return <p className="empty-list">None returned.</p>;
  }

  return (
    <ul className="result-list">
      {items.map((item, index) => (
        <li key={`${item}-${index}`}>{item}</li>
      ))}
    </ul>
  );
}

function ProviderSelect({
  id,
  label,
  value,
  onChange,
  disabled,
}: {
  id: string;
  label: string;
  value: ProviderName;
  onChange: (value: ProviderName) => void;
  disabled: boolean;
}) {
  return (
    <label className="field">
      <span>{label}</span>
      <select
        id={id}
        value={value}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value as ProviderName)}
      >
        {PROVIDERS.map((provider) => (
          <option key={provider.value} value={provider.value}>
            {provider.label}
          </option>
        ))}
      </select>
    </label>
  );
}

function ResultPanel({ result }: { result: DebateResponse }) {
  function handleExport() {
    downloadMarkdownReport(buildDebateMarkdownReport(result));
  }

  return (
    <section className="result-panel" aria-labelledby="results-title">
      <div className="section-heading">
        <div>
          <p className="section-kicker">Debate Result</p>
          <h2 id="results-title">Judge Summary</h2>
        </div>
      </div>

      <div className="export-card">
        <div>
          <h3>Markdown Export</h3>
          <p>Downloads the current debate as a local Markdown file. Nothing is stored by the server.</p>
        </div>
        <button className="secondary-button export-button" type="button" onClick={handleExport}>
          Export Markdown Report
        </button>
      </div>

      <article className="result-card primary-result">
        <h3>Judge Summary</h3>
        <p>{result.judge_summary}</p>
      </article>

      <div className="result-grid">
        <article className="result-card">
          <h3>Strongest Argument A</h3>
          <p>{result.strongest_argument_a || "None returned."}</p>
        </article>
        <article className="result-card">
          <h3>Strongest Argument B</h3>
          <p>{result.strongest_argument_b || "None returned."}</p>
        </article>
        <article className="result-card">
          <h3>Weakest Assumption A</h3>
          <p>{result.weakest_assumption_a || "None returned."}</p>
        </article>
        <article className="result-card">
          <h3>Weakest Assumption B</h3>
          <p>{result.weakest_assumption_b || "None returned."}</p>
        </article>
      </div>

      <div className="result-grid">
        <article className="result-card">
          <h3>Unresolved Questions</h3>
          {renderList(result.unresolved_questions)}
        </article>
        <article className="result-card">
          <h3>Recommended Next Steps</h3>
          {renderList(result.recommended_next_steps)}
        </article>
        <article className="result-card">
          <h3>Suggested Follow-up Debates</h3>
          {renderList(result.suggested_follow_up_debates)}
        </article>
      </div>

      <section className="transcript" aria-labelledby="transcript-title">
        <h3 id="transcript-title">Full Debate Transcript</h3>
        <div className="transcript-grid">
          <article>
            <h4>{result.debater_a_role} Opening</h4>
            <p>{result.debater_a_opening}</p>
          </article>
          <article>
            <h4>{result.debater_b_role} Opening</h4>
            <p>{result.debater_b_opening}</p>
          </article>
          <article>
            <h4>{result.debater_a_role} Rebuttal</h4>
            <p>{result.debater_a_rebuttal}</p>
          </article>
          <article>
            <h4>{result.debater_b_role} Rebuttal</h4>
            <p>{result.debater_b_rebuttal}</p>
          </article>
        </div>
      </section>

      <section className="models-used" aria-labelledby="models-title">
        <h3 id="models-title">Models Used</h3>
        <dl>
          <div>
            <dt>Debater A</dt>
            <dd>
              {result.models_used.debater_a.provider} / {result.models_used.debater_a.model}
            </dd>
          </div>
          <div>
            <dt>Debater B</dt>
            <dd>
              {result.models_used.debater_b.provider} / {result.models_used.debater_b.model}
            </dd>
          </div>
          <div>
            <dt>Judge</dt>
            <dd>
              {result.models_used.judge.provider} / {result.models_used.judge.model}
            </dd>
          </div>
        </dl>
      </section>
    </section>
  );
}

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isHealthLoading, setIsHealthLoading] = useState(true);
  const [healthError, setHealthError] = useState<string | null>(null);
  const [topic, setTopic] = useState(DEFAULT_TOPIC);
  const [debateMode, setDebateMode] = useState<DebateModeSlug>("builder_vs_breaker");
  const [debaterAProvider, setDebaterAProvider] = useState<ProviderName>("openai");
  const [debaterBProvider, setDebaterBProvider] = useState<ProviderName>("gemini");
  const [judgeProvider, setJudgeProvider] = useState<ProviderName>("openai");
  const [validationMessage, setValidationMessage] = useState<string | null>(null);
  const [debateError, setDebateError] = useState<string | null>(null);
  const [result, setResult] = useState<DebateResponse | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  const selectedMode = useMemo(() => getDebateMode(debateMode), [debateMode]);

  useEffect(() => {
    const controller = new AbortController();

    async function loadHealth() {
      try {
        const nextHealth = await fetchHealth(controller.signal);
        setHealth(nextHealth);
        setHealthError(null);
      } catch {
        setHealth(null);
        setHealthError("Backend unavailable");
      } finally {
        setIsHealthLoading(false);
      }
    }

    loadHealth();

    return () => controller.abort();
  }, []);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const question = topic.trim();

    if (!question) {
      setValidationMessage("Please enter a debate question before running the debate.");
      setDebateError(null);
      setResult(null);
      return;
    }

    setValidationMessage(null);
    setDebateError(null);
    setResult(null);
    setIsRunning(true);

    try {
      const response = await runDebate({
        question,
        debate_mode: debateMode,
        debater_a_provider: debaterAProvider,
        debater_b_provider: debaterBProvider,
        judge_provider: judgeProvider,
      });
      setResult(response);
    } catch (caughtError) {
      const message =
        caughtError instanceof Error
          ? caughtError.message
          : "The debate could not be completed. Please check the backend logs and try again.";
      setDebateError(message);
    } finally {
      setIsRunning(false);
    }
  }

  function handleClear() {
    setTopic(DEFAULT_TOPIC);
    setValidationMessage(null);
    setDebateError(null);
    setResult(null);
  }

  return (
    <main className="app-shell">
      <section className="intro">
        <p className="project-label">Mythadis Labs App #2</p>
        <h1>Mythadis AI Debate Arena</h1>
        <p className="tagline">The books are fiction. The questions are real.</p>
      </section>

      <section className="status-panel" aria-labelledby="backend-status-title">
        <div className="section-heading">
          <div>
            <p className="section-kicker">Local Stack</p>
            <h2 id="backend-status-title">Backend Status</h2>
          </div>
          <span className={health?.status === "ok" ? "status healthy" : "status unavailable"}>
            {isHealthLoading ? "Checking" : health?.status === "ok" ? "Healthy" : "Unavailable"}
          </span>
        </div>

        {healthError ? <p className="error">{healthError}</p> : null}

        <dl className="status-grid">
          <div>
            <dt>App</dt>
            <dd>{health?.app ?? "-"}</dd>
          </div>
          <div>
            <dt>OpenAI configured</dt>
            <dd>{health ? yesNo(health.openai_configured) : "-"}</dd>
          </div>
          <div>
            <dt>Gemini configured</dt>
            <dd>{health ? yesNo(health.gemini_configured) : "-"}</dd>
          </div>
          <div>
            <dt>OpenAI model</dt>
            <dd>{health?.models.openai ?? "-"}</dd>
          </div>
          <div>
            <dt>Gemini model</dt>
            <dd>{health?.models.gemini ?? "-"}</dd>
          </div>
        </dl>
      </section>

      <section className="workspace">
        <form className="debate-form" onSubmit={handleSubmit} noValidate>
          <div className="section-heading">
            <div>
              <p className="section-kicker">Run Debate</p>
              <h2>Question And Debate Setup</h2>
            </div>
          </div>

          <label className="field topic-field" htmlFor="topic">
            <span>Debate question</span>
            <textarea
              id="topic"
              value={topic}
              disabled={isRunning}
              rows={6}
              placeholder="Example: Should small cafes use AI tools to improve daily profit decisions?"
              onChange={(event) => {
                setTopic(event.target.value);
                if (validationMessage) {
                  setValidationMessage(null);
                }
              }}
            />
          </label>

          {validationMessage ? <p className="validation-message">{validationMessage}</p> : null}

          <div className="form-grid">
            <label className="field">
              <span>Debate mode</span>
              <select
                value={debateMode}
                disabled={isRunning}
                onChange={(event) => setDebateMode(event.target.value as DebateModeSlug)}
              >
                {DEBATE_MODES.map((mode) => (
                  <option key={mode.slug} value={mode.slug}>
                    {mode.displayName}
                  </option>
                ))}
              </select>
            </label>

            <ProviderSelect
              id="debater-a-provider"
              label="Debater A provider"
              value={debaterAProvider}
              disabled={isRunning}
              onChange={setDebaterAProvider}
            />
            <ProviderSelect
              id="debater-b-provider"
              label="Debater B provider"
              value={debaterBProvider}
              disabled={isRunning}
              onChange={setDebaterBProvider}
            />
            <ProviderSelect
              id="judge-provider"
              label="Judge provider"
              value={judgeProvider}
              disabled={isRunning}
              onChange={setJudgeProvider}
            />
          </div>

          <div className="mode-profile" aria-live="polite">
            <div>
              <h3>{selectedMode.displayName}</h3>
              <p>{selectedMode.description}</p>
            </div>
            <dl>
              <div>
                <dt>Debater A</dt>
                <dd>{selectedMode.debaterA}</dd>
              </div>
              <div>
                <dt>Debater B</dt>
                <dd>{selectedMode.debaterB}</dd>
              </div>
            </dl>
          </div>

          <div className="form-actions">
            <button className="primary-button" type="submit" disabled={isRunning}>
              {isRunning ? "Running Debate" : "Run Debate"}
            </button>
            <button className="secondary-button" type="button" disabled={isRunning} onClick={handleClear}>
              Clear
            </button>
          </div>
        </form>

        <aside className="run-state" aria-live="polite">
          {isRunning ? (
            <>
              <h2>Running debate</h2>
              <p>The backend completes these steps in sequence. This may take time.</p>
              <ol className="progress-list">
                {PROGRESS_STAGES.map((stage) => (
                  <li key={stage}>{stage}</li>
                ))}
              </ol>
            </>
          ) : (
            <>
              <h2>Ready</h2>
              <p>Choose a question, mode, and providers. Results are shown here after the backend finishes.</p>
            </>
          )}
        </aside>
      </section>

      {debateError ? (
        <section className="error-panel" aria-live="polite" aria-label="Debate error">
          <h2>Debate Error</h2>
          <p>{debateError}</p>
        </section>
      ) : null}

      {result ? <ResultPanel result={result} /> : null}
    </main>
  );
}
