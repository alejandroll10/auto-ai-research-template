### Faithful-mode override (applies because `faithful: true` in `pipeline_state.json`)

The INCREMENTAL-forwarding (Step 5) and OBVIOUS-forwarding (Step 6) instructions above do **not** fire. Document the verdict in `output/seed/limitations.md` (one paragraph: the seed's named result, the prototype/novelty verdict, what this implies for the paper's contribution claim) and proceed to Stage 2 with the contract intact.

Do NOT inject the "find a result the existing literature does not imply" instruction into the theory-generator prompt, and do NOT inject the "find a non-obvious result within the model" instruction. Both instructions can pull theory-generator toward a different result than the seed's stated one — a substitution, which is forbidden in faithful mode. Theory-generator may still **add** non-obvious or non-incremental extensions on top of the faithfully-implemented contract; what it may not do is replace the contract's stated result as the headline because the original was flagged OBVIOUS or INCREMENTAL.

Append a row to `process_log/pivot_log.md`: stage = `stage_1`, agent = `idea-prototyper` or `novelty-checker`, verdict = the actual verdict, classification = `[DOCUMENT-AND-PROCEED]`.
