import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
MATHML = "{http://www.w3.org/1998/Math/MathML}"


class FormulaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.formulas = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-tex" in attrs:
            self.formulas.append({"tex": attrs["data-tex"], "display": attrs.get("data-display") == "true"})


class LatexTests(unittest.TestCase):
    def render(self, formulas, **options):
        process = subprocess.run(["node", "tests/render-latex.mjs"], cwd=ROOT,
                                 input=json.dumps({"formulas": formulas, **options}),
                                 capture_output=True, text=True, timeout=30)
        self.assertEqual(process.returncode, 0, process.stderr)
        return json.loads(process.stdout)

    def test_actual_formulas_render_as_accessible_csp_compatible_mathml(self):
        html = (ROOT / "site/index.html").read_text()
        parser = FormulaParser()
        parser.feed(html)
        self.assertEqual(len(parser.formulas), 9)
        self.assertTrue(all(not formula["display"] for formula in parser.formulas[:4]),
                        "heading formulas must stay inline, not centered display blocks")
        expected = [r"s(n)=\sum\limits_{\substack{d\mid n\\1\le d<n}}d", r"n_{k+1}=s(n_k)", "s(1)=0", "n_k"]
        self.assertEqual([f["tex"] for f in parser.formulas[:4]], expected)
        self.assertTrue(all(formula["display"] for formula in parser.formulas[4:]))
        for formula, rendered in zip(parser.formulas, self.render(parser.formulas)):
            self.assertTrue(rendered["ok"], formula)
            self.assertEqual(rendered["assignments"], 1, "unchanged formulas should be cached")
            root = ET.fromstring(rendered["markup"])
            math = root.find(MATHML + "math")
            self.assertIsNotNone(math)
            self.assertEqual(math.get("display") == "block", formula["display"])
            annotation = math.find(".//" + MATHML + "annotation")
            self.assertEqual(annotation.text, formula["tex"])
            for element in root.iter():
                self.assertNotIn("style", element.attrib, "keep the existing no-inline-style CSP")
                self.assertFalse(any(name.lower().startswith("on") for name in element.attrib))
                self.assertNotIn(element.tag, ["script", "iframe", "img"])
        self.assertLess(html.index("<h1>Aliquot</h1>"), html.index('class="formula tex-math"'))
        self.assertLess(html.index('class="formula tex-math"'), html.index('<form class="controls"'))
        self.assertNotIn('class="math"', html)  # The old upper-right formula is gone.
        self.assertNotIn("Sum the proper divisors. Repeat.", html)
        self.assertIn("proper positive divisors", html)
        css = (ROOT / "site/site.css").read_text()
        formula_rule = css.split(".formula{", 1)[1].split("}", 1)[0]
        group_rule = css.split(".formula-group{", 1)[1].split("}", 1)[0]
        self.assertNotIn("overflow", formula_rule)
        self.assertIn("flex-wrap:wrap", group_rule)
        self.assertIn("justify-content:flex-start", group_rule)
        self.assertIn("align-items:baseline", group_rule)
        sum_markup = self.render([parser.formulas[0]])[0]["markup"]
        self.assertIsNotNone(ET.fromstring(sum_markup).find(".//" + MATHML + "munder"),
                             "sum conditions belong below the operator, not beside the equation")
        self.assertNotIn(".tex-math,#point-factorization", css)

    def test_research_summary_preserves_hypotheses_and_supplied_image(self):
        html = (ROOT / "site/index.html").read_text()
        research = html.split('<h3>What an escaping orbit would require</h3>', 1)[1]
        for qualification in ["Conditional result, not a solution", "classical S-unit",
                              "historical novelty", "no term repeats", "nonperiodicity",
                              "does not mean every prime occurs", "s(0)"]:
            self.assertIn(qualification, research)
        parser = FormulaParser()
        parser.feed(research)
        expected = [
            r"n_0\in\mathbb Z_{>0},\qquad n_{k+1}=s(n_k)=\sum_{\substack{d\mid n_k\\1\le d<n_k}}d",
            r"\forall k\ge0,\ n_k>0;\qquad \forall\,0\le i<j,\ n_i\ne n_j",
            r"\forall S\subseteq\mathbb P,\quad |S|<\infty\ \Longrightarrow\ \left|\{n>1:P(n)\cup P(s(n))\subseteq S\}\right|<\infty",
            r"\forall S\subseteq\mathbb P,\quad |S|<\infty\ \Longrightarrow\ \left|\{k\ge0:P(n_k)\cup P(n_{k+1})\subseteq S\}\right|<\infty",
            r"\left|\bigcup_{k\ge0}P(n_k)\right|=\aleph_0",
        ]
        self.assertEqual([f["tex"] for f in parser.formulas], expected)
        image = ROOT / "site/images/prime-support-whiteboard.png"
        self.assertTrue(image.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertIn('src="images/prime-support-whiteboard.png"', research)
        self.assertIn("summary, not the proof", research)

    def test_plain_text_example_matches_exact_arithmetic(self):
        from aliquot import aliquot_sum
        html = (ROOT / "site/index.html").read_text()
        self.assertIn('class="formula-example"', html)
        self.assertIn("1 + 2 + 3 + 4 + 6 = 16", html)
        self.assertIn("1 + 2 + 4 + 8 = 15", html)
        self.assertIn("excluding 12 itself", html)
        self.assertIn("12 → 16 → 15 → …", html)
        self.assertIn('href="https://en.wikipedia.org/wiki/Aliquot_sequence"', html)
        self.assertIn("Catalan’s 1888 conjecture, later extended by Dickson, remains open.", html)
        self.assertLess(html.index('class="formula-history"'), html.index('<form class="controls"'))
        self.assertEqual(aliquot_sum(12), 16)
        self.assertEqual(aliquot_sum(16), 15)
        self.assertLess(html.index('class="formula-example"'), html.index('<form class="controls"'))

    def test_factorization_has_real_superscripts(self):
        result = self.render([{"tex": r"2^{20} \times 3"}])[0]
        self.assertTrue(result["ok"])
        root = ET.fromstring(result["markup"])
        self.assertIsNotNone(root.find(".//" + MATHML + "msup"))
        self.assertEqual(result["assignments"], 1)

    def test_invalid_tex_and_missing_library_keep_readable_fallbacks(self):
        formulas = [{"tex": r"\frac{"}, {"tex": r"\def\a{\a}\a"}, {"tex": "n" * 4097}]
        for result in self.render(formulas):
            self.assertFalse(result["ok"])
            self.assertEqual(result["text"], "Readable fallback")
            self.assertEqual(result["markup"], "")
        result = self.render([{"tex": "s(n)"}], withoutLibrary=True)[0]
        self.assertFalse(result["ok"])
        self.assertEqual(result["text"], "Readable fallback")

    def test_untrusted_tex_cannot_create_links_images_or_script_elements(self):
        results = self.render([
            {"tex": r"\href{javascript:alert(1)}{x}"},
            {"tex": r"\includegraphics{https://example.invalid/image.png}"},
            {"tex": r"\htmlClass{injected}{x}"},
        ])
        for result in results:
            if result["ok"]:
                root = ET.fromstring(result["markup"])
                for element in root.iter():
                    self.assertNotIn(element.tag.rsplit("}", 1)[-1], ["a", "img", "script", "iframe"])
                    self.assertNotIn("href", element.attrib)
                    self.assertNotIn("src", element.attrib)
            else:
                self.assertEqual(result["text"], "Readable fallback")

    def test_vendor_is_pinned_and_licensed(self):
        bundle = ROOT / "site/vendor/katex/katex.min.js"
        self.assertEqual(hashlib.sha256(bundle.read_bytes()).hexdigest(),
                         "103a53763cc033bba8d175bf3f0ba597c3505c9b6747dd3f2c7bc2a6bfcc8ae7")
        self.assertIn("Permission is hereby granted", (bundle.parent / "LICENSE").read_text())
