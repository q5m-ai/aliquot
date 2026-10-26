from contextlib import redirect_stderr, redirect_stdout
from math import gcd, isqrt
from pathlib import Path
import io
import json
import unittest
from unittest.mock import patch

from aliquot import ComputationLimit, factorize
from aliquot.__main__ import main
from aliquot.exponent_vectors import independent_sum, sigma, value
from aliquot.handoff import (
    MAX_PARAMETER, MAX_SOURCE, _pair_sigma, control_progression,
    geometric_supply7, handoff_block, handoff_report, supplier_roundtrip,
)

ROOT = Path(__file__).resolve().parents[1]


def direct_sigma(n):
    return sum(d + (n//d if d*d != n else 0)
               for d in range(1,isqrt(n)+1) if n%d==0)


def order(n,p):
    exponent=0
    while n%p==0:
        exponent+=1
        n//=p
    return exponent


class HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=handoff_report()

    def test_artifact_reproduces_and_all_progression_candidates_remain(self):
        raw=(ROOT/'research/results/supplier-handoff.json').read_text()
        self.assertEqual(raw,json.dumps(self.report,ensure_ascii=False,separators=(',',':'))+'\n')
        audit=self.report['audit']
        self.assertEqual(audit['counts'],{'candidateParameters':21,'admitted':3,
                                         'returnedSupply7':1,'returnedGuard':0})
        self.assertEqual([int(x['p']) for x in audit['candidates']],list(range(28638,1000001,48503)))
        self.assertEqual([x['primeParameter'] for x in audit['admitted']],['77141','659177','853189'])
        for row in audit['candidates']:
            p=int(row['p'])
            self.assertEqual(p%7,1)
            self.assertEqual((15*p+28)%(13**2*41),0)
            if row['status']=='composite_parameter':
                factors=[(int(q),e) for q,e in row['factors']]
                self.assertEqual(factorize(p),factors)
                self.assertNotEqual(factors,[(p,1)])
        small=handoff_report(bound=1000)
        self.assertEqual(small['audit']['counts']['candidateParameters'],0)
        # Named controls are explicitly separate from the parameter cohort.
        self.assertEqual(small['named'],self.report['named'])
        self.assertEqual(small['supplierRoundTrip'],self.report['supplierRoundTrip'])

    def test_geometric_supply_formula_all_orders_and_huge_exponents(self):
        for base in range(2,81):
            for exponent in range(25):
                geometric=sum(base**i for i in range(exponent+1))
                self.assertEqual(geometric_supply7(base,exponent),order(geometric,7))
        self.assertEqual(geometric_supply7(13,1),1)
        self.assertEqual(geometric_supply7(13,2),0)
        self.assertEqual(geometric_supply7(3,3),0)
        self.assertEqual(geometric_supply7(3,5),1)
        self.assertEqual(geometric_supply7(29,7**30-1),30)
        self.assertEqual(geometric_supply7(13,2*7**30-1),31)
        self.assertEqual(geometric_supply7(14,10**100),0)

    def test_CRT_controls_exact_valuations_not_only_divisibility(self):
        for core,targets,phase in [(13,[(13,2,9),(41,1,15)],6),
                                   (13,[(13,1,1)],6),
                                   (39,[(3,2,1),(13,1,4)],2),
                                   (13,[(181,3,17)],1)]:
            c=control_progression(core,targets,phase=phase)
            r,m=int(c['residue']),int(c['modulus'])
            linear,constant=int(c['L']),int(c['B'])
            self.assertEqual(gcd(r,m),1)
            self.assertEqual(linear,2*direct_sigma(core)-core)
            self.assertEqual(constant,2*direct_sigma(core))
            for k in range(7):
                parameter=r+k*m
                self.assertEqual(core*parameter%7,phase)
                image=linear*parameter+constant
                for prime,e,unit in targets:
                    self.assertEqual(order(image,prime),e)
                    self.assertEqual(image//prime**e%prime,unit)
            for a,q in c['parameterCongruences']:
                self.assertEqual(r%int(q),int(a))
        c=self.report['progression']
        self.assertEqual((c['residue'],c['modulus']),('77141','25852099'))
        # An actual small prime parameter also checks the multiplicative formula.
        small=control_progression(13,[(13,1,1)])
        self.assertEqual(small['residue'],'337')
        u=13*337
        self.assertEqual(2*direct_sigma(u)-u,15*337+28)

    def test_prime_parameter_coprimality_exception_cannot_be_ignored(self):
        c=control_progression(13,[(223,1,1)],phase=1)
        self.assertEqual(c['residue'],'13')
        self.assertEqual(c['excludedPrimeDivisorsOf'],'26')
        # 13 is a prime in this progression, but divides the fixed core.
        self.assertEqual(15*13+28,223)
        self.assertEqual(2*direct_sigma(13**2)-13**2,197)
        self.assertNotEqual(197,223)

    def test_old_supplier_loses_even_exponent_and_fresh_supplier_replaces_it(self):
        b=self.report['named']['replacementAndFailedRenewal']
        self.assertTrue(b['entryGuard'])
        self.assertEqual(b['aliquotPath'],['28079324','32400004','39909884'])
        u,v,w=b['cofactors']
        self.assertEqual(u['factors'],[['13',1],['77141',1]])
        self.assertEqual(v['factors'],[['13',2],['41',1],['167',1]])
        self.assertEqual(w['factors'],[['761',1],['1873',1]])
        self.assertEqual(u['suppliers7'],[{'prime':'13','exponent':1,'supply':1}])
        self.assertEqual({row['prime'] for row in v['suppliers7']},{'41','167'})
        self.assertEqual(w['suppliers7'],[])
        self.assertTrue(b['twoStepFirstReturn'])
        self.assertFalse(b['returnedSupply7'])
        self.assertFalse(b['returnedGuard'])
        self.assertEqual(b['backSupply13']['supply13'],0)
        self.assertEqual(b['backSupply13']['returnedExponent13'],0)
        self.assertGreater(90077*int(w['n']),126645*int(u['n']))

    def test_a_successful_supplier_return_is_not_full_guard_renewal(self):
        b=self.report['supplierRoundTrip']['positive']
        self.assertTrue(b['entryGuard'])
        self.assertTrue(b['twoStepFirstReturnToUnitary13Phase'])
        self.assertTrue(b['returnedSupply7'])
        self.assertFalse(b['returnedGuard'])
        self.assertEqual(b['aliquotPath'],['72001748','83079724','99703604'])
        u,v,w=b['cofactors']
        self.assertEqual([int(x['n'])%7 for x in (u,v,w)],[6,1,6])
        self.assertEqual([dict((int(p),e) for p,e in x['factors']).get(13,0) for x in (u,v,w)],[1,2,1])
        self.assertEqual(v['factors'],[['13',2],['97',1],['181',1]])
        self.assertEqual(b['backSupply13'],{'R':'97','sigmaR':'98','supply13':0,
                                           'returnedExponent13':1,'conditionMet':True})
        self.assertGreater(30589*int(w['n']),41565*int(u['n']))
        repeat=self.report['supplierRoundTrip']['failedRepeat']
        self.assertFalse(repeat['entryGuard'])
        self.assertFalse(repeat['twoStepFirstReturnToUnitary13Phase'])
        self.assertEqual([x['n'] for x in repeat['cofactors']],['3560843','5044789','5044791'])
        self.assertEqual(factorize(5044789),[(5044789,1)])
        # The returned cofactor is COMPOSITE; never reuse the prime-only affine map.
        tail=3560843//13
        self.assertEqual(factorize(tail),[(11,1),(37,1),(673,1)])
        self.assertEqual(15*tail+28,4108693)
        correction=28*(direct_sigma(tail)-tail-1)
        self.assertEqual(correction,936096)
        self.assertEqual(4108693+correction,5044789)

    def test_extra_back_supply_can_destroy_the_unitary_return(self):
        b=self.report['supplierRoundTrip']['backSupplyCounterexample']
        self.assertTrue(b['middlePattern'])
        self.assertFalse(b['entryGuard'])
        self.assertEqual(b['backSupply13']['R'],'5137')
        self.assertEqual(factorize(5137),[(11,1),(467,1)])
        self.assertEqual(b['backSupply13']['sigmaR'],'5616')
        self.assertEqual(b['backSupply13']['supply13'],1)
        self.assertEqual(b['backSupply13']['returnedExponent13'],2)
        self.assertFalse(b['twoStepFirstReturnToUnitary13Phase'])
        # Failure of this phase is not loss of every possible7-supplier.
        self.assertTrue(b['returnedSupply7'])

    def test_no_replacement_and_nonunitary_replacement_are_explicit_controls(self):
        for name,expected_exponents in [('noGuaranteedReplacement',(2,0)),
                                        ('replacementExponentEven',(2,2))]:
            b=self.report['named'][name]
            self.assertFalse(b['entryGuard'])
            self.assertFalse(b['twoStepFirstReturn'])
            self.assertEqual((b['middleExponent13'],b['middleExponent41']),expected_exponents)
            self.assertEqual(b['cofactors'][1]['supply7'],0)
            self.assertEqual(b['cofactors'][2]['residue7'],3)

    def test_all_reported_edges_and_valuations_independently(self):
        blocks=list(self.report['audit']['admitted'])+list(self.report['named'].values())+list(self.report['supplierRoundTrip'].values())
        for b in blocks:
            states=b['cofactors']
            for s in states:
                n=int(s['n'])
                self.assertEqual(direct_sigma(n),int(s['sigma']))
                self.assertEqual(order(direct_sigma(n),7),s['supply7'])
                self.assertEqual(factorize(n),[(int(p),e) for p,e in s['factors']])
            for a,c in zip(states,states[1:]):
                n,m=int(a['n']),int(c['n'])
                self.assertEqual(2*direct_sigma(n)-n,m)
                self.assertEqual(gcd(n,28),1)
                self.assertEqual(direct_sigma(28*n)-28*n,28*m)

    def test_exact_back_supply_equivalences_on_independent_rest_grid(self):
        # Algebraic equivalences for arbitrary unitary rest blocks, not an
        # assertion that every such block has a source in either guarded class.
        for r in range(1,1001):
            sr=direct_sigma(r)
            if gcd(r,13*41)==1:
                v=13**2*41*r
                w=2*183*42*sr-v
                self.assertEqual(order(w,13)==1,order(sr,13)==1)
            if gcd(r,13*181)==1:
                v=13**2*181*r
                w=2*183*182*sr-v
                self.assertEqual(order(w,13)==1,sr%13!=0)
                self.assertEqual(w,13*(5124*sr-2353*r))

    def test_saturation_refinement_and_actual_middle_edge_are_separate(self):
        certificate=self.report['congruenceObstruction']
        self.assertIsNone(certificate['primeParameterWitness'])
        refinement=certificate['exampleRefinement']
        p0=int(refinement['residue'])
        self.assertEqual((p0-77141)%25852099,0)
        self.assertEqual(gcd(p0,int(refinement['modulus'])),1)
        linear_image=15*p0+28
        for q,e in [(13,2),(41,1),(30757,1),(3361,1)]:
            self.assertEqual(order(linear_image,q),e)
        for q,target,e in [(30757,13,3),(3361,41,2)]:
            self.assertEqual(factorize(q),[(q,1)])
            self.assertEqual(direct_sigma(q),q+1)
            self.assertEqual(order(q+1,target),e)
        # A separately factored middle term verifies valuation freezing and an
        # actual scaled edge. We do NOT assert it has a prime predecessor in
        # the displayed progression, nor that p0 itself is prime.
        factors=((13,2),(41,1),(3361,1),(30757,1))
        v=value(factors)
        total=independent_sum(factors)+v
        self.assertEqual(total,sigma(factors))
        w=2*total-v
        self.assertEqual((order(w,13),order(w,41)),(2,1))
        self.assertEqual(gcd(v,28),1)
        scaled=((2,2),(7,1),*factors)
        self.assertEqual(independent_sum(scaled),28*w)

    def test_domains_and_work_source_CRT_budgets(self):
        for core in [0,1,2,7,27,True,1000001]:
            with self.assertRaises(ValueError):
                control_progression(core,[(13,2,1)])
        for targets in [[],[(13,1,1)]*9,[(13,1,1),(13,2,1)],[(15,1,1)],
                        [(13,0,1)],[(13,9,1)],[(13,True,1)],[(13,1,0)],[(13,1,13)],
                        [(1000001,1,1)],[(13,1)],[(13,1,1,1)],[(True,1,1)]]:
            with self.assertRaises(ValueError):
                control_progression(13,targets)
        for p in [2,3,5,7]:
            with self.assertRaises(ValueError):
                control_progression(13,[(p,1,1)])
        for phase in [0,7,True,'6']:
            with self.assertRaises(ValueError):
                control_progression(13,[(13,1,1)],phase=phase)
        with self.assertRaises(ValueError):
            control_progression(13,[(101,8,1),(103,8,1),(107,8,1)])
        for base,e in [(1,0),(0,2),(MAX_SOURCE+1,1),(13,-1),(13,True),(True,1)]:
            with self.assertRaises(ValueError):
                geometric_supply7(base,e)
        for p in [0,1,15,13,True,MAX_PARAMETER+1]:
            with self.assertRaises(ValueError):
                handoff_block(p)
        for u in [0,True,12,169,39]:
            with self.assertRaises(ValueError):
                supplier_roundtrip(u)
        with self.assertRaises(ComputationLimit):
            _pair_sigma(MAX_SOURCE+1)
        with self.assertRaises(ComputationLimit):
            supplier_roundtrip(13*(14*MAX_SOURCE+1))
        with self.assertRaises(ComputationLimit):
            handoff_report(max_work=1)
        for bound in [0,True,1000001]:
            with self.assertRaises(ValueError):
                handoff_report(bound=bound)

    def test_cli_reproduction_and_failures_are_atomic(self):
        output=io.StringIO()
        with redirect_stdout(output),redirect_stderr(io.StringIO()):
            self.assertEqual(main(['handoff','--compact']),0)
        self.assertEqual(json.loads(output.getvalue()),self.report)
        for args in [['handoff','--max-work','1'],['handoff','--bound','1000001']]:
            output=io.StringIO()
            with redirect_stdout(output),redirect_stderr(io.StringIO()):
                self.assertEqual(main(args),1)
            self.assertEqual(output.getvalue(),'')
        with patch('aliquot.__main__.MAX_REPORT_BYTES',32):
            output=io.StringIO()
            with redirect_stdout(output),redirect_stderr(io.StringIO()):
                self.assertEqual(main(['handoff']),1)
            self.assertEqual(output.getvalue(),'')


if __name__=='__main__':
    unittest.main()
