# Literature audit: fixed prime support and aliquot sums

**Status:** broader online literature search, not an exhaustive bibliographic
certification. Historical novelty of Proposition K in [GLOBAL.md](GLOBAL.md)
remains unverified. A directly related fixed-support result for amicable pairs
and cycles is explicitly published; those consequences must not be presented
as new here. No conjecture resolution follows.

## 1. Exact target and the closest explicit predecessor

Our target is finiteness, for each prescribed finite prime set S, of

```text
{n > 1 : every prime dividing n*s(n) belongs to S}.
```

Here s(n)=σ(n)−n. This imposes only one directed edge n→s(n), not a
return edge s(n)→n.

Paul Pollack, *Finiteness theorems for perfect numbers and their kin*,
American Mathematical Monthly 119 (2012), 670–681, explicitly states at the
end of section 5 (author manuscript, pp. 11–12):

> for any finite set of primes P, there are only finitely many amicable pairs
> for which the support of NM is a subset of P

He immediately adds that the obvious generalizations for sociable cycles and
amicable tuples hold, and says the proof uses only tools already displayed in
the article. The paper develops supernatural-number compactness, limits of
prime exponents, abundancy, and valuation arguments.

- [Corrected author manuscript](https://www.pollack-math.net/dickson-fixed.pdf)
- [Errata, Monthly 120 (2013), 482–483](https://www.pollack-math.net/dickson-errata.pdf)

Both were consulted. The original global continuity claim for abundancy on
supernatural numbers is false. The correction establishes continuity on the
closed subspace with a prescribed bound on support size, and explicitly says
this suffices for all applications in the paper.

**Comparison:** Proposition K implies fixed-support finiteness for amicable
pairs and cycles, even without prescribing the period: every cycle vertex is
in its finite set of admissible sources. Pollack already explicitly identifies
the cycle direction of this subject. His quoted statement does not itself
assert finiteness of arbitrary one-way aliquot edges, nor does finite cycle
count by itself exclude an infinite nonperiodic path. Do not silently equate
these statements or attribute Proposition K to Pollack without further evidence.

The exponent-subsequence step in our proof is also part of this established
compactness tradition, not a new proof technique.

## 2. Older general machinery

J.-H. Evertse, *On sums of S-units and linear recurrences*, Compositio
Mathematica 53 (1984), 225–244:
[primary text](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf).
Theorem 1 gives nondegenerate projective finiteness, including S-unit equations.
Thus the qualitative machinery used in Proposition K does not originate with
the 2002 theorem. The paper also discusses greatest-prime-factor growth for
nondegenerate linear recurrence sequences. An aliquot orbit is not known to
be such a recurrence; those results cannot simply be applied to it.

J.-H. Evertse, H. P. Schlickewei, and W. M. Schmidt, *Linear equations in
variables which lie in a multiplicative group*, Annals of Mathematics 155
(2002), 807–836:
[author manuscript](https://pub.math.leidenuniv.nl/~evertsejh/00-equation.pdf).
Theorem 1.1 supplies the stronger quantitative finite-rank result cited in
GLOBAL.md. Nondegeneracy (no vanishing subsum) is essential. Our proof selects
a minimal zero subsum containing a fixed nonzero constant before invoking it.
Neither general paper is identified here as publishing the exact aliquot
application.

## 3. Related finiteness results with different hypotheses

- **Artjuhov and Borho (1970s), as exposited by Pollack (2012).** For fixed k,
  finitely many amicable pairs satisfy both ω(NM)≤k and Ω(gcd(N,M))≤k
  (Theorem 8). Here ω counts distinct prime factors and Ω counts them with
  multiplicity. Bounding the *number* of primes is not prescribing their
  identities; bounding the common-factor exponents is an additional hypothesis.
- **Paul Pollack, *On relatively prime amicable pairs*, Moscow Journal of
  Combinatorics and Number Theory 5 (2015), 36–51.**
  [Primary text](https://www.pollack-math.net/borhoexplicit3.pdf), Theorem 1:
  for a coprime amicable pair with ω(NM)=K, one has
  NM < (2K)^(2K²). Coprimality cannot be omitted.
- **Yuta Suzuki, *On amicable tuples*, Illinois Journal of Mathematics 62
  (2018), 225–252.**
  [Primary text](https://projecteuclid.org/journals/illinois-journal-of-mathematics/volume-62/issue-1-4/On-amicable-tuples/10.1215/ijm/1552442661.pdf).
  Improves the coprime-pair bound and treats anarchic harmonious tuples.
  An amicable k-tuple satisfies σ(M_i)=Σ M_j for every i; for k>2 this is
  not the definition of a sociable cycle. Its introduction explicitly
  distinguishes the sociable-number problem from its tuple results.

## 4. Related prime-support and statistical work, not substitutes

- **Florian Luca, *On numbers n for which the prime factors of σ(n) are among
  the prime factors of n*, Results in Mathematics 45 (2004), 79–87.**
  [DOI](https://doi.org/10.1007/BF03322999). Bibliographic lead, not a fully
  checked theorem here. Pollack–Pomerance describe it as studying prime-deficient
  numbers with bounded ω(n). It concerns σ(n), not s(n).
- **Paul Pollack and Carl Pomerance, *Prime-perfect numbers*.**
  [Primary text](https://math.dartmouth.edu/~carlp/pperfs13.pdf).
  Proves infinitely many n with the same distinct prime divisors as σ(n);
  section 5.2 discusses prime-deficient numbers and cites Luca. This varies
  prime support across examples, and does not transfer through subtraction.
- **Lee Troupe, *On the number of prime factors of values of the
  sum-of-proper-divisors function*.**
  [Primary text](https://arxiv.org/html/1405.3587v3).
  Normal-order results for ω(s(n)) and Ω(s(n)) concern almost all inputs,
  not every term of an exceptional individual orbit.
- **Florian Luca and Carl Pomerance, *The range of the sum-of-proper-divisors
  function*, Acta Arith.168 (2015), 187–199.**
  [Later author-hosted text](https://www.math.dartmouth.edu/~carlp/LucaPomeranceAA2.pdf).
  Theorem1.2 proves positive lower density of even aliquot values; the following
  paragraph states a fixed-arithmetic-progression extension. Lemmas2.1–2.5 and
  section3 control small-prime parts and distinct-image collisions. These are
  statistical results, not universal fixed-support or orbit theorems. The
  [earlier draft](https://www.math.dartmouth.edu/~carlp/rangeofs6.pdf) previously
  cited here lacks the later rough-squarefreeness Lemma2.2 needed in the
  collision proof; use the later version for the backward adaptation below.

## 5. Search scope, negative findings, and remaining work

Queries covered aliquot sequences/sums, sum-of-proper-divisors, σ(n)−n,
finite/fixed/prescribed prime support, bounded largest prime factors,
smooth/friable numbers, S-units, amicable-pair finiteness, sociable cycles,
prime-perfect and prime-deficient numbers. References in the primary texts
were followed selectively, especially from Pollack to Borho/Artjuhov and from
Suzuki back to Pollack. Errata were checked for the closest predecessor.
Search-generated summaries were not accepted as mathematical evidence.

No exact earlier statement of Proposition K or its escaping-orbit corollary
was located in this search. That is a report about retrieval, not evidence
that no such publication exists. This was not a complete MathSciNet/zbMATH
review, an exhaustive forward-citation search, or a full inspection of older
German/Russian sources. Luca's exact theorem remains a specific unchecked
lead. Expert consultation and those bibliographic checks are still needed.

**Current attribution of K:** an independently derived application of classical
S-unit finiteness, with historical novelty unverified and explicit related
fixed-support cycle finiteness already published by Pollack (2012).

## 6. Subsequent backward-coverage feasibility pass

[Notebook11](BACKWARD-COVERAGE.md) revisits the distinct-image problem, not
fixed prime support. Both complete LP versions above and the publication-list
entry were consulted. The main published proof uses deficient sources, whereas
excluding a least escaping seed needs smaller, hence abundant, predecessors.
The notebook supplies an explicit **LP-method adaptation** on bounded-abundancy
sources, using their normal-order lemma to bound the needed totient/divisor
weights and their later squarefreeness lemma for rough gcds. It gives positive
lower density for the specified abundant-core/square-root family. That exact
restriction was not located as a theorem statement in the inspected texts;
this is neither a novelty claim nor an unqualified quotation of Theorem1.2.

Pomerance's [*The first function and its iterates*](https://www.math.dartmouth.edu/~carlp/aliquot8.pdf),
in *Connections in Discrete Mathematics* (2018), pp.125–138, was also read.
Its section2 explains the almost-all ratio relation s²(n)/s(n)∼s(n)/n, and
section3 bounds inverse-image sizes. Density-one assertions still leave room
for an exceptional orbit. Its extension s(0)=0 is not adopted here.

The one million-target census is independent finite evidence, not a proof of
the analytic bounds. The remaining gap is forcing a hypothetical least escaping
seed into a covered class, not merely obtaining positive density. This bounded
pass is not an exhaustive modern citation or novelty review.
