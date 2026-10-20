"""Run with python3 -m aliquot; JSON integer values are decimal strings."""

import argparse
import json
import sys

from . import ComputationLimit, DEFAULT_MAX_WORK, aliquot_sum
from .research import DEFAULT_BOUND, scan_six


def decimal_integer(raw):
    if not raw.isascii() or not raw.isdigit() or raw.startswith("0"):
        raise argparse.ArgumentTypeError("expected a positive decimal integer without leading zeroes")
    try:
        return int(raw)
    except ValueError as error:
        raise argparse.ArgumentTypeError("decimal input exceeds this Python runtime's conversion budget") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description="Exact, bounded aliquot computations; not a divergence test.")
    commands = parser.add_subparsers(dest="command", required=True)
    scan = commands.add_parser("scan-six", help="independently checked one-step census")
    scan.add_argument("--bound", type=decimal_integer, default=DEFAULT_BOUND)
    total = commands.add_parser("sum", help="compute one exact proper-divisor sum")
    total.add_argument("n", type=decimal_integer)
    total.add_argument("--max-work", type=decimal_integer, default=DEFAULT_MAX_WORK)
    args = parser.parse_args(argv)
    try:
        if args.command == "scan-six":
            result = scan_six(args.bound)
        else:
            result = {"n": str(args.n), "sum": str(aliquot_sum(args.n, max_work=args.max_work)),
                      "status": "exact", "max_work": args.max_work}
        # Serialize completely before writing: failures cannot emit partial reports.
        output = json.dumps(result, ensure_ascii=False, indent=2)
    except (ValueError, ComputationLimit, ArithmeticError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
