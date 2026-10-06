"""Where each teacher's files live, and how their course list is read.

Everything personal sits in one gitignored folder, `local/` in the repo
(override with $MATERIALS_LOCAL):

    local/courses.json                        aliases, titles, nicknames, project folders
    local/samples/<alias>/<category>/         the teacher's ideal examples (drop zone)
    local/style.md                            patterns shared by all of the teacher's samples
    local/courses/<alias>/<category>.md       what is specific to one course and category
    local/previews/<alias>/<category>.html    HTML style preview the teacher approves before
                                              conventions are saved (HTML first, always)

Categories: assessment (quizzes/tests), practice (worksheets), activity (labs,
investigations). courses.json uses the same format as canvas-harness, so one
file can serve both tools.
"""

import json
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CATEGORIES = ("assessment", "practice", "activity")
CATEGORY_HELP = {
    "assessment": "an ideal quiz or test (what students see, plus the answer key if you have one)",
    "practice": "an ideal practice worksheet or problem set",
    "activity": "an ideal activity, lab or investigation handout",
}


class SetupError(Exception):
    """A teacher file is missing or malformed; the message says how to fix it."""


def local_dir():
    return Path(os.environ.get("MATERIALS_LOCAL") or REPO / "local").expanduser()


def courses_path():
    return local_dir() / "courses.json"


def samples_dir(alias, category):
    return local_dir() / "samples" / alias / category


def style_path():
    return local_dir() / "style.md"


def conventions_path(alias, category):
    return local_dir() / "courses" / alias / f"{category}.md"


def preview_path(alias, category):
    return local_dir() / "previews" / alias / f"{category}.html"


def name_key(text):
    """Compare course names loosely: case, spaces, punctuation and a leading @ don't matter."""
    return re.sub(r"[^0-9a-z]", "", str(text).lower())


def course_names(course):
    """Every name a course answers to: alias, nicknames and title."""
    return [course["alias"], *course.get("nicknames", []), course["name"]]


def load_courses(path=None):
    """courses.json -> {alias: course}. Missing file = empty. Same rules as canvas-harness:
    aliases are identifiers, and no name (alias, nickname or title) may mean two courses."""
    path = Path(path or courses_path())
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text())
    except (OSError, ValueError) as e:
        raise SetupError(f"cannot read {path}: {e}")
    courses = raw.get("courses") if isinstance(raw, dict) else None
    if not isinstance(courses, list):
        raise SetupError(f"{path.name} must look like {{\"courses\": [{{\"alias\": ..., \"name\": ...}}]}}")
    out, owner = {}, {}
    for c in courses:
        if not isinstance(c, dict) or not all(k in c for k in ("alias", "name")):
            raise SetupError(f"{path.name}: every course needs alias and name")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", str(c["alias"])):
            raise SetupError(f"{path.name}: alias {c['alias']!r} must be letters, digits or _ (starting with a letter)")
        if c["alias"] in out:
            raise SetupError(f"{path.name}: alias @{c['alias']} is used twice")
        nicks = c.get("nicknames", [])
        if not isinstance(nicks, list) or not all(isinstance(n, str) and name_key(n) for n in nicks):
            raise SetupError(f"{path.name}: @{c['alias']} nicknames must be a list of names")
        for n in course_names(c):
            other = owner.setdefault(name_key(n), c["alias"])
            if other != c["alias"]:
                raise SetupError(f"{path.name}: the name {n!r} would mean both @{other} and @{c['alias']}; "
                                 "give it to one course only")
        out[c["alias"]] = c
    return out


def resolve_course(text, courses):
    """(matches, candidates) for what the teacher calls a class. Exact (normalized) matches only."""
    key = name_key(text)
    if not key:
        return [], []
    matches = [a for a, c in courses.items() if any(name_key(n) == key for n in course_names(c))]
    candidates = [a for a, c in courses.items() if a not in matches and any(
        key in name_key(n) or name_key(n) in key for n in course_names(c) if name_key(n))]
    return matches, candidates


def project_dir(course):
    """A course's local project folder (absolute or ~/...), or None."""
    proj = course.get("local_project")
    return Path(proj).expanduser().resolve() if proj else None
