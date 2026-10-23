"""Content-addressed asset URLs must match the files actually served."""

import hashlib
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit

from scripts.version_assets import version_page

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script" and "src" in attrs:
            self.urls.append(attrs["src"])
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.urls.append(attrs["href"])


class AssetVersionTests(unittest.TestCase):
    def test_every_page_uses_current_content_hashes_for_css_and_js(self):
        counts = {}
        shared = {}
        for page in sorted(SITE.rglob("*.html")):
            parser = AssetParser()
            parser.feed(page.read_text())
            counts[str(page.relative_to(SITE))] = len(parser.urls)
            for url in parser.urls:
                with self.subTest(page=page, url=url):
                    parsed = urlsplit(url)
                    self.assertFalse(parsed.scheme or parsed.netloc)
                    self.assertTrue(parsed.path.startswith("/"))
                    asset = SITE / parsed.path.lstrip("/")
                    expected = hashlib.sha256(asset.read_bytes()).hexdigest()[:16]
                    self.assertEqual(parse_qs(parsed.query), {"v": [expected]})
                    self.assertEqual(shared.setdefault(parsed.path, url), url)
        self.assertEqual(counts, {"index.html": 5, "research/index.html": 4})

    def test_refresh_is_idempotent_and_asset_changes_update_the_url(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            (site / "example.css").write_text("body{color:black}")
            html = '<link rel="stylesheet" href="/example.css"><a href="/research/">Research</a>'
            first = version_page(html, site)
            self.assertNotEqual(first, html)
            self.assertEqual(version_page(first, site), first)
            (site / "example.css").write_text("body{color:blue}")
            second = version_page(first, site)
            self.assertNotEqual(second, first)
            self.assertIn('<a href="/research/">Research</a>', second)
            self.assertEqual(second.count("?v="), 1)
            self.assertEqual(version_page(second, site), second)

    def test_check_command_accepts_committed_pages_without_modifying_them(self):
        before = {p: p.read_bytes() for p in SITE.rglob("*.html")}
        result = subprocess.run(["python3", "scripts/version_assets.py", "--check"],
                                cwd=ROOT, capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, {p: p.read_bytes() for p in before})
