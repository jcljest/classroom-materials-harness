"""bin/materials: small helpers the Claude skills (and teachers) run.

    status            what is set up per course and category, and what to do next
    which NAME        which course a name or nickname means
    init              create the sample drop folders for every course
    samples [ALIAS]   list sample files and whether Claude can read them directly
    extract FILE      plain text from .docx, .pptx or .html (for studying samples)
"""

import argparse
import html
import re
import sys
import zipfile
from pathlib import Path

from . import settings as st
from .settings import SetupError

PROG = "materials"
SETUP_HINT = "First time? Open this repo in Claude Code and type /setup."
DIRECT = {".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".html", ".htm", ".md", ".txt", ".csv"}
EXTRACT = {".docx", ".pptx"}


def _sample_files(alias, category):
    d = st.samples_dir(alias, category)
    if not d.is_dir():
        return []
    return sorted(f for f in d.rglob("*") if f.is_file() and not f.name.startswith(".") and f.name != "README.txt")


def readability(path):
    ext = Path(path).suffix.lower()
    if ext in DIRECT:
        return "read directly"
    if ext in EXTRACT:
        return "read via `materials extract`"
    return "NOT readable: save as PDF and drop that in instead"


def cmd_init(courses):
    made = 0
    for alias in courses:
        for cat in st.CATEGORIES:
            d = st.samples_dir(alias, cat)
            if not d.exists():
                d.mkdir(parents=True)
                made += 1
            note = d / "README.txt"
            if not note.exists():
                note.write_text(f"Drop {st.CATEGORY_HELP[cat]} for @{alias} here.\n"
                                "One or two of your best examples is enough. PDF works best.\n"
                                "Remove student names and grades first.\n")
    print(f"sample folders ready under {st.local_dir() / 'samples'} ({made} created)")
    return 0


def cmd_samples(courses, only=None):
    for alias in ([only] if only else sorted(courses)):
        if alias not in courses:
            print(f"unknown course @{alias}", file=sys.stderr)
            return 2
        print(f"@{alias}  {courses[alias]['name']}")
        for cat in st.CATEGORIES:
            files = _sample_files(alias, cat)
            print(f"  {cat}: {len(files)} file(s)  ({st.samples_dir(alias, cat)})")
            for f in files:
                print(f"    {f.relative_to(st.samples_dir(alias, cat))}  [{readability(f)}]")
    return 0


def _xml_text(xml, para_tag, text_tag):
    out = []
    for para in re.findall(rf"<{para_tag}[ >].*?</{para_tag}>", xml, flags=re.S):
        out.append("".join(html.unescape(t) for t in re.findall(rf"<{text_tag}(?: [^>]*)?>(.*?)</{text_tag}>", para, flags=re.S)))
    return "\n".join(line for line in out if line.strip())


def extract_text(path):
    path = Path(path)
    ext = path.suffix.lower()
    if ext == ".docx":
        with zipfile.ZipFile(path) as z:
            return _xml_text(z.read("word/document.xml").decode("utf-8", "replace"), "w:p", "w:t")
    if ext == ".pptx":
        with zipfile.ZipFile(path) as z:
            slides = sorted((n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                            key=lambda n: int(re.search(r"(\d+)", n).group(1)))
            parts = [f"--- slide {i} ---\n" + _xml_text(z.read(n).decode("utf-8", "replace"), "a:p", "a:t")
                     for i, n in enumerate(slides, 1)]
            return "\n".join(parts)
    if ext in (".html", ".htm"):
        text = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", path.read_text(errors="replace"))
        text = re.sub(r"(?i)<(br|/p|/div|/h\d|/li|/tr)\b[^>]*>", "\n", text)
        text = html.unescape(re.sub(r"<[^>]+>", "", text))
        return "\n".join(line.strip() for line in text.splitlines() if line.strip())
    raise SetupError(f"{path.name}: extract handles .docx, .pptx and .html; Claude reads PDFs and images directly")


def cmd_which(courses, name):
    if not courses:
        print(f"No courses in {st.courses_path()}. {SETUP_HINT}")
        return 1
    matches, candidates = st.resolve_course(name, courses)
    if matches:
        c = courses[matches[0]]
        print(f"@{c['alias']} = {c['name']}")
        return 0
    print(f"no course is called {name!r}.")
    for a in candidates:
        print(f"  maybe @{a} = {courses[a]['name']}")
    if not candidates:
        print("  courses: " + ", ".join(f"@{a} ({c['name']})" for a, c in sorted(courses.items())))
    return 1


def cmd_status(courses):
    if not courses:
        print(f"[TODO] courses: no {st.courses_path().name} yet. {SETUP_HINT}")
        return 1
    done, learned = True, 0
    style = st.style_path()
    print(f"[{'ok  ' if style.exists() else 'TODO'}] teacher-wide style: "
          + (str(style) if style.exists() else "not learned yet; run /learn-style after adding samples"))
    done = done and style.exists()
    for alias, c in sorted(courses.items()):
        nick = f" (also called: {', '.join(c['nicknames'])})" if c.get("nicknames") else ""
        print(f"@{alias}  {c['name']}{nick}")
        for cat in st.CATEGORIES:
            files, conv = _sample_files(alias, cat), st.conventions_path(alias, cat)
            preview = st.preview_path(alias, cat)
            if not conv.exists() and preview.exists():
                done = False
                print(f"  [TODO] {cat}: HTML style preview waiting for your approval ({preview}); "
                      "say what to change, or approve it in /learn-style")
            elif conv.exists():
                learned += 1
                newer = [f.name for f in files if f.stat().st_mtime > conv.stat().st_mtime]
                if newer:
                    print(f"  [warn] {cat}: new samples since conventions were learned ({', '.join(newer)}); "
                          "run /learn-style to update")
                else:
                    print(f"  [ok  ] {cat}: conventions learned from {len(files)} sample(s)")
            elif files:
                done = False
                print(f"  [TODO] {cat}: {len(files)} sample(s) waiting; run /learn-style")
            else:
                print(f"  [----] {cat}: no sample yet; drop {st.CATEGORY_HELP[cat]} in {st.samples_dir(alias, cat)}")
    done = done and learned > 0
    print("\nAll set." if done else "\nNot finished yet: see the TODO lines (or run /setup).")
    return 0 if done else 1


def main(argv=None):
    ap = argparse.ArgumentParser(prog=PROG, description="Helpers for classroom-materials-harness.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status", help="what is set up per course and category, and what to do next")
    sub.add_parser("which", help="which course a name or nickname means").add_argument("name", nargs="+")
    sub.add_parser("init", help="create the sample drop folders for every course")
    sub.add_parser("samples", help="list sample files and whether Claude can read them").add_argument("alias", nargs="?")
    sub.add_parser("extract", help="plain text from .docx, .pptx or .html").add_argument("file")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "extract":
            print(extract_text(args.file))
            return 0
        courses = st.load_courses()
        if args.cmd == "status":
            return cmd_status(courses)
        if args.cmd == "which":
            return cmd_which(courses, " ".join(args.name))
        if not courses:
            print(f"No courses yet. {SETUP_HINT}", file=sys.stderr)
            return 2
        if args.cmd == "init":
            return cmd_init(courses)
        return cmd_samples(courses, args.alias.lstrip("@") if args.alias else None)
    except (SetupError, zipfile.BadZipFile, KeyError, OSError) as e:
        print(f"{PROG}: {e}", file=sys.stderr)
        return 2
