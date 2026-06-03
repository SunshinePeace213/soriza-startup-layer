# Anthropic

**Engineering Culture**: AI safety research lab built around empirical alignment work. Engineering and research are tightly coupled — researchers ship production systems and engineers contribute to safety work. Long-term thinking on capabilities, calibrated honesty about risks. Evals-driven everything: every claim about a model needs an eval to back it.

## Title Ladder

| Level | IC Title |
|-------|---------|
| — | Member of Technical Staff (MTS) |
| — | Senior Member of Technical Staff |
| — | Principal Member of Technical Staff |
| — | Distinguished Member of Technical Staff |

Research and engineering tracks share the MTS ladder. Manager track exists but is intentionally thin — most leads remain ICs.

## Distinctive Practices

- **Constitutional AI / RLAIF**: Pioneered training models against a written constitution rather than purely human feedback
- **Mechanistic interpretability**: Heavy investment in understanding why models behave the way they do, not just what they do
- **Responsible Scaling Policy (RSP)**: Public commitments tying capability tier to required safety mitigations
- **Red-teaming**: Internal and external adversarial testing as a release gate, not an afterthought
- **Evals before claims**: No model improvement is announced without an eval that captures it
- **Long context + extended thinking**: Engineering for 1M-token windows and reasoning budgets as first-class features
- **Prompt caching as platform feature**: Caching the system prompt to make agentic workflows affordable

## Key Vocabulary

alignment, RLHF, RLAIF, Constitutional AI, evals, helpfulness/harmlessness/honesty (HHH), mechanistic interpretability, red-team, RSP (Responsible Scaling Policy), context window, extended thinking, prompt caching, tool use, computer use, Claude, Sonnet/Opus/Haiku, Messages API, system prompt, agentic

## Persona Flavor

Safety-first by default — willing to slow down to be right. Empirical: shows results before claims. Writes carefully because words about model behavior get quoted in policy debates. Treats every model release as a chance to lower risk, not just raise capability. Comfortable with ambiguity at the frontier — distinguishes "we don't know yet" from "we know it doesn't work."
