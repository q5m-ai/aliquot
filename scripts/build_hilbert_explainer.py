#!/usr/bin/env python3
"""Build the explanatory SVG with exact Python-derived labels; no dependencies.

The optional PNG is a convenience preview, not mathematical data. To regenerate:
uv run --no-project --with resvg-py==0.5.0 python scripts/build_hilbert_explainer.py --png
"""

import argparse
from hashlib import sha256
from html import escape
from pathlib import Path
from struct import pack
import sys
from zlib import crc32

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from aliquot.hilbert import address, checked_sum  # noqa: E402

OUTPUT = ROOT / "research/results/hilbert-explained.svg"
PREVIEW = OUTPUT.with_suffix(".png")


def render():
    blue, orange, ink, muted = "#1d4ed8", "#c2410c", "#172033", "#526176"
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="960" height="1540" viewBox="0 0 960 1540" role="img" aria-labelledby="title desc">',
        '<title id="title">The Hilbert insight: a divisibility ruler, not an orbit rule</title>',
        '<desc id="desc">Three panels: a Hilbert path labels a four-by-four grid; 18 and 1170 have matching base-four endings and orientation, hence matching local grid positions and powers-of-two fingerprints; their actual aliquot successors are 21 and 2106, with opposite parity. These two sources are being compared, not asserted to be consecutive orbit terms.</desc>',
        '<rect width="960" height="1540" fill="#f3f6fb"/>',
        '<style>text{font-family:DejaVu Sans,sans-serif;fill:#172033}.mono{font-family:DejaVu Sans Mono,monospace}</style>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#c2410c"/></marker></defs>',
    ]

    def text(x, y, label, size=20, color=ink, weight="normal", cls="", anchor="start"):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" style="fill:{color}" class="{cls}" text-anchor="{anchor}">{escape(str(label))}</text>')

    def rect(x, y, w, h, fill, stroke="none", radius=0):
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')

    text(36, 44, "The Hilbert insight", 32, weight="bold")
    text(36, 77, "An exact link between digits and geometry — not yet a rule for aliquot motion.", 20, muted)

    # 1: Fixed even-order convention. Each first digit colors a quadrant.
    rect(24, 100, 912, 370, "white", "#dce3ef", 16)
    text(44, 138, "1  Fold the number line into a square", 25, weight="bold")
    ox, oy, cell = 60, 166, 64
    colors = ("#f1f5f9", "#dbeafe", "#eef2ff", "#f1f5f9")
    for n in range(16):
        p = address(n)
        rect(ox + cell * p.x, oy + cell * (3 - p.y), cell, cell, colors[n // 4], "white")
    coords = [address(n) for n in range(16)]
    path = " ".join(f"{ox + cell * (p.x + .5)},{oy + cell * (3.5 - p.y)}" for p in coords)
    parts.append(f'<polyline points="{path}" fill="none" stroke="#8998ae" stroke-width="4"/>')
    for n, p in enumerate(coords):
        x, y = ox + cell * (p.x + .5), oy + cell * (3.5 - p.y)
        fill = blue if n == 6 else "white"
        parts.append(f'<circle cx="{x}" cy="{y}" r="19" fill="{fill}"/>')
        text(x, y + 7, n, 21, "white" if n == 6 else ink, anchor="middle")
    text(366, 192, "6 = 12₄", 32, blue, "bold", "mono")
    text(366, 234, "First digit 1: choose the blue quarter.")
    text(366, 266, "Then 2: its upper-right cell → 6.")
    text(366, 308, "Each extra base-4 digit chooses one")
    text(366, 338, "of four smaller squares. Turns and")
    text(366, 368, "reflections keep the path connected.")
    text(366, 414, "Gray path = 0, 1, 2, 3, …  NOT s(n).", 19, muted)
    text(60, 447, "The digits are an address, not a factorization.", 20, muted)

    # 2: Compare labels, not a purported orbit. All coordinates use one H.
    rect(24, 490, 912, 600, "white", "#dce3ef", 16)
    text(44, 530, "2  Matching endings preserve a geometric fingerprint", 25, weight="bold")
    text(44, 564, "Same last 3 digits + same final orientation ⇒ same position modulo 8.", 19, blue)
    text(44, 592, "Different 8 × 8 tiles, shown aligned below. This does not mean nearby.", 18, muted)
    a, b = 18, 1170
    pa, pb = address(a), address(b)
    for left, n, p in ((76, a, pa), (512, b, pb)):
        word = "".join(str((n >> (2 * k)) & 3) for k in range(5, -1, -1))
        text(left, 637, f"{n} =", 25, weight="bold")
        rect(left + 200, 611, 70, 34, "#dbeafe", radius=5)
        text(left + 139, 638, word[:3], 28, muted, cls="mono")
        text(left + 202, 638, word[3:], 28, blue, "bold", "mono")
        text(left + 275, 638, "₄", 24)
        tx, ty, unit = left + 12, 666, 23
        for x in range(8):
            for y in range(8):
                chosen = (x, y) == (p.x % 8, p.y % 8)
                rect(tx + x * unit, ty + (7 - y) * unit, unit, unit,
                     blue if chosen else "#f4f7fc", "#dce3ef")
        text(left + 217, 707, f"State {p.state}", 24, blue, "bold")
        text(left + 217, 741, "Same final", 19, muted)
        text(left + 217, 768, "orientation", 19, muted)
        text(left + 217, 795, "of the decoder.", 19, muted)
        text(left + 12, 882, f"Local cell: ({p.x % 8}, {p.y % 8})", 22, blue, "bold")
        text(left + 12, 915, f"Actual H({n}): ({p.x}, {p.y})", 20)
    gap = b - a
    norm = (pb.x - pa.x) ** 2 + (pb.y - pa.y) ** 2
    power = gap & -gap
    rect(48, 941, 864, 125, "#eff6ff", radius=10)
    text(68, 973, f"Number gap:         {gap:,} = {power} × {gap // power}", 22, cls="mono")
    text(68, 1007, f"Squared map gap:    {norm:,} = {power} × {norm // power}", 22, cls="mono")
    text(68, 1043, "Both contain exactly seven factors of 2. Their sizes are NOT equal.", 19, blue)

    # 3: These, unlike the comparison above, are actual aliquot arrows.
    rect(24, 1110, 912, 335, "white", "#dce3ef", 16)
    text(44, 1150, "3  But that fingerprint does not predict the next term", 25, weight="bold")
    for left, n in ((76, a), (512, b)):
        successor = checked_sum(n)
        text(left, 1211, n, 31, weight="bold")
        parts.append(f'<path d="M{left + 100} 1200H{left + 180}" fill="none" stroke="{orange}" stroke-width="3" marker-end="url(#arrow)"/>')
        text(left + 205, 1211, successor, 31, orange, "bold")
        text(left + 205, 1243, "ODD" if successor % 2 else "EVEN", 22, orange, "bold")
        odd = n
        while odd % 2 == 0:
            odd //= 2
        square_description = "a square" if n == 18 else "not a square"
        text(left, 1283, f"Odd part: {odd} — {square_description}.", 18, muted)
    text(48, 1325, "Divisor sums see a distinction this digit-and-orientation summary lost.", 20)
    text(48, 1364, "This persists with arbitrarily many matching ending digits:", 19, muted)
    text(48, 1396, "18 and 18(1 + 4^j), j ≥ 3, share state I and their last j digits,", 19)
    text(48, 1423, "but their aliquot successors have opposite parity.", 19)
    text(36, 1486, "An exact divisibility ruler — not yet an orbit rule.", 26, blue, "bold")
    text(36, 1519, "This rejects a simple digit-state shortcut, not every Hilbert method. The conjecture remains open.", 17, muted)
    return "\n".join(parts + ["</svg>", ""])


def source_tag(svg):
    """A valid PNG text chunk tying the convenience preview to its exact SVG."""
    payload = b"source-svg-sha256\0" + sha256(svg.encode()).hexdigest().encode()
    chunk = b"tEXt" + payload
    return pack(">I", len(payload)) + chunk + pack(">I", crc32(chunk))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check SVG and preview source hash without writing.")
    parser.add_argument("--png", action="store_true", help="Also render an optional PNG preview (needs resvg-py).")
    args = parser.parse_args()
    if args.check and args.png:
        parser.error("--check does not render the optional PNG")
    expected = render()
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text() != expected:
            print("Stale explanatory SVG: run python3 scripts/build_hilbert_explainer.py", file=sys.stderr)
            return 1
        if not PREVIEW.is_file() or source_tag(expected) not in PREVIEW.read_bytes():
            print("Stale PNG preview: rerun the optional --png command in this script's docstring.", file=sys.stderr)
            return 1
    else:
        OUTPUT.write_text(expected)
        if args.png:
            import resvg_py
            png = resvg_py.svg_to_bytes(svg_string=expected)
            if png[-12:] != b"\0\0\0\0IEND\xaeB`\x82":
                raise ValueError("Renderer did not return a PNG ending in IEND")
            PREVIEW.write_bytes(png[:-12] + source_tag(expected) + png[-12:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
