---
name: setup
description: First-time setup (or changes to setup) for classroom-materials-harness. Asks the teacher about their courses and what they call them, creates sample folders, has them drop in their ideal assessment, practice worksheet and activity, then learns their style. Use when the user types /setup, just cloned the repo, wants to add or remove a course, or when `bin/materials status` shows TODO lines.
---

# /setup

Goal: from a fresh clone to `bin/materials status` saying **All set.**, by
asking the teacher short questions. The teacher's main job is to share a few
of their best materials. You do the rest.

## Ground rules

- Ask with AskUserQuestion when there are 2–4 clear choices. Otherwise ask in
  plain text. One topic at a time.
- After each step, run `bin/materials status` and continue from the first TODO.
- Keep the teacher oriented: one line on what's done and what's next.
- Never put student names, grades or other student information in any file.

## 0. Start

Run `bin/materials status`.

- If `local/courses.json` exists, this is a **re-run**. Ask what to change:
  add a course, remove a course, change what they call a course, add
  samples / re-learn their style, or just check. Do only that, then finish with step 5.
- Otherwise, tell them there are 5 short steps, and that the main thing
  they'll do is drop in one ideal example of an assessment, a practice
  worksheet and an activity for each course.

## 1. Check that the delete guard is on

Run `find / -maxdepth 0 -name __hook_probe__ -delete`. It can't match anything,
so it's harmless either way.

- **Blocked by the delete guard:** hooks are on. Continue.
- **It ran:** the project's hooks aren't running. Tell the teacher to reopen
  Claude Code in this folder and accept the project's settings (or check
  `/hooks`), then run `/setup` again. Stop here.

## 2. Courses

If `../canvas-harness/local/courses.json` exists (they also use canvas-harness),
offer to reuse it: same format, same aliases and nicknames. If they agree,
copy it to `local/courses.json` and skip to the confirmation below.

Otherwise, for each course they teach, ask:

- **Course title**, as they'd write it on a handout.
- **Short name (alias):** lowercase letters, digits, `_` (e.g. `chem`, `ap2`), unique.
- **What they call it (nicknames):** "AP", "AP Physics", "3rd period", and so on.
  Case, spaces and punctuation don't matter. A name can belong to only one
  course, and `materials` rejects overlaps. Point out near overlaps ("Physics"
  vs "AP Physics") and ask which course the shorter name should mean.
- **Course folder (optional):** where new materials for this course should
  be saved (e.g. `~/Documents/Chemistry`). Check it exists with `ls`.

Write `local/courses.json`:

```json
{"courses": [{"alias": "chem", "name": "Chemistry 101", "nicknames": ["Chem", "Gen Chem"],
              "local_project": "~/Documents/Chemistry"}]}
```

Show a summary table and get a yes. Then run `bin/materials which "<a nickname>"` once to show it works.

## 3. Sample folders and samples

Run `bin/materials init`. Then explain, using the list from `bin/materials status`:

> For each course, drop **one or two of your best examples** into these folders:
> - `local/samples/<alias>/assessment/`: an ideal quiz or test (and its key, if you have one)
> - `local/samples/<alias>/practice/`: an ideal practice worksheet
> - `local/samples/<alias>/activity/`: an ideal activity, lab or investigation
>
> PDF works best. Use blank or teacher copies, with no student work. If a course
> doesn't use a category, skip it. If two courses share a style, the same file
> can go in both.

Offer to open the folder (`open local/samples` on macOS). Wait until they say
they're done. Run `bin/materials samples` and deal with anything NOT readable
(ask for a PDF export).

## 4. Learn their style

Follow the `learn-style` skill. It tells the teacher the patterns it found,
asks about gaps, builds a short **HTML preview** per category in their style,
revises it with their feedback, and saves the conventions only after they
approve each preview.

## 5. Finish

Run `bin/materials status`. It should say **All set.** Recap:

- their courses, aliases and nicknames;
- what was learned (teacher-wide style, plus which course/category files exist),
  and where the approved previews are (`local/previews/`);
- categories with no sample yet: they'll be asked about those when needed, or
  they can drop a sample in later and run `/learn-style`;
- how to use it: "make a practice worksheet on <topic> for <class>" and
  similar requests follow their learned conventions.
