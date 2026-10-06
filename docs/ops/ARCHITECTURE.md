# Architecture

## Purpose

classroom-materials-harness is a clonable Claude Code harness that learns a
teacher's style from their own example materials and then produces new
assessments, practice worksheets and activities in that style.

## Flow

```
samples (ideal examples) -> /learn-style -> HTML style preview -> teacher approves -> conventions -> material skills -> HTML handout -> teacher approves -> final (PDF / post)
local/samples/<a>/<cat>/    patterns +       local/previews/        (revise until      local/style.md                  course folder
```

## Layout

| part | role |
|---|---|
| `materials_harness/` | `bin/materials`: status, course lookup, sample folders, text extraction |
| `.claude/skills/setup` | onboarding interview |
| `.claude/skills/learn-style` | samples -> pattern report -> confirmed conventions |
| `.claude/skills/<material>` | material tools (stage 2+), all read conventions first |
| `templates/conventions/` | the pattern checklist per file |
| `local/` (gitignored) | everything personal |

## Boundaries

- Code and skills are generic; a teacher's style lives only in `local/` as confirmed conventions.
- HTML first: every output is a self-contained HTML preview the teacher approves before anything is finalized.
- Every convention line cites its evidence (a sample file or the teacher's words).
- No student information in any file.
- `courses.json` is format-compatible with canvas-harness (shared aliases and nicknames).
- Handoff to canvas-harness: material skills write HTML into the course's `local_project`, which `canvas-harness pdf` can render and post.
