"""Validate the educational figure's exact examples and reproducible source."""

from pathlib import Path
from struct import unpack
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from zlib import crc32

from aliquot.hilbert import address
from aliquot.two_adic import _divisor_pair_sum, valuation_two
from scripts.build_hilbert_explainer import render, source_tag

ROOT = Path(__file__).resolve().parents[1]


class HilbertExplainerTests(unittest.TestCase):
    def test_demonstrated_address_and_congruence(self):
        six = address(6)
        self.assertEqual(int("12", 4), 6)
        self.assertEqual((six.x, six.y, six.state), (1, 3, "I"))
        a, b = address(18), address(1170)
        self.assertEqual((a.state, b.state), ("I", "I"))
        self.assertEqual((a.x, a.y, b.x, b.y), (5, 1, 13, 41))
        self.assertEqual((a.x % 8, a.y % 8), (b.x % 8, b.y % 8))
        self.assertEqual(int("000102", 4), 18)
        self.assertEqual(int("102102", 4), 1170)
        gap = 1170 - 18
        norm = (b.x - a.x) ** 2 + (b.y - a.y) ** 2
        self.assertEqual((gap, norm), (1152, 1664))
        self.assertEqual((valuation_two(gap), valuation_two(norm)), (7, 7))
        self.assertEqual(_divisor_pair_sum(18), 21)
        self.assertEqual(_divisor_pair_sum(1170), 2106)

    def test_svg_and_preview_source_match(self):
        expected = render()
        path = ROOT / "research/results/hilbert-explained.svg"
        self.assertEqual(path.read_text(), expected)
        svg = ET.fromstring(expected)
        ns = {"s": "http://www.w3.org/2000/svg"}
        self.assertEqual(len(svg.findall(".//s:circle", ns)), 16)
        text = " ".join(svg.itertext())
        for phrase in ("ODD", "EVEN", "1,152 = 128 × 9", "1,664 = 128 × 13",
                       "This does not mean nearby.", "conjecture remains open."):
            self.assertIn(phrase, text)
        png = path.with_suffix(".png").read_bytes()
        self.assertTrue(png.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertEqual(unpack(">II", png[16:24]), (960, 1540))
        self.assertIn(source_tag(expected), png)
        # Check all PNG chunk CRCs with the standard library; no image package.
        pos = 8
        types = []
        while pos < len(png):
            length = unpack(">I", png[pos:pos + 4])[0]
            chunk = png[pos + 4:pos + 8 + length]
            checksum = unpack(">I", png[pos + 8 + length:pos + 12 + length])[0]
            self.assertEqual(crc32(chunk), checksum)
            types.append(chunk[:4])
            pos += length + 12
        self.assertEqual(pos, len(png))
        self.assertEqual((types[0], types[-1]), (b"IHDR", b"IEND"))

    def test_check_command_does_not_need_the_optional_renderer(self):
        result = subprocess.run([sys.executable, "scripts/build_hilbert_explainer.py", "--check"],
                                cwd=ROOT, text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
