# 09 — Supplier renewal: a precise return lemma and its failed closure

**Outcome:** a guarded two-step first return to a 28-core residue phase has a
written proof and a uniform gain greater than 15/13. Its guard does **not**
regenerate. An exact example shows why retaining a supplying prime is not
enough: cancellation raises its exponent from 1 to 2, destroying its supply
of 7. Separately, a sharp residue-supplier theorem identifies precisely the
scope of the template `R≡−1 (mod M) ⇒ M|σ(R)`.

These are local deductions using classical arithmetic, not a claimed historical
novelty, closed infinite-orbit mechanism, divergent seed, or solution. The return
construction extends the unitary-supplier method of [note 03](REGENERATION.md);
it does not replace that method's missing closure argument. “Proved” means the
argument below, with imported Dirichlet's theorem stated explicitly—not that
finite tests or an AI audit establish a theorem.

## 1. Fixed diagnostics, not success-filtered return classes

This follows the plan in [note 08](EXPONENT-VECTORS.md). Before this diagnostic
run we fixed the following arithmetic phases and windows. The source traces
had already been examined: this is **not** a blind holdout or a statistical
preregistration.

- `clean6`: n>6 with v₂(n)=v₃(n)=1.
- `clean28`: n>28 with v₂(n)=2 and v₇(n)=1.
- `A7`: σ(d₇(n))≥2d₇(n) and σ(n)>2n, where d₇ contains the complete
  prime powers at 2,3,5,7.
- `surplus6` / `surplus28`: the corresponding clean core with strict divisor-sum
  supply surpluses at both of its primes.
- First returns to each phase: examine at most **64 actual edges**. Report
  gains, losses, neutral returns, termination, cycles, exhausted windows, and
  censored continuation separately.
- A different experiment asks whether **some** A7 checkpoint above the starting
  value exists within **8, 32, or 64** edges. Its existence is the outcome being
  tested, not an entry condition. Keeping only successful checkpoints would
  make the gain assertion tautological.
- The independent small census covers **2≤n≤100000**, including failures. It
  also tests four source-only compressed states, plus all cofactors u≤100000
  in the explicit guarded family in §4.

No new large-orbit factorization was requested. The analysis first replays the
prime proofs and exact edges in
[`exponent-vectors-extended.json`](results/exponent-vectors-extended.json),
records that file's SHA-256, and derives
[`supplier-renewal.json`](results/supplier-renewal.json). The latter contains
1296 unique certified positive sources and 1290 complete source/successor vector
pairs; five missing successor factorizations and the separate terminal 1→0
edge account for the difference. Per-seed counts and overlapping windows are
not independent trials. Shared source diagnostics are deduplicated.

### Deciding A7 at an unfactored frontier

Write n=dr, where d=d₇(n) and gcd(d,r)=1. The exact condition is

```text
n ∈ A7  ⇔  σ(d)≥2d and (r>1 or σ(d)>2d).
```

Indeed, σ(n)/n=(σ(d)/d)(σ(r)/r), and σ(r)>r exactly when r>1. This needs only
stripping the four small primes, not factoring r. Thus a final known value can
sometimes certify an A7 return even when its full factorization is unresolved.
Strict-surplus membership is left unknown when it cannot be decided. Knowing
the membership or abundance of that value does **not** give its next edge.

## 2. Exact factor supply and the missing renewal information

For a certified vector E(n), each complete block pᵃ contributes

```text
(v₂(1+p+⋯+pᵃ), v₃(1+p+⋯+pᵃ), v₅(1+p+⋯+pᵃ), v₇(1+p+⋯+pᵃ)).
```

The columns sum to the corresponding valuations of σ(n). We record the actual
prime identities, not only their multiset of exponents. Each edge also records
supply margins, tied-coordinate normalized differences modulo ℓ², and the exact
extra cancellation valuations. A zero normalized residue means a lower bound
on cancellation, not its exact valuation.

For m=s(n)>0, split **whole prime-power blocks** as m=A R, where A uses primes
already dividing n, and R uses only new primes. Then gcd(A,R)=1 and

```text
d_ℓ = max(0, v_ℓ(m)+1−v_ℓ(σ(A))),
v_ℓ(σ(m))>v_ℓ(m)  ⇔  v_ℓ(σ(R))≥d_ℓ.
```

This is multiplicativity and valuation addition, not a renewal assumption.
We also have gcd(R,nσ(n))=1. The artifact identifies disappeared blocks, changed
exponents of retained blocks, each new supplier, and the old/new supply totals.
For a changed retained prime, its cancellation accounting is recorded even
when that prime lies **outside** 2,3,5,7.

For instance, 276→396 has A=36 and R=11. Both the 2- and 3-demands are 3;
σ(11)=12 supplies only 2 and 1. No all-surplus inference is available.

## 3. A sharp residue supplier lemma

### Proposition R — universal negative-one supply

Let M>2 be an integer. The following are equivalent:

1. For every positive integer R≡−1 (mod M), M divides σ(R).
2. M divides 24.

**Proof of sufficiency.** For M|24, every unit d modulo M satisfies d²≡1:
odd squares are 1 modulo 8, and nonzero squares are 1 modulo 3. Every divisor
of R is a unit modulo M. R cannot be a square, since that would give both
R≡1 and R≡−1 modulo M, impossible for M>2. Pair its distinct divisors d,R/d.
Each pair has sum

```text
d + R/d ≡ d − d⁻¹ ≡ 0 (mod M).
```

Summing the pairs proves the assertion.

**Proof of necessity.** If some unit a has a²≢1 modulo M, **Dirichlet's theorem**
gives distinct primes p≡a and q≡−a⁻¹ modulo M. Their residue classes are reduced;
there are infinitely many choices, so distinctness is no restriction. For R=pq,

```text
R≡−1 (mod M),
σ(R)≡(a+1)(1−a⁻¹)=a−a⁻¹≢0 (mod M).
```

It remains to classify moduli all of whose units square to 1. If an odd prime
r divides M, reduction to the field modulo r shows every nonzero element is a
root of X²−1. Thus r−1≤2 and r=3. The unit 2 modulo 9 excludes a factor 9;
the unit 3 modulo 16 excludes a factor 16. These units can be lifted to units
modulo M by the Chinese remainder theorem. Hence M=2ᵃ3ᵇ with a≤3 and b≤1,
so M|24. The converse was already checked. ∎

The quantifier M>2 matters: odd squares such as 9 disprove the assertion for
M=2. M=1 is trivial. No assertion is made about **all other forms** of modular
guards: for example, an exact unitary factor 13 supplies 7.

Consequently R≡23 (mod 24) always supplies at least three factors of 2 and one
of 3 to σ(R). Both bounds are sharp, already at R=23. It does not supply 7:

```text
335=5·67≡−1 (mod 168),    σ(335)=408,    7∤408.
```

Even strengthening this particular template to a negative-one residue modulo
168 does not fix that problem. Likewise, R=95 modulo 48 and R=143 modulo 72
refute the corresponding stronger whole-modulus claims. The finite scan of
moduli 3..128 finds counterexamples for every excluded modulus, but that scan
is an illustration; the necessity proof is the all-modulus statement.

### Stronger obstruction — no reduced progression forces 5- or 7-supply

More generally, for any prime ℓ≥5, any modulus K≥1, and any residue r coprime
to K, there are infinitely many squarefree semiprimes R≡r (mod K) for which
ℓ does not divide σ(R). Their primes can also avoid any prescribed finite set.

**Proof.** Put L=lcm(K,ℓ), and choose a unit c modulo L lifting r modulo K.
Choose a unit x modulo L whose residue modulo ℓ is neither −1 nor −c.
There are ℓ−1≥4 unit residues and at most two exclusions; CRT supplies the
other prime-power components. Set y=cx⁻¹ modulo L. Neither x nor y is −1
modulo ℓ. Dirichlet supplies distinct primes p≡x and q≡y modulo L, outside
any given finite set. Then R=pq≡r modulo K, while neither factor of
σ(R)=(p+1)(q+1) is divisible by ℓ. Vary q to obtain infinitely many R. ∎

Thus finer **reduced congruence classes on an unrestricted cofactor** cannot
force the missing 7-supplier. This does not exclude nonreduced congruences
forcing a unitary factor, extra factorization restrictions, or constraints
imposed by an actual preceding aliquot edge. It is not a nonexistence proof
for a guarded orbit class. For ℓ=3 the assertion would be false, as Proposition R
already shows. The proof is a Dirichlet construction, not inferred from tests.

### Corollary — local residue-certified exponent preservation

In the old/new split m=A R, suppose

```text
m>6,  6|m,  R≡23 (mod 24),  d₂≤3,  d₃≤1.
```

Then v₂(σ(m))>v₂(m) and v₃(σ(m))>v₃(m). Subtracting m preserves these two
exponents in s(m), and s(m)>m because every multiple of 6 above 6 is abundant.
This is a one-step conclusion **from m**, not a return to n's exponent vector,
and does not regenerate the same residual guard.

The census has 488 eligible sources; all 488 obey the corollary. None renews
this same residual guard at the next edge within that census. The latter is
a bounded observation, **not** a theorem of impossible consecutive guards.
The first witness is

```text
936 → 1794 → 2238,
1794=78·23,   2238=6·373.
```

At the first split, R=23 and the corollary applies. At the second, R=373≡13
modulo 24 and σ(373)=374 supplies no 3. Thus even this provable supply event
need not reproduce itself.

## 4. The promised precise first-return lemma

Put T(u)=2σ(u)−u. Whenever gcd(u,28)=1,

```text
s(28u)=28T(u).
```

Define the base phase and its **present-arithmetic guard** by

```text
B = {28u : u>1, gcd(u,28)=1, u≡−1 (mod 7)},
G₁₃ = {u : 28u∈B, 7|σ(u), 13||T(u)}.
```

Here 13||T(u) means exponent exactly 1. It is decidable from σ(u) modulo 169;
it does not assume any long future return or require factoring T(u)'s remaining
cofactor. Ordinary divisibility by 13 would not suffice.

### Proposition S — a guarded two-step first return with gain >15/13

For every u∈G₁₃, the path

```text
28u → 28v → 28w,       v=T(u),  w=T(v),
```

is a genuine two-step **first** return to B. All three terms have the clean
28-core, both steps grow, and w/u>15/13.

**Proof.** u is odd, so v is odd. Since 7|σ(u) and u≡−1 modulo 7, v≡1 modulo 7.
Thus gcd(v,28)=1 and the reduction is valid at both sources. Write v=13z;
13||v gives gcd(13,z)=1. Therefore

```text
σ(v)=14σ(z),
w=2σ(v)−v≡−v≡−1 (mod 7),
w≥28z−13z=15z=(15/13)v.
```

w is odd and coprime to 7, so 28w∈B. The middle term is not in B since its
cofactor is 1 modulo 7. Finally T(u)=u+2s(u)>u for u>1, giving w/u>15/13;
the second step also grows. ∎

There are infinitely many entries: primes p≡349 modulo 1183=7·13² satisfy

```text
p≡−1 (mod 7),    p≡11 (mod 169),    T(p)=p+2≡13 (mod 169).
```

The progression is reduced, so Dirichlet's theorem supplies infinitely many
such primes. Only p is required to be prime. No prime-tuples conjecture or
primality assumption on v or w is being smuggled in. This is the same finite
entry-construction method as [Proposition F](REGENERATION.md), not an iterable
mechanism or a new claim of arbitrary-length growth.

### Exact nonclosure, not merely an omitted proof

The smallest census example gives

```text
349 → 351 → 769              under T,
9772 → 9828 → 21532          under s.
```

But T(769)=771=3·257 is not divisible by 13, and σ(771)=1032 is not divisible
by 7. Thus **no** replacement unitary divisor of 771 could supply 7 either.
The next two-step cofactor path is 769→771→1293, ending at 5 rather than −1
modulo 7. The successful first return did not renew even the broader
“some unitary supplier of 7 at the middle term” condition.

More revealingly, the first example whose returned cofactor loses 7-supply is

```text
1987 → 1989=3²·13·17 → 4563=3³·13²       under T,
55636 → 55692 → 127764                 under s.
```

Here σ(1989)=3276=2²·3²·7·13. At prime 13, the two terms in
2σ(1989)−1989 have equal valuation 1. Cancellation raises the result's
13-exponent to 2. **The supplying prime is retained, but stops supplying 7:**

```text
σ(13)=14,       σ(13²)=183,
σ(4563)=σ(3³)σ(13²)=40·183=7320,       7∤7320.
```

The endpoint is in B and is larger, but is outside G₁₃. This is precisely a
prime-exponent mechanism—not just a relabelling of the integer path. Tracking
only cancellations at 2,3,5,7 would miss the decisive change at 13.

Among all u≤100000, 265 satisfy G₁₃ and all pass the two-step lemma. Only 8
return to G₁₃; 257 do not. Of those failures, 134 lose returned 7-supply and
247 lose the next unitary-13 condition (these reasons overlap). Eleven of the
265 are prime entries in the displayed fixed progression. These counts neither
prove nor suggest that any of the eight successful renewals continues forever.

The stronger automatic endpoint supply in the 3-based [Proposition E](REGENERATION.md)
does not transfer to 7: negative-one residue forces 3-supply, but not 7-supply,
exactly as Proposition R distinguishes.

## 5. Actual return blocks and adversarial controls

The A7 first returns within 64 edges are:

| Seed | Gain | Loss | Neutral | Terminated without return | Censored |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 276 | 238 | 6 | 0 | 0 | 1 |
| 552 | 120 | 2 | 0 | 0 | 0 |
| 564 | 199 | 5 | 0 | 0 | 0 |
| 660 | 134 | 6 | 0 | 0 | 0 |
| 966 | 185 | 0 | 0 | 0 | 0 |
| 12 | 0 | 0 | 0 | 1 | 0 |
| 30 | 6 | 0 | 0 | 1 | 0 |
| 138 | 75 | 11 | 0 | 1 | 0 |
| 318 | 26 | 0 | 0 | 1 | 0 |
| 220 | 0 | 0 | 1 | 0 | 0 |
| 28 | 0 | 0 | 0 | 0 | 0 |

There are no other A7 first-return status categories in this particular run;
all are retained in the implementation. The strict-surplus phases sometimes
have undecidable frontier membership. Seed 28 is not in A7: it is perfect.

The previously known 660 block at index 9 remains a losing first return:

```text
47952 → 94586 → 47296 → 46684 → 42524 → 31900.
```

More severely, in the 276 trace:

```text
n₁₇₁ = 9039664938664952483187163910 ∈ A7,
first positive-time A7 return: n₂₂₇ = 351121244430380.
```

The first return takes 56 steps and loses value. The 8-, 32-, and 64-step
profitable-checkpoint claims all fail at this source, with the complete windows
observed, not censored. This does **not** imply permanent failure of recovery:
the same certified artifact has its first larger A7 checkpoint at index 313,
142 steps later, with value 11800507429706023344513135120. Choosing 142 or a
larger horizon after seeing this example would not establish a universal
recovery bound.

The 64-step checkpoint search also retains six terminating failures in the
138 trace, one in 318, and a certified cycle failure at 220. It keeps two
censored 276 searches. A terminating control's many profitable returns cannot
be distinguished from perpetual regeneration by counting past successes.

The driver-loss mechanisms are different:

- At 276's edge 169, (v₂(n),v₂(σ(n)))=(2,1): an actual supply shortfall forces
  the successor exponent to 1.
- At 966's edge 172, that pair is (2,2): cancellation adds three factors of 2,
  making the successor exponent 5. Divisibility by 28 remains, but the exact
  driver is lost.

## 6. Current supplier summaries are still not autonomous states

The census compares four compressed current states: the four source exponents;
then those exponents plus total supply; then every block's exponent and supply
column, retaining the identities 2,3,5,7 but not other prime labels; finally that
state plus normalized tie residues modulo ℓ². The target is the successor's
four strict-surplus booleans and its A7 membership. No successor factorization
is included in the state. Repeated-state occupancy is reported to avoid a
vacuous “prediction” on uniquely identifying states.

Even the richest state has 1032 ambiguous buckets among 22465 A7 sources.
A small exact collision is

```text
860=2²·5·43  →  988=2²·13·19,
1340=2²·5·67 → 1516=2²·379.
```

The source exponents and every compressed supply column agree; there are no
target-prime cancellation ties to refine. At the successors, σ(988)=1960 has
v₂=3>2, whereas σ(1516)=2660 has v₂=2. Thus even this richer summary cannot
determine future supply. Keeping the complete prime-labelled vector avoids
this information loss, but does not magically give a finite closed state system.

The census also directly refutes one-step closure of `surplus6` (1626 losses
among 3901 sources) and `surplus28` (277 among 341). Their first counterexamples
are 30→42 and 364→420. These are exact failures of these specific classes,
not a prohibition on every richer guard or variable-time return rule.

## 7. Verification, reproduction, and the narrowed next obligation

```sh
python3 -m aliquot renewal --compact > /tmp/supplier-renewal.json
cmp /tmp/supplier-renewal.json research/results/supplier-renewal.json
python3 -m aliquot verify-renewal research/results/supplier-renewal.json
python3 -m unittest discover -s tests -p test_renewal.py -v
```

`--source` selects a different certified exponent-vector artifact; its exact
hash is recorded. `--bound` is limited to 2..100000. Parent replay retains
[note 08's bounds](EXPONENT-VECTORS.md), including the 16 MiB file limit and
aggregate proof/edge caps. No probable-prime shortcut is introduced.

Two read-only AI mathematical analyses agreed on the modulus classification,
the guarded prime-entry return, and the failure at 349. They proposed different
additional factor-handoff guards, but neither supplied an iterable class. Their
agreement is not human peer review or a novelty check; those further handoff
proposals are not presented here as achieved closure.

The small census checks its factor-product sums against independent additive
divisor sieves through 100000 and 304920 (the largest first image). The guarded
28-family checks both cofactor sums and the actual scaled aliquot edges by
independent divisor-pair enumeration, with an explicit inclusive 100000000
source cap. A cap failure raises unresolved computation, not a negative sample.
All persisted integers are exact; potentially large values are decimal strings.
Terminal 0 has no exponent vector or outgoing aliquot edge.

`verify-renewal` replays the parent proof evidence, reruns all derived
computations, and compares **every** report field, including negative outcomes
and censoring. It is reproducible reconstruction with independent arithmetic
cross-checks, not a separate formal theorem prover or an independently written
second implementation of the return classifier. Tests additionally check the
small-prime phase criterion, cancellation identities, nonclosure witnesses,
corrupted evidence, terminal/cycle behavior, atomic CLI failure, and budgets.

The next mathematical obligation is narrower now: **prove a handoff that
survives cancellation at the supplying primes themselves**, or gives a finite
return through a specified alternative phase when a supplier's exponent changes
parity. Prime retention alone, negative-one residue alone, and current supply
margins alone each have explicit failures. Any proposed replacement must still
prove its own guard regeneration and net gain over complete return blocks,
including losing excursions. None of those whole-orbit obligations is supplied
by this note. All research remains outside the served `site/` directory.
