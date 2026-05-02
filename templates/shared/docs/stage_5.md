# Stage 5: Paper Writing

**Agent:** `paper-writer`

1. **Paper outline.** Launch paper-writer with instruction: "Write an outline only — do not write LaTeX yet." Provide: theory draft, literature map, scorer assessment (including the **presentation notes** section — the paper-writer must address these), self-attack report, `output/stage3/implications.md`, and any `output/puzzle_triage/triage_pN.md` reports that exist (the paper-writer's puzzle-framing rule gates on the triager's measurement-quality verdict). The paper-writer produces `paper/outline.md` with: section-by-section plan, what goes where, how to address self-attack weaknesses, how to incorporate scorer presentation notes, which results to highlight, target length per section.
2. **Review the outline.** Check: does it address the self-attack points? Is the positioning against the literature accurate? Is the structure appropriate for the target journal? If not, provide feedback and re-launch.
3. **Write.** Launch paper-writer with the approved outline + all inputs. Paper-writer creates files in `paper/sections/`:
   - `introduction.tex`
   - `model.tex`
   - `results.tex`
   - `discussion.tex`
   - `conclusion.tex`
   - `appendix.tex` (if needed)
   Paper-writer may *also* populate the internet appendix (`paper/internet_appendix.tex`, a separate compile that ships with the deploy) when a single proof exceeds ~3 pages or the in-paper appendix would otherwise exceed ~30% of main-text length. If the trigger does not fire, the IA file stays as the placeholder skeleton and is ignored downstream.
4. Paper-writer **updates** `paper/main.tex` (a skeleton with a `% PIPELINE-MANAGED` block already exists from setup.sh) — adds `\input` commands for each section file, fills `\title{...}`, `\author{...}`, and the abstract, and adjusts the bibliography commands. **Do not overwrite from scratch and do not delete or modify the `% PIPELINE-MANAGED` block** (the `\usepackage{arpipeline}` line and surrounding markers); these are the deployment fingerprint that downstream tooling depends on. The same `% PIPELINE-MANAGED` discipline applies to `paper/internet_appendix.tex`'s preamble if the IA is populated.
5. **Scan for `[NEEDS THEORY-EXPLORER: ...]` markers.** Paper-writer flags any numerical claim it cannot source from `output/stage2b/` or `output/stage3a/`. For each marker: re-invoke theory-explorer on that specific claim, directing output to `output/stage2b/exploration_for_<claim_id>.md` (do not overwrite the primary `exploration.md`). Wait for the output file, then re-launch paper-writer to fill the gap. Never let a draft ship with `[NEEDS THEORY-EXPLORER]` placeholders or with numerical prose paper-writer authored on its own.
6. **Early bib-verify.** Launch `bib-verifier` on the draft. Same procedure as Stage 8 (OpenAlex + WebSearch fallback). If fabrications or fix-needed cites are found, re-launch paper-writer to drop or correct them before referees see the draft. Stage 8 still runs near the end as the final cite-key check; Stage 9 (polish) then audits the prose-level claims about each cite.
7. Commit: `pipeline: stage 5 — paper draft written`
