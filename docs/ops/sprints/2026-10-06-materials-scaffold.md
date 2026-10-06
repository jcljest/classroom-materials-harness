---
id: 2026-10-06-materials-scaffold
module: materials
status: ready_for_review
health: green
owner_session: null
worktree: classroom-materials-harness
started: 2026-10-06
updated: 2026-10-06
base_commit: ba47e6c
depends_on: []
blocks: []
---

# Stage 1: repo scaffold, /setup, /learn-style

## Objective

A clonable repo where a teacher sets up their courses, drops in an ideal
assessment, practice worksheet and activity per course, and gets confirmed
conventions learned from them.

## Why This Matters

The owner wants to share their modular material tools so other teachers can
get materials in their own style without writing conventions by hand.

## Scope

- `bin/materials` (status, which, init, samples, extract) + tests.
- Sample folder layout and conventions templates (style + 3 categories).
- `/setup` and `/learn-style` skills.
- Delete guard (shared with canvas-harness), README, CLAUDE.md, LICENSE (MIT, Jeffrey Lai), NOTICE.
- docs/ops records.

## Non-goals

- Stage 2: porting the fluency-worksheet and printable-quiz skills.
- Stage 3: STEP investigation skill (renderer/verifier exist, skill does not).
- Publishing to GitHub (owner creates the empty repo first).

## Acceptance Criteria

- [x] `materials` commands tested: course validation (canvas-harness compatible), which, init, samples readability, docx/pptx/html extract, status progression including stale samples.
- [x] Delete guard tests pass in this repo; the /setup hook probe is a harmless command the guard denies.
- [x] `/setup` and `/learn-style` skills written; learn-style requires confirmation before writing and cites evidence per line.
- [x] No teacher-specific data in tracked files.
- [x] Dry run: a scratch teacher with real sample PDFs gets correct `samples`/`status` output.
- [x] HTML-first previews (owner request): /learn-style builds an HTML style preview per category in `local/previews/<alias>/<category>.html`; conventions are written only after the teacher approves a preview; `status` shows previews awaiting approval; HTML-first rule documented for all materials.

## Plan

1. Package + CLI + tests.
2. Templates, skills.
3. Docs, records, dry run.

## Progress / Checkpoints

### 2026-10-06
- Owner decisions: repo name classroom-materials-harness; v1 tools = learn-style, fluency worksheet, printable quiz, STEP investigation (staged); conventions learned from one ideal sample per category per course, shown as patterns before saving.
- Inventory of existing tools: modular-fluency-worksheet and printable-quiz are generic (read course conventions); graph.js and print-worksheet.css reusable; step-investigation has assets but no SKILL.md; step-teacher-card empty.
- Note: this record was created after the first code was written (process slip); contents reflect actual work.
- Built package, CLI, tests, templates, skills, docs.
- Owner: previews should be HTML (fastest for Claude) and teacher preferences confirmed on an HTML preview before being finalized. Added: `preview_path`, status TODO for unapproved previews (+ test), learn-style steps 4-5 (build/revise/approve preview, then write conventions), templates carry 'Approved preview:', HTML-first rule in CLAUDE.md/README/setup, ADR-0002.

## Files Changed

- materials_harness/{__init__,__main__,settings,cli}.py, bin/materials, tests/test_cli.py
- templates/conventions/{style,assessment,practice,activity}.md
- .claude/settings.json, .claude/hooks/guard_deletes.py (+ tests), .claude/skills/{setup,learn-style}/SKILL.md
- README.md, CLAUDE.md, LICENSE, NOTICE.md, .gitignore
- docs/ops/{ARCHITECTURE.md, modules/materials.md, decisions/ADR-0001-learn-style-from-samples.md}

## Verification Evidence

### Commands Run

```text
python3 -m unittest discover -s tests                 -> Ran 9 tests, OK
python3 -m unittest discover -s .claude/hooks/tests   -> Ran 5 tests, OK
guard_deletes.decide(setup probe)                      -> deny (harmless if hooks are off)
scratch teacher + copies of real sample PDFs/PNG       -> init 6 folders; samples lists readability; status TODO per category; which ap2 -> @ap
personal-data scan of all files                        -> only author credit and generic examples
```

### Results

- Stage 1 criteria verified offline. NOT yet exercised: /learn-style on real samples in a live session (needs teacher confirmation); hook probe inside a session opened in this repo.

## Decisions

- [ADR-0001](../decisions/ADR-0001-learn-style-from-samples.md)
- [ADR-0002](../decisions/ADR-0002-html-first-previews.md)

## Dependency Changes

- None.

## Risks / Blockers

- Pattern quality depends on sample quality; one sample per category is thin, so the skill marks single-sample patterns for confirmation.

## Human Decision Needed

- None.

## Handoff

### Outcome
Stage 1 scaffold built; offline-verified.

### Current State
ready_for_review; initial commit ba47e6c pushed to origin/main (github.com/jcljest/classroom-materials-harness).

### Next Action
Live /setup + /learn-style run on real samples; then Stage 2.
