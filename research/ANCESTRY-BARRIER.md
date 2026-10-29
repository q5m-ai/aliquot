# 12. Beyond density: a bounded-depth ancestry obstruction

**Result:** every fixed-depth extension of the smaller-ancestor filter removes
only a density-zero part of the abundant direct roots. Even imposing strictly
increasing forward prefixes leaves at least X/48−o(X) survivors through X.
This is an asymptotic limitation theorem, not another large census, an escaping
orbit, or a solution. It uses an established Erdős growth theorem; historical
novelty and independent human verification remain unestablished.

The result does **not** cover general forward coalescence. We separate that
case, give a positive-density one-step obstruction as a corollary of note11,
and exhibit abstract maps showing why growth and density facts alone cannot
settle infinite behavior. No positive global merger/descent mechanism emerged.

## 1. Definitions and the surviving classical input

For positive n, s(n)=σ(n)−n. Zero is a terminal symbol, and s(0) is undefined.
An iteration reaching zero cannot subsequently reach a positive target. Put

\[
 A_X=\{n\le X:s(n)>n\}.
\]

Let R_h(X) consist of abundant targets N≤X for which **no positive m<N**
reaches N in 1,…,h steps. Intermediate values are **unrestricted**; this is
not a graph truncated at X. Define

\[
 e_h(X)=\#\{n\in A_X:\neg[n<s(n)<\cdots<s^h(n)]\}.
\]

A terminated or undefined full prefix fails the condition, without assigning a
value to s(0). Write G_h for the set satisfying that strict-growth condition.
Erdős's valid fixed-depth growth result is

\[
 e_h(X)=o(X)\qquad\text{for every fixed }h.                 \tag{E}
\]

### A necessary provenance correction

P. Erdős, [*On asymptotic properties of aliquot sequences*](https://users.renyi.hu/~p_erdos/1976-22.pdf),
*Mathematics of Computation*30 (1976), 641–645,
[DOI](https://doi.org/10.1090/S0025-5718-1976-0404115-8), states more than we
can safely import. The small-prime persistence lemma and the lower-growth
argument are usable. Do **not** import its asserted general upper/decreasing
iterate estimates.

Pomerance's [2018 survey, introduction](https://www.math.dartmouth.edu/~carlp/aliquot8.pdf)
states exactly the fixed-depth abundant-growth result used here. His
[2020 lecture, slides24–25](https://www.math.dartmouth.edu/~carlp/upintconf.pdf)
explicitly records that Erdős withdrew his claimed proof of the analogous
arbitrary-depth decreasing assertion; the two-step case and a conditional
extension are different results. These sources and the complete1976 paper
were inspected. No exceptional-set inverse-image conjecture is assumed.

For a safe derivation of (E), let d_L(n) be the full prime-power part of n
supported on primes≤L. Erdős's Lemma2 preserves this part for almost every
seed through any **fixed** number of iterations. Moreover,

\[
 \frac1X\sum_{n\le X}\left(\frac{\sigma(n)}n-
       \frac{\sigma(d_L(n))}{d_L(n)}\right)
 \le\sum_{d>L}\frac1{d^2}\le\frac1L.
\]

Indeed the omitted reciprocal divisors have a prime factor>L and thus exceed
L. Markov's inequality bounds the omitted contribution. Davenport's continuous
abundancy distribution controls the arbitrarily narrow band just above2.
Consequently, apart from arbitrarily small density, abundant n have an abundant
d_L(n) for sufficiently large fixed L. Its persistence forces every iterate in
the chosen fixed prefix to remain abundant, establishing (E). This does not
supply upper control of those iterates or a uniform growing-depth rate.

## 2. An elementary positive-density supply of direct roots

Partition the abundant **sources** through X into

\[
\begin{aligned}
 B_X&=\{n\in A_X:s(n)>X\},\\
 D_X&=\{n\in A_X:s(n)\le X,\ s(n)\text{ is not abundant}\},\\
 U_X&=\{n\in A_X:s(n)\le X,\ s(n)\text{ is abundant}\}.
\end{aligned}
\]

The abundant targets having smaller direct predecessors are exactly s(U_X).
A smaller predecessor is automatically abundant, and every source in U_X is
smaller than its target. Hence the exact accounting identity is

\[
 \boxed{|R_1(X)|=|B_X|+|D_X|+|U_X|-|s(U_X)|.}             \tag{1}
\]

The last term is the excess of source count over distinct-image count, **not**
an ordered-pair second moment. Also |D_X|≤e₂(X)=o(X).

For n=12t, the five distinct proper divisors t,2t,3t,4t,6t give s(n)≥16t.
Thus every multiple of12 in (3X/4,X] lies in B_X, proving the unconditional
finite bound

\[
 \boxed{|R_1(X)|\ge
 \lfloor X/12\rfloor-\lfloor X/16\rfloor=X/48+O(1).}       \tag{2}
\]

These multiples are unused **sources**, not an identified family of uncovered
targets. The argument is a counting argument; it does not assert that those
same multiples are roots. Neither Proposition X nor any orbit conjecture is
needed for (1)–(2).

## 3. Proposition Y: fixed-depth ancestry scarcely reduces the direct roots

For every integer h≥1 and every positive integer X,

\[
 \boxed{|R_1(X)\setminus R_h(X)|
 \le\sum_{\ell=2}^{h}e_\ell(X)\le(h-1)e_h(X).}            \tag{3}
\]

The empty sum for h=1 is zero.

**Proof.** Take an excluded direct root N and a witnessing path

\[
 m=x_0\to x_1\to\cdots\to x_t=N,\qquad m<N,\quad t\le h,
\]

stopped at its **first** arrival at N. All vertices are positive. No vertex
repeats before that arrival, since determinism would give an earlier arrival.

Let a be the minimum vertex, at index i. Then a≤m<N≤X, and a is not the
endpoint. Its next vertex is larger, so a is abundant. The final predecessor
exceeds N: a smaller one would contradict N∈R₁(X), and equality would violate
first arrival. Therefore the suffix from a to N has length ℓ=t−i≥2 and
contains a downward step. The starting value a is counted by e_ℓ(X).

For each pair (a,ℓ) there is at most one target s^ℓ(a). Counting possible pairs
proves (3). In particular it does not matter how high the intermediate values
rise. We count small exceptional **starting values**, not the potentially large
inverse image of a density-zero set. Initially deficient witnesses are also
handled: their path minimum, not necessarily their initial value, is charged. ∎

For independent backward and forward budgets h,k≥1, it follows that

\[
 0\le |R_1(X)|-|R_h(X)\cap G_k|
 \le\sum_{\ell=2}^{h}e_\ell(X)+e_k(X).                    \tag{4}
\]

For any **fixed** h,k, (E) turns the right side into o(X). Thus these survivors
have the same lower and upper densities as the direct roots; existence of an
ordinary density for R₁ is not asserted. In particular,

\[
 \boxed{|R_h(X)\cap G_h|
       \ge X/48-o(X)\qquad(h\text{ fixed}).}              \tag{5}
\]

Strict growth is sufficient, not necessary, to pass finite termination,
repetition and descent-below-the-start tests. Those weaker forward checks can
only leave more survivors. They are not being identified with G_h.

### A genuine indirect exclusion

The exact path

\[
 372\longrightarrow524\longrightarrow400
\]

has 372<400<524. Target400 is abundant and has no smaller **direct**
predecessor, but has this smaller two-step ancestor. Its absence of smaller
direct predecessors is checked exhaustively in the regression, not asserted
from this path alone. This demonstrates that (3) is not saying the extra
filter never helps; it bounds the asymptotic number of additional exclusions.

## 4. An unbounded-depth diagonal corollary, not infinite survival

Choose increasing integer thresholds X_j≥j so that

\[
 e_j(X)\le X/j^2\qquad(X\ge X_j).
\]

Such thresholds exist by (E); take X₁=1. Define
H(X)=max{j:X_j≤X}. Then H is nondecreasing and tends to infinity. From (4),

\[
 |R_{H(X)}(X)\cap G_{H(X)}|
 \ge\lfloor X/12\rfloor-\lfloor X/16\rfloor-X/H(X).        \tag{6}
\]

Even the single set of seeds passing both tests through their assigned depth
H(N) has lower density at least1/48: for N≤X, H(N)≤H(X), so the survivors in
(6) belong to that set.

**Each individual seed is still assigned only a finite test.** These statements
do not produce any seed passing every depth. Decreasing sets can all have
density1 and have empty intersection, as {n:n≥j} illustrates. No divergent
orbit follows from the diagonal corollary.

No effective formula, numerical threshold or growth rate for H is supplied.
An explicit rate would require, for example,

\[
 H(X)e_{H(X)}(X)=o(X),
\]

or the sharper weighted exception bound from (4). The1976 paper's brief
remarks on growing-depth lower bounds do not by themselves establish this
budget. This diagonalization is standard, not a separate breakthrough.

## 5. Coalescence is not ancestry

A smaller-seed coalescence means

\[
 s^i(N)=s^j(m),\qquad m<N,\quad i,j\ge0.
\]

Ancestry is the case i=0; forward descent to a smaller value is j=0.
**The interior case i,j>0 is not covered by Proposition Y.** Both paths can
increase while merging, as in

\[
 174\longrightarrow186\longleftarrow126.
\]

Different offsets also matter:

\[
 56\longrightarrow64\longleftarrow76\longleftarrow48.
\]

Neither example forces a smaller seed to pass through174 or56. The first
merger has no downward edge at all. The second does, but it ends at64, not56;
charging56 would require inverse-image control absent from the ancestry proof.
The original seed—not merely a later, larger iterate—must exceed the competing
seed to contradict minimal escape.

### Corollary Z: a stronger one-step shared-successor obstruction

Let M(X) consist of abundant u≤X with s(v)≠s(u) for every positive v<u.
For each target T in the covered set 𝓑(X) of [Proposition X](BACKWARD-COVERAGE.md#3-proposition-x-a-positive-density-lp-method-corollary),
choose its least positive predecessor u_T. Some predecessor is below T, so
u_T<T≤X and u_T is abundant. Different T have different u_T, giving

\[
 |M(X)|\ge|\mathcal B(X)|\gg X.
\]

For every fixed h, removing e_h(X)=o(X) exceptions still leaves positive density
of these sources with strictly increasing h-step prefixes. Thus even the
**one-step shared-successor** cover has positive-density misses, not merely
infinitely many misses.

This is an immediate corollary of X, not a new collision estimate. The sources
may have smaller direct ancestors or later mergers. Separate positive-density
bounds for M(X) and R_h(X) do not imply a positive-density intersection. This
corollary depends on X; Proposition Y and the explicit1/48 bound do not.

## 6. Two logical countermodels: why the quantifiers do not prove escape

These are **not aliquot maps**. They show precisely what the growth/ancestry
facts alone fail to imply, not that an arithmetic proof for s is impossible.

Write n=2^k u with u odd, and let E={n:k≥u}. Through X this set has
O((log X)²) elements, since both k and u are at most log₂X. Define

\[
 F_-(n)=\begin{cases}1&n\in E,\\2n&n\notin E,\end{cases}
 \qquad
 F_+(n)=\begin{cases}
 \text{least power of2 greater than }n&n\in E,\\
 2n&n\notin E.
 \end{cases}
\]

- Every F_- orbit eventually enters1↔2: doubling preserves u and eventually
  raises k to u, where the next step goes to1.
- Every F_+ orbit strictly increases and eventually joins the powers-of-two
  ray, so every orbit escapes.
- Every odd n≥3 has **no predecessor at all** for either map: outputs are even,
  or1. Such n pass every ancestry depth.
- For each fixed h, almost every seed has its first h steps equal to successive
  doublings under either map. A first exceptional encounter requires
  2^j n∈E for some j<h, giving at most O_h((log X)²) starting values through X.
- More strongly, each odd n≥3 doubles for its first **n steps**, before any
  exceptional rule is applied. A density-half set therefore survives even
  this explicit linearly growing test depth in the entirely cyclic model.

Both maps have positive boundary outflow: all nonexceptional n∈(X/2,X] map
above X. Every seed coalesces with1, but the common component is cyclic in
one map and escaping in the other. These properties cannot settle infinite
behavior without additional arithmetic information about exceptional encounters.

### Bounded coalescence can also defeat ancestry survivors

A separate example shows why Y cannot simply be restated for coalescence:

\[
 f(n)=\begin{cases}
 2n+1&n\text{ even},\\
 \text{least power of2 greater than }n&n\text{ odd}.
 \end{cases}
\]

Every step grows. Its image has density1/4 (the odd numbers congruent to1
modulo4, apart from initial exceptions, plus powers of2), so its roots at
every ancestry depth have density3/4. Boundary outflow is at least X/4−O(1).
Nevertheless **every n≥5 coalesces with a smaller m with both offsets positive
and at most2**:

- For odd n, write f(n)=2^k. Take m=2^(k−2), giving f²(m)=f(n).
- For even 2^k<n<2^(k+1), take m=2^k; both second iterates are2^(k+2).
- For n=2^k≥8, take m=2^(k−1)+1<n. Then f(m)=n, so f²(m)=f(n).

Thus abundant-root and growth estimates do not abstractly imply a
bounded-coalescence obstruction. This map need not have the divisor-sum
structure of s, and nothing here rules out using that additional structure.

## 7. What changed, and what remains missing

The backward proposal now has both a positive-density covering result and a
positive-density obstruction. More importantly, the obstruction survives every
fixed amount of ancestry search and forward checking, with unrestricted
intermediate values. This is a rigorous reason not to expect a larger fixed
budget to resolve the exceptional-seed problem.

It is **not** a theorem about all finite certificates, every algorithm, or
arithmetic proofs in general. General forward coalescence, effective
orbit-dependent/unbounded-time arguments, and other arithmetic resources remain
outside it. No mechanism forcing an actual exceptional aliquot orbit to descend
or merge has been obtained. Restating that obligation is not a new strategy.

The two read-only committee analyses agreed on the ancestry theorem. Their
bounds were reconciled to (3), and their countermodels address distinct limits:
infinite-survival inference versus bounded coalescence. Their agreement is not
human peer review or formal theorem certification. The claims above are written
arguments from identified classical inputs, with novelty unverified.

## 8. Targeted exact regressions, not a new asymptotic experiment

[`tests/test_ancestry.py`](../tests/test_ancestry.py) checks:

- the root accounting and floor bound for each target cutoff through1000;
- all depth1–4 prefixes from seeds1–1000, allowing excursions above1000;
- the minimum-path charging and two-budget inequalities in that finite universe;
- independently summed edges for the named ancestry and coalescence witnesses;
- termination, cycles, a noninitial minimum in an explicit toy path, and the
  countermodel constructions.

The aliquot checks use trial factorization and independent divisor-pair sums.
Encountered sources are capped at100000; a breach fails the regression rather
than being called a mathematical exception. No large Lehmer factorization,
new report schema, CLI, or website feature is added. Finite tests do not prove
(E), little-o estimates, or either infinite behavior of the abstract maps.

```sh
python3 -m unittest discover -s tests -p test_ancestry.py -v
```
