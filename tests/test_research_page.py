"""Static-site navigation, presentation boundaries, and mathematical scope."""

from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlsplit

from aliquot import aliquot_sum

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SOURCE_REVISION = "78b6c8b92ad71e1febfca577bd57de5b0a32c5b1"


class PageParser(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

    @property
    def ids(self):
        return [attrs["id"] for _, attrs in self.elements if "id" in attrs]


class ResearchPageTests(unittest.TestCase):
    def test_home_is_an_explorer_with_a_link_not_an_embedded_timeline(self):
        home = (SITE / "index.html").read_text()
        self.assertIn('<a id="research" href="/research/">Research</a>', home)
        self.assertNotIn('class="research-timeline"', home)
        self.assertNotIn('/research.css', home)
        self.assertIn('id="graph"', home)
        research = (SITE / "research/index.html").read_text()
        self.assertIn('<a href="/research/" aria-current="page">Research</a>', research)
        self.assertIn('<a href="/">Explore</a>', research)
        self.assertNotIn('<canvas', research)
        scripts = [urlsplit(attrs["src"]).path for tag, attrs in PageParser(research).elements if tag == "script"]
        self.assertEqual(scripts, ["/vendor/katex/katex.min.js", "/latex.js"])

    def test_timeline_has_dated_accessible_entries_and_expandable_details(self):
        html = (SITE / "research/index.html").read_text()
        page = PageParser(html)
        self.assertEqual(len([tag for tag, _ in page.elements if tag == "h1"]), 1)
        entries = [attrs["id"] for tag, attrs in page.elements if tag == "li"]
        self.assertEqual(entries, ["recovery", "prime-templates", "factor-transport", "prime-supply", "prime-support"])
        dates = [attrs["datetime"] for tag, attrs in page.elements if tag == "time"]
        self.assertEqual(dates, ["2026-10-22"] * 4 + ["2026-10-21"])
        self.assertEqual(len([tag for tag, _ in page.elements if tag == "article"]), 5)
        self.assertEqual(len([tag for tag, _ in page.elements if tag == "summary"]), 5)
        self.assertIn('href="#timeline">Skip to timeline', html)
        for _, attrs in page.elements:
            if "data-tex" in attrs:
                self.assertEqual(attrs.get("tabindex"), "0", "formula scrollers must be keyboard reachable")
                self.assertTrue(attrs.get("aria-label"))
        css = (SITE / "research.css").read_text()
        self.assertIn("overflow-x: auto", css)
        self.assertIn("background: #fff", css)
        self.assertIn("@media (max-width: 500px)", css)
        for decoration in ["box-shadow", "border-radius", "border-left", "position: sticky"]:
            self.assertNotIn(decoration, css)
        for removed in ["journal-deck", "journal-rail", "result-tag", "orbit-example", "open-question"]:
            self.assertNotIn(removed, html)
        for slogan in ["Finite growth.", "Infinite questions.", "Growth is not yet renewal."]:
            self.assertNotIn(slogan, html)

    def test_formula_overflow_is_horizontal_only_with_block_math_wrapper(self):
        css = (SITE / "research.css").read_text()
        formula_rule = css.split(".research-formula {", 1)[1].split("}", 1)[0]
        self.assertIn("overflow-x: auto", formula_rule)
        self.assertIn("overflow-y: hidden", formula_rule)
        self.assertNotIn("height:", formula_rule, "formula height must grow with its MathML")
        self.assertIn(".research-formula > .katex { display: block; }", css)
        self.assertNotIn("scrollbar-width: none", css, "wide mobile formulas must remain scrollable")

    def test_local_links_assets_and_accessible_references_resolve_on_all_pages(self):
        for relative in ["index.html", "research/index.html", "reverse/index.html"]:
            path = SITE / relative
            page = PageParser(path.read_text())
            with self.subTest(page=relative):
                self.assertEqual(len(page.ids), len(set(page.ids)), "IDs must be unique")
                for _, attrs in page.elements:
                    for attribute in ["aria-labelledby", "aria-describedby"]:
                        for identifier in attrs.get(attribute, "").split():
                            self.assertIn(identifier, page.ids)
                    for attribute in ["href", "src"]:
                        if attribute not in attrs:
                            continue
                        url = urlsplit(attrs[attribute])
                        if url.scheme or url.netloc:
                            continue
                        target = (SITE / url.path.lstrip("/")) if url.path else path
                        if target.is_dir():
                            target = target / "index.html"
                        self.assertTrue(target.is_file(), attrs[attribute])
                        if url.fragment:
                            self.assertIn(url.fragment, PageParser(target.read_text()).ids)
                    self.assertNotIn("style", attrs, "retain the no-inline-style CSP")
                    self.assertFalse(any(key.lower().startswith("on") for key in attrs))

    def test_source_links_are_pinned_and_research_data_is_not_served(self):
        html = (SITE / "research/index.html").read_text()
        links = [attrs["href"] for tag, attrs in PageParser(html).elements
                 if tag == "a" and "/blob/" in attrs.get("href", "")]
        self.assertGreaterEqual(len(links), 7)
        for link in links:
            self.assertIn(f"/blob/{SOURCE_REVISION}/research/", link)
            note = urlsplit(link).path.split(f"/blob/{SOURCE_REVISION}/", 1)[1]
            self.assertTrue((ROOT / note).is_file(), note)
        self.assertEqual(sorted(p.name for p in (SITE / "research").iterdir()), ["index.html"])
        for path in SITE.rglob("*"):
            self.assertFalse(path.is_symlink(), path)
            self.assertNotIn(path.suffix, {".py", ".md"}, path)
        self.assertTrue((ROOT / "docs/vendor/katex.md").is_file())
        self.assertTrue((SITE / "vendor/katex/LICENSE").is_file())
        self.assertIn("Sources are pinned", html)
        self.assertIn("Historical novelty is unverified", html)
        self.assertIn("not human mathematical review or formal verification", html)
        self.assertIn("Conjecture open", html)

    def test_new_results_keep_their_hypotheses_and_limits(self):
        html = (SITE / "research/index.html").read_text()

        def entry(identifier):
            return html.split(f'<li id="{identifier}">', 1)[1].split("</li>", 1)[0]

        recovery = entry("recovery")
        for text in ["every fixed deficient core D &gt; 1", "every real G &gt; 1",
                     "infinitely many primes p coprime to D", "No repeated recovery on one seed is proved",
                     "orbit later reaches zero", "not itself perfect"]:
            self.assertIn(text, recovery)
        self.assertIn(r"n=Dp,\qquad s(n)&lt;n,\qquad s^2(n)&gt;Gn", recovery)
        templates = entry("prime-templates")
        for text in ["repeating schedule", "At every source", "prime and coprime",
                     "Composite cofactors and nonperiodic schedules", "recurrent transition graph",
                     "Necessary, not sufficient", "need not occur consecutively"]:
            self.assertIn(text, templates)
        transport = entry("factor-transport")
        self.assertIn("coprime v, w &gt; 1", transport)
        self.assertIn("gcd(u, 6) = 1 at each source", transport)
        self.assertIn("does not regenerate the input", transport)
        supply = entry("prime-supply")
        for text in ["complete prime-power factors", "all greater than B", "0 &lt; ε &lt; 2",
                     "fixed deficiency margin is essential", "Perfect or abundant"]:
            self.assertIn(text, supply)
        self.assertIn("Conditional on escape", entry("prime-support"))

    def test_displayed_finite_examples_match_exact_arithmetic(self):
        html = (SITE / "research/index.html").read_text()
        for n, successor in [(844, 640), (640, 890), (29274, 43302), (43302, 55770)]:
            self.assertIn(str(n), html)
            self.assertIn(str(successor), html)
            self.assertEqual(aliquot_sum(n), successor)
        # The displayed rebound is not an escaping witness: verify its full finite tail.
        tail = [844, 640, 890, 730, 602, 454, 230, 202, 104, 106, 56, 64, 63, 41, 1, 0]
        for n, successor in zip(tail, tail[1:]):
            self.assertEqual(aliquot_sum(n), successor)
        self.assertEqual(29274 // 6, 7 * 17 * 41)
        self.assertEqual(43302 // 6, 7 * 1031)
        self.assertEqual(55770 // 6, 13**2 * 5 * 11)
        self.assertIn("844 → 640 → 890", html)
        self.assertIn("at least four distinct primes above 10", html)
        self.assertLess(3 * 11**3, 4 * 10**3)
        self.assertGreater(3 * 11**4, 4 * 10**4)
