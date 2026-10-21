from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
import io
import json
from math import gcd, isqrt
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from aliquot import ComputationLimit, aliquot_sum
from aliquot.__main__ import main
from aliquot.core_returns import (
    MAX_PRECISION, MAX_SOURCE, MAX_STEPS, ambiguity_class, base_four_step,
    core_return_report, core_step, trace_driver,
)
from aliquot.regeneration import valuation
from aliquot.research import divisor_sieve

ROOT = Path(__file__).resolve().parents[1]


def order(n, prime):
    exponent = 0
    while n % prime == 0:
        exponent += 1
        n //= prime
    return exponent


class CoreReturnTests(unittest.TestCase):
    def test_bridge_iff_against_sieve(self):
        sums = divisor_sieve(100_000)
        for core, a, q in [(6, 1, 3), (28, 2, 7)]:
            for n in range(core, len(sums), core):
                if valuation(n, 2) != a:
                    continue
                step = core_step(n, core)
                self.assertEqual(step.successor, sums[n])
                self.assertEqual(step.sigma_cofactor, sums[step.cofactor] + step.cofactor)
                self.assertEqual(step.next_a, valuation(sums[n], 2))
                self.assertEqual(step.next_b, order(sums[n], q))
                if step.b >= 2:
                    self.assertEqual(step.bridge_predicted, step.next_a == a and step.next_b == 1)
                else:
                    self.assertIsNone(step.bridge_predicted)
                self.assertEqual(gcd(step.cofactor, 2 * q), 1)
                self.assertGreaterEqual(step.successor, n)
                if n > core:
                    self.assertGreater(step.successor, n)

    def test_good_and_bad_spikes(self):
        for core, n, following, restored in [(6, 54, 66, True), (6, 90, 144, False),
                                            (6, 12978, 19470, True),
                                            (28, 1372, 1428, True), (28, 60564, 105420, True),
                                            (28, 19404, 42840, False)]:
            step = core_step(n, core)
            self.assertEqual(step.successor, following)
            self.assertEqual(step.bridge_predicted, restored)
        # Odd b alone does not guarantee restoration of the ODD prime exponent.
        step = core_step(17836, 28)
        self.assertEqual(step.b, 3)
        self.assertEqual(step.sigma_cofactor, 14)
        self.assertFalse(step.bridge_predicted)
        self.assertEqual((step.next_a, step.next_b), (2, 2))
        # A base-4 zero count misses the binary carry that leaves driver 28.
        step = core_step(19404, 28)
        self.assertEqual((step.a, step.next_a), (2, 3))
        self.assertEqual(step.a // 2, step.next_a // 2)

    def test_base_four_phase_and_conditional_absorbing_tag(self):
        sums = divisor_sieve(100_000)
        for u in range(1, 10_000, 2):
            state = base_four_step(u)
            following = u + 2 * sums[u]
            self.assertEqual(int(state["next"]), following)
            self.assertEqual(state["square"], isqrt(u) ** 2 == u)
            self.assertEqual(state["nextMod4"], following % 4)
            if u % 6 == 5:
                self.assertEqual(following % 3, 1)
                if (sums[following] + following) % 3 == 0:
                    returned = following + 2 * sums[following]
                    self.assertEqual(returned % 3, 2)
                    if u % 4 == 1:
                        self.assertEqual(returned % 4, 1)
                    elif isqrt(following) ** 2 == following:
                        self.assertEqual(returned % 4, 1)
                    else:
                        self.assertEqual(returned % 4, 3)
                    if u % 12 == 5 and following % 5 == 0 and gcd(5, following // 5) == 1:
                        self.assertEqual((sums[following] + following) % 72, 0)
                        self.assertEqual((returned + following) % 144, 0)
        self.assertEqual(base_four_step(49)["next"], "65")

    def test_arbitrary_precision_examples_are_only_finite_regressions(self):
        # Written Dirichlet proof covers all precisions; this checks named witnesses.
        for k, p in [(1, 653), (2, 6053), (3, 27653), (4, 27653), (5, 27653)]:
            entry = ambiguity_class(k, 2)
            local = int(entry["localModulus"])
            self.assertEqual(p % local, 5)
            self.assertEqual((p + 1) % local, 6)
            self.assertEqual(p % 25, 3)
            self.assertEqual(gcd(int(entry["primeResidue"]), int(entry["primeModulus"])), 1)
            self.assertEqual((valuation(p + 1, 2), valuation(p + 1, 3)), (1, 1))
            middle = p + 2
            returned = middle + 2 * aliquot_sum(middle)
            self.assertEqual(returned % 3, 2)
            self.assertEqual(middle % 25, 5)  # Exactly one factor of 5.
        self.assertEqual(7 + 2 * aliquot_sum(7), 9)  # Basepoint fails only two-step return.
        big = core_step(4 * 7 ** 30, 28)
        self.assertEqual(big.successor, 7 * ((7 ** 31 - 1) // 6) - 4 * 7 ** 30)

    def test_traces_use_actual_aliquot_map_after_core_prime_hit(self):
        trace = trace_driver(1316, 28)
        self.assertEqual(trace["status"], "driver_exit")
        self.assertEqual(trace["terms"][:3], ["1316", "1372", "1428"])
        self.assertEqual(trace["terms"][-2:], ["19404", "42840"])
        # T(49)=65, but s(28*49)=28*51; multiplicativity is invalid at cofactor 49.
        self.assertNotEqual(int(trace["terms"][2]), 28 * (49 + 2 * aliquot_sum(49)))
        self.assertEqual([s["bridgePredicted"] for s in trace["spikes"]], [True, False])
        for core, seed, bridge_source, target in [(6, 1578, "12978", "19470"),
                                                (28, 9772, "60564", "105420")]:
            trace = trace_driver(seed, core)
            self.assertEqual(trace["status"], "term_limit")
            self.assertEqual(trace["spikes"][0]["n"], bridge_source)
            self.assertEqual(trace["spikes"][0]["next"], target)
            self.assertTrue(trace["spikes"][0]["bridgePredicted"])
            self.assertGreater(int(trace["terms"][-1]), MAX_SOURCE)
        self.assertEqual(trace_driver(28, 28)["status"], "cycle")

    def test_limits_do_not_claim_driver_exit(self):
        self.assertEqual(trace_driver(1316, 28, max_steps=1)["status"], "step_limit")
        limited = trace_driver(1316, 28, max_source=1316)
        self.assertEqual(limited["status"], "term_limit")
        self.assertEqual(limited["terms"], ["1316", "1372"])
        limited = trace_driver(318, 6, max_work=1)
        self.assertEqual(limited["status"], "factorization_limit")
        self.assertEqual(limited["terms"], ["318"])
        self.assertEqual(trace_driver(90, 6, max_source=90)["status"], "driver_exit")
        with self.assertRaises(ComputationLimit):
            core_step(318, 6, max_work=1)

    def test_invalid_inputs(self):
        for bad in [0, -1, True, 1.5, "30"]:
            with self.assertRaises(ValueError):
                base_four_step(bad)
            with self.assertRaises(ValueError):
                core_step(bad, 6)
            with self.assertRaises(ValueError):
                trace_driver(bad, 6)
            with self.assertRaises(ValueError):
                ambiguity_class(bad, 2)
        for bad_core in [1, 4, 7, 84, True, 6.0]:
            with self.assertRaises(ValueError):
                core_step(30, bad_core)
        for n, core in [(12, 6), (2, 6), (56, 28), (100, 28)]:
            with self.assertRaises(ValueError):
                core_step(n, core)
        with self.assertRaises(ValueError):
            base_four_step(2)
        for k, ell in [(1, 1), (MAX_PRECISION + 1, 2), (1, MAX_PRECISION + 1)]:
            with self.assertRaises(ValueError):
                ambiguity_class(k, ell)
        for options in [{"max_steps": 0}, {"max_steps": MAX_STEPS + 1},
                        {"max_source": MAX_SOURCE + 1}, {"max_source": 0}, {"max_work": 0}]:
            with self.assertRaises(ValueError):
                trace_driver(30, 6, **options)

    def test_verification_fails_closed(self):
        step = replace(core_step(1372, 28), bridge_predicted=False)
        with patch("aliquot.core_returns.core_step", return_value=step):
            with self.assertRaises(ArithmeticError):
                trace_driver(1372, 28)
        with patch("aliquot.core_returns._divisor_pair_sum", return_value=123):
            with self.assertRaises(ArithmeticError):
                core_return_report()

    def test_report_and_prime_corridor(self):
        report = core_return_report()
        expected = json.loads((ROOT / "research/results/core-returns.json").read_text())
        self.assertEqual(report, expected)
        corridor = report["primeCore84Corridor"]
        self.assertEqual([x["cofactorPrime"] for x in corridor], [True, True, True, False])
        self.assertEqual([x["valuationThreeOfCofactorPlusFour"] for x in corridor], [3, 2, 1, 0])
        self.assertEqual(corridor[-1]["next"], "19628")
        self.assertEqual(19628 % 28, 0)
        self.assertNotEqual(19628 % 84, 0)

    def test_cli_and_failure_output(self):
        result = subprocess.run([sys.executable, "-m", "aliquot", "core-returns"], cwd=ROOT,
                                text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), core_return_report())
        for error in [ComputationLimit("unresolved"), ArithmeticError("mismatch")]:
            out, err = io.StringIO(), io.StringIO()
            with patch("aliquot.__main__.core_return_report", side_effect=error):
                with redirect_stdout(out), redirect_stderr(err):
                    status = main(["core-returns"])
            self.assertEqual(status, 1)
            self.assertEqual(out.getvalue(), "")
            self.assertTrue(err.getvalue())
