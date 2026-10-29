# 10 — Replacing a supplier, restoring it, and testing the full guard

**Result:** a supplying prime that is disabled by cancellation can be replaced
by a guaranteed fresh supplier. A stronger guarded handoff then actually
**restores the original supplier** after two steps. But the full entry guard
still fails to reproduce itself, even when composite cofactors are allowed.
A further theorem rules out fixing this old-supplier restoration strategy by
any finite congruence refinement of its prime-entry progression, using actual
prime predecessors rather than freely chosen middle cofactors.

This is more than preserving the prime's identity: the restored exponent is
exactly 1, and the restored block again supplies 7. It is less than a closed
return class. Written proofs, exact counterexamples, and a small bounded
progression audit are separated below. No infinite orbit, solution to the
aliquot conjecture, historical novelty, or human peer review is claimed.

The methods are multiplicativity, valuation comparisons, classical lifting the
exponent, CRT, and Dirichlet's theorem. They extend the guarded unitary-block
method of [note 03](REGENERATION.md), the correction identities of
[note 06](BLOCK-TRANSPORT.md), and the failure in
[note 09](SUPPLIER-RENEWAL.md). They do not supersede those notes' unresolved
whole-orbit obligations.

## 1. The exact exponent, not just the supplying prime

For a prime q≠7, write d=ord₇(q) when q≢1 modulo7. The exact supply is

```text
v₇(σ(qᵉ)) = v₇(e+1)                                  if q≡1 mod7,
           = 0                                        if d∤(e+1),
           = v₇(qᵈ−1) + v₇((e+1)/d)                  otherwise.
```

For q=7 it is zero. These follow from the geometric-sum identity and the
classical odd-prime lifting-the-exponent formula. Thus a q≡−1 modulo7 block
supplies 7 exactly when e is odd; primes of order3 or6 require different
exponent classes. For example, 3³ supplies no7 but 3⁵ does. Parity alone is
not the rule for arbitrary supplying primes.

For an odd current prime q with exponent a in u, put b=v_q(σ(u)). On the
cofactor map T(u)=2σ(u)−u, the next exponent is min(a,b) if a≠b. If a=b,
it is a+c, where c is the valuation of the difference of the normalized
units. Consequently an old q≡−1 modulo7 can survive as a prime while its
supply switches off. Note09's 13¹→13² example is precisely this event.

A proposed repair must handle both **replacement** and the next guard. Merely
adding more valuation supply can also be wrong: §5 gives an example where
extra supply prevents the desired unitary exponent from returning.

## 2. One-step exponent control is possible

### Proposition T — controlled output valuations in a prime-parameter family

Fix an odd A>1 with gcd(A,7)=1 and 7|σ(A), and put

```text
L = 2σ(A)−A,       B = 2σ(A).
```

Choose finitely many distinct primes ℓ with ℓ∤LB, positive exponents k_ℓ,
and units c_ℓ modulo ℓ. Choose a nonzero input cofactor residue r modulo7.
There is a reduced arithmetic progression of prime parameters p such that,
for every p in it with p∤2A,

```text
Ap≡r mod7,
v_ℓ(T(Ap)) = k_ℓ             for every chosen ℓ.
```

There are infinitely many such primes, by **Dirichlet's theorem**.

**Proof.** Coprimality gives the exact affine formula

```text
T(Ap)=Lp+B.
```

Impose, for every target prime,

```text
p ≡ (ℓ^k_ℓ c_ℓ−B)L⁻¹  (mod ℓ^(k_ℓ+1)),
p ≡ r A⁻¹               (mod7).
```

The target residue is nonzero modulo ℓ because ℓ∤B and ℓ∤L. Also ℓ≠7
because 7|B, so these moduli are pairwise coprime. CRT gives a reduced
progression, and its congruences give exactly the requested valuations.
Dirichlet supplies infinitely many primes; excluding primes dividing2A removes
only finitely many. ∎

The coprimality exception is substantive. With A=13, a progression can contain
p=13, but the affine expression gives223 whereas T(13²)=197. Neither being
prime nor satisfying a congruence licenses overlapping factor blocks.

This theorem controls **one image**, not its later factorization or divisor
sum. For a composite x coprime to A, the actual correction is

```text
T(Ax)=Lx+B+Bδ(x),       δ(x)=s(x)−1.
```

One may not reapply the prime-only affine map to a returned composite cofactor.
No simultaneous-prime assumption is hidden in the construction: only the
initial parameter p is required to be prime.

## 3. Repairing the lost 13-supply with a fresh 41

Use cofactor phases

```text
U = {u>1 : u odd, u≡−1 mod7},
C = {u∈U : v₁₃(u)=1}.
```

They correspond to actual aliquot phases28U and28C. Every u∈C has a unitary
factor13, so 7|σ(u). For any source coprime to28,

```text
s(28u)=28T(u).
```

Define H₄₁ by u∈C, 41∤u, and

```text
v₁₃(T(u))=2,       v₄₁(T(u))=1.
```

This guard does **not** require u/13 to be prime. The condition41∤u makes
41 a genuinely new supplier, not a relabelled old block.

### Proposition U — guaranteed replacement, with a first return

Every u∈H₄₁ has a genuine two-step first return to28U after scaling by28,
with gain greater than126645/90077. The old13 block loses its7-supply, while
the new41 block supplies7 at the middle term.

**Proof.** Put v=T(u)=13²·41·R, with gcd(R,13·41)=1. Since σ(u) is divisible
by7, v≡1 modulo7 and is odd. Thus both scaled transitions are valid clean-28
steps. Multiplicativity gives

```text
σ(v)=183·42·σ(R),
w=T(v)≡−1 mod7.
```

The middle term is outside U; the endpoint w is in U. The block13² supplies
no7, but41 does. Writing u=13z with gcd(z,13)=1, the guard excludes z=1, so

```text
v=28σ(z)−13z >15z = (15/13)u,
w≥(2·183·42−13²·41)R =8443R,
w/v≥8443/6929.
```

Multiplication proves w/u>126645/90077. ∎

### Infinitely many finite entries, not repeated renewal

For A=13, L=15 and B=28. A concrete progression from Proposition T is

```text
p ≡ 77141 (mod 25852099),       25852099=7·13³·41².
```

It combines p≡1 mod7, p≡246 mod2197, and p≡1496 mod1681. These force
v₁₃(15p+28)=2 and v₄₁(15p+28)=1. Hence every prime in this reduced
progression supplies an entry u=13p to H₄₁. No primality of either output is
assumed. Each entry is a separate finite construction, not a continuation of
the previous one.

At the first displayed prime parameter,

```text
1002833=13·77141
  → 1157143=13²·41·167
  → 1425353=761·1873                         under T,
28079324 →32400004 →39909884                under s.
```

The replacement works and the first return gains. But σ(1425353)=1427988 is
not divisible by7, and13 has disappeared. The endpoint is not even in C,
let alone H₄₁. Thus this is an exact failure of the repair's full renewal,
not an argument based on a factorization timeout.

### The next missing supply becomes explicit

For any H₄₁ middle term v=13²·41·R,

```text
w = 15372σ(R)−6929R,
v₁₃(w)=1  ⇔  v₁₃(σ(R))=1.                    (1)
```

The first coefficient is coprime to13 and the second term has valuation2.
If the first term's valuation is1, subtraction gives exactly1. Every other
valuation gives0 or at least2, proving the equivalence. For R=167, σ(R)=168
supplies no13, explaining the vanished old supplier.

This suggests a better replacement: a prime that supplies **both7 and13**.
The smallest prime congruent to−1 modulo91 is181, with σ(181)=182=2·7·13.

## 4. A genuine supplier round trip: 13 →181 →13

Define H₁₈₁ by u∈C, 181∤u, and the finite arithmetic guard

```text
T(u)=13²·181·R,
gcd(R,13·181)=1,
13∤σ(R).                                             (2)
```

The first two conditions are exact exponent and coprimality conditions.
The last is a substantive divisor-sum guard on the remaining block. Recognizing
it can require factoring the explicit integer R derived from T(u); it is not
a prediction based only on small residues, or a demand that all future returns
succeed. **Composite cofactors are allowed at both endpoints.**

### Proposition V — the old supplier itself returns

Every u∈H₁₈₁ has a genuine two-step first return to28C after scaling by28,
with gain greater than41565/30589. All three cofactors have7-supply: initially
from13, at the middle from the fresh181, and at the return from13 again.

**Proof.** Write v=T(u) and w=T(v). As before, v is odd and1 modulo7, hence
both scaled source steps are valid. The unitary middle split gives

```text
σ(v)=183·182·σ(R),
w=13[5124σ(R)−2353R].                               (3)
```

Modulo13 the bracket is2σ(R). Thus

```text
v₁₃(w)=1  ⇔  13∤σ(R).                              (4)
```

Also 7|σ(v), so w is odd and−1 modulo7. Therefore w∈C, and its unitary13
again supplies7. The middle term was outside C, so this is a first return.
As z=u/13>1 under the guard, v/u>15/13. Using σ(R)≥R in(3),

```text
w/v ≥2771/2353,
w/u > (15/13)(2771/2353)=41565/30589.
```

This proves the claim. ∎

The regained7-supply also permits one further growing clean-28 step. It does
not establish another two-step return to C or regeneration of(2).

**Infinitude boundary:** CRT/Dirichlet can force the middle13² and181 exponents
for infinitely many prime parameters. It does **not** here prove the additional
condition13∤σ(R) for infinitely many of them. We exhibit entries to H₁₈₁;
we do not assert an infinite entry family for this stronger guard.

## 5. Exact success, full-guard failure, and two necessary restrictions

### Supplier restoration succeeds, but its guard does not return

Take the prime parameter 197807:

```text
2571491=13·197807
  →2967133=13²·97·181
  →3560843=13·11·37·673                       under T,
72001748 →83079724 →99703604                under s.
```

Here R=97 and σ(R)=98 is coprime to13. The13 exponent follows1→2→1;
its7-supply really is restored. The gain is273911/197807, exceeding the
proved lower bound.

However, the next middle cofactor is the prime5044789, so it has neither
the13² block nor the181 block required by(2). The actual next two-step block is

```text
3560843 →5044789 →5044791=3·1681597          under T,
99703604 →141254092 →141254148             under s.
```

The last cofactor is3 modulo7, not in C. Changing the choice of a supplying
factor cannot make the prime5044789 supply7: its divisor sum5044790 is2
modulo7. The complete entry guard has failed, despite the preceding successful
supplier round trip.

The returned cofactor273911=11·37·673 is composite. Applying the prime-only
affine formula would incorrectly give4108693 instead of5044789. The exact
correction is

```text
28δ(273911)=936096.
```

The class C and implementation already allow this composite cofactor; the
nonclosure is **not** merely failure to land in a prime-cofactor class.

### Too much back-supply destroys the unitary return

Dropping13∤σ(R) from(2) is false. The prime parameter10475711 gives

```text
136184243=13·10475711
  →157135693=13²·181·5137
  →216957299=13²·1283771,
5137=11·467,       σ(5137)=5616=13·432.
```

The middle block is unitary exactly as required, and fresh181 supplies7.
But the tail's extra13-supply makes the returned13 exponent2, not1. This
agrees with the if-and-only-if criterion(4). The endpoint still has7-supply
from another prime; the counterexample concerns restoration of the specified
supplier/phase, not all future growth or all possible replacements.

### Ordinary divisibility does not certify a replacement supplier

In the41 construction, the prime parameter14337023 gives the middle term

```text
215055373=13²·41²·757.
```

Both13 and41 now have even exponents, and σ(757)=758 supplies no7. The
next cofactor is262953071≡3 modulo7, so the proposed two-step U return fails.
The simpler control p=1429 gives13·1429→13²·127→5·5077: the original
supplier fails and there is no guaranteed replacement at all.

These are counterexamples to weakened guards, not exceptions to Propositions
U or V. None is a conclusion about the full orbit's eventual fate.

## 6. A no-go for congruence-only repair, with actual prime predecessors

The numerical examples disprove the displayed guards' closure. There is also
a universal obstruction to repairing the old-13 return merely by adding more
congruences to the **prime parameter**. Unlike note09's unrestricted-cofactor
obstruction, this result keeps an actual prime predecessor throughout.

### Proposition W — finite first-image exponents can be held unchanged

Fix an odd A>1 and write L=2σ(A)−A, B=2σ(A). Suppose a reduced progression
p≡a modulo K fixes the valuations

```text
v_ℓ(v)=e_ℓ,       v=T(Ap)=Lp+B,
```

at finitely many chosen primes ℓ, for its prime parameters p∤2A. Then there
are infinitely many prime parameters in the same progression for which

```text
v_ℓ(T(v))=e_ℓ              for every chosen ℓ.
```

The exponents e_ℓ are fixed finite nonnegative integers. The assertion concerns
T; an aliquot interpretation still requires the perfect-core coprimality guards.

**Proof.** Set P=∏ℓ^(e_ℓ+1). By Dirichlet choose a prime q≡−1 modulo P,
avoiding the finitely many prime divisors of KABL. Fix this q. Impose

```text
p≡L⁻¹(q−B)  (mod q²).
```

This condition forces q||v. It is reduced modulo q, because q∤LB, and its
modulus is coprime to K. CRT combines it with the original reduced progression;
Dirichlet gives infinitely many prime p in the combined progression, excluding
p|2A. The prime q is new to Ap: q∤A and p≢0 modulo q.

Since q is unitary in v, q+1 divides σ(v). Hence

```text
v_ℓ(2σ(v))≥e_ℓ+1>e_ℓ=v_ℓ(v).
```

Unequal-valuation subtraction now gives v_ℓ(T(v))=e_ℓ for every chosen prime. ∎

Only one prime varies at a time: choose and fix q first, then vary p in its
progression. There is no prime-tuples assumption, nor an assumed factorization
of the remaining part of v.

### Application: no finite congruence refinement forces13 to restore its supply

Take any multiple K of25852099 and any a≡77141 modulo25852099 with
gcd(a,K)=1. Every prime p in that progression still has the H₄₁ first-image
exponents v₁₃(v)=2 and v₄₁(v)=1. Proposition W gives infinitely many such
actual prime entries with

```text
13²||T(v),       41||T(v).
```

The returned term **does supply7**, through41, but13 is still at an even
exponent and does not supply7. It is outside C and outside H₄₁. Thus even
retaining returned7-supply does not repair old-13 restoration.

Any compatible finite collection of congruences on p, including exact
valuations at finitely many fixed primes of the affine first image, decomposes
into finitely many progressions. Every nonempty reduced component admits this
counterconstruction. Components containing only finitely many prime parameters
are not covered by this assertion. Neither are factorization-dependent guards
on σ(R), later iterates, or a different supplier/return phase.

The same argument applies to a prime-parameter progression fixing middle
exponents13² and181¹: an auxiliary unitary q can force the returned exponents
to stay2 and1. So finite congruence refinement alone cannot imply the extra
tail-sigma exclusion in H₁₈₁. This does not rule out H₁₈₁ itself or some richer
factorization-aware subclass; it identifies why the noncongruential guard
cannot simply be removed.

For a small explicit **modular** construction over the original41 progression,
two auxiliary primes suffice:

```text
30757+1=2·7·13³,       3361+1=2·41².
```

Add conditions making each occur to exponent1 in15p+28. Both prime-parameter
classes are reduced and compatible with the base class. The artifact records
the resulting CRT progression and its forced returned exponents. It does
**not** assert that the least residue is prime or present it as an observed
prime-input orbit. Prime existence here comes from the written Dirichlet proof.
For an arbitrary refinement K, the proof chooses auxiliary primes avoiding K;
these two particular primes are not asserted to work for every K.

## 7. Small bounded audit, not longer Lehmer traces

The exact report [`supplier-handoff.json`](results/supplier-handoff.json)
includes all prime-parameter candidates p≤1000000 satisfying the necessary
congruences for the41 construction. Those congruences reduce to

```text
p≡28638 (mod48503),       48503=7·13²·41.
```

There are21 integer candidates in that interval. Eighteen are proved composite;
the three prime parameters77141,659177,853189 satisfy the exact exponent
guards. All three pass Proposition U; only one has7-supply at its return,
and none returns to H₄₁. Rejected parameters are retained in the artifact.
These are an exhaustive check of this particular progression interval, not
independent survival trials or a blind holdout.

The named negative controls and the181 supplier round trip are **separate**
from that prime-parameter cohort. Some have larger prime parameters. Their
bounds and full exact factorizations are explicit; they are not smuggled into
the bounded cohort's counts. No Lehmer sequence was extended.

## 8. Reproduction and remaining obligation

```sh
python3 -m aliquot handoff --compact > /tmp/supplier-handoff.json
cmp /tmp/supplier-handoff.json research/results/supplier-handoff.json
python3 -m unittest discover -s tests -p test_handoff.py -v
```

`aliquot/handoff.py` has no external dependencies. It uses exhaustive trial
factorization, with the default 2000000 work units **per call**, and checks all
reported cofactor sums and both actual scaled edges independently by divisor
pairs. The inclusive independent-source cap is10000000000. A source or work
limit raises unresolved computation and emits no partial report; it is never
a failed mathematical sample or a probable-prime acceptance.

The progression cohort bound is at most1000000. The prime-parameter block API
accepts parameters at most20000000; the named181 checks accept a current
cofactor and are bounded by the explicit source checks. The generic CRT helper
caps the fixed core and target primes at1000000, targets at8, exponents at8,
and the combined modulus at128 bits. The proof of Proposition T is not limited
by those implementation caps. The geometric7-supply helper handles huge
exponents without expanding the prime power. Large persisted integers and
rational components are decimal strings. Terminal0 has no role in this positive
cofactor construction; the aliquot map is never evaluated there.

Tests reconstruct the complete artifact, independently check every named edge,
verify the exact back-supply equivalences on a bounded unitary-block grid,
exercise all geometric-supply orders and huge exponents, check CRT exceptions,
and retain full-guard and weakened-guard failures. The additional saturation
test uses exhaustive divisor enumeration on a separately factored
middle-to-return identity; it asserts neither a prime predecessor nor another
observed prime-input trace. Tests and AI critiques do
not formally verify the universal proofs or certify historical novelty.

**What is now isolated:** one can force a parity-changing loss, force a fresh
replacement, and even restore the original supplying exponent. But a finite
congruence refinement of the prime-entry construction cannot guarantee that
restoration universally. What remains unproved is preservation of the
**whole handoff guard on the evolving tail**,
including its divisor-sum exclusions and the composite correction. The next
step must address that tail transformation or an alternative closed collection
of phases, not infer perpetual renewal from another successful finite circuit.
All notes, code, and artifacts remain outside the served `site/` directory.
