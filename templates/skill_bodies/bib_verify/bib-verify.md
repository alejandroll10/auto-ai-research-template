## What this is

A bibliography sanity check. Verifies every citation in the paper's references file against OpenAlex (a free bibliographic database covering ~250M scholarly works). Catches hallucinated, mistitled, or wrong-year citations before they ship.

Backing script: `code/utils/bib_verify/verify_bib.sh`. Reads `EMAIL` from `.env` for the OpenAlex polite pool.

## When to use

- After paper-writer finishes a draft and after every referee round that adds or changes citations.
- Before the pipeline marks `"status": "complete"`.
- Ad hoc whenever you want to sanity-check a bibliography (`/bib-verify` from the user, or `code/utils/bib_verify/verify_bib.sh` from any agent).

## How to run

```bash
# Auto-detects paper/references.bib, references/references.bib,
# references/references.md, or paper/references.md (in that order)
code/utils/bib_verify/verify_bib.sh

# Or pass an explicit file
code/utils/bib_verify/verify_bib.sh references/references.md
code/utils/bib_verify/verify_bib.sh paper/references.bib
```

Outputs:
- `output/bib_verification.md` — human-readable report grouped by status
- `output/bib_verification.jsonl` — one JSON object per entry (for machine triage)

## Status meanings

| Status | What it means | What to do |
|--------|---------------|------------|
| **VERIFIED** | OpenAlex returned a hit with title similarity ≥ 0.85 and matching year. High confidence the paper exists as cited. | Nothing. Move on. |
| **RESOLVED** | Title similarity 0.60–0.85, or year off by >1. Probably the same paper, but the cite is sloppy. | Read the matched title/venue. If it's clearly the right paper with a typo in the cite, fix the cite. If not, demote to MISS and triage. |
| **MISS** | No good OpenAlex match. Three possibilities: (a) SSRN-only working paper not indexed, (b) very recent (last few months), (c) fabricated. | Run the SSRN/WebSearch fallback below. Only mark as fabricated after the fallback also fails. |

## SSRN / WebSearch fallback for MISS entries

OpenAlex has weak coverage of SSRN-only working papers and very recent preprints. So a MISS is not automatic evidence of fabrication — but the burden of proof shifts to confirming the paper exists.

For each MISS:

1. **WebSearch** the title in quotes. Try variants:
   - `"Exact Title Of Paper" author-last-name`
   - `"Exact Title" site:ssrn.com`
   - `"Exact Title" site:nber.org`
   - `"Exact Title" site:arxiv.org`
2. If a real result appears (matching title + plausible authors + year), the cite is real but unindexed by OpenAlex. Mark it RESOLVED-VIA-WEBSEARCH and capture the URL.
3. If WebSearch also returns nothing matching, mark it FABRICATED.

**Be honest at this step.** A vague hit ("paper with similar topic by different author") is not a confirmation. The whole point of verification is to catch hallucinations; don't soften the verdict to avoid the work of removing a cite.

## Final triage report

After both passes, write a triage section to `output/bib_verification.md` (append, don't overwrite the script-generated content):

```markdown
## Triage

### Confirmed (no action)
- N entries VERIFIED by OpenAlex
- M entries RESOLVED-VIA-WEBSEARCH (URLs added below)

### Cite fixes needed
- `key1`: title typo — change "..." → "..."
- `key2`: wrong year — change 2019 → 2020
- ...

### Likely fabrications (remove or replace)
- `key3`: "..." — no OpenAlex hit, no WebSearch match. Likely hallucinated.
- ...
```

## Rules

- **Don't accept the verdict blindly.** OpenAlex sometimes returns a high-similarity match that is the wrong paper (common-title collisions). For RESOLVED entries, glance at the venue and authors before treating it as a fix.
- **Don't auto-edit the bibliography.** Report findings; let the caller (paper-writer or human) decide how to fix. Editing `.tex` or the references file is downstream of this skill's job.
- **EMAIL is required for the polite pool.** If `EMAIL` is missing from `.env`, the script still works but rate limits are tighter and lookups may fail. Warn if you notice many `api-error` notes in the report.
- **MISS ≠ fabricated.** Always run the WebSearch fallback before declaring fabrication. False accusations of fabrication are as bad as missing real ones.
