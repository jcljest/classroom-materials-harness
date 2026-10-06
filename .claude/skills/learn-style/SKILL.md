---
name: learn-style
description: Study a teacher's sample materials (their ideal assessment, practice worksheet and activity per course) and turn the patterns into confirmed conventions files that the material-making skills follow. Use when the user types /learn-style, adds or changes samples, says "learn my style", or when `bin/materials status` shows samples waiting or new samples since conventions were learned.
---

# /learn-style

Turn the teacher's best examples into written conventions. **Show the
patterns as an HTML preview first, and write conventions only after the
teacher approves it.** The teacher should recognize their own materials in
the preview, and correct anything you got wrong.

## 1. See what's there

Run `bin/materials samples`. For each course and category with files:

- PDFs, images, HTML, Markdown and text: read them directly (Read tool; for
  long PDFs read every page).
- `.docx` and `.pptx`: run `bin/materials extract <file>`. Formatting is lost,
  so ask for a PDF export if look and layout matter (they usually do).
- Anything marked NOT readable: ask the teacher to save it as PDF.

**Privacy:** if a sample shows student names, grades or other student
information, stop. Ask the teacher to replace it with a blank or teacher
copy. Never copy student information into any file.

## 2. Find the patterns

Use the headings in `templates/conventions/` as the checklist:
`style.md` (teacher-wide) and `assessment.md`, `practice.md`, `activity.md`
(per course). For each item, record:

- **what you see**, concretely ("Name / Date / Period on one line, top
  right"; "3-part scaffold: readings, calculation, meaning in 2-3 sentences"),
- **evidence**: which sample file(s) and page,
- **strength**: seen in every sample, in some, or in only one (one example
  is a guess, so say so).

Then sort them:

- **Teacher-wide** (→ `local/style.md`): seen the same way in samples from
  more than one course or category, like header, fonts, tone, numbering and
  answer-key policy.
- **Course and category specific** (→ `local/courses/<alias>/<category>.md`):
  everything else, plus anything that *differs* between courses (e.g. AP
  hides formula hints, regular physics gives them).

Leave an item blank rather than guess. Gaps become questions in step 3.

## 3. Tell the teacher briefly, then ask

In the chat, keep it short, because the preview in step 4 is the real check:

1. **"Here's your style"**: the 5-10 strongest teacher-wide patterns, each with its evidence.
2. **Per course**: what's specific to each category, and how courses differ.
3. **Questions**: a few at a time, only for what the samples can't show:
   things like "Do students see point values?", "Should the answer key show
   full worked solutions?" and "Is the one-problem-per-page layout deliberate?".
   Use AskUserQuestion for clear choices.

## 4. Show it as an HTML preview, then revise until approved

HTML is the fastest thing to build and the easiest to judge. Teachers confirm
what they *see*, not a list. For each course and category that had samples,
write `local/previews/<alias>/<category>.html`:

- **A short version of the real thing**: 1-2 items (a mini quiz, two
  worksheet problems, or the first page of an activity) on a topic from the
  samples, with new numbers or contexts. Follow every pattern you found:
  header, fonts (closest web-safe match), layout, numbering, stimulus type,
  scaffold, answer space, wording of instructions.
- **Answer-key style**: one short key section on its own printed page,
  labeled TEACHER COPY, so they can check how keys look too.
- **Self-contained**: a single file with inline CSS and inline SVG for graphs
  and diagrams, no external files, `@page { size: letter }`, and print CSS so
  it prints the way the teacher's materials do.
- **Preview notes**: a screen-only panel at the top (hidden when printing,
  via `@media print`) listing the patterns shown, each with its evidence,
  and anything you guessed. That way the teacher can see what's deliberate.

Open it (`open <file>` on macOS, `xdg-open` on Linux) and ask: "Does this look
and work like your materials? What would you change?" Edit the same file for
each round of feedback and reopen it. Repeat until the teacher **approves**
that preview. Their words win over your reading of the samples.

## 5. Write the conventions (only after approval)

Copy each template from `templates/conventions/` and fill it in:

- `local/style.md`
- `local/courses/<alias>/<category>.md` for each category that had samples

Fill in the "Learned from:" line (file names and today's date), and add
"Approved preview: local/previews/<alias>/<category>.html". Material skills use
the approved preview as the visual reference. End every line with its
evidence: `(seen in: …)`, or `(teacher said)` for anything that changed during
preview feedback. Keep the template's headings. Delete lines that don't apply
rather than writing "N/A".

Write a category's conventions only after its preview is approved. An
unapproved preview stays a TODO in `bin/materials status`.

A category with no sample gets no file. Tell the teacher the material
skills will interview them about that category when they first need it,
or they can drop in a sample later.

## 6. Check

Run `bin/materials status`. The categories you studied should show `[ok  ]`.
Give a one-paragraph recap: what you learned, what you asked, and what's
still missing.

## Re-running

When samples are added or changed (status shows `[warn] ... new samples`),
study only those categories. Report what changed compared to the existing
conventions file as a short before/after list, update that category's
preview to show the change, and rewrite the conventions only after the teacher
approves the updated preview.
Never silently drop a `(teacher said)` line. Those came from the teacher, not
the samples.
