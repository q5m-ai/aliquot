"""Refresh content-hash CSS/JS URLs in the static pages; no build step required.

Run python3 scripts/version_assets.py after editing an asset.
Use --check to validate without writing files.
"""

import argparse
import hashlib
from pathlib import Path
import re
from urllib.parse import urlsplit

SITE = Path(__file__).resolve().parents[1] / "site"
ASSET_URL = re.compile(r'\b(href|src)="(/[^"?#]+\.(?:css|js))(?:\?[^"#]*)?"')


def version_page(html, site):
    def replace(match):
        attribute, path = match.groups()
        asset = (site / urlsplit(path).path.lstrip("/")).resolve()
        if not asset.is_relative_to(site.resolve()):
            raise ValueError(f"Asset outside site: {path}")
        digest = hashlib.sha256(asset.read_bytes()).hexdigest()[:16]
        return f'{attribute}="{path}?v={digest}"'

    return ASSET_URL.sub(replace, html)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if asset URLs need refreshing")
    args = parser.parse_args()
    stale = []
    for page in sorted(SITE.rglob("*.html")):
        original = page.read_text()
        updated = version_page(original, SITE)
        if original != updated:
            stale.append(str(page.relative_to(SITE)))
            if not args.check:
                page.write_text(updated)
    if args.check and stale:
        parser.exit(1, "Stale asset URLs: " + ", ".join(stale) +
                    ". Run python3 scripts/version_assets.py\n")


if __name__ == "__main__":
    main()
