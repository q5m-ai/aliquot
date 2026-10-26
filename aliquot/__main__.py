"""Run with python3 -m aliquot; JSON integer values are decimal strings."""

import argparse
import json
import sys

from . import ComputationLimit, DEFAULT_MAX_WORK, aliquot_sum
from .research import DEFAULT_BOUND, scan_six
from .two_adic import scan_two_adic
from .regeneration import regeneration_report
from .core_returns import core_return_report
from .exponent_vectors import MAX_REPORT_BYTES, vector_report, verify_report
from .certified import DEFAULT_WORK
from .renewal import DEFAULT_SOURCE, renewal_report, verify_renewal_report
from .handoff import handoff_report


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
    two_adic = commands.add_parser("scan-two-adic", help="checked valuation law and two-step C6 census")
    two_adic.add_argument("--bound", type=decimal_integer, default=DEFAULT_BOUND)
    commands.add_parser("regeneration", help="checked finite return blocks and counterexamples")
    commands.add_parser("core-returns", help="checked base-4 phases and perfect-core restoration")
    vectors = commands.add_parser("vectors", help="four-track bounded exponent-vector report")
    vectors.add_argument("--bound", type=decimal_integer, default=10_000)
    vectors.add_argument("--steps", type=decimal_integer, default=256)
    vectors.add_argument("--bits", type=decimal_integer, default=256)
    vectors.add_argument("--max-work", type=decimal_integer, default=DEFAULT_WORK)
    vectors.add_argument("--trial-work", type=decimal_integer, default=DEFAULT_MAX_WORK)
    vectors.add_argument("--compact", action="store_true", help="compact JSON for reproducible artifacts")
    verify = commands.add_parser("verify-vectors", help="independently replay orbit and primality certificates")
    verify.add_argument("path")
    renewal = commands.add_parser("renewal", help="supplier diagnostics and bounded guarded-return falsification")
    renewal.add_argument("--source", default=DEFAULT_SOURCE)
    renewal.add_argument("--bound", type=decimal_integer, default=100_000)
    renewal.add_argument("--compact", action="store_true")
    verify_renewal = commands.add_parser("verify-renewal", help="rebuild and compare a supplier-renewal report")
    verify_renewal.add_argument("path")
    verify_renewal.add_argument("--source", default=DEFAULT_SOURCE)
    handoff = commands.add_parser("handoff", help="checked supplier replacement, round-trip, and failed guard renewal")
    handoff.add_argument("--bound", type=decimal_integer, default=1_000_000,
                         help="prime-parameter cohort bound; named controls are separate")
    handoff.add_argument("--max-work", type=decimal_integer, default=DEFAULT_MAX_WORK)
    handoff.add_argument("--compact", action="store_true")
    total = commands.add_parser("sum", help="compute one exact proper-divisor sum")
    total.add_argument("n", type=decimal_integer)
    total.add_argument("--max-work", type=decimal_integer, default=DEFAULT_MAX_WORK)
    args = parser.parse_args(argv)
    try:
        if args.command == "scan-six":
            result = scan_six(args.bound)
        elif args.command == "scan-two-adic":
            result = scan_two_adic(args.bound)
        elif args.command == "regeneration":
            result = regeneration_report()
        elif args.command == "core-returns":
            result = core_return_report()
        elif args.command == "vectors":
            result = vector_report(bound=args.bound, max_steps=args.steps,
                                   max_bits=args.bits, max_work=args.max_work,
                                   trial_work=args.trial_work)
        elif args.command == "renewal":
            result = renewal_report(args.source, bound=args.bound)
        elif args.command == "handoff":
            result = handoff_report(bound=args.bound, max_work=args.max_work)
        elif args.command == "verify-renewal":
            with open(args.path, "rb") as source:
                data = source.read(MAX_REPORT_BYTES + 1)
            if len(data) > MAX_REPORT_BYTES:
                raise ValueError("Renewal report exceeds the 16 MiB input budget")
            verify_renewal_report(json.loads(data), args.source)
            result = {"status": "verified", "scope": "Exact reconstruction of bounded diagnostics; no infinite-return claim."}
        elif args.command == "verify-vectors":
            with open(args.path, "rb") as source:
                data = source.read(MAX_REPORT_BYTES + 1)
            if len(data) > MAX_REPORT_BYTES:
                raise ValueError("Vector report exceeds the 16 MiB input budget")
            verify_report(json.loads(data))
            result = {"status": "verified", "scope": "Exact finite orbit prefixes and prime certificates only."}
        else:
            result = {"n": str(args.n), "sum": str(aliquot_sum(args.n, max_work=args.max_work)),
                      "status": "exact", "max_work": args.max_work}
        # Serialize completely before writing: failures cannot emit partial reports.
        compact = getattr(args, "compact", False)
        output = json.dumps(result, ensure_ascii=False, indent=None if compact else 2,
                            separators=(",", ":") if compact else None)
        if args.command in ("vectors", "renewal", "handoff") and len(output.encode("utf-8")) > MAX_REPORT_BYTES:
            raise ValueError("Report exceeds the 16 MiB output budget")
    except (ValueError, ComputationLimit, ArithmeticError, OSError, KeyError, TypeError, RecursionError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
