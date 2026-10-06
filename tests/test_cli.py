import io
import json
import os
import sys
import tempfile
import time
import unittest
import zipfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from materials_harness import cli  # noqa: E402
from materials_harness import settings as st  # noqa: E402

PHYS = {"alias": "phys", "name": "Physics Fall", "nicknames": ["Physics", "Regular Physics"]}
AP = {"alias": "ap", "name": "AP Physics 2 Fall", "nicknames": ["AP", "AP2", "AP Physics"]}


class Base(unittest.TestCase):
    def setUp(self):
        self.local = Path(tempfile.mkdtemp())
        self.env = mock.patch.dict(os.environ, {"MATERIALS_LOCAL": str(self.local)})
        self.env.start()
        self.addCleanup(self.env.stop)

    def write_courses(self, *courses):
        (self.local / "courses.json").write_text(json.dumps({"courses": list(courses)}))

    def run_cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            rc = cli.main(list(argv))
        return rc, out.getvalue() + err.getvalue()


class Courses(Base):
    def test_resolve_and_collisions(self):
        self.write_courses(PHYS, AP)
        courses = st.load_courses()
        self.assertEqual(st.resolve_course("ap physics", courses)[0], ["ap"])
        self.assertEqual(st.resolve_course("physics", courses)[0], ["phys"])
        self.write_courses(PHYS, {**AP, "nicknames": ["physics"]})
        with self.assertRaises(st.SetupError):
            st.load_courses()

    def test_canvas_harness_roster_is_compatible(self):
        # canvas-harness rosters carry extra keys (id, pdf_prefix); they must load here unchanged.
        self.write_courses({**AP, "id": 2002, "pdf_prefix": "AP2", "local_project": "~/x"})
        self.assertEqual(st.load_courses()["ap"]["id"], 2002)

    def test_which(self):
        self.write_courses(PHYS, AP)
        rc, out = self.run_cli("which", "AP2")
        self.assertEqual((rc, out.strip()), (0, "@ap = AP Physics 2 Fall"))
        rc, out = self.run_cli("which", "phys", "class")
        self.assertEqual(rc, 1)
        self.assertIn("maybe @phys", out)


class Samples(Base):
    def test_init_creates_drop_folders(self):
        self.write_courses(PHYS, AP)
        rc, _ = self.run_cli("init")
        self.assertEqual(rc, 0)
        for alias in ("phys", "ap"):
            for cat in st.CATEGORIES:
                self.assertTrue((st.samples_dir(alias, cat) / "README.txt").exists())
        self.assertEqual(self.run_cli("init")[0], 0)  # safe to re-run

    def test_samples_lists_readability(self):
        self.write_courses(AP)
        self.run_cli("init")
        d = st.samples_dir("ap", "practice")
        for name in ("hw.pdf", "notes.docx", "old.pages"):
            (d / name).write_bytes(b"x")
        rc, out = self.run_cli("samples", "@ap")
        self.assertEqual(rc, 0)
        self.assertIn("practice: 3 file(s)", out)
        self.assertIn("hw.pdf  [read directly]", out)
        self.assertIn("notes.docx  [read via `materials extract`]", out)
        self.assertIn("old.pages  [NOT readable", out)
        self.assertNotIn("README.txt", out)


class Extract(Base):
    def make_zip(self, name, files):
        p = self.local / name
        with zipfile.ZipFile(p, "w") as z:
            for n, data in files.items():
                z.writestr(n, data)
        return p

    def test_docx(self):
        doc = ('<w:document><w:body><w:p><w:r><w:t>Name: ____</w:t></w:r></w:p>'
               '<w:p><w:r><w:t xml:space="preserve">1. Find the </w:t></w:r><w:r><w:t>slope &amp; units.</w:t></w:r></w:p>'
               '</w:body></w:document>')
        p = self.make_zip("q.docx", {"word/document.xml": doc})
        self.assertEqual(cli.extract_text(p), "Name: ____\n1. Find the slope & units.")

    def test_pptx_slides_in_order(self):
        s = '<p:sld><a:p><a:r><a:t>{}</a:t></a:r></a:p></p:sld>'
        p = self.make_zip("a.pptx", {"ppt/slides/slide10.xml": s.format("ten"), "ppt/slides/slide2.xml": s.format("two")})
        text = cli.extract_text(p)
        self.assertLess(text.index("two"), text.index("ten"))
        self.assertIn("--- slide 1 ---", text)

    def test_html_and_unsupported(self):
        p = self.local / "w.html"
        p.write_text("<style>p{}</style><h1>Practice</h1><p>Q1 &lt;3</p><script>x()</script>")
        self.assertEqual(cli.extract_text(p), "Practice\nQ1 <3")
        rc, out = self.run_cli("extract", str(self.local / "x.pdf"))
        self.assertEqual(rc, 2)
        self.assertIn("reads PDFs and images directly", out)


class Status(Base):
    def test_progression(self):
        rc, out = self.run_cli("status")
        self.assertEqual(rc, 1)
        self.assertIn("/setup", out)

        self.write_courses(AP)
        self.run_cli("init")
        sample = st.samples_dir("ap", "assessment") / "quiz.pdf"
        sample.write_bytes(b"x")
        rc, out = self.run_cli("status")
        self.assertEqual(rc, 1)
        self.assertIn("[TODO] assessment: 1 sample(s) waiting", out)
        self.assertIn("[----] practice: no sample yet", out)

        preview = st.preview_path("ap", "assessment")
        preview.parent.mkdir(parents=True)
        preview.write_text("<html></html>")
        rc, out = self.run_cli("status")
        self.assertEqual(rc, 1)
        self.assertIn("[TODO] assessment: HTML style preview waiting for your approval", out)

        st.style_path().write_text("# style\n")
        conv = st.conventions_path("ap", "assessment")
        conv.parent.mkdir(parents=True)
        conv.write_text("# conventions\n")
        rc, out = self.run_cli("status")
        self.assertEqual(rc, 0, out)
        self.assertIn("[ok  ] assessment: conventions learned from 1 sample(s)", out)

        later = time.time() + 5
        os.utime(sample, (later, later))
        rc, out = self.run_cli("status")
        self.assertIn("new samples since conventions were learned (quiz.pdf)", out)


if __name__ == "__main__":
    unittest.main()
