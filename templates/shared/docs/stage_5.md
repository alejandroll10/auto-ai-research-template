# Stage 5: Paper Writing

**Agent:** `paper-writer`

1. **Paper outline.** Launch paper-writer with instruction: "Write an outline only — do not write LaTeX yet." Provide: theory draft, literature map, scorer assessment (including the **presentation notes** section — the paper-writer must address these), self-attack report. The paper-writer produces `paper/outline.md` with: section-by-section plan, what goes where, how to address self-attack weaknesses, how to incorporate scorer presentation notes, which results to highlight, target length per section.
2. **Review the outline.** Check: does it address the self-attack points? Is the positioning against the literature accurate? Is the structure appropriate for the target journal? If not, provide feedback and re-launch.
3. **Write.** Launch paper-writer with the approved outline + all inputs. Paper-writer creates files in `paper/sections/`:
   - `introduction.tex`
   - `model.tex`
   - `results.tex`
   - `discussion.tex`
   - `conclusion.tex`
   - `appendix.tex` (if needed)
4. Paper-writer creates `paper/main.tex` with `\input` commands
5. Commit: `pipeline: stage 5 — paper draft written`
