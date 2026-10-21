from contextlib import redirect_stderr, redirect_stdout
from dataclasses import replace
from fractions import Fraction
import io
import json
from math import gcd
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from aliquot import ComputationLimit, factorize
from aliquot.__main__ import main
from aliquot.research import divisor_sieve
from aliquot.regeneration import (
    MAX_STEPS, MAX_TERM, certify_regeneration, coupled_step, in_return_class,
    prime_entry_class, regeneration_report, trace_first_return, valuation,
)

ROOT = Path(__file__).resolve().parents[1]


class RegenerationTests(unittest.TestCase):
    def test_coupled_law_against_independent_sieve(self):
        sums = divisor_sieve(10_000)
        for n in range(1, len(sums)):
            step = coupled_step(n)
            self.assertEqual(step.successor, sums[n])
            self.assertEqual(step.sigma_cofactor, sums[step.cofactor] + step.cofactor)
            self.assertEqual(step.supply_two, valuation(sums[n] + n, 2))
            self.assertEqual(step.supply_three, valuation(sums[n] + n, 3))
            self.assertEqual(step.next_a, valuation(sums[n], 2) if sums[n] else None)
            self.assertEqual(step.next_b, valuation(sums[n], 3) if sums[n] else None)

    def test_prime_power_contributions_and_large_exact_inputs(self):
        for q in [5, 7, 11, 13, 17, 19]:
            for e in range(13):
                sigma_m = sum(q ** j for j in range(e + 1))
                step = coupled_step(2 ** 3 * 3 ** 2 * q ** e)
                self.assertEqual(step.sigma_cofactor, sigma_m)
                self.assertEqual(step.supply_two, valuation(sigma_m, 2))
                self.assertEqual(step.supply_three, 1 + valuation(sigma_m, 3))
        step = coupled_step(2 ** 300)
        self.assertEqual(step.successor, 2 ** 300 - 1)
        self.assertEqual(step.next_a, 0)

    def test_three_adic_tie_can_stay_or_rise(self):
        for n, following_b in [(6, 1), (42, 3)]:
            step = coupled_step(n)
            self.assertEqual(step.b, 1)
            self.assertEqual(step.supply_three, 1)
            self.assertEqual(step.next_b, following_b)
        self.assertEqual(coupled_step(72).successor, 123)
        self.assertEqual(coupled_step(72).next_a, 0)

    def test_unitary_factor_certificate_and_nonclosure(self):
        certificate = certify_regeneration(53, 5)
        self.assertEqual(certificate["cofactorPath"], ["53", "55", "89"])
        self.assertEqual(certificate["aliquotPath"], ["318", "330", "534"])
        self.assertEqual(certificate["strictGrowthFactorLowerBound"],
                         {"numerator": "7", "denominator": "5"})
        self.assertEqual(certificate["actualGrowthFactor"],
                         {"numerator": "89", "denominator": "53"})
        # The returned cofactor does NOT inherit the sufficient entry condition.
        with self.assertRaises(ValueError):
            certify_regeneration(89, 5)
        self.assertEqual(trace_first_return(534)["stepsComputed"], 4)
        # Coprimality is necessary for multiplying the divisor sums.
        with self.assertRaises(ValueError):
            certify_regeneration(23, 5)  # T(23)=25; 5 is not unitary.
        with self.assertRaises(ValueError):
            certify_regeneration(5, 7)  # T(5)=7, but 3 does not divide sigma(7).

    def test_crt_classes_and_finite_prime_examples(self):
        for d, p in [(5, 53), (35, 9833), (55, 53), (385, 383), (5005, 5003)]:
            entry = prime_entry_class(d)
            residue, modulus = int(entry["residue"]), int(entry["modulus"])
            self.assertEqual(modulus, 6 * d * d)
            self.assertEqual(residue % 6, 5)
            self.assertEqual(residue % (d * d), d - 2)
            self.assertEqual(gcd(residue, modulus), 1)
            self.assertEqual(p % modulus, residue)
            self.assertEqual(factorize(p), [(p, 1)])
            certify_regeneration(p, d)
        self.assertEqual(prime_entry_class(5), {"residue": "53", "modulus": "150"})

    def test_first_returns_termination_and_cycles(self):
        self.assertEqual(trace_first_return(30)["terms"], ["30", "42", "54", "66"])
        terminating = trace_first_return(66)
        self.assertEqual(terminating["status"], "terminated")
        self.assertEqual(terminating["terms"][-1], "0")
        cycle = trace_first_return(3162)
        self.assertEqual(cycle["status"], "cycle")
        self.assertEqual(cycle["terms"][-3:], ["1184", "1210", "1184"])
        self.assertEqual(cycle["terms"][cycle["cycleStartIndex"]], "1184")
        descent = trace_first_return(500394)
        self.assertEqual(descent["status"], "returned")
        self.assertEqual(descent["stepsComputed"], 27)
        self.assertEqual(descent["terms"][-1], "344226")
        self.assertEqual(descent["growthFactor"],
                         {"numerator": "57371", "denominator": "83399"})
        self.assertTrue(all(int(n) % 36 != 30 for n in descent["terms"][1:-1]))
        self.assertTrue(all(int(n) % 2 == 0 for n in descent["terms"]))
        initial = coupled_step(500394)
        self.assertGreater(initial.supply_two, initial.a)
        self.assertGreater(initial.supply_three, initial.b)

    def test_limits_are_unresolved_not_no_return(self):
        self.assertEqual(trace_first_return(30, max_steps=1)["status"], "step_limit")
        limited = trace_first_return(30, max_term=30)
        self.assertEqual(limited["status"], "term_limit")
        self.assertEqual(limited["terms"], ["30", "42"])
        self.assertEqual(trace_first_return(318, max_term=30)["stepsComputed"], 0)
        limited = trace_first_return(318, max_work=1)
        self.assertEqual(limited["status"], "factorization_limit")
        self.assertEqual(limited["terms"], ["318"])
        # Known outcomes need no further factorization; the cap is on sources.
        self.assertEqual(trace_first_return(318, max_term=330)["status"], "returned")
        self.assertEqual(certify_regeneration(53, 5, max_term=330)["aliquotPath"][-1], "534")
        with self.assertRaises(ComputationLimit):
            certify_regeneration(53, 5, max_term=318)
        with self.assertRaises(ComputationLimit):
            certify_regeneration(53, 5, max_work=1)

    def test_invalid_domains(self):
        for bad in [0, -1, True, 1.5, "30"]:
            for operation in [coupled_step, in_return_class, trace_first_return, prime_entry_class]:
                with self.assertRaises(ValueError):
                    operation(bad)
            with self.assertRaises(ValueError):
                valuation(bad, 2)
        for prime in [0, 1, 5, True, 2.0]:
            with self.assertRaises(ValueError):
                valuation(12, prime)
        for d in [1, 2, 3, 7, 9]:
            with self.assertRaises(ValueError):
                prime_entry_class(d)
        for kwargs in [{"max_steps": 0}, {"max_steps": MAX_STEPS + 1},
                       {"max_term": MAX_TERM + 1}, {"max_term": 0}, {"max_work": 0}]:
            with self.assertRaises(ValueError):
                trace_first_return(30, **kwargs)
        with self.assertRaises(ValueError):
            trace_first_return(6)
        with self.assertRaises(ValueError):
            certify_regeneration(7, 5)

    def test_mismatches_fail_closed(self):
        broken = replace(coupled_step(318), supply_three=999)
        with patch("aliquot.regeneration.coupled_step", return_value=broken):
            with self.assertRaises(ArithmeticError):
                trace_first_return(318)
        with patch("aliquot.regeneration._divisor_pair_sum", return_value=123):
            with self.assertRaises(ArithmeticError):
                certify_regeneration(53, 5)

    def test_committed_report_and_exact_ratios(self):
        expected = json.loads((ROOT / "research/results/regeneration-examples.json").read_text())
        self.assertEqual(regeneration_report(), expected)
        for entry in expected["primeEntryExamples"]:
            lower = entry["strictGrowthFactorLowerBound"]
            actual = entry["actualGrowthFactor"]
            self.assertGreater(Fraction(int(actual["numerator"]), int(actual["denominator"])),
                               Fraction(int(lower["numerator"]), int(lower["denominator"])))

    def test_cli_and_report_failures(self):
        result = subprocess.run([sys.executable, "-m", "aliquot", "regeneration"], cwd=ROOT,
                                text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), regeneration_report())
        for error in [ComputationLimit("unresolved"), ArithmeticError("verification mismatch")]:
            out, err = io.StringIO(), io.StringIO()
            with patch("aliquot.__main__.regeneration_report", side_effect=error):
                with redirect_stdout(out), redirect_stderr(err):
                    status = main(["regeneration"])
            self.assertEqual(status, 1)
            self.assertEqual(out.getvalue(), "")
            self.assertTrue(err.getvalue())
