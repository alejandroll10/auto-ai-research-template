### Faithful-mode override (applies because `faithful: true` in `pipeline_state.json`; supersedes the seeded-mode override)

Referees do not know this is a faithful run. They evaluate the paper as if it were a normal pipeline submission; that is the correct behavior — corrupting the evaluation signal corrupts the paper. The faithful constraint enters at the triager's classification of the editor's canonical comment list, not at the referees themselves.

**Reject**: revise and resubmit with the contract intact. Stop and write a post-mortem to `output/seed/abandon_report.md` only after **2 rounds where the editor's aggregated verdict was Reject and the rejection cites genuinely fundamental flaws in the seed's own claims** — not in the choice of topic, framing, or research question. A Reject vote that the editor escapes to Major Revision + Downgrade per its tier-fit escape rule does **not** count toward this 2-rejection threshold. Do NOT return to Stage 0 or Stage 1.

**Major Revision — comment classification under the faithful contract**, in addition to the normal `[FIX]`/`[LIMITS]`/`[RESPONSE]`/`[NOTE]` tags:

- "Paper would be stronger if it were about X instead" → `[RESPONSE]`. The seed names the topic.
- "The mechanism is wrong, try Y" → adopt Y ONLY if required for mathematical correctness. If Y is "more publishable" or "more aligned with the recent literature," classify as `[RESPONSE]`.
- "Scope is too narrow / too broad" → if the contract intentionally specifies the scope, classify as `[LIMITS]` (one sentence in limitations) rather than `[FIX]`.
- "The buried result Y is more interesting than the headline X" → `[RESPONSE]`. The contract names the headline.
- "This is the wrong identification strategy" — adopt only if the new strategy is required for the result to be correctly identified (i.e., the original is inconsistent or biased), not because the new strategy is "more credible" / "more standard." If the seed's named identification strategy is internally consistent, classify as `[RESPONSE]`.
- Comments on math, derivations, missing proofs, identification consistency, internal validity → `[FIX]` as normal.

**Mechanism referee verdicts (`referee-mechanism`)**: filter against the contract.

- **MECHANISM-VALID / MECHANISM-PARTIAL** — apply normally.
- **MECHANISM-MISATTRIBUTED** — the math delivers a different driver than the contract claims. Document the finding in `output/seed/mechanism_concern.md`. **Required action**: revise the presentation to match what the math supports while keeping the contract's named mechanism as the studied object — present the math-supported driver as a structural characterization of the contract's mechanism, with the gap acknowledged as a limitation. Do NOT rewrite the paper around an unrelated mechanism the seed never proposed. If the actual driver is so different from the contract's named mechanism that no honest narrow-framing exists, escalate to operator with `output/seed/mechanism_concern.md` as the artifact.
- **MECHANISM-DECORATIVE** — the mechanism referee judges the contract's mechanism to be window dressing for what the math actually delivers. Document in `output/seed/mechanism_concern.md`. Strip unsupported generality and present what the math delivers as a structural characterization, preserving the contract's named topic. DECORATIVE does NOT count toward the 2-rejection abandon threshold.

**Tier-fit escape**: the editor may downgrade the journal tier in faithful mode. The contract specifies what the paper is about; it does not specify which journal must accept it. A downgrade with the contract intact is a normal outcome of faithful mode and is logged but not blocked.

The contract is the contract. Referee feedback refines execution, not direction.
