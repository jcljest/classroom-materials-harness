# classroom-materials-harness

Teach Claude Code **your** style once, then ask it for new assessments,
practice worksheets and activities that look and work like yours.

You give it one or two of your best examples per course. Claude studies them,
shows you the patterns it recognizes (your header, your scaffolding, how you
word instructions, how your answer keys work), asks about anything the
samples can't show, and saves those conventions once you've confirmed them.
Every new handout for that course follows them.

## Quick start

1. Clone this repo and open the folder in Claude Code. When it asks whether
   to trust the project's settings, say yes. That turns on the delete guard
   (see [Safety](#safety)).
2. Type `/setup`. Claude asks about your courses and what you call them,
   creates a sample folder for each one, and asks you to drop in:
   - an ideal **assessment** (quiz or test),
   - an ideal **practice** worksheet,
   - an ideal **activity** (lab or investigation).
3. Claude studies them (`/learn-style`), tells you what it recognized, and
   builds a short **HTML preview** of each category in your style. It opens in
   your browser. Say what's off, Claude revises it, and your conventions are
   saved only once you approve the preview.

**HTML first.** Everything Claude makes is a self-contained HTML page first,
because that's the fastest thing to build and the easiest for you to check.
You look at it in your browser, ask for changes, and approve it. Only then
does it become the final version (print it to PDF, or post it with
canvas-harness).

`bin/materials status` shows what's done and what's next at any time.

## How it's organized

| path | what it holds |
|---|---|
| `local/courses.json` | your courses: short name (`@chem`), title, nicknames, course folder |
| `local/samples/<course>/<category>/` | your example materials (drop zone) |
| `local/style.md` | patterns shared by all your samples (header, fonts, tone, answer keys) |
| `local/courses/<course>/<category>.md` | what's specific to one course and category |
| `local/previews/<course>/<category>.html` | the HTML style preview you approved (the visual reference) |
| `templates/conventions/` | the checklist of patterns Claude looks for |

`local/` is gitignored, so your materials and conventions are never committed.
Every learned convention says where it came from, either `(seen in: your-file.pdf)`
or `(teacher said)`, so you can check and correct it.

`courses.json` uses the same format as [canvas-harness](https://github.com/jcljest/canvas-harness).
If you use both, `/setup` can reuse your course list.

## Material tools

| category | tool | status |
|---|---|---|
| practice | fluency worksheet: tiered problems, given graph/table stimulus, fixed response scaffold, separate answer key | coming next |
| assessment | printable one-page quiz with a computed graph and a shared answer key | coming next |
| activity | STEP-style investigation: 2-page student handout and 1-page teacher card from one spec | planned |

## Commands

```sh
bin/materials status            # what's set up and what's next
bin/materials which "AP"        # which course a name or nickname means
bin/materials init              # create sample folders for every course
bin/materials samples [@course] # list samples and whether Claude can read them
bin/materials extract file.docx # plain text from .docx/.pptx/.html
```

Claude reads PDFs and images directly. Word and PowerPoint files are read
as text only, so export them to PDF when layout matters.

## Safety

`.claude/settings.json` turns on a **delete guard** (`.claude/hooks/guard_deletes.py`):
Claude must ask before deleting anything, and catastrophic deletes (`rm -rf`
of `/`, `~`, `..`, `.git`, `local/`, the project, or anything outside it) are
always blocked. It's pattern-based: it catches mistakes, not a determined bypass.

**Privacy:** use blank or teacher copies as samples. Claude is told to stop if
a sample contains student names or grades, and never to copy student
information into any file.

## Requirements

- Claude Code
- Python 3.9+ (standard library only)

## Tests

```sh
python3 -m unittest discover -s tests
python3 -m unittest discover -s .claude/hooks/tests
```

## License

MIT © Jeffrey Lai. Use it, change it and share it. Just keep the copyright
notice. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).
