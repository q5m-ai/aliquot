# 14. A maximum-based contradiction attempt

**Outcome:** assuming every aliquot orbit is bounded gives a genuine maximum
for each orbit and for each fixed finite collection of seeds. We tried to
contradict that maximum using abundance, guaranteed recovery after a decrease,
and closure of a finite collection. The first two exclude specified arithmetic
families of possible maxima. The closure argument fails: orbit sets need not
contain smaller integers, or even the orbits of their divisors.

A useful exact obstruction emerges: no initial integer interval through B is
forward-closed once B >= 24, although the entire cohort of seeds 1 through 24
has a finite forward closure with maximum 55. Thus an indefinitely expanding
*interval enclosure* is not evidence of an escaping orbit. No contradiction,
divergent seed, proof/disproof, or historical novelty is claimed.

The [return-closure follow-up](RETURN-CLOSURE.md) attempts to supply the missing
renewal step. It obtains a finite-relay construction and a progression-wide
obstruction to uniformly bounded returns, but still no infinite closure.

Throughout, s(n) = sigma(n) - n for positive n. Stop at 0; s(0) is undefined.
Here “acyclic” means an infinite orbit with no repeated positive value, not a
finite path to 0. Such an infinite orbit tends to infinity: each finite set of
integers can be visited only finitely often. The hypothesis we try to refute is
exactly the Catalan–Dickson conjecture, not a uniform bound on all seeds.

## 1. Start with a legitimate maximum

Assume every orbit terminates or eventually cycles. Let O(n) be the set of
values visited from n, including terminal 0 when reached. Then

\[
 H(n)=\max O(n)
\]

exists. It depends on n, and H(n) >= n. If s(n) > 0, determinism gives

\[
 H(n)=\max\{n,H(s(n))\}.
\]

For n = 1, H(1) = 1 directly; no value of H(0) or s(0) is needed.

Take any seed and put M = H(n). Because M itself occurs on the orbit,

\[
 s(M)\le M,\qquad O(M)\subseteq O(n),\qquad H(M)=M.       \tag{1}
\]

Thus M is deficient or perfect. A successful contradiction would find a
reason that this *same orbit* must eventually exceed M. Merely exhibiting a
different seed whose peak is larger does not violate (1).

The assumption is stronger than needed to discuss one verified bounded orbit;
the statements below about its maximum apply independently to that orbit.

## 2. First attack: rule out an abundant maximum

Every proper multiple of a perfect number is abundant. Indeed, if D is perfect
and n = Du with u > 1, the scaled proper divisors ud, for d a proper divisor of
D, are distinct proper divisors of n summing to u s(D) = n. The additional
proper divisor 1 is distinct from them. Hence s(n) > n.

In particular, a maximum M > 6 cannot be divisible by 6. This would immediately
contradict (1) if we could prove that some orbit stays among multiples of 6
larger than 6 forever.

But that condition is not preserved. An exact terminating example is

```text
30 -> 42 -> 54 -> 66 -> 78 -> 90 -> 144 -> 259
   -> 45 -> 33 -> 15 -> 9 -> 4 -> 3 -> 1 -> 0.
```

The peak 259 is deficient and is not divisible by 6. The attempted contradiction
stops exactly when the growing class is lost. The exact exit classification in
[note 01](README.md#2-a-growing-class-with-an-exact-exit-criterion) narrows the
possible exits but does not prove that an orbit avoids them forever.

## 3. Second attack: a decrease need not permit a maximum

We can exclude some deficient candidates as well, by proving that they rebound
above their starting value. This uses the already established mechanism in
[note 07](RECOVERY.md#2-a-guaranteed-loss-followed-by-a-more-than-compensating-rebound),
not a new unbounded-orbit construction.

**Two-step peak exclusion.** If q is prime and q = 51 modulo 160, then
M = 4q cannot be the global maximum of any orbit containing it.

**Proof.** Such a positive prime q is greater than 7 and coprime to 4. Therefore

\[
 s(M)=s(4q)=3q+7<M,\qquad 160\mid(3q+7).
\]

For any d dividing m, scaling the proper divisors of d gives
s(m)/m >= s(d)/d. As s(160) = 218, it follows that

\[
 s^2(M)\ge\frac{109}{80}(3q+7)
          >\frac{327}{320}M>M.                           \tag{2}
\]

Here s^2 is composition. The first inequality requires only divisibility,
not coprimality of 160 and the complementary factor. Equation (2) contradicts
M being the maximum. This proves the exclusion. ∎

For example, q = 211 gives

```text
844 -> 640 -> 890.
```

So a first downward step cannot certify the peak. However, the new value 890
is outside the 4q input family, and its complete continuation is

```text
890 -> 730 -> 602 -> 454 -> 230 -> 202 -> 104
    -> 106 -> 56 -> 64 -> 63 -> 41 -> 1 -> 0.
```

The actual peak is 890. Applying the maximum argument just moves us to a
candidate that this exclusion does not cover. Proving one profitable recovery,
or arbitrarily large finite recoveries with varying seeds, does not supply
perpetual recovery on one orbit.

Even a prime can be the maximum of an orbit starting abundantly:

```text
784 -> 983 -> 1 -> 0.
```

Here 784 = 2^4 * 7^2, so s(784) = 31 * 57 - 784 = 983, which is prime.
Thus “an abundant start cannot end its growth at a prime” is not a valid repair.

## 4. Third attack: use one maximum for a fixed finite cohort

The uniform-bound idea does become valid for a *fixed finite nonempty* set F of seeds.
Under the assumption,

\[
 S_F=\bigcup_{n\in F}O(n),\qquad B_F=\max S_F
\]

are finite. Every positive x in S_F has s(x) in S_F. Consequently, if we could
find a visited x with s(x) > B_F, we would have a contradiction.

A tempting replacement is to find **any** x <= B_F with s(x) > B_F. That is
possible for every sufficiently large B_F, by the following elementary lemma.
But it does not ensure that x is visited.

### Exact obstruction to an interval enclosure

**Lemma.** For every integer B >= 24, some positive x <= B satisfies s(x) > B.
Equivalently, the interval {0, ..., B} is not forward-closed at its positive
sources.

**Proof.** For 24 <= B <= 35, take x = 24, since s(24) = 36.

For B >= 36, write B = 12q + r with q >= 3 and 0 <= r <= 11. Set x = 12q.
The five distinct proper divisors q, 2q, 3q, 4q, 6q give

\[
 s(x)\ge16q=12q+4q\ge12q+12>B.
\]

In both cases x <= B. ∎

Direct verification below 24 shows that the positive endpoints of all closed
initial intervals are exactly

\[
 B\in\{1,2,\ldots,11,16,17,22,23\}.                     \tag{3}
\]

The lemma proves the unbounded part of this classification; a finite test alone
does not do so. Zero is included as a terminal target, not an evaluated source.

### Why this still does not contradict boundedness

The entire cohort F = {1, ..., 24} has the exact finite closure

\[
 S_F=\{0,1,\ldots,24\}\cup\{36,55\}.
\]

Indeed all positive sources through 24 have successors in that set, and the
only added sources satisfy

```text
24 -> 36 -> 55 -> 17 -> 1 -> 0.
```

Every element listed is either an initial seed or a visited value. The maximum
is 55. Although

```text
48 < 55,       s(48) = 76 > 55,
```

48 is **not in S_F**. Adjoining its orbit enlarges the cohort; it does not
extend any old orbit. Filling every gap up to each new maximum can repeat
forever without contradicting finite closure of the original cohort.

More formally, define the interval-enclosure iteration

\[
 B_{j+1}=\max\bigl(B_j,\max_{1\le x\le B_j}s(x)\bigr).
\]

For B_0 >= 24 the lemma gives B_{j+1} > B_j at every stage, hence B_j tends
to infinity. This is a proved divergence of an *enclosure algorithm*, not of
an aliquot orbit. It already happens for the fully resolved cohort through 24.

### Divisor closure does not rescue the argument

One might instead try adjoining only divisors of visited numbers. But their
future orbit maxima need not lie below the original peak. Exact complete
orbits give

```text
30 -> 42 -> 54 -> 66 -> 78 -> 90 -> 144 -> 259 -> ... -> 0
60 -> 108 -> 172 -> 136 -> 134 -> 70 -> 74 -> 40 -> 50 -> 43 -> 1 -> 0.
```

Although 30 divides 60,

\[
 H(30)=259>172=H(60).
\]

The valid one-step inequality s(60) >= 2 s(30) cannot be iterated as a
divisibility relation: the successors need not divide one another. Therefore
H is not even monotone under divisibility, let alone under numerical order.

## 5. Where the contradiction attempt stops

We have ruled out abundant peaks and a concrete family of deficient peaks.
We have also shown exactly why forcing an interval bound to expand is not a
substitute for forcing a fixed orbit to expand.

A sufficient next lemma would be an arithmetically specified nonempty class X
such that every n in X has a later **actual** iterate R(n) in X with R(n) > n.
Under the boundedness assumption, take the largest member of X visited by an
orbit starting in X. Its promised larger return contradicts maximality. The
intermediate terms need not grow, and return times need not be uniform.

This is a conditional certificate, not a result obtained here. The explicit
class X = {4q : q prime, q = 51 modulo 160} proves growth after two steps, but
844 -> 640 -> 890 shows that its endpoint is not in X. The complete displayed
orbit has no later larger member of X either, so this example refutes the
proposed return property for that class. The class of proper multiples of 6
fails closure as well.

Alternatively, prove that one fixed finite cohort reaches arbitrarily large
values. Its finite maximum under the assumption would give a contradiction;
this is the same-seed/cohort condition in
[note 13](BOUNDARY-OUTFLOW.md#7-the-precise-remaining-target). We have not proved
it for any cohort. Merely excluding more local peak shapes does not establish
it, because every possible maximum on the chosen orbit must be addressed.

**Verdict:** this is a genuine extremal proof attempt with rigorous exclusions
and explicit failed repairs, but it does not refute universal boundedness.
The remaining gap is arithmetic control of successive visited states, not the
existence of a maximum for a finite collection.

## 6. Verification and scope

[`tests/test_maximum_contradiction.py`](../tests/test_maximum_contradiction.py)
checks the finite claims separately from the written proofs:

- all named orbit edges, stopping at 0 or the first repeat, with at most 100
  transitions; the named paths have positive sources below 1000;
- the exact closure of seeds 1 through 24 and its missing witness 48;
- interval endpoints and the explicit witness construction through B = 1000;
- the two-step exclusion for every prime q = 51 modulo 160 through q = 10000;
  all evaluated positive sources are at most 40000;
- rational inequalities by integer cross-multiplication, without floating point;
- explicit rejection of an exceeded source/step budget, never classification as
  termination, cycling, or divergence.

Each evaluated aliquot sum is obtained by the repository's exact trial-division
factorization and independently checked by summing divisor pairs through the
integer square root. These are regression checks, not independent mathematical
peer review or proof of universal behavior. No probable-prime shortcut is used,
and no site or deployment changes are part of this attempt.

Reproduce the focused checks with

```sh
python3 -m unittest discover -s tests -p 'test_maximum_contradiction.py' -v
```

Validation completed for this change: the nine focused tests passed; both
`python3 -m unittest discover -s tests -v` and `npm test` passed all 294 tests.
`node --check` passed for `site/explorer.js`, `site/math.js`, and `site/latex.js`.
These checks validate the finite arithmetic and repository regressions, not a
resolution of the conjecture.
