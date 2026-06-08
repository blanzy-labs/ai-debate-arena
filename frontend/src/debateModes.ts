import type { DebateModeSlug } from "./types";

export type DebateModeOption = {
  slug: DebateModeSlug;
  displayName: string;
  description: string;
  debaterA: string;
  debaterB: string;
};

export const DEBATE_MODES: DebateModeOption[] = [
  {
    slug: "optimist_vs_skeptic",
    displayName: "Optimist vs Skeptic",
    description: "Stress-test promise versus risk.",
    debaterA: "Optimist",
    debaterB: "Skeptic",
  },
  {
    slug: "builder_vs_breaker",
    displayName: "Builder vs Breaker",
    description: "Stress-test implementation versus failure modes.",
    debaterA: "Builder",
    debaterB: "Breaker",
  },
  {
    slug: "humanist_vs_technologist",
    displayName: "Humanist vs Technologist",
    description: "Stress-test human impact versus technical capability.",
    debaterA: "Humanist",
    debaterB: "Technologist",
  },
  {
    slug: "security_lead_vs_product_lead",
    displayName: "Security Lead vs Product Lead",
    description: "Stress-test risk control versus product delivery.",
    debaterA: "Security Lead",
    debaterB: "Product Lead",
  },
];

export function getDebateMode(slug: DebateModeSlug) {
  return DEBATE_MODES.find((mode) => mode.slug === slug) ?? DEBATE_MODES[1];
}
