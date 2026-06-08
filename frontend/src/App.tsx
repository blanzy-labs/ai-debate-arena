import { useEffect, useState } from "react";

type HealthResponse = {
  status: string;
  app: string;
  version: string;
  openai_configured: boolean;
  gemini_configured: boolean;
  models: {
    openai: string;
    gemini: string;
  };
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

function yesNo(value: boolean | undefined) {
  return value ? "yes" : "no";
}

export default function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function loadHealth() {
      try {
        const response = await fetch(`${API_BASE_URL}/health`, {
          signal: controller.signal,
        });

        if (!response.ok) {
          throw new Error(`Health check failed with ${response.status}`);
        }

        setHealth(await response.json());
        setError(null);
      } catch (caughtError) {
        if (caughtError instanceof DOMException && caughtError.name === "AbortError") {
          return;
        }

        setHealth(null);
        setError("Backend unavailable");
      } finally {
        setIsLoading(false);
      }
    }

    loadHealth();

    return () => controller.abort();
  }, []);

  return (
    <main className="app-shell">
      <section className="intro">
        <p className="project-label">Mythadis Labs App #2</p>
        <h1>Mythadis AI Debate Arena</h1>
        <p className="tagline">The books are fiction. The questions are real.</p>
      </section>

      <section className="status-panel" aria-labelledby="backend-status-title">
        <div className="section-heading">
          <h2 id="backend-status-title">Backend Status</h2>
          <span className={health?.status === "ok" ? "status healthy" : "status unavailable"}>
            {isLoading ? "Checking" : health?.status === "ok" ? "Healthy" : "Unavailable"}
          </span>
        </div>

        {error ? <p className="error">{error}</p> : null}

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

      <section className="placeholder">
        <h2>Local Debate MVP foundation is ready.</h2>
        <p>Next slice: provider layer and debate workflow.</p>
      </section>
    </main>
  );
}
