"""Finite examples and presentation contracts for the causal thought experiment.

These checks do not verify the universal mathematical arguments on the page.
"""

from html.parser import HTMLParser
from math import isqrt
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit

from aliquot import aliquot_sum

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
PAGE = SITE / "causal/index.html"
SOURCE_REVISION = "bb10bad78fcf431cdbc6da5edbb9c5f4119ae588"


class PageParser(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def divisor_pair_sum(n):
    total = 0
    for divisor in range(1, isqrt(n) + 1):
        if n % divisor == 0:
            other = n // divisor
            if divisor < n:
                total += divisor
            if other != divisor and other < n:
                total += other
    return total


class CausalPageTests(unittest.TestCase):
    def setUp(self):
        self.html = PAGE.read_text()
        self.page = PageParser(self.html)
        self.formulas = {
            attrs["id"]: attrs["data-tex"]
            for _, attrs in self.page.elements
            if "data-tex" in attrs and "id" in attrs
        }

    def assert_edge(self, source, target):
        self.assertGreater(source, 0, "zero must never be a source")
        self.assertEqual(aliquot_sum(source), target)
        self.assertEqual(divisor_pair_sum(source), target)

    def rows(self, identifier, environment="gathered"):
        tex = self.formulas[identifier]
        start, end = rf"\begin{{{environment}}}", rf"\end{{{environment}}}"
        self.assertTrue(tex.startswith(start) and tex.endswith(end))
        return tex.removeprefix(start).removesuffix(end).split(r"\\")

    def integer_paths(self, identifier):
        paths = []
        for row in self.rows(identifier):
            self.assertRegex(row, r"^\d+(?:\\prec\d+)+$")
            paths.append([int(n) for n in row.split(r"\prec")])
        return paths

    def test_navigation_static_runtime_and_accessible_formulas(self):
        for path in SITE.rglob("*.html"):
            with self.subTest(page=path.relative_to(SITE)):
                html = path.read_text()
                navigation = html.split('<nav class="site"', 1)[1].split("</nav>", 1)[0]
                self.assertIn('href="/causal/"', navigation)
                self.assertEqual(navigation.count('aria-current="page"'), 1)
        self.assertIn('<a href="/causal/" aria-current="page">Causal view</a>', self.html)
        self.assertIn('href="#thought-experiment">Skip to thought experiment', self.html)
        self.assertEqual(sum(tag == "h1" for tag, _ in self.page.elements), 1)
        self.assertNotIn("<canvas", self.html)
        scripts = [urlsplit(attrs["src"]).path for tag, attrs in self.page.elements if tag == "script"]
        self.assertEqual(scripts, ["/vendor/katex/katex.min.js", "/latex.js"])
        for _, attrs in self.page.elements:
            if "data-tex" in attrs:
                self.assertEqual(attrs.get("tabindex"), "0")
                self.assertEqual(attrs.get("role"), "group")
                self.assertTrue(attrs.get("aria-label"))
                self.assertEqual(attrs.get("data-display"), "true")
        self.assertIn('/research.css?', self.html)
        css = (SITE / "causal.css").read_text()
        self.assertIn("max-width: 820px", css)
        self.assertIn("@media (max-width: 500px)", css)

    def test_displayed_integer_chains_are_exact_with_explicit_prefix_bounds(self):
        examples = {
            "example-merges": [
                [121, 12, 16, 15, 9, 4, 3, 1, 0],
                [26, 16],
                [30, 42, 54, 66, 78, 90, 144, 259],
                [259, 45, 33, 15],
            ],
            "example-unresolved": [
                [276, 396, 696, 1104, 1872, 3770],
                [306, 396],
            ],
        }
        for identifier, expected in examples.items():
            with self.subTest(example=identifier):
                paths = self.integer_paths(identifier)
                self.assertEqual(paths, expected)
                for path in paths:
                    for source, target in zip(path, path[1:]):
                        self.assert_edge(source, target)
        self.assertIn("five verified steps, not a measured full lifetime", self.html)
        self.assertIn("prefix proves neither eventual death nor immortality", self.html)

    def test_displayed_event_coordinates_synchronize_unequal_lead_ins(self):
        times = {}
        starts = []
        for row in self.rows("example-clock"):
            events = []
            for token in row.split(r"\prec"):
                match = re.fullmatch(r"\((-?\d+),(\d+)\)", token)
                self.assertIsNotNone(match, token)
                events.append(tuple(map(int, match.groups())))
            starts.append(events[0])
            for time, value in events:
                self.assertEqual(times.setdefault(value, time), time)
            for (time, value), (next_time, successor) in zip(events, events[1:]):
                self.assertEqual(next_time, time + 1)
                self.assert_edge(value, successor)
        self.assertEqual(starts, [(-2, 121), (-1, 26)])
        self.assertEqual(times[16], 0)

    def test_death_clock_counts_backwards_not_elapsed_length(self):
        tex = self.formulas["example-death-clock"]
        self.assertEqual(tex, r"\begin{gathered}3\prec1\prec0,\\T_{\mathrm{clock}}(3)=-2,\quad T_{\mathrm{clock}}(1)=-1,\quad T_{\mathrm{clock}}(0)=0\end{gathered}")
        path = [3, 1, 0]
        for index, value in enumerate(path):
            self.assertIn(rf"T_{{\mathrm{{clock}}}}({value})={index - 2}", tex)
        for source, target in zip(path, path[1:]):
            self.assert_edge(source, target)
        for text in ["not the nonnegative orbit length T(n)", "nor the cofactor map T(u)",
                     "only when a finite endpoint exists", "would assume the conjecture, not prove it"]:
            self.assertIn(text, self.html)

    def test_first_repeat_death_depends_on_the_displayed_branch_history(self):
        paths = []
        for row in self.rows("example-recurrence", "aligned"):
            tokens = row.split(r"&\quad", 1)[1].split(r"\prec")
            path = []
            for index, token in enumerate(tokens):
                match = re.fullmatch(r"(\d+)_(\d+)(\^\{\\dagger\})?", token)
                self.assertIsNotNone(match, token)
                value, displayed_index, dagger = match.groups()
                self.assertEqual(int(displayed_index), index)
                self.assertEqual(bool(dagger), index == len(tokens) - 1)
                path.append(int(value))
            self.assertEqual(len(set(path[:-1])), len(path) - 1)
            self.assertIn(path[-1], path[:-1], "death must mark the first repeated visit")
            for source, target in zip(path, path[1:]):
                self.assert_edge(source, target)
            paths.append(path)
        self.assertEqual(paths, [[220, 284, 220], [562, 284, 220, 284]])
        self.assertEqual(paths[0][1], paths[1][1], "the displayed coordinates agree at 284")
        self.assertNotEqual(set(paths[0][:2]), set(paths[1][:2]), "the visited sets do not agree")
        self.assertEqual([len(path) - 1 for path in paths], [2, 3])

    def test_contracted_endpoints_have_verified_entry_edges_and_closed_cycles(self):
        tex = self.formulas["example-endpoints"]
        self.assertEqual(tex, r"\begin{gathered}95\prec25\prec D_{\{6\}},\qquad119\prec25,\qquad143\prec25,\\562\prec D_{\{220,284\}}\end{gathered}")
        for path in [[95, 25, 6], [119, 25], [143, 25], [562, 284]]:
            for source, target in zip(path, path[1:]):
                self.assert_edge(source, target)
        for cycle in [[6], [220, 284]]:
            for source, target in zip(cycle, cycle[1:] + cycle[:1]):
                self.assert_edge(source, target)
        self.assertIn("death at cycle entry, not at first repetition", self.html)
        self.assertIn("agree on mortality, not on death time", self.html)
        self.assertIn("Remove its internal cycle edges", self.html)
        self.assertIn("not an algorithm for discovering unknown cycles", self.html)

    def test_scope_distinguishes_the_model_from_an_arithmetic_solution(self):
        for text in [
            "A reformulation, not a solution", "not a physical model", "s(0) is undefined",
            "strict causal precedence, not numerical inequality",
            "First-repeat death depends on history", "locally finite strict partial order",
            "Acyclic does not mean terminating", "No finite prefix is enough",
            "Historical novelty is unverified", "software tests do not verify this theorem",
            "never evidence of divergence", "does not change the explorers’ stopping rules",
        ]:
            self.assertIn(text, self.html)
        formulas = [attrs["data-tex"] for _, attrs in self.page.elements if "data-tex" in attrs]
        for tex in [
            r"\forall n_0\in\mathbb Z_{>0},\qquad\tau(n_0)<\infty",
            r"\tau(n_0)=\infty\quad\Longrightarrow\quad n_k\longrightarrow\infty",
            r"\tau(n_0)=\infty\quad\Longrightarrow\quad P^{+}(n_kn_{k+1})\longrightarrow\infty",
            r"e_0\prec e_1\prec e_2\prec\cdots",
        ]:
            self.assertIn(tex, formulas)
        self.assertTrue(any(r"\forall L\ \exists n_0\quad\not\Longrightarrow\quad\exists n_0\ \forall L" in tex for tex in formulas))

    def test_source_links_are_pinned_outside_the_served_directory(self):
        links = [attrs["href"] for tag, attrs in self.page.elements
                 if tag == "a" and "/blob/" in attrs.get("href", "")]
        self.assertEqual(len(links), 4)
        for link in links:
            self.assertIn(f"/blob/{SOURCE_REVISION}/research/", link)
            source = urlsplit(link).path.split(f"/blob/{SOURCE_REVISION}/", 1)[1]
            self.assertTrue((ROOT / source).is_file())
        self.assertEqual([path.name for path in (SITE / "causal").iterdir()], ["index.html"])
