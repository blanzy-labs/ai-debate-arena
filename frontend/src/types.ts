export type ProviderName = "openai" | "gemini";

export type DebateModeSlug =
  | "optimist_vs_skeptic"
  | "builder_vs_breaker"
  | "humanist_vs_technologist"
  | "security_lead_vs_product_lead";

export type HealthResponse = {
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

export type DebateRequest = {
  question: string;
  debate_mode: DebateModeSlug;
  debater_a_provider: ProviderName;
  debater_b_provider: ProviderName;
  judge_provider: ProviderName;
};

export type DebateResponse = {
  question: string;
  debate_mode: DebateModeSlug;
  debater_a_role: string;
  debater_b_role: string;
  debater_a_opening: string;
  debater_b_opening: string;
  debater_a_rebuttal: string;
  debater_b_rebuttal: string;
  judge_summary: string;
  strongest_argument_a: string;
  strongest_argument_b: string;
  weakest_assumption_a: string;
  weakest_assumption_b: string;
  unresolved_questions: string[];
  recommended_next_steps: string[];
  suggested_follow_up_debates: string[];
  models_used: {
    debater_a: ModelUsed;
    debater_b: ModelUsed;
    judge: ModelUsed;
  };
};

export type ModelUsed = {
  provider: string;
  model: string;
};
