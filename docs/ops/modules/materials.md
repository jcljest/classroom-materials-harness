---
module: materials
health: green
updated: 2026-10-06
---

# materials

## Purpose

The whole product: style learning, conventions, and material-making skills.

## Inputs

- `local/courses.json`, teacher samples in `local/samples/<alias>/<category>/`.

## Outputs

- `local/style.md`, `local/courses/<alias>/<category>.md`; generated HTML handouts (stage 2+).

## Interfaces / Contracts

- `bin/materials <status|which|init|samples|extract>`.
- Categories: assessment, practice, activity.
- `courses.json`: `{"courses": [{alias, name, nicknames?, local_project?, ...}]}`; extra keys allowed (canvas-harness compatible). No name may mean two courses.
- Conventions files follow `templates/conventions/*.md` headings; each line cites `(seen in: file)` or `(teacher said)`.
- `$MATERIALS_LOCAL` overrides `local/`.

## Invariants

- Conventions are written only after the teacher approves an HTML style preview (`local/previews/<alias>/<category>.html`).
- Every material is HTML first and approved before any final format.
- No student information in any file.
- No teacher-specific data in tracked files.

## Dependencies

- Python 3.9+ stdlib; Claude Code. Chrome/Chromium optional (page checks, stage 2).

## Non-goals

- Posting to an LMS (that's canvas-harness).

## License

- MIT, copyright Jeffrey Lai.

## Current Health

**Green**

Reason: Stage 1 scaffold.

## Active Sprints

- 2026-10-06-materials-scaffold

## Next Milestone

Stage 2: port fluency worksheet and printable quiz to read learned conventions.
