# Research notebook 01: growth is easy; invariance is the obstacle

**Status:** foundational deductions and a bounded, independently cross-checked
experiment. No proof or disproof of the aliquot conjecture, no divergent orbit,
and no claim of mathematical novelty. The results below belong to the classical
guide/driver framework; this notebook makes one small case explicit.

## 1. The exact question

For a positive integer n, define

```text
σ(n) = sum of all positive divisors of n
s(n) = σ(n) − n.
```

Start at n₀ ≥ 1 and apply nₖ₊₁ = s(nₖ) while nₖ > 0. In particular,
s(1) = 0; **s(0) is undefined**. The site's 0 → 0 continuation is only a
visualization convention, not part of this definition.

The **Catalan–Dickson aliquot conjecture** says every such orbit terminates at
0 or eventually enters a positive cycle (including a perfect-number fixed
point). It remains an open problem in the sources listed below. This is not the
claim that every orbit terminates, nor the unrelated Catalan/Mihăilescu theorem.

### Elementary reduction: a counterexample must tend to infinity

A repeated positive value forces a periodic tail, since s is deterministic.
If an infinite orbit is bounded, the pigeonhole principle forces a repetition.
Conversely, a finite terminating orbit or an eventually periodic orbit is bounded.

Moreover, a nonterminating, nonperiodic orbit has no repeated values. For each
fixed B it can visit {1, …, B} only finitely many times. Thus it must eventually
stay above B: **nₖ → ∞**, not merely have a large peak. It need not increase
monotonically. This observation does not supply an effective bound or decision
procedure.

Proof-side target: establish an orbit-wise bound or eventual return/descent
argument for every seed, allowing cycles. A least counterexample, if one exists,
cannot ever fall below its seed; this does not imply step-by-step growth.
Disproof-side target: exhibit one seed and prove escape for all future iterates.
Neither a finite growing prefix nor an exhausted computational budget suffices.

## 2. A growing class with an exact exit criterion

Write v₂(a) for the exponent of 2 in a positive integer a. Consider the explicitly
defined class

```text
C6 = { n > 0 : v₂(n) = 1 and 3 divides n }
   = { n > 0 : n ≡ 6 (mod 12) }.
```

This is a useful setting for the classical driver 6, not a claim that C6 is
forward-invariant or that it captures all growing orbits.

### Proposition 1: growth inside C6

s(6) = 6. For every n ∈ C6 with n > 6, s(n) > n.

**Proof.** In fact, for every multiple n > 6 of 6, the three distinct proper
divisors n/2, n/3, n/6 sum to n. The additional proper divisor 1 is distinct
from all three. Hence s(n) ≥ n + 1. ∎

### Proposition 2: complete one-step exit classification

Let n = 2r ∈ C6, so r is odd and divisible by 3. Then

```text
s(n) = 3σ(r) − 2r,
3 divides s(n),
s(n) ∈ C6  ⇔  4 divides σ(r).
```

Exactly two types of n leave C6:

1. **Odd successor:** n = 2u², with u odd and 3 | u.
2. **Successor divisible by 4:** n = 2p^(4a+1) u², where a ≥ 0, p is prime,
   p ≡ 1 (mod 4), u is odd, 3 | u, and gcd(p, u) = 1.

All other members of C6 remain in C6 for the next step. Leaving C6 says nothing
by itself about later growth, termination, or re-entry.

**Proof.** Multiplicativity gives σ(2r) = 3σ(r). Since 3 | r, the successor
is divisible by 3. As r is odd, reducing 3σ(r) − 2r modulo 4 gives:

| v₂(σ(r)) | Successor | In C6? |
| --- | --- | --- |
| 0 | odd | no |
| 1 | divisible by 4 | no |
| ≥ 2 | congruent to 2 modulo 4 | yes |

For an odd prime p and exponent e ≥ 0,

```text
v₂(σ(p^e)) = 0                              if e is even,
             v₂(p + 1) + v₂(e + 1) − 1     if e is odd.
```

For even e, the geometric sum has an odd number of odd terms. For odd e, write
e + 1 = 2^t b with b odd. Factoring p^(2^t b) − 1 into p^b − 1 and the t
successive factors p^(2^j b) + 1 shows that its 2-adic valuation is
v₂(p − 1) + v₂(p + 1) + t − 1; dividing by p − 1 gives the formula.
Here odd b preserves the valuations of p ± 1, and every factor with j ≥ 1
has valuation 1 because an odd square is 1 modulo 8.

Valuations add across the prime-power factors of σ(r). Consequently:

- v₂(σ(r)) = 0 iff every exponent of r is even, i.e. r is a square.
- v₂(σ(r)) = 1 iff exactly one prime p has an odd exponent e, with
  p ≡ 1 (mod 4) and e ≡ 1 (mod 4); all other exponents are even.

In the second case write e = 4a + 1 and r = p^(4a+1) u² with p ∤ u.
Since p ≠ 3 and 3 | r, necessarily 3 | u. These are exactly the two cases
stated above. ∎

The **exponent restriction matters**: 2250 = 2 · 3² · 5³ stays in C6 even
though its odd part has just one odd prime exponent and that prime is 1 mod 4.
Replacing “4a+1” by “any odd exponent” would make the criterion false.

### Conditional escape certificate — the unproved part is explicit

If some n₀ > 6 has **every** iterate in C6, Proposition 1 makes that orbit
strictly increasing. Successive terms are both 6 modulo 12, so

```text
nₖ ≥ n₀ + 12k.
```

This would disprove the full conjecture. We have **not** found such a seed with
a proof of perpetual membership. Proposition 2 turns the missing obligation
into avoidance of two explicit exit families at every future step; it does
not prove that avoidance.

Both exit types can actually be reached from another member of C6:

```text
438 → 450 → 759       (odd exit at 450)
 78 →  90 → 144       (multiple-of-4 exit at 90).
```

Nor is sustained initial growth enough:

```text
30 → 42 → 54 → 66 → 78 → 90 → 144 → 259 → 45 → 33 → 15 → 9 → 4 → 3 → 1 → 0.
```

The step 90 → 144 leaves C6, but growth continues for another step. “Loses this
class” must not be reported as “starts decreasing” or “sequence terminates.”

## 3. An obstruction to a simpler divergence argument

**Proposition 3.** For every fixed d > 1, the set of all positive multiples of
d is not forward-invariant under s.

**Proof.** Choose any prime p | d and put L = p(p − 1), x = d^L. For a prime
power q^a in the prime factorization of d, the corresponding factor in σ(x) is
σ(q^(aL)). Modulo p:

- if q = p, this geometric sum is 1;
- if q ≡ 1 (mod p), it is aL + 1 ≡ 1;
- otherwise, Fermat's little theorem gives q^(aL) ≡ 1, and the geometric-sum
  formula, dividing by the nonzero residue q − 1, again gives 1.

Thus σ(x) ≡ 1 (mod p), while x ≡ 0 (mod p). Therefore s(x) ≡ 1 (mod p),
so d cannot divide s(x). ∎

For even d the simpler witness x = d² works: the divisor sum of a square is
odd by the prime-power product formula, so s(x) is odd.

This rules out an escape certificate consisting **only** of “all multiples of
one fixed d.” It does not rule out a restricted subset, a union of classes,
a multistep certificate, or divergent orbits. In particular, it is not evidence
for the full conjecture merely because this simple disproof strategy fails.

## 4. Reproducible finite check, separate from the proofs

From the repository root, with Node.js 22+ and no dependencies:

```sh
node research/driver-six.mjs --bound 100000
# Equivalent convenience command:
npm run research:driver-six -- --bound 100000

# Byte-for-byte reproduction of the committed JSON:
node research/driver-six.mjs --bound 100000 > /tmp/driver-six-100000.json
cmp /tmp/driver-six-100000.json research/results/driver-six-100000.json
npm test
node --check site/explorer.js
```

The [committed report](results/driver-six-100000.json) exhausts all **8,333**
sources n ∈ C6 with **n ≤ 100,000**, taking exactly **one step per source**:

| Outcome | Sources |
| --- | ---: |
| Remain in C6 (including the fixed point 6) | 7,821 |
| Exit to an odd value | 37 |
| Exit to a multiple of 4 | 475 |

The first exits are 18 → 21 and 90 → 144. As a separate check of one count,
the odd-exit sources are 18t² for odd t ≤ 74, giving exactly 37 sources.

The experiment:

- computes exact sums using BigInt trial factorization and the product formula;
- independently recomputes every sum using a BigInt additive proper-divisor
  sieve, which uses neither factorization nor the exit criterion;
- checks the predicted exit type, divisibility by 3, and strict growth above 6;
- rejects mismatches instead of publishing a partially verified report;
- limits the source bound to 1…1,000,000, inclusive; it never truncates an
  orbit or labels a bound as divergence. Successors may exceed the source bound
  and are still computed exactly; they are not iterated by this experiment.

Number arithmetic is used only for bounded indices, exponents, and counts;
all divisor sums, prime powers, and sequence values use BigInt. Trial division
proves the factors prime; there are no probable-prime assumptions. s(0) is not
evaluated. The small bound is intentional: this is a theorem-regression check,
not a serious attempt to extend unresolved large sequences.

The two arithmetic algorithms share a Node runtime and runner: this is
**algorithmically independent checking**, not independent researchers' review
or a proof-assistant formalization. Tests also compare direct divisor
enumeration on 1…300, compare both algorithms on every input 1…10,000, exercise
boundary/invalid cases and exponent traps, and reproduce the full report.

The fraction of retained sources in this finite interval is **not** a survival
probability along an orbit. Orbit values are neither uniformly sampled nor
independent. The mathematical proofs above do not rely on these counts.
All research code and results remain outside the served `site/` directory.

## 5. Next research question and acceptance criteria

Study the restricted statement:

> Every orbit starting in C6 above 6 eventually leaves C6.

A proof would eliminate this *particular* perpetual-growth mechanism, not prove
the aliquot conjecture: an orbit could move among other growing classes. A
rigorous counterexample would disprove the full conjecture by the conditional
escape certificate. The restricted statement may itself be very difficult.

Next, examine **two-step reachability of the exit families**, rather than just
one-step growth or a larger seed census. Any proposed invariant subclass must:

1. contain an explicit seed above 6;
2. have a proof that every member's successor stays in the subclass;
3. imply avoidance of both exact exit forms, accounting for prime exponents;
4. justify every primality/factorization assertion without an unproved oracle.

A finite test can reject a proposed invariant by producing a witness. It cannot
establish the universal closure assertion. Seek an independent mathematical
review of any candidate closure argument before calling it a result.

## 6. Initial literature map (not a comprehensive review)

- **Definition/status, consulted:** Eric W. Weisstein,
  [“Catalan's Aliquot Sequence Conjecture,” MathWorld](https://mathworld.wolfram.com/CatalansAliquotSequenceConjecture.html).
  Identifies the open termination-or-cycle conjecture.
- **Expository source, consulted:** A. S. Mosunov,
  [*What do we know about aliquot sequences?*](https://www.cs.uleth.ca/~hadi/2016-09-29-aliquot_sequences.pdf),
  seminar slides, September 29, 2016, reporting joint work with K. Chum,
  R. K. Guy, and M. J. Jacobson, Jr. Parts I–III discuss the opposing
  Guy–Selfridge conjecture, guides/drivers, driver loss, and why averaged
  growth statistics require care. The date matters: its numerical records
  are not asserted to be current here.
- **Primary source to obtain and read:** R. K. Guy and J. L. Selfridge,
  [*What drives an aliquot sequence?*](https://doi.org/10.1090/S0025-5718-1975-0384669-X),
  *Mathematics of Computation* 29 (1975), 101–107. Also consult their
  [1980 corrigendum](https://doi.org/10.2307/2006239), p. 319. Bibliographic
  metadata was checked through Crossref; the original AMS PDF returned HTTP
  403, and neither full text nor the corrigendum has been reviewed here.
  Do not attribute unverified precise statements to these papers.

Literature heuristics are not used as premises in Propositions 1–3. Their
proofs are written out so that the first research artifact is auditable even
while the primary-source review remains unfinished.
