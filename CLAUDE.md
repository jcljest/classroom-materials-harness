# classroom-materials-harness: notes for Claude

- If `local/courses.json` doesn't exist, the teacher hasn't set up yet. Suggest `/setup`.
  `bin/materials status` shows what's done and what's next.
- **Before making any material**, resolve the course with `bin/materials which "<their words>"`,
  then read `local/style.md` and `local/courses/<alias>/<category>.md`.
  Conventions beat generic defaults. The teacher's request beats conventions;
  offer to record a lasting change.
- **HTML first, always.** Every material is built as self-contained HTML first,
  opened for the teacher, and revised until approved. Final formats (PDF,
  posting through canvas-harness) come only after approval. Conventions are
  saved only after the teacher approves an HTML style preview.
- If the needed conventions file is missing, offer `/learn-style` (if samples
  exist) or ask the teacher about the checklist in `templates/conventions/<category>.md`.
- **Privacy:** never put student names, grades or other student information in
  any file. If a sample contains them, stop and ask for a blank copy.
- **Deleting:** the delete guard asks before any delete. Don't work around it.
- **Generic code:** code, templates, skills and docs must not contain any one
  teacher's names, school, courses or paths; those belong only in `local/`.
  The exception is author credit: keep "Jeffrey Lai" in `LICENSE`, `NOTICE.md`
  and the README's License section.
- Run both test suites after changes (see README → Tests).
- Design records live in `docs/ops/`.
