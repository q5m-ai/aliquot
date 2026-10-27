# Small-gain feedback and aliquot dynamics

## 1. Verdict

**Unresolved. No candidate proof or disproof of the Catalan–Dickson conjecture is obtained.**

The strongest arithmetic result of this attempt is the following finite-block theorem:

> For every real G>0, infinitely many prime inputs n=20p have two actual growing
> steps 20p → 4v → 20w, with each displayed core unitary, and w>Gp.
> Nevertheless the product of the *bare core gains* is
> [s(20)/20][s(4)/4]=33/40<1.

Thus even exact return to the starting core representation does not make its
bare gain product a stability certificate. These are **chosen unitary
factors, not disjoint driver states**: the constructed middle term also has a
unitary 20-core. No loss and subsequent recreation of that driver is claimed.
The composite-cofactor contribution can arbitrarily overwhelm the bare gain. Section 4 gives the proof, using Dirichlet's theorem,
not a numerical extrapolation. It does **not** give one seed with infinite gain.

There is also a valid finite-graph comparison theorem that includes the
cofactor contribution, and an explicit contraction threshold for the same
20→4→20 loop. Its arithmetic hypotheses are not invariant. A natural growing
supplier class fails renewal at the very small example
3580→3980→4420. These results are written mathematical arguments awaiting
independent mathematical review, not computer-certified universal theorems.

### What was developed before consulting the synthesis

The initial mapping was n=dp with p prime and gcd(d,p)=1:

    s(dp)=s(d)p+σ(d).

A periodic sequence of cores gives a rational affine return map. Integrality
consumes denominators; an integral expanding affine map eventually makes a
later prime cofactor divisible by an earlier one. On consulting
[the synthesis](../../SYNTHESIS.md) and its sources, this was found to be
**already Proposition P of [RECOVERY.md](../../RECOVERY.md)**, including cycle
handling. It is not an addition of this attempt. Proposition Q there already
uses weighted graph gains and gaps in scaled-prime sets. The revised attempt
below keeps the exact composite contribution instead of re-proving P or Q.

Throughout, σ(n) is the positive-divisor sum and s(n)=σ(n)−n for n>0.
Iteration stops at 0; s(0) is never used. A repeated positive value forces a
cycle. Otherwise an infinite orbit has distinct terms and tends to infinity.
Consequently an orbit-wise size bound, not convergence to zero, is sufficient
for the conjecture. No assumption about the existence of odd perfect numbers
is made.

## 2. Mathematical bridge: which gains are actually available?

### Source insight and nontransferring hypotheses

Dashkovskiy–Rüffer–Wirth, *An ISS Small-Gain Theorem for General Networks*,
Theorem 4 and Corollary 7, assume that the component systems are already
input-to-state stable with specified input-output gains. A robust nonlinear
gain condition, or spectral radius less than one in the linear setting,
then controls their interconnection. For two linear gains the latter
condition is their product being less than one. The primary source's
introduction, theorem statement, linear corollary, and two-system discussion
were consulted; see section 8.

Aliquot factorization does not supply such ISS subsystems. For example,
writing x=log n and A(n)=σ(n)/n gives, while s(n)>0,

    x_next=x+log(A(n)−1).

This is an accumulator driven by an arithmetic observable, not a proven
stable open-loop system. No bound on its accumulated input has been supplied.
Nor is A(s(n)) controlled by a small present cofactor excess: section 4
proves the contrary for a fixed pair of actual core modes.

I therefore do **not** invoke an ISS theorem on aliquot sequences. The bridge
is an elementary switched, positive comparison system derived next. Its
finite graph describes alternatives taken by one trajectory, not simultaneous
summation of signals. Accordingly the relevant condition is on **all directed
cycle products**, not an unsupported spectral-radius claim about an ordinary
adjacency matrix.

### Exact composite feedback identity

For a unitary split n=Du, meaning gcd(D,u)=1, multiplicativity gives

    s(Du)=s(D)u+σ(D)s(u).                                      (1)

Define η(u)=s(u)/u, including η(1)=0. This is the relative cofactor
contribution; it is nonnegative. If the next term has another unitary split
s(D_i u)=D_j u', then

    u' = a_ij u+b_ij s(u) = [a_ij+b_ij η(u)]u,
    a_ij=s(D_i)/D_j,       b_ij=σ(D_i)/D_j.                    (2)

The a's are the bare core gains; bη is the feedback contribution that must
not be omitted. Around a core cycle the product of the a's is
∏ s(D_i)/D_i. For a prime cofactor, s(u)=1, so the extra term in (2) is
constant, not zero. For a composite cofactor it need not even be bounded
relative to u.

Identity (1) is elementary and its equivalent corrections are already used
in [BLOCK-TRANSPORT.md](../../BLOCK-TRANSPORT.md) and RECOVERY.md. It fails
without unitarity: s(6·9)=66, whereas s(6)·9+σ(6)s(9)=102.

## 3. Proved comparison theorem; conditional application to aliquot orbits

### Theorem 1 — a finite-core small-gain certificate including leakage

Fix finitely many integers D_i≥2, a finite directed graph of allowed mode
transitions, a finite threshold B≥0, and nonnegative **rational** numbers
ε_ij. Consider an actual positive aliquot trajectory with a representation
n_k=D_(i_k)u_k, gcd(D_(i_k),u_k)=1 at every term greater than 1 before
termination. Reaching 1 is handled separately by the final step 1→0. Suppose:

1. Every transition whose endpoints both exceed 1 follows an edge i→j.
2. Whenever its source n_k>B, η(u_k)≤ε_ij.
3. For g_ij=a_ij+b_ij ε_ij, every directed cycle has gain product at most 1.

Then the trajectory is bounded, so it terminates or eventually cycles.
The same conclusion holds if these assumptions begin only after a finite
prefix. A prime term can be treated separately: its next values are 1,0.

**Proof.** If the trajectory reaches 1 it terminates, so assume all terms
exceed 1. For each vertex i let w_i be the largest product of g's along a
path starting at i, allowing the empty path with product 1. Removing a cycle
of product at most 1 cannot decrease a path product. Hence the maximum is
attained on one of finitely many simple paths. In particular w_i is finite,
positive, rational, and

    w_j g_ij ≤ w_i

on every edge. A common scaling makes all w_i positive integers. For a
source above B, (2) implies

    V_(k+1)=w_j u_(k+1) ≤ w_i u_k=V_k.                        (3)

For a source at most B there are only finitely many possible n and modes.
Let H be the maximum of V at the initial term and all quantities
w_j s(n)/D_j for 1≤n≤floor(B), s(n)>0, and all modes j. Including modes
that are not realizable only enlarges this finite bound. If there are no
such small sources, omit that maximum. Induction gives V_k≤H: a large
source cannot increase it, and a small source has a bounded successor.
Therefore

    n_k ≤ H max_i(D_i/w_i).

A bounded deterministic positive-integer orbit repeats unless it terminates.
This allows fixed points and nontrivial cycles. ∎

The theorem is a proved implication, **not** verification of its hypotheses
for arbitrary aliquot orbits. In particular, a mode assignment is not a proof
that all exits are covered, and a measured bound on η is not a uniform bound.

This extends the bookkeeping to arbitrary composite cofactors when explicit
relative-input bounds are available. It is not a strengthening of all of
Proposition Q: Q handles zero bare-cycle margin with prime cofactors by an
arithmetic-gap argument, whereas a positive ε can destroy that margin.

### A concrete, nonvacuous leakage threshold

For the alternating unitary cores 20 and 4,

    s(20)=22, σ(20)=42, s(4)=3, σ(4)=7,
    a_(20,4)=11/2,        a_(4,20)=3/20.

If both source cofactors in each pair of steps have η≤t, the full two-edge
upper gain is

    (11+21t)(3+7t)/40.

It is at most 1 precisely when 0≤t≤1/21. At t=1/21 the individual gains
are 6 and 1/6, with integer weights w_20=6, w_4=1. Thus this is an exact
small-gain certificate, including composite cofactors, for any tail satisfying
those guarded bounds.

In fact η(u)=1/21 never occurs. It would imply u=21s(u), so 21|u; the
prime-power product formula then gives η(u)≥η(21)=11/21, a contradiction.
Consequently every completed return satisfying the common threshold strictly
decreases the integer checkpoint u, and such a positive alternating tail
cannot persist forever.

For example, if a cofactor has at most two distinct prime divisors and all
are at least 47, with **arbitrary exponents**, then

    1+η(u)=σ(u)/u < (47/46)^2,
    η(u) < 93/2116 < 1/21.

The bound also holds at u=1. This gives a genuine restricted obstruction to
an escaping alternating tail, even though core 20 alone is abundant. It is
not a restriction known to hold on general trajectories. The bounded scan
contains the actual descending block

    9820=20·491 → 10844=4·2711 → 8140=20·407.

The two source cofactors 491 and 2711 are prime and satisfy the threshold.
The endpoint is not asserted to preserve it.

**Cycles are not silently excluded.** On 220=20·11 ↔ 284=4·71, the exact
edge-dependent bounds ε_(20,4)=1/11 and ε_(4,20)=1/71 give gains 71/11
and 11/71. Weights 71 and 11 make V constant. This is an allowed instance
of Theorem 1, not an exception to its conclusion.

## 4. Proved arithmetic obstruction: arbitrarily large gain around a subunit bare cycle

### Theorem 2 — exact core restoration with unbounded finite amplification

For every G>0 there are infinitely many primes p, coprime to 20, for which

    20p → 4v → 20w,
    gcd(v,4)=gcd(w,20)=1,
    4v>20p, 20w>4v, and w>Gp.                                (4)

Thus the selected core schedule is 20→4→20 with exact unitary
representations, although its bare cycle product is 33/40<1. The modes need
not be unique or disjoint; Theorem 1 explicitly permits chosen unitary splits.

**Proof.** The primes 5 and 199 will supply the restoration divisibility (primality of
199 can be checked by the primes 2,3,5,7,11,13). Their divisor sums multiply to

    σ(5)σ(199)=6·200=1200=2^4·3·5^2.                          (5)

Let K be squarefree and composed only of primes outside
{2,3,5,7,11,199}. Choose it so that

    γ=s(3980K)/(3980K)>max(1,10G/11).                         (6)

Such K exist: since 3980=4·5·199 and σ(3980)=8400,

    1+γ=(420/199) ∏_(q|K)(1+1/q),

and this product is unbounded. The classical elementary Euler-product
argument is ∏(1+1/q)=∏(1−1/q²)∏(1−1/q)^(-1): the first product has a
positive limit and the second diverges. Removing finitely many primes does
not change divergence.

Put M0=4·25·199²=3960100 and impose

    p ≡ 179 (mod M0),
    11p ≡ −21 (mod K).                                       (7)

The moduli are coprime. Both congruences are reduced: gcd(179,M0)=1,
and K is coprime to 11 and 21. CRT therefore gives a reduced class modulo
M0 K. **Dirichlet's theorem on primes in reduced arithmetic progressions**
supplies infinitely many primes p in it. Discard any finitely many p≤5.
No simultaneous-prime-values conjecture is being assumed.

For these primes define

    v=(11p+21)/2,       s(20p)=22p+42=4v.

Because p=179+M0 t,

    v=995+(11M0/2)t.

Hence v is odd, v≡995 mod 25, v≡995 mod 199², and K|v. In particular,

    v_5(v)=v_199(v)=1,

so 5 and 199 are unitary factors of v. Equation (5) gives 1200|σ(v).
The middle term m=4v consequently has v_2(m)=2, v_5(m)=1, while
σ(m)=7σ(v) has v_2 at least 4 and v_5 at least 2. Subtracting m preserves
the smaller valuation at each prime. Thus

    v_2(s(m))=2,       v_5(s(m))=1,

and s(m)=20w with w odd and 5∤w. This proves the exact returned unitary core,
not just divisibility by 20.

For any c|m the product formula gives σ(m)/m≥σ(c)/c, by monotonicity of
each prime-power factor. Here 3980K|m, so s(m)/m≥γ. Also

    m/(20p)=(22p+42)/(20p)>11/10.

It follows that

    s(m)/(20p)>11γ/10>G.

The first step grows, and γ>1 makes the second grow as well. Since
s(m)/(20p)=w/p, all of (4) follows. ∎

**Scope of the core return.** The proof also gives v_5(v)=1, so the middle
term 4v itself has the unitary 20-core, with cofactor v/5. Thus it is not a
forced switch between maximal cores, nor restoration after loss of the
20-driver. It is a real aliquot block with the specified, overlapping unitary
representations. The bare subunit product depends on that choice; the exact
identity (2) and its full gains account for the remaining factors.

This is an adaptation of the CRT/Dirichlet amplification mechanism already
in Proposition O of RECOVERY.md. The specific additional feature here is
**an arbitrarily amplifying actual block with a bare-contracting chosen core
cycle and exact unitary endpoint**. No historical novelty or new
lost-driver-regeneration theorem is claimed.

### Corollary: no locally bounded gain from present small cofactor excess

For every ε>0 and H>0, primes in the construction can be chosen with

    η(p)<ε,       η(v)>H,

while p≡179 mod M0 and the actual core transition is 20→4. To see this,
choose K so large that σ(4v)/(4v)≥1+γ>(7/4)(1+H), and then choose a
sufficiently large prime p in (7). Since v is odd,

    σ(4v)/(4v)=(7/4)(1+η(v)).

Thus an estimate η(v)≤C+g(η(p)) with g bounded on a neighborhood of zero
cannot hold even in this fixed prime-congruence input family. For primes,
s(p)=1 exactly; their composite defect s(p)−1 is identically zero. The same
family fixes p, σ(p), 20p, σ(20p), and the first successor modulo M0.
It therefore also defeats a feedback gain based only on these particular
finite tags. This does not exclude all factorization-aware state variables
or an unbounded reserve accounting for future bursts.

### Why the amplification does not iterate

The smallest named instance is

    p=179, v=995=5·199, w=221=13·17,
    3580 → 3980 → 4420.

The returned cofactor is not prime. Thus even though the core is exactly
restored, the input prime family is not restored.

A more serious attempted repair allows composites. Let X consist of n=20u
with gcd(u,20)=1 for which

    v=(11u+21s(u))/2 is an odd positive integer,
    v_5(v)=v_199(v)=1.                                       (8)

These are **present-arithmetic** conditions on u and s(u), not a definition
by successful future iterations. Every member has an actual return 20w
with gcd(w,20)=1, by the same supply calculation (5). Moreover,

    s(20u)/(20u)=11/10+(21/10)η(u) ≥ 11/10,
    s(4v)/(4v) ≥ s(3980)/3980 = 221/199,
    20w/(20u) ≥ 2431/1990 > 1.                               (9)

Growth and exact core restoration therefore hold for **every member of X**.
But X is not closed. At u=179, the return is w=221, and the next candidate
middle cofactor is

    (11·221+21s(221))/2=1541=23·67,

which is not divisible by 5 or 199. The entry supplier guard is lost.
Enlarging X merely to retain the alternating core shape does not repair
closure either: exact continuation of this example gives

    3580 → 3980 → 4420 → 6164 → 5260 → 5828 → 4924.

The first two complete core loops grow. The third attempted endpoint 4924
is not divisible by 20. No conclusion about the later orbit is used.

This is where the attempt follows arithmetic beyond the original analogy:
prime divisibility is used to restore the core, not to estimate a control
norm. It succeeds for one return and fails to regenerate its suppliers.

## 5. A further restriction on possible Lyapunov repairs

### Theorem 3 — no fixed-window descent for a power-comparable height

For any fixed integer h≥1, R>1, and cutoff B, there is n>B with

    s^(j+1)(n)>R s^j(n),       0≤j<h.                        (10)

Consequently there is no function V on positive integers, constants
c,C,α>0, fixed h, and finite cutoff such that simultaneously

    c n^α ≤ V(n) ≤ C n^α

for all sufficiently large n and V(s^h(n))≤V(n) for every sufficiently
large source whose first h iterates are positive. This includes a positive
power of n times bounded finite-state weights, and log-height corrections
of the form log V=α log n+O(1).

**Proof of (10).** This is a quantitative variation of the Lenstra supply
chain reproduced in [GLOBAL.md](../../GLOBAL.md), not a new infinite-orbit
construction. Let p_i be the successive primes. Choose t with
∏_(i≤t)(1+1/p_i)>R+1. Choose L=t+h, put a_1=2, and recursively choose
positive exponents satisfying

    p_i^(a_i+1) | σ(p_(i+1)^a_(i+1)),       i<L.              (11)

One explicit choice is, with q=p_(i+1),

    M=p_i^(a_i+1)(q−1),       a_(i+1)=φ(M)−1.

Here gcd(q,M)=1, so Euler's theorem makes M divide q^(a_(i+1)+1)−1;
division by q−1 proves (11). These exponents are positive.

Suppose a number has exact valuations a_i at p_i for i≤l. For each i<l,
the next prime-power factor in (11) makes v_(p_i)(σ(n))≥a_i+1.
Subtracting n leaves valuation exactly a_i. Thus one step retains the
prescribed prefix through l−1. Start with ∏_(i≤L)p_i^a_i, optionally
multiplied by a sufficiently large prime outside that prefix to exceed B.
For the first h sources the first t prime powers are present, hence

    σ(n_j)/n_j ≥ ∏_(i≤t)(1+1/p_i)>R+1.

This proves (10). Each chosen seed has only a finite guaranteed supply chain.

For the height claim choose R with cR^(hα)>C and choose n beyond all cutoffs.
Equation (10) gives

    V(s^h(n)) ≥ c[s^h(n)]^α > cR^(hα)n^α > Cn^α ≥ V(n),

a contradiction. ∎

This does not exclude a proper height with unbounded arithmetic corrections,
seed-dependent waiting times, or a return map. It explains why simply adding
bounded mode weights and testing a longer *fixed* window cannot supply a
universal repair. Lenstra's original arbitrary-length increasing-prefix
result and its relevance to fixed-time descent are already in the repository;
the uniform-amplification version and height consequence here use the same
supply-chain mechanism. No novelty is asserted.

## 6. Results, failed routes, and exact remaining obligation

### Separation of claims

- **Written proofs:** the exact identity (1); Theorem 1 as a comparison
  implication; the explicit leakage threshold; Theorem 2 and its low-input/
  unbounded-output corollary; the growing but nonclosed class X; Theorem 3.
- **Conditional, not established globally:** finite core coverage, bounds on
  η along every used edge, all exits covered by a nonexpansive full-gain graph,
  or indefinite membership in X or a refinement.
- **Finite observations:** the named traces and the bounded scan in section 7.
  Their frequencies are not probabilities for an orbit.
- **Speculation, not a result:** an unbounded arithmetic storage variable might
  account for future cofactor supply bursts, or a variable-time decomposition
  might compensate them. No such variable or compensation law was found.

### Strongest proposals actually tested

| Proposal | Exact failure or disposition |
| --- | --- |
| Apply an ISS theorem directly to size and abundance | No ISS subsystem estimate is verified. Theorem 2's corollary disproves the natural locally bounded cofactor-to-cofactor gain. |
| Exclude periodic affine prime-core schedules | Already Proposition P, not an addition; composite outputs break the affine template. |
| Use 33/40<1 for the 20→4→20 loop | Drops the bη terms. 3580→3980→4420 grows, and Theorem 2 proves unbounded finite amplification on that actual guarded loop. |
| Propagate the small-input threshold η≤1/21 | At p=179, η(p)=1/179, but η(v)=205/995=41/199>1/21. The failure is arbitrarily large, not just a near-threshold exception. |
| Restore the core and thereby regenerate the source class | Core restoration is true; supplier restoration is false. In X, 179 returns to 221, whose next middle cofactor 1541 lacks both suppliers. |
| Enlarge to the bare alternating core shape | The same short trace leaves that shape at 5828→4924. Neither growth nor all exits are controlled by the enlargement. |
| Repair a size height with bounded mode weights or a fixed longer window | Theorem 3 rules out this global class of heights, not all Lyapunov methods. |

### Remaining obligation, without renaming the full conjecture

There is **no surviving closed escape class** from this attempt. For the
specific disproof route, the remaining sufficient obligation is concrete:
find a nonempty present-arithmetic refinement Y⊆X, exhibit u_0 with
20u_0∈Y, and prove that the actual two-step return of every member of Y
again belongs to Y. Growth would then follow from (9), giving escape of
that explicit seed. We attempted Y=X and the prime-entry subclass; both
fail at the witness above. Defining Y by the requirement that all future
returns succeed would not establish this obligation. No suitable refinement
is proposed as if it had been found.

For the proof route, even the restricted question of an escaping tail
alternating unitary cores 20 and 4 with arbitrary composite cofactors is
not settled here. On a guarded return its exact equation is

    v=(11u+21s(u))/2,
    w=(33/40)u+(63/40)s(u)+(7/20)s(v),                         (12)

with gcd(u,20)=1, v odd, and w a positive odd integer not divisible by 5.
One-return descent is equivalent to

    63s(u)+14s(v) ≤ 7u.                                     (13)

Theorem 1 proves it under the stated leakage bounds; Theorem 2 gives
arbitrarily large violations despite exact core return. The divisibility
guards have not yielded a bound on repeated violations or their compensation.
Proving boundedness for all iterates of this particular guarded return would
still address only a restricted itinerary, not all aliquot sequences.
An identity for accumulated gains is not being advertised as a new missing
theorem: bounded accumulated gains would simply be boundedness in other words.

A complete positive solution would need an additional arithmetic resource or
another argument covering arbitrary cores and all excursions. A complete
negative solution would need actual indefinite renewal, not the quantifier
“for every finite G there exists a seed.” Neither has been supplied.

## 7. Evidence and reproducibility

All new files are confined to this approach directory and
`tests/test_small_gain_feedback.py`. There are no site, API, deployment,
shared-note, credential, or dependency changes. No other worktrees, branches,
agents, session transcripts, or shared agent memory were consulted. No
commits, pushes, PRs, merges, or deployments were performed.

### Bounds declared before computation

The exploratory and reproduced scan tests **1≤u≤5000 inclusive**, restricting
to gcd(u,20)=1, and at most **two** aliquot transitions from each 20u.
Thus there are 2000 inputs and first sources at most 100000. Each trial
factorization call has **10000 work units**. The reproduction also enforces
an inclusive **1000000 second-source cap**. A known successor is not subjected
to that cap until it is to be used as a source. No hard orbit is extended.

An additive proper-divisor sieve through **1000000 inclusive** independently
checks both sums for every completed input. The maximum observed second
source was 276444, and the maximum endpoint was 707868. There were **zero
unresolved inputs** and zero arithmetic discrepancies. The program preserves
factorization failures or source-cap stops explicitly in an unresolved list;
a regression deliberately uses a one-unit budget on the four coprime inputs
with 1≤u≤10. All **4 of those 4 inputs are unresolved**, and none is
classified as a successful computation. A second boundary regression uses
the same four inputs with 10000 work units but a second-source cap of 200:
three complete and the input u=9 is explicitly unresolved at its known
successor 366. The completed endpoint 203 is retained even though it exceeds
that source cap.

The first exploratory shell command stopped before running Python because
`pdftotext` was absent. It was rerun without that unrelated prerequisite;
no dependency was installed. Literature HTML was used instead.

### Finite scan observations (not proof premises)

| Quantity | Count |
| --- | ---: |
| Completed two-step inputs | 2000 |
| Actual unitary 20→4→20 blocks | 211 |
| Growing / equal-endpoint / decreasing guarded blocks | 180 / 4 / 27 |
| Growing guarded blocks with prime initial cofactor | 14 |
| Guarded blocks satisfying both η≤1/21 bounds | 21 |

All 21 threshold blocks decrease, as the proof predicts. The first growing
block in this interval is 540→1140→2220, with ratio 37/9. The largest observed
guarded ratio is 2369/297 at 41580→119700→331660. These are bounded observations,
not global extrema or claims about continuation.

The three named traces in `evidence.json` contain **10 transitions total**,
at most six in any one trace. Every named transition is checked both by the
repository's proven trial-factorization sum and by independent divisor-pair
enumeration. The full scan's second algorithm is additive, not factor-based.
All persisted orbit integers and rational components are decimal strings;
counts and explicit small bounds remain JSON integers.

The dedicated tests additionally cover unitary identities for
**1≤D,u≤60 inclusive** (products ≤3600), the nonunitary counterexample,
finite-graph weights including a rejected expansive cycle, the amicable pair,
the exact threshold, the supplier guard, and CRT congruences for
K=13·17·19. That CRT representative is not asserted to be prime.
Two Lenstra supply links with exponents 2,7,8747 are checked by finite
geometric summation/modular exponentiation. No huge supply-chain seed is
constructed or factored.

### Commands actually run

From the repository root, Python **3.12.3**:

```sh
python3 research/approaches/small-gain-feedback/verify.py \
  > research/approaches/small-gain-feedback/evidence.json
python3 -m unittest discover -s tests -p test_small_gain_feedback.py -v
```

**Result: all 9 focused tests passed.** The verifier completed with the zero
unresolved count above. These commands are also the reproduction recipe.
The following additional checks were run after the final edits:

```sh
python3 research/approaches/small-gain-feedback/verify.py \
  > /tmp/small-gain-feedback-evidence.json
cmp /tmp/small-gain-feedback-evidence.json \
  research/approaches/small-gain-feedback/evidence.json
python3 -m py_compile research/approaches/small-gain-feedback/verify.py \
  tests/test_small_gain_feedback.py
python3 -m unittest discover -s tests -p test_small_gain_feedback.py -v
```

Byte-for-byte reproduction, compilation, and the 9 focused tests passed.
They use no new runtime dependencies. Full-suite and browser checks are not
claimed by this report; no commit or browser change is being made.

The independent arithmetic checks share a Python runtime and author. They
are not independent researchers' proof review, a proof assistant, or a test
of Dirichlet's theorem or any infinite assertion.

## 8. Prior work and source scope

1. **Small-gain source:** Sergey Dashkovskiy, Björn S. Rüffer, Fabian R. Wirth,
   *An ISS Small-Gain Theorem for General Networks*, Mathematics of Control,
   Signals, and Systems 19 (2007), 93–122;
   [arXiv:math/0506434](https://arxiv.org/abs/math/0506434),
   [primary HTML](https://arxiv.org/html/math/0506434v1),
   DOI [10.1007/s00498-007-0014-8](https://doi.org/10.1007/s00498-007-0014-8).
   Theorem 4, Corollary 7, and section 4.1 were checked directly. The
   finite-path weighting argument here is derived in full, not attributed
   as a literal application of that continuous-state theorem.
2. **Lenstra benchmark:** P. Erdős, *On Asymptotic Properties of Aliquot
   Sequences*, Mathematics of Computation 30 (1976), 641–645,
   [public paper](https://www.renyi.hu/~p_erdos/1976-22.pdf).
   The Lenstra construction and attribution were checked against GLOBAL.md's
   explicit transcription; the original PDF was not independently re-audited
   during this attempt. Theorem 3 includes the entire argument needed here.
3. **Repository overlap audited:** SYNTHESIS.md, README.md, LITERATURE.md,
   FOUR-ADIC.md (J and denominator depletion), GLOBAL.md (finite supply chains
   and fixed-support limits), BLOCK-TRANSPORT.md (composite corrections), and
   RECOVERY.md (O, P, Q, failed renewal, and deficiency margins). The initial
   affine-template idea is already P; the graph method overlaps Q; the
   amplification proof deliberately adapts O. The 20→4→20 restoration with
   subunit bare gain and its common leakage threshold are specific outputs
   of this attempt relative to those notes, not claims of historical novelty.
4. **Imported arithmetic:** Dirichlet's theorem in Theorem 2; Euler's theorem
   modulo an integer in Theorem 3; classical prime-product divergence as
   explained in Theorem 2. No probabilistic prime model or prime-tuples
   conjecture is used. No broader exhaustive bibliographic novelty search
   was performed, so historical priority is explicitly unassessed.

For reproducibility of the public-source access, the abstract and primary
HTML were retrieved with bounded `curl -L --fail --max-time` requests and
converted to plain text with Python's standard-library `html.parser`.
Only the sections identified above, not every proof in that paper, were read.

## 9. Fruitfulness assessment

**Not useful toward a resolution in this attempt.** The bridge does produce
an exact composite-aware comparison theorem and a sharp algebraic threshold
for a particular graph. It also produces a rigorous arbitrarily amplifying
block around a bare-contracting *chosen* core cycle and identifies exactly
why the natural gain estimate and supplier renewal fail. The constructed
middle term retains a 20-core as well, so this is not a new driver-restoration
mechanism.

Those are scoped arithmetic and applicability results. They provide neither
a new bound for an unrestricted orbit nor a seed with a closed escape
mechanism. The finite amplification is an adaptation of known tools, and the
initial prime-template route was already in the repository. A restricted
obstruction, an attractive control interpretation, and passing regressions
are not being counted as progress to a proof or disproof.

**The Catalan–Dickson conjecture remains unresolved by this work.**
