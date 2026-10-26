#!/usr/bin/env python3
"""Reproduce the small Hilbert proof diagnostic. Nothing here is served."""

import argparse
from html import escape
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from aliquot.hilbert import address, build_report  # noqa: E402

OUTPUT = ROOT / "research/results/hilbert-base4.json"
FIGURE = ROOT / "research/results/hilbert-base4.svg"
COLORS = {"I": "#2563eb", "S": "#a16207", "C": "#9333ea", "T": "#be123c"}


def render_figure(report):
    """Plot fixed prefixes of one absolute Hilbert map, never n modulo a bound.

    The gray path connects consecutive integer labels; the orange arrows are
    actual aliquot steps. Display rounding is not used in the arithmetic.
    """
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="740" viewBox="0 0 1120 740" role="img" aria-labelledby="title desc">',
        '<title id="title">Aliquot values on one nested-even Hilbert path</title>',
        '<desc id="desc">Left: the terminating orbit of 12. Right: ten verified steps from 276, with the known value 5964 outside the plotted prefix. Orange arrows are aliquot steps, not moves along the gray Hilbert path. This is not a divergence test.</desc>',
        '<rect width="1120" height="740" fill="#fff"/>',
        '<style>text{font-family:system-ui,sans-serif;fill:#172033}.heading{font-size:20px;font-weight:600}.label{font-size:12px;paint-order:stroke;stroke:white;stroke-width:4px;stroke-linejoin:round}.caption{font-size:14px}</style>',
        '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" fill="#c2410c"/></marker></defs>',
        '<text x="28" y="34" class="heading">Hilbert addresses reorganize values; they do not prescribe the next aliquot term</text>',
        '<text x="28" y="60" class="caption">Gray: integer order. Orange: n → s(n). Point color: terminal orientation I / S / C / T.</text>',
    ]
    traces = {int(t["seed"]): t for t in report["traces"]}
    for left, seed, side, subtitle in [
        (28, 12, 8, "12 → 16 → 15 → 9 → 4 → 3 → 1 → 0"),
        (588, 276, 64, "276: a finite prefix, not a divergent orbit"),
    ]:
        parts.append(f'<text x="{left}" y="108" class="heading">{escape(subtitle)}</text>')
        parts.append(f'<text x="{left}" y="133" class="caption">H(0)…H({side * side - 1}); {side} × {side} cells, y increases upward</text>')
        ox, oy, extent = left + 24, 170, 448

        def screen(x, y):
            return ox + extent * x / (side - 1), oy + extent * (side - 1 - y) / (side - 1)

        def xy(x, y):
            a, b = screen(x, y)
            return f"{a:.3f},{b:.3f}"

        background = [address(n) for n in range(side * side)]
        path = " ".join(xy(h.x, h.y) for h in background)
        parts.append(f'<polyline points="{path}" fill="none" stroke="#dce2e8" stroke-width="1"/>')
        points = traces[seed]["points"]
        visible = [p for p in points if int(p["n"]) < side * side]
        for p, q in zip(points, points[1:]):
            if int(p["n"]) >= side * side or int(q["n"]) >= side * side:
                continue  # Do not clip/wrap the exact successor back into the grid.
            a = xy(int(p["x"]), int(p["y"]))
            b = xy(int(q["x"]), int(q["y"]))
            parts.append(f'<polyline points="{a} {b}" fill="none" stroke="#c2410c" stroke-width="2" marker-end="url(#arrow)"/>')
        for p in visible:
            x, y = screen(int(p["x"]), int(p["y"]))
            # Two adjacent high terms need distinct label placement.
            dx, dy = (7, 18) if p["n"] == "3790" else (7, -9)
            anchor = "start"
            if p["n"] in ("3050", "2716", "2772"):
                dx, anchor = -7, "end"
            label = p["n"] if seed == 276 else f'{p["n"]} ({p["base4"]}₄)'
            title = f'n={p["n"]}, base 4={p["base4"]}, H=({p["x"]},{p["y"]}), state={p["state"]}'
            parts.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="4" fill="{COLORS[p["state"]]}"><title>{escape(title)}</title></circle>')
            parts.append(f'<text x="{x + dx:.3f}" y="{y + dy:.3f}" text-anchor="{anchor}" class="label">{escape(label)}</text>')
        caption = ("7 exact steps; s(0) is undefined, so iteration stops." if seed == 12 else
                   "2772 → 5964 is verified; 5964 is outside this panel.")
        parts.append(f'<text x="{left}" y="650" class="caption">{escape(caption)}</text>')
        if seed == 276:
            parts.append(f'<text x="{left}" y="673" class="caption">Continuation unresolved at the 4095 source cap; no wraparound.</text>')
    for i, (state, color) in enumerate(COLORS.items()):
        x = 28 + i * 66
        parts.append(f'<circle cx="{x + 4}" cy="696" r="4" fill="{color}"/><text x="{x + 14}" y="701" class="caption">{state}</text>')
    parts.append('<text x="28" y="730" class="caption">Exact values and bounds: hilbert-base4.json. Argument and failed proof routes: research/HILBERT.md.</text>')
    return "\n".join(parts + ["</svg>", ""])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check artifacts without writing.")
    args = parser.parse_args()
    report = build_report()
    artifacts = [(OUTPUT, json.dumps(report, indent=2) + "\n"), (FIGURE, render_figure(report))]
    for path, expected in artifacts:
        if args.check:
            if not path.is_file() or path.read_text() != expected:
                print(f"Stale artifact: {path.relative_to(ROOT)}", file=sys.stderr)
                return 1
        else:
            path.write_text(expected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
