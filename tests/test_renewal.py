from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import io
import json
from math import gcd, isqrt, prod
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from aliquot import ComputationLimit, factorize
from aliquot.__main__ import main
from aliquot.renewal import (
    DEFAULT_SOURCE, MAX_REPORT_BYTES, PHASES, TARGETS, _pair_sigma,
    guard13, orbit_diagnostics, pair_diagnostic, phases, read_source,
    renewal_census, renewal_report, source_diagnostic, state, valuation,
    verify_renewal_report, walk_return,
)
from aliquot.research import divisor_sieve

ROOT = Path(__file__).resolve().parents[1]


def direct_sigma(n):
    return sum(d + (n//d if d*d != n else 0)
               for d in range(1, isqrt(n)+1) if n % d == 0)


def order(n, p):
    e = 0
    while n % p == 0:
        e += 1
        n //= p
    return e


def get(n):
    return state(tuple(factorize(n)))


class RenewalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = renewal_report()
        cls.source, cls.digest = read_source(DEFAULT_SOURCE)

    def test_full_artifact_reproduction_and_census_totals(self):
        raw = (ROOT / 'research/results/supplier-renewal.json').read_text()
        self.assertEqual(json.loads(raw), self.report)
        self.assertEqual(raw, json.dumps(self.report, ensure_ascii=False, separators=(',', ':'))+'\n')
        self.assertEqual(self.report['sourceArtifact']['sha256'], self.digest)
        self.assertEqual(self.report['orbits']['uniqueCertifiedSources'], 1296)
        census = self.report['census']
        self.assertEqual(census['sources'], 99999)
        self.assertEqual([(v['eligible'], v['retained'], v['lost'])
                          for v in census['guardClosure'].values()], [(3901,2275,1626), (341,64,277)])
        self.assertEqual([census['residue24'][k] for k in
                          ['eligible','localLemmaPassed','nextGuardRetained','nextGuardLost']], [488,488,0,488])
        family = census['guarded28Family']['counts']
        self.assertEqual(family, {'eligible':265, 'twoStepLemmaPassed':265,
                                 'guardRenewed':8, 'guardLost':257, 'primeProgressionEntries':11})

    def test_supply_columns_and_cancellation_against_additive_sieve(self):
        sums = divisor_sieve(3000)
        for n in range(1, 3001):
            s = get(n)
            self.assertEqual(s.total_sigma, n+sums[n])
            for (p, e), column in zip(s.factors, s.columns):
                expected = p**e+sums[p**e]
                self.assertEqual(column, tuple(order(expected, ell) for ell in TARGETS))
                if p in TARGETS:
                    self.assertEqual(column[TARGETS.index(p)], 0)
            row = source_diagnostic(s)
            if n == 1:
                self.assertEqual(row['next'], '0')
                self.assertIsNone(row['extraValuations'])
                self.assertIsNone(row['primitiveTriple'])
                continue
            self.assertEqual(row['extraValuations'], [order(sums[n],p)-min(order(n,p),order(n+sums[n],p)) for p in TARGETS])
            triple = {k:int(v) for k,v in row['primitiveTriple'].items()}
            self.assertEqual(triple['u']+triple['r'], triple['v'])
            for a,b in [('u','v'),('u','r'),('v','r')]:
                self.assertEqual(gcd(triple[a],triple[b]), 1)

    def test_old_new_block_demands_independently(self):
        for n in range(2, 2001):
            s, m = get(n), direct_sigma(n)-n
            following = get(m)
            d = pair_diagnostic(s, following)
            old, residual = int(d['oldPart']), int(d['newPart'])
            self.assertEqual(old*residual, m)
            self.assertEqual(gcd(old,residual), 1)
            self.assertEqual(gcd(residual,n*direct_sigma(n)), 1)
            self.assertEqual(d['oldSupply'], [order(direct_sigma(old),p) for p in TARGETS])
            self.assertEqual(d['newSupply'], [order(direct_sigma(residual),p) for p in TARGETS])
            self.assertEqual(d['strictSurplusRenewed'], [order(direct_sigma(m),p)>order(m,p) for p in TARGETS])
            self.assertEqual(d['newSupply'], [sum(row['contribution'][i] for row in d['newSuppliers']) for i in range(4)])
            self.assertTrue(all(m%int(row['prime']) for row in d['lostBlocks']))
            self.assertTrue(all(row['oldExponent']!=row['newExponent'] for row in d['changedBlocks']))
        pair = pair_diagnostic(get(276), get(396))
        self.assertEqual((pair['oldPart'],pair['newPart']), ('36','11'))
        self.assertEqual(pair['demand'][:2], [3,3])
        self.assertEqual(pair['newSupply'][:2], [2,1])
        self.assertEqual(pair['strictSurplusRenewed'][:2], [False,False])

    def test_A7_frontier_membership_does_not_require_full_factorization(self):
        sums = divisor_sieve(20000)
        for n in range(1, 20001):
            d = prod(p**e for p,e in factorize(n) if p<=7)
            expected = direct_sigma(d)>=2*d and sums[n]>n
            self.assertEqual(phases(n)[2], expected)
            self.assertEqual(phases(n)[2], phases(n,n+sums[n])[2])
        for n in [1,6,28,496,8128]:
            self.assertFalse(phases(n)[2])
        self.assertEqual(phases(0), (False,)*5)
        self.assertIsNone(phases(30)[3])
        self.assertFalse(phases(32)[3])
        self.assertIsNone(phases(364)[4])

    def test_negative_one_supplier_theorem_and_scope(self):
        sums = divisor_sieve(10000)
        for m in [3,4,6,8,12,24]:
            for r in range(m-1,10001,m):
                self.assertEqual((r+sums[r])%m, 0)
        for m,r in [(7,27),(16,15),(48,95),(56,55),(168,335)]:
            self.assertEqual(r%m, m-1)
            self.assertNotEqual(direct_sigma(r)%m, 0)
        self.assertEqual(direct_sigma(335),408)
        self.assertEqual(335%24,23)
        self.assertNotEqual(408%7,0)
        self.assertNotEqual(direct_sigma(9)%2,0)  # M>2 is essential.
        for row in self.report['census']['modulusTests']:
            if row['theoremGuarantees']:
                self.assertIsNone(row['counterexample'])
            else:
                witness = row['counterexample']
                self.assertIsNotNone(witness)
                r = int(witness['R'])
                self.assertEqual(direct_sigma(r),int(witness['sigma']))
                self.assertEqual(r%row['modulus'],row['modulus']-1)
                self.assertNotEqual(int(witness['sigma'])%row['modulus'],0)

    def test_reduced_residue_classes_have_semiprime_nonsuppliers(self):
        # Finite witnesses illustrating the separate Dirichlet proof, not an
        # inference of an all-modulus theorem from a successful search.
        primes = [n for n in range(2,501) if direct_sigma(n)==n+1]
        for ell in [5,7]:
            eligible = [p for p in primes if p!=ell and (p+1)%ell]
            for modulus in range(1,33):
                witnessed = {}
                for i,p in enumerate(eligible):
                    for q in eligible[i+1:]:
                        r = p*q%modulus
                        if gcd(r,modulus)==1:
                            witnessed.setdefault(r,(p,q))
                for r in range(modulus):
                    if gcd(r,modulus)==1:
                        self.assertIn(r,witnessed)
                        p,q=witnessed[r]
                        self.assertNotEqual(p,q)
                        self.assertEqual(p*q%modulus,r)
                        self.assertNotEqual(direct_sigma(p*q)%ell,0)

    def test_residue24_proves_only_local_supply_not_guard_regeneration(self):
        n,m,t = get(936),get(1794),get(2238)
        first, second = pair_diagnostic(n,m), pair_diagnostic(m,t)
        self.assertTrue(first['residue24Guard'])
        self.assertEqual(first['newPart'],'23')
        self.assertEqual(m.exponents[:2], t.exponents[:2])
        self.assertGreater(t.n,m.n)
        self.assertFalse(second['residue24Guard'])
        self.assertEqual(second['newPart'],'373')
        self.assertFalse(second['strictSurplusRenewed'][1])

    def test_guarded_28_first_return_and_failed_renewal(self):
        u,v,w = 349,351,769
        self.assertTrue(guard13(u,direct_sigma(u)))
        self.assertEqual(v,2*direct_sigma(u)-u)
        self.assertEqual(w,2*direct_sigma(v)-v)
        self.assertEqual((u%7,v%7,w%7),(6,1,6))
        self.assertEqual((v%13,v%169),(0,13))
        self.assertGreater(13*w,15*u)
        self.assertEqual([direct_sigma(28*x)-28*x for x in (u,v)], [28*v,28*w])
        self.assertFalse(guard13(w,direct_sigma(w)))
        self.assertEqual(2*direct_sigma(w)-w,771)
        self.assertNotEqual(771%13,0)
        # Infinitely many progression entries are a theorem using Dirichlet,
        # not something asserted from this finite list of prime inputs.
        for p in range(349,100001,1183):
            if direct_sigma(p)==p+1:
                self.assertTrue(guard13(p,p+1))
        self.assertFalse(guard13(167,168))  # 167+2=13^2: ordinary divisibility fails.
        # A retained supplier itself can cease supplying 7: a cancellation at
        # the OUTSIDE prime 13 changes its exponent from odd to even.
        witness = self.report['census']['guarded28Family']['returnedSupplyLossWitness']
        self.assertEqual(witness['cofactors'], ['1987','1989','4563'])
        self.assertEqual(factorize(4563), [(3,3),(13,2)])
        self.assertEqual(direct_sigma(4563),7320)
        self.assertNotEqual(7320%7,0)
        change = next(b for b in witness['returnTransition']['changedBlocks'] if b['prime']=='13')
        self.assertEqual((change['oldExponent'],change['sourceSigmaExponent'],change['newExponent'],change['cancellationExtra']), (1,1,2,1))
        self.assertEqual((change['oldContribution'][3],change['newContribution'][3]), (1,0))

    def test_compressed_current_states_are_not_autonomous_even_on_A7(self):
        # Strongest tested signature: valuations, every block's supply column,
        # actual identities of 2,3,5,7, and tie-unit residues modulo ell^2.
        a,b = get(860),get(1340)
        def key(s):
            blocks = tuple(sorted((e,p if p in TARGETS else 0,col)
                                  for (p,e),col in zip(s.factors,s.columns)))
            return s.exponents,s.supplies,blocks,s.tie_residues
        self.assertEqual(key(a),key(b))
        self.assertTrue(a.membership[2] and b.membership[2])
        self.assertEqual((a.successor,b.successor),(988,1516))
        following = [get(s.successor) for s in (a,b)]
        self.assertNotEqual([x.supplies[0]>x.exponents[0] for x in following][0],
                            [x.supplies[0]>x.exponents[0] for x in following][1])
        audit = self.report['census']['stateSufficiency']['A7']['supplyBlocksAndTieResidues']
        self.assertEqual((audit['sources'],audit['ambiguousBuckets']), (22465,1032))
        self.assertGreater(audit['sourcesInRepeatedBuckets'],0)

    def test_returns_keep_losses_and_controls(self):
        traces = {t['seed']:t for t in self.report['orbits']['traces']}
        loss660 = next(r for r in traces['660']['firstReturns'] if r['index']==9 and r['phase']=='A7')
        self.assertEqual((loss660['start'],loss660['steps'],loss660['end']),('47952',5,'31900'))
        loss276 = next(r for r in traces['276']['firstReturns'] if r['index']==171 and r['phase']=='A7')
        self.assertEqual((loss276['steps'],loss276['end']), (56,'351121244430380'))
        for h in [8,32,64]:
            recovery = next(r for r in traces['276']['recoveries'] if r['index']==171 and r['horizon']==h)
            self.assertEqual((recovery['status'],recovery['steps']),('window_failure',h))
        parent276 = next(t for t in self.source['traces'] if t['seed']=='276')
        starting = int(parent276['rows'][171]['n'])
        later = next((i,row['n']) for i,row in enumerate(parent276['rows'])
                     if i>171 and int(row['n'])>starting and phases(int(row['n']))[2])
        self.assertEqual(later,(313,'11800507429706023344513135120'))
        self.assertEqual(traces['220']['firstReturnCounts']['A7'],{'neutral':1})
        self.assertEqual(traces['220']['recoveryCounts']['64'],{'cycle_failure':1})
        self.assertEqual(traces['138']['recoveryCounts']['64']['terminated_failure'],6)
        self.assertEqual(traces['318']['recoveryCounts']['64']['terminated_failure'],1)
        self.assertTrue(all(t['inputStatus']=='factorization_limit' for seed,t in traces.items()
                            if seed in ['276','552','564','660','966']))

    def test_driver_losses_are_supply_shortfall_and_tie_not_same_branch(self):
        rows = {r['n']:r for r in self.report['orbits']['edgeDiagnostics']}
        parents = {t['seed']:t for t in self.source['traces']}
        row276 = rows[parents['276']['rows'][169]['n']]
        row966 = rows[parents['966']['rows'][172]['n']]
        self.assertEqual((row276['exponents'][0],row276['supply'][0],row276['extraValuations'][0]),(2,1,0))
        self.assertEqual((row966['exponents'][0],row966['supply'][0],row966['extraValuations'][0]),(2,2,3))

    def test_censoring_cycles_and_last_known_membership(self):
        states = {n:get(n) for n in [12,16,15,9,4,3,1,30,220,284]}
        self.assertEqual(walk_return(12,'A7',{12:16},states)['status'],'censored')
        self.assertEqual(walk_return(12,'A7',{12:16},states,horizon=1)['status'],'window_failure')
        self.assertEqual(walk_return(12,'A7',{12:16,16:15,15:9,9:4,4:3,3:1,1:0},states)['status'], 'terminated_failure')
        cycle = {220:284,284:220}
        result = walk_return(220,'A7',cycle,states)
        self.assertEqual((result['status'],result['steps'],result['gain']),('returned',2,{'numerator':'1','denominator':'1'}))
        self.assertEqual(walk_return(220,'A7',cycle,states,profitable=True)['status'],'cycle_failure')
        # 42 is not factored here: its clean6/A7 membership is still known.
        self.assertEqual(walk_return(30,'clean6',{30:42},states)['status'],'returned')
        self.assertEqual(walk_return(30,'A7',{30:42},states)['status'],'returned')
        self.assertEqual(walk_return(30,'surplus6',{30:42},states)['status'],'censored_membership')

    def test_corrupt_source_and_derived_evidence_are_rejected(self):
        bad = deepcopy(self.source)
        bad['traces'][0]['rows'][0]['next']='397'
        with self.assertRaises(ArithmeticError):
            orbit_diagnostics(bad)
        with patch('aliquot.renewal.renewal_report',return_value=self.report):
            self.assertTrue(verify_renewal_report(self.report))
            mutations = [
                lambda r:r['sourceArtifact'].update(sha256='0'*64),
                lambda r:r['census']['residue24'].update(nextGuardRetained=1),
                lambda r:r['orbits']['edgeDiagnostics'][0].update(extraValuations=[99]*4),
                lambda r:r['orbits']['traces'][0]['firstReturns'][0].update(status='cycle_failure'),
                lambda r:r['plan'].update(firstReturnHorizon=64.0),
                lambda r:r['plan'].update(targets=[True,3,5,7]),
            ]
            for mutate in mutations:
                bad = deepcopy(self.report)
                mutate(bad)
                with self.assertRaises(ValueError):
                    verify_renewal_report(bad)

    def test_domains_and_resource_bounds(self):
        for n in [0,-1,True,1.5]:
            with self.assertRaises(ValueError):
                valuation(n,2)
        for p in [1,11,2.0,True]:
            with self.assertRaises(ValueError):
                valuation(24,p)
        for n in [-1,True,1.5]:
            with self.assertRaises(ValueError):
                phases(n)
        for bound in [1,0,-1,True,100001]:
            with self.assertRaises(ValueError):
                renewal_census(bound)
        for factors in [[(2,10**12)],[(2**600,1)],[(2,256),(3,256)],[(2,1),(2,2)]]:
            with self.assertRaises(ValueError):
                state(factors)
        with self.assertRaises(ValueError):
            pair_diagnostic(get(12),get(15))
        with self.assertRaises(ValueError):
            guard13(349,348)
        with self.assertRaises(ComputationLimit):
            _pair_sigma(10**8+1)
        for phase,h in [('bad',8),('A7',65),('A7',0)]:
            with self.assertRaises(ValueError):
                walk_return(12,phase,{}, {},horizon=h)
        for bad in [[],{}, {'schema':'aliquot-supplier-renewal-v1','plan':[]},
                    {'schema':'aliquot-supplier-renewal-v1','plan':{'censusBound':'0'}},
                    {'schema':'aliquot-supplier-renewal-v1','plan':{'censusBound':'9'*100}}]:
            with self.assertRaises(ValueError):
                verify_renewal_report(bad)

    def test_cli_reproduction_failure_is_atomic_and_inputs_are_bounded(self):
        stdout,stderr=io.StringIO(),io.StringIO()
        with redirect_stdout(stdout),redirect_stderr(stderr):
            self.assertEqual(main(['renewal','--bound','100','--compact']),0)
        small=json.loads(stdout.getvalue())
        self.assertEqual(small['census']['bound'],'100')
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(json.dumps(small).encode()); temp.flush()
            with redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
                self.assertEqual(main(['verify-renewal',temp.name]),0)
            temp.seek(0);temp.truncate(MAX_REPORT_BYTES+1);temp.flush()
            for command in [['verify-renewal',temp.name],['renewal','--source',temp.name]]:
                out=io.StringIO()
                with redirect_stdout(out),redirect_stderr(io.StringIO()):
                    self.assertEqual(main(command),1)
                self.assertEqual(out.getvalue(),'')
        with patch('aliquot.__main__.renewal_report',return_value={'large':'x'*100}),patch('aliquot.__main__.MAX_REPORT_BYTES',32):
            out=io.StringIO()
            with redirect_stdout(out),redirect_stderr(io.StringIO()):
                self.assertEqual(main(['renewal']),1)
            self.assertEqual(out.getvalue(),'')


if __name__ == '__main__':
    unittest.main()
