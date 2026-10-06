---
id: ADR-0001
status: accepted
date: 2026-10-06
affected_modules:
  - materials
supersedes: null
superseded_by: null
---

# ADR-0001: Learn conventions from the teacher's ideal samples, per course and category

## Context

The original worksheet and quiz skills read a hand-written
`assessment-conventions.md` per course, created by interview. The owner wants
teachers to supply their ideal assessment, practice worksheet and activity,
have Claude recognize their style, and scaffold each course modularly.

## Decision

- Three categories: assessment, practice, activity.
- Samples go in `local/samples/<alias>/<category>/`.
- `/learn-style` reports patterns with evidence and strength, asks about gaps,
  and writes files only after the teacher confirms:
  - `local/style.md`: patterns shared across the teacher's samples;
  - `local/courses/<alias>/<category>.md`: course- and category-specific rules.
- Every line cites its source: `(seen in: file)` or `(teacher said)`. Re-learning
  never drops `(teacher said)` lines silently.
- Separate repo from canvas-harness, sharing the `courses.json` format.

## Options Considered

- Per-course only: duplicates the teacher's shared style in every course file.
- Teacher-wide only: blurs real differences between courses (e.g. AP vs. regular scaffolding).
- Interview only: slower, and teachers describe their style less accurately than their materials show it.

## Consequences

- Material skills must read both files, with the course file winning on conflicts.
- A category without samples has no file; material skills fall back to the interview checklist.
