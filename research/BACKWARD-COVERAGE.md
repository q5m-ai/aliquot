# 11. Backward coverage: a passed density gate, not a least-seed contradiction

**Outcome of one bounded feasibility pass:** the distinct-image density target
can be justified by adapting existing Luca–Pomerance machinery. The computation
below also distinguishes real coverage from repeated representations. Neither
result forces a hypothetical least escaping seed into the covered set. **Stop
at that remaining proof obligation rather than enlarge the census.**

The mathematical argument, imported literature, and finite experiment are
separate. This is not a solution, a novelty claim, or an independent human or
formal certification of the adapted argument. No additional Lehmer orbit steps
were computed.

## 1. The exact backward target

If an escaping orbit exists, let N be its least possible starting value. Then
s(N)>N: a smaller successor would itself escape, while equality is a fixed
point. Also, N has **no positive predecessor m<N**; every such predecessor
would escape too. Such a smaller predecessor is necessarily abundant.

For an abundant integer C and prime p with p∤C,

\[
 N=s(Cp)=s(C)p+\sigma(C)>Cp.
\]

Define the proposed covered set through a **target** bound X by

\[
 \mathcal B(X)=\{N\le X:s(N)>N,\ N=s(C)p+\sigma(C),\
 s(C)>C,\ p\text{ prime},\ p\nmid C,\ C^2\le N\}.
\]

The root restriction is C²≤N, not merely C²≤X. For a fixed finite list of
cores the image count is O(X/log X), by the prime number theorem. Varying
cores is essential to a positive-density target, and introduces collisions.
Perfect or deficient cores can sometimes also give smaller predecessors;
they are not silently admitted to this particular sufficient family.

A convenient subfamily is C=6u with gcd(u,6)=1 and u>1. Then

\[
 N=6[(2\sigma(u)-u)p+2\sigma(u)]
\]

is a proper multiple of6, hence abundant, and C is abundant. This guarantees
the direction and target abundance, **not** distinctness of the images.

## 2. Literature provenance: use the later version

Florian Luca and Carl Pomerance, *The range of the sum-of-proper-divisors
function*, **Acta Arith.168 (2015), 187–199**:

- [Later author-hosted text](https://www.math.dartmouth.edu/~carlp/LucaPomeranceAA2.pdf),
  linked from [Pomerance's publication list](https://www.math.dartmouth.edu/~carlp/).
- [Earlier draft](https://www.math.dartmouth.edu/~carlp/rangeofs6.pdf), previously
  linked in this repository's literature note.

Theorem1.2 proves positive lower density of even aliquot values. The following
paragraph explicitly states an extension to every fixed arithmetic progression.
The proof counts distinct values by smooth-part stratification and a second
moment, not by assuming independence of prime representations.

The main displayed proof starts with **deficient** sources, the opposite of
our required direction. Its theorem statement does not explicitly assert the
abundant-core/target-square-root restriction above. The argument in section3
is an **adaptation of that proof**, not a quotation of a stronger published
statement or an assertion of historical novelty.

There is a material version difference: the later text includes **Lemma2.2**, a
rough-prime squarefreeness statement needed for the quadratic-congruence count
in its small-gcd collision estimate. Its large-gcd tail estimate is also
revised. The older draft alone is not the basis for the adaptation.

The later paper's inputs used below are Lemmas2.1, 2.2, 2.4, 2.5 and section3,
including equations(3.1)–(3.14). Lemma2.4 imports a normal-order theorem for
τ(s(n)); the original proof calls that lemma optional, but our replacement
bound **uses it**. None of these almost-all statements is applied along an
arbitrary orbit.

As related context, Pomerance's [*The first function and its iterates*](https://www.math.dartmouth.edu/~carlp/aliquot8.pdf)
(2018), section2, explains the almost-all relation s²(n)/s(n)∼s(n)/n;
section3 studies inverse-image sizes. Such statistical facts do not decide an
exceptional least seed. That paper sets s(0)=0 for its purposes; this repository
continues to leave s(0) undefined.

## 3. Proposition X: a positive-density LP-method corollary

There is a constant c>0 such that, for every sufficiently large X,

\[
 \#\mathcal B(X)\ge cX.
\]

This remains true after restricting to C=6u, gcd(u,6)=1, u>1. It implies
positive lower relative density among abundant targets, since their count
through X is at most X. No numerical value of c is claimed.

### 3.1 Canonical sources and a bounded-abundancy restriction

Use source scale x and the nested factorization

\[
 n=pC=pqrk,\qquad C=q\ell,\quad\ell=rk,
\]

where p,q,r are primes and

\[
 x^{1/120}<k\le x^{1/60},\quad
 x^{1/15}<r\le x^{1/12},\quad
 x^{7/20}<q\le x^{11/30},\quad
 x/(2C)<p\le x/C.
\]

Require k=6v, gcd(v,6)=1. The primes p,q,r are, in that order, the three
largest prime factors, so this parametrization counts **distinct sources**.
For sufficiently large x,

\[
 x/2<n\le x,\quad C\le x^{7/15},\quad
 p>\tfrac12x^{8/15}>C.
\]

The reciprocal sums over the r and q intervals tend to positive constants;
the reciprocal sum over the k interval with v₂(k)=v₃(k)=1 is asymptotic to
(log x)/2160. Uniform prime counts in the outer dyadic interval therefore give
at least δx sources for some fixed δ>0 and all sufficiently large x.

Choose a fixed B>2ζ(2)/δ and retain only n with σ(n)/n≤B. Indeed,

\[
 \sum_{n\le x}\frac{\sigma(n)}n
 =\sum_{d\le x}\frac1d\lfloor x/d\rfloor\le\zeta(2)x,
\]

so this removes fewer than δx/2 sources. Every divisor t of a retained n
satisfies σ(t)/t≤B. In particular this holds for C, ℓ, and k.
All four are proper multiples of6. The image N=s(n) is also a proper multiple
of6, and

\[
 C^2<n<N\le(B-1)x.
\]

Thus all retained images have the required direction, abundance and core bound.
We have so far counted sources only.

### 3.2 Regularity at every nested variable

Write y₀(t)=log log t/log log log t and use the common cutoff y=y₀(x)/2.
Require the density-one properties of LP Lemmas2.1, 2.4, 2.5 at n,C,ℓ,k.
Exclude the density-zero exceptional set in Lemma2.2 at C; its hypothesis
P⁺(C)>√C is automatic here. Also exclude k having a prime divisor in (y,y₀(x)].

These restrictions cost o(x) sources, not an assumed uniform error in every
smooth-part stratum. For any density-zero exceptional set E,

\[
 \sum_{\substack{t\le z\\t\in E}}\frac1t=o(\log z).
\]

For exceptions at C, multiply this harmonic bound by the outer prime-count
bound O(x/log x). At ℓ and k, the remaining prime reciprocal sums are O(1),
so the same argument applies. Exceptions at n cost o(x) directly. The prime
reciprocal sum in (y,y₀(x)] tends to zero, so excluding the specified divisors
of k also costs o(x). Canonical factorization prevents hidden multiplicities
in these upper bounds.

All nested variables are at least x^(1/120), so y₀(t)>y eventually. No nested
variable has a prime factor in (y,y₀(x)]. Consequently LP Lemma2.1 gives the
**same** y-smooth part d for n,C,ℓ,k and their positive s-images:

\[
 \gcd(t,\sigma(t))=d,\qquad d\operatorname{rad}(d)\mid\sigma(t).
\]

For C specifically, write s(C)=dw. Its rough factor w has every prime divisor
above y₀(C), not just y: Lemma2.1 also rules out factors in the intervening
interval. Lemma2.2 therefore makes w squarefree. This justifies squarefreeness
of the later rough gcd h; a weakened cutoff alone would not do so.

### 3.3 The replacement for deficiency

Put L=log log x. Lemma2.4 implies ω(w)=O(L). Mertens' theorem gives

\[
 \frac w{\varphi(w)}
 \le\prod_{y<q\le L^2}(1-1/q)^{-1}
       \exp(O(L/L^2))=O(1).
\]

Here log(L²)/log y stays bounded. Also

\[
 \frac d{\varphi(d)}\le\zeta(2)\frac{\sigma(d)}d\le\zeta(2)B.
\]

It follows, uniformly over retained cores, that

\[
 \boxed{\frac{s(C)}{\varphi(s(C))}\ll_B1},\qquad
 \frac{\sigma(s(C))}{s(C)}\ll_B1,\qquad
 \sum_{h\mid s(C)}\frac{\tau(h)}h
 \le\left(\frac{\sigma(s(C))}{s(C)}\right)^2\ll_B1.
\]

These are the bounds for which simply replacing “deficient” by “abundant” in
the original proof would be invalid.

For completeness, the other deficiency-sensitive parts of LP section3 change
as follows; the exponent gaps in their sieve estimates are unchanged:

| Original use | Replacement |
| --- | --- |
| Rule out a distinct-core collision with σ(C)=σ(C′) | min(p,p′)≫x^(8/15), whereas max(s(C),s(C′))≪_B x^(7/15). Thus neither large prime can divide the other coefficient; equality would force p=p′ and C=C′. |
| Keep the two-prime sieve interval long | Cs(C′)≪_B x^(14/15), leaving the same fixed power gap below x. Also s(C′)>C′. |
| Bound coefficient totient ratios; discard factors shared with s(C′) | Each relevant divisor's ratio is bounded by the boxed estimate. |
| Bound the large-h congruence's integer | σ(ℓ),s(ℓ)≪_B ℓ, so its absolute value is O_B(x^(3/10))<x^(1/3). The reduced-fraction and monotonicity argument is unchanged. |
| Count the small-h quadratic residue pairs | h is squarefree by Lemma2.2 at C, as checked above; there are at most τ(h) pairs. |
| Apply Brun–Titchmarsh in those residue classes | h divides s(C′), hence h/φ(h)≪_B1; the same modulus/exponent bounds apply. |
| Sum the final small-h divisor weights | Use the displayed τ(h)/h bound instead of the original constant4. |

LP Lemma2.5 still bounds large-prime factors shared with σ(C); its threshold
(log log C)² is no larger than L². Their normal-order divisor bound still gives
the required powers of log x in the large-h and intermediate-h errors. No
prime-tuples lower bound is being assumed: the simultaneous-prime steps are
**upper-bound sieves**, as in LP.

### 3.4 Distinct images, then rescale to the target bound

Let A(x) be the resulting canonical source family, with #A(x)≫_B x.
Stratify by d, its largest y-smooth divisor. LP's smooth-part tail estimate and
(3.1)–(3.3), now with the retained density constant, select strata D satisfying

\[
 \#A_d(x)\gg_B\frac{x}{d\log y},\qquad
 \sum_{d\in D}\frac1d\gg_B\log y.
\]

For R_d(N)=#{n∈A_d(x):s(n)=N}, the collision calculation (3.5)–(3.14), with
the replacements just checked, gives

\[
 \sum_N R_d(N)^2\ll_B\frac{x}{d\log y}.
\]

This is the imported substantial estimate, not a consequence of the finite
census. Different strata have disjoint image supports because s(n) has the
same y-smooth part d. Cauchy–Schwarz therefore gives

\[
 \#s(A(x))\ge\sum_{d\in D}
 \frac{(\sum_N R_d(N))^2}{\sum_N R_d(N)^2}\gg_B x.
\]

Finally set x=X/(B−1). All these distinct abundant images lie at most X and
belong to the stated square-root-core family. This proves the proposition by
adaptation of LP's estimates. It does not assert that all abundant targets,
or any particular exceptional seed, are covered. ∎

## 4. One exact bounded census

[`aliquot/backward.py`](../aliquot/backward.py) tests three nested sets of
**abundant targets**, not arbitrary outputs or representation counts:

1. **Square-root core:** exactly the proposed family B(X).
2. **Any abundant prime core:** the same family without C²≤N.
3. **All smaller predecessors:** every m<N with s(m)=N, regardless of shape.

The inclusive target cap is 1000000. Every smaller source is automatically
within it. A multiplicative least-factor sieve and an independent additive
divisor sieve agree at every positive integer through the cap. The family
representation sets are independently rebuilt from core/prime parameters,
using the additive sums and its exact prime characterization s(p)=1. The two
sets must be exactly equal. No probable-prime test is used.

The primary rule, comparison families, and prefix levels were fixed before
this run. Related traces and examples had already been studied; this is not
blind holdout evidence. Prefixes and overlapping preimages are not independent
trials. There are no censored samples inside this finite universe. An invalid
bound, arithmetic mismatch or output-cap failure aborts without partial JSON.

| Target bound | Abundant targets | Square-root core targets | Any abundant prime core targets | All smaller-predecessor targets |
| ---: | ---: | ---: | ---: | ---: |
| 1000 | 246 | 22 | 54 | 97 |
| 10000 | 2488 | 436 | 797 | 1049 |
| 100000 | 24795 | 5339 | 8853 | 10384 |
| 1000000 | 247545 | 58896 | 93288 | 104107 |

At the largest bound the shares are **23.7920%, 37.6853%, and 42.0558%**.
The uncovered part of the proposed family partitions exactly into:

- 34392 targets with an abundant prime core but none meeting C²≤N;
- 10819 with a smaller predecessor but no admitted abundant prime core;
- **143438 with no smaller direct predecessor at all**.

The latter assertion is complete for each such target. It does **not** say
these targets have no larger predecessor or are globally untouchable.

### Representations are not necessarily distinct sources

The unrestricted prime-core family has 243512 representations, 125026 distinct
predecessors, and 93288 distinct targets. For example,

\[
 s(60)=108=s(12)\cdot5+\sigma(12)=s(20)\cdot3+\sigma(20).
\]

Both representations use **one** source60, and both fail C²≤108.

For the square-root family there is at most one representation per source.
To prove this, suppose two eligible distinct unitary primes p<q divide a source
m=Dpq, with gcd(D,pq)=1. Since q≥3 and σ(D)≤D(D+1)/2,

\[
 \frac{s(Dpq)}{q^2}
 <\sigma(D)(1+1/q)^2-D
 \le\frac{16}{9}\sigma(D)-D
 \le\frac{8D^2-D}{9}<D^2.
\]

The first inequality follows by increasing p to q in the affine expression,
whose p-coefficient is positive. Thus the representation with core Dq violates
(Dq)²≤s(m), a contradiction. **Distinct remaining representations really are
distinct sources**, but different sources can still collide.

The first such collision in the census is

\[
 s(276)=396=s(306),\qquad
 16\cdot23+28=21\cdot17+39.
\]

Writing r(N) for the square-root-family multiplicity, the million-bound data
have

\[
 \sum r=70694,\qquad\sum r^2=100552,\qquad
 \#\{r>0\}=58896.
\]

The finite Cauchy lower bound is exactly
70694²/100552=1249410409/25138, about49702 distinct targets. Its 29858 ordered
off-diagonal representation pairs all concern different predecessors. These
finite moments do **not** supply an asymptotic bound. Proposition X instead
uses a restricted regular source family and stratified literature estimates.
The clean-six-core subset has 19933 sources and 15087 distinct targets here;
it is not the additional asymptotic regularity selection used in that proof.

## 5. The stopping point

None of **276,552,564,660,966** has a smaller direct predecessor. This is
exhaustive arithmetic for those particular targets, not an unresolved search.
Thus even the complete one-edge filter leaves all five Lehmer seeds eligible.
So does it leave12 and220, whose terminating and cyclic behavior respectively
show that being uncovered is not evidence of escape. The named controls30,
138 and318 are also retained, without another orbit continuation.

The density subgoal passes by established collision machinery with the
explicit adaptation above. **The global inference still fails:** a least
escaping seed could lie outside a positive-density covered set. Even density
one would not itself exclude a single exceptional seed. There is no proved
condition forcing that seed into B(X), and no backward-coverage proof of the
aliquot conjecture here.

Nor does the census rule out multistep exclusions: a path from a smaller seed
could first exceed N and then arrive at N. That is a different obligation,
not supplied by direct-predecessor counts or by the LP estimate. Do not restart
supplier-circuit expansion, increase the cap, or replace this gap with an
independence assumption on the strength of these results.

## 6. Reproduction and scope of verification

```sh
python3 -m aliquot backward --compact > /tmp/backward-coverage.json
cmp /tmp/backward-coverage.json research/results/backward-coverage.json
python3 -m unittest discover -s tests -p test_backward.py -v
```

The [persisted report](results/backward-coverage.json) has schema
`aliquot-backward-coverage-v1`. Targets, sources, cores, primes, second moments,
and rational components use decimal strings; small counts remain exact JSON
integers. Examples retain complete predecessor counts, show at most32 sources
per target and explicitly count any omitted examples. Aggregate counts are
never sample-truncated. Bound1 is valid with no abundant targets; zero is not
a source and has no divisor sum.

The report reconstructs deterministically. Tests additionally use literal
divisor enumeration for the small universe, verify named factors and edges,
check histograms/moments/partitions, distinguish C²≤N from C²≤X, and test
atomic CLI failures. They do not verify analytic sieve theorems or certify
Proposition X. All code and data stay outside the served `site/` directory.
