# 13. Boundary outflow: exits, returns, and the same-seed requirement

**Outcome:** almost all immediate exits reach any fixed multiple of the fence
before returning or cycling in the intervening band, as the fence grows. This
first-passage deduction uses the valid Erdős small-prime persistence lemma and
Davenport's abundancy distribution. It is stronger than merely staying outside
for a fixed time, but does not force escape: the successful starts can change
at every scale. Counting all incoming edges is a different quantity: even after
removing the infinitely many prime-to-1 edges, incoming semiprime sources
eventually outnumber all possible outgoing sources.

The useful replacement is labelled-seed accounting and control of eventual
returns or outside cycles. No such whole-orbit control, divergent seed,
resolution, or historical novelty is claimed. This is a bounded mathematical
follow-up to [note 12](ANCESTRY-BARRIER.md), not another large census.

## 1. Plain-language dictionary

Imagine a **fence at B**. Numbers from 0 through B are inside; larger numbers
are outside. For example, with the fence at 15:

```text
12 -> 16 -> 15 -> 9 -> 4 -> 3 -> 1 -> 0
      outside   back inside
```

The first arrow leaves the fence; the second returns. This sequence terminates.

| Name | Symbol | Read it as |
| --- | --- | --- |
| Next number | s(n) | Add the proper positive divisors of n. |
| Fence | B | The largest number we call inside. |
| Immediate exits | Out(B) | How many starts 1 through B step outside immediately? |
| Observation horizon | h | How many arrows from the starting value we follow. |
| Returned by then | Back(B,h) | How many of those exit starts have come back inside by step h? |
| Cycled outside | Cycle(B,h) | How many have repeated an outside value before returning, by step h? |
| Still open | Open(B,h) | How many have done neither within those h steps? |

These counts refer to the **same exit starts**. Merging paths retain their
starting labels. A return closes this excursion, not necessarily the entire
orbit. “Still open” means an exactly computed finite prefix, not an escaping
orbit. A computational budget failure is separately unresolved and must not be
silently counted as a verified prefix.

In formulas, `#` means “how many,” `<=` means “at most,” and s^j(n) means
“apply the next-number rule j times,” **not** raise s(n) to a power. Floor
brackets mean round down. Zero is terminal; s(0) remains undefined.

## 2. What immediate outflow already proves

Let the set of immediate exit starts be

\[
 E_B=\{1\le n\le B:s(n)>B\},\qquad
 \operatorname{Out}(B)=|E_B|.
\]

For n=12t, the five distinct proper divisors t,2t,3t,4t,6t sum to 16t.
Consequently every multiple of 12 between 3B/4 and B steps above B, and

\[
 \operatorname{Out}(B)\ge
 \lfloor B/12\rfloor-\lfloor B/16\rfloor.                 \tag{1}
\]

For a large fence this is roughly B/48 guaranteed exits: a little over 2% of
all the starts inside. At B=1000 the guaranteed count is 21; the actual count
is 65. The floor formula is exact; the percentage is an asymptotic description.
This is the existing elementary argument from note 12, not a new growth theorem.

If outgoing edges from all positive sources through B are compared with
incoming edges restricted to sources *and* targets through B (including target
0), the proposed ratio is simply

\[
 \frac{B}{B-\operatorname{Out}(B)}.
\]

It measures the one-step leak from the window. Counting the same collection
of edges at both ends instead always gives equal totals.

## 3. A stronger deduction: almost no exits return quickly

For each h>=1, partition E_B by the first observed event: return inside,
repeat outside before any return, or neither event through step h. This gives

\[
 \operatorname{Out}(B)=\operatorname{Back}(B,h)
  +\operatorname{Cycle}(B,h)+\operatorname{Open}(B,h).       \tag{2}
\]

Let e_h(B) count abundant starts n<=B whose first h steps are **not strictly
increasing**. A terminated prefix fails this condition. The valid classical
input, with its provenance and limitations audited in
[note 12, section 1](ANCESTRY-BARRIER.md#1-definitions-and-the-surviving-classical-input),
is

\[
 e_h(B)/B\longrightarrow0\quad\text{for each fixed }h.     \tag{3}
\]

This imports the established abundant-growth result, not Erdős's withdrawn
general decreasing-iterate assertion. No effective rate in h or B is supplied.

**Excursion corollary.** For every B,h>=1,

\[
 \operatorname{Back}(B,h)+\operatorname{Cycle}(B,h)
 \le e_h(B).                                             \tag{4}
\]

**Proof.** Every immediate exit start is abundant: s(n)>B>=n. If its first
h steps strictly increase, every term after the first remains above B and no
value repeats. Thus either of the two closing events requires failure of that
strict-growth prefix. Charge each event to its own starting seed; there is no
assumption that different paths remain disjoint. Equation (4) follows. ∎

Combining (1), (3), and (4) gives

\[
 \frac{\operatorname{Open}(B,h)}{\operatorname{Out}(B)}
 \longrightarrow1\qquad\text{for each fixed }h.            \tag{5}
\]

**In words:** choose the number of steps first. As the fence becomes large,
almost all immediate exits are still outside and unrepeated after that many
steps. This is a consequence of an existing theorem, not an extrapolation
from the small table below.

### Why this still permits universal termination or cycling

For a *fixed fence*, there are only finitely many immediate exit starts. If
every one eventually terminates or cycles, each either returns inside or
repeats outside after some finite time. Waiting long enough therefore gives
Open(B,h)=0. There need be no waiting time that works uniformly as B grows.

Both of these can therefore be true:

```text
Fix a viewing time, then enlarge the fence: almost all exits still look open.
Fix a fence, then wait sufficiently long: every exit closes.
```

The all-cyclic sparse-funnel countermodel in
[note 12, section 6](ANCESTRY-BARRIER.md#6-two-logical-countermodels-why-the-quantifiers-do-not-prove-escape)
exhibits this compatibility. It is not an aliquot map. No exchange of these
two limiting operations is justified by (3) or (5).

## 4. A stronger attack: reach the next fence before coming back

Put a second fence at twice the first: B and 2B. Follow an immediate exit until
one of three things happens:

1. It reaches above 2B: **this stage succeeds**.
2. It returns to at most B: **this excursion returns**.
3. It repeats while between B and 2B: **it is cycling in the band**.

Every stage ends after finitely many steps, because the band contains only
finitely many integers. Reaching the second fence is not an escaping orbit;
it may come back later or enter a cycle above that fence.

**Fixed-scale first-passage corollary.** For any fixed real number lambda>1,
let Fail_lambda(B) count exit starts that return to at most B or cycle in
(B,lambda B] *before* reaching above lambda B. Then

\[
 \frac{\operatorname{Fail}_{\lambda}(B)}{B}\longrightarrow0,
 \qquad
 \frac{\operatorname{Out}(B)-\operatorname{Fail}_{\lambda}(B)}
      {\operatorname{Out}(B)}\longrightarrow1.             \tag{FP}
\]

**In words:** for a sufficiently large fence, almost every immediate exit
reaches the next doubled fence before coming back. The same holds for any
other fixed enlargement factor. No effective threshold or convergence rate
is asserted. The proof's waiting time depends on the allowed exceptional
fraction as well as the enlargement factor; it does not assert one fixed
passage horizon with only o(B) failures.

### Proof with the order of choices explicit

Write A(n)=sigma(n)/n for abundancy, and d_L(n) for the full prime-power part
of n supported on primes at most L. These auxiliary symbols are used only in
this proof. Fix lambda>1 and any error allowance epsilon>0.

1. By continuity of Davenport's limiting abundancy distribution, choose a
   fixed delta>0 so the abundant numbers with 2<A(n)<=2+2delta have density
   less than epsilon/3. This excludes a narrow band of barely abundant starts.
2. Choose a fixed L large enough that 1/(L delta)<epsilon/3. The elementary
   reciprocal-divisor bound used in note 12 gives

   \[
   \frac1B\sum_{n\le B}[A(n)-A(d_L(n))]
      \le\sum_{d>L}\frac1{d^2}\le\frac1L.                \tag{Tail}
   \]

   Indeed every divisor not supported on primes at most L exceeds L. Thus
   at most B/(L delta) starts have A(n)-A(d_L(n))>delta. Outside these two
   exceptional sets, an abundant n has A(d_L(n))>2+delta.
3. Choose a fixed integer H with (1+delta)^(H-1)>lambda. Erdős's valid
   small-prime persistence lemma keeps d_L(n) dividing each of the first H
   iterates for all but o(B) initial n. Both L and H are fixed **before**
   taking B to infinity. The lemma is quoted and audited in note 12; no
   decreasing-iterate estimate or exceptional-set inverse-image bound is used.
4. If d divides m, then A(m)>=A(d), by the prime-power product formula.
   Consequently every guarded step grows by a factor greater than 1+delta.
   After an immediate exit above B, the path reaches above lambda B by step H,
   with neither a return nor a repetition on the way.

Failures therefore number at most 2epsilon B/3+o(B). Since epsilon was arbitrary,
Fail_lambda(B)/B tends to zero. The exit lower bound (1) gives the second limit
in (FP). ∎

This is a deduction from the same classical inputs as note 12, not a claimed
new theorem of historical significance. The full 1976 paper was reinspected;
only Lemma 2 and the elementary lower-growth resources are used. Its withdrawn
upper/decreasing assertions and unquantified growing-depth remarks are not.

### Why stage successes cannot simply be multiplied

The next stage's travellers are **not a fresh sample of starts through 2B**.
They are selected descendants of the previous stage, may overshoot the next
fence immediately, and may carry many merged labels. A density-zero bad set
could contain every one of those selected descendants. Neither independence
nor a bound on their labelled losses follows from (FP).

Thus the stronger result supplies large excursions, not an infinitely
repeatable journey. The sparse-funnel countermodel from note 12 likewise
succeeds across every fixed scale for almost all exit starts while every orbit
eventually cycles.

## 5. Counting all incoming edges goes in the opposite direction

If every positive target inside the fence is allowed, infinitely many outside
primes point to 1. Remove that exceptional target and define instead

\[
 \operatorname{In}_{\ge2}(B)
 =\#\{m>B:2\le s(m)\le B\}.
\]

This count is finite. Such a source m must be composite. If p is its least
prime divisor, m/p>=sqrt(m) is a proper divisor distinct from 1, so
s(m)>=1+sqrt(m). Therefore

\[
 m\le(B-1)^2.                                            \tag{6}
\]

Nevertheless the incoming count eventually exceeds B by an arbitrarily large
factor. Let P be the number of primes at most floor((B-1)/2). Every pair of
distinct such primes p<q gives a different source pq with

\[
 s(pq)=p+q+1\le B.
\]

There are P(P-1)/2 such sources, and at most B of them are inside the fence.
Hence the exact lower bound

\[
 \operatorname{In}_{\ge2}(B)\ge P(P-1)/2-B.                \tag{7}
\]

The standard prime number theorem, P asymptotic to B/(2 log B), makes the
right side grow like B^2/(8(log B)^2), which eventually dominates B. Since
Out(B)<=B, the all-source outflow/inflow ratio tends to zero even without
prime-to-1 edges. The prime number theorem is an imported classical input;
the finite arithmetic inequality (7) does not depend on it.

This does **not** prove that every outgoing path returns. Most of these
incoming sources need not lie on any of the outgoing paths. Global inflow is
not matched returning traffic. Reversing the ratio does not fix the inference.

## 6. Conservation works only when starting labels are retained

Choose a finite collection of starts inside a fixed fence. Put one labelled
token on each start and follow each token along its own orbit. If two orbits
merge, the shared value carries both tokens; neither label disappears.

For any finite observed prefix of one token's path,

\[
 \text{number of outward crossings}
 -\text{number of inward crossings}
 =\begin{cases}1&\text{last observed value is outside},\\
                0&\text{last observed value is inside}.
   \end{cases}                                          \tag{8}
\]

The proof telescopes the indicator “currently outside” over consecutive
edges. Sum (8) over the same starting labels for an exact cohort balance. A
path stops at 0; no value for s(0) is required.

An actual aliquot merger illustrates the difference from unique-edge counts.
At fence 174:

```text
126 --\
       186 -> 198 -> 270 -> 450 -> 759 -> 393 -> 135
174 --/                                           back inside
```

There are two different exit edges but only one *distinct* return edge,
393->135. Both starting labels return across that same edge. Two exits versus
one return edge therefore does not force any escaping orbit.

Even a token that stays outside forever might be in a cycle above the fence.
The elementary toy map “double odd numbers; fix even numbers” has
3->6->6 above fence 5. Permanent residence outside one fence is not escape.

## 7. The precise remaining target

For a fixed B, the still-open seed sets decrease with h. Their intersection
consists exactly of immediate exit starts that never return and never repeat.
Any such orbit has infinitely many distinct positive integer values and thus
eventually leaves every finite range: it escapes.

Conversely, an escaping orbit starting inside a fence has a **last** visit
inside. That visit supplies an immediate exit start in the intersection.
Thus controlling eventual excursions is a correct reformulation, but defining
the intersection does not show it contains anything.

A useful way to prevent the moving-seed error is to choose a **fixed finite
cohort** before raising any fences. If that same cohort can be proved to reach
arbitrarily high fences, at least one of its seeds escapes. Otherwise every
seed in this finite cohort has a finite peak, and the maximum of those peaks
bounds the whole cohort. Outside cycles are automatically excluded by the
arbitrarily-high-fence requirement.

This criterion is elementary bookkeeping, not a new arithmetic mechanism.
We have **not** proved it for any fixed cohort. A successful continuation needs
an arithmetic bound on eventual return/cycle losses, or a repeatable,
forward-compatible mechanism linking the same seed to higher fences. A new
snapshot population at each fence, or a longer fixed observation time, does
not supply that missing condition.

One sufficient certificate would start with a finite cohort of immediate
exit starts at B_0, placing each label at its first successor. Track those same
labels through fences B_0, 2B_0, 4B_0, and so on. A label already above a stage's
higher fence passes
that stage immediately; otherwise follow it within the finite band until it
passes, returns below the lower fence, or repeats. Permanently discard labels
at the latter two events. If independently proved arithmetic bounds a_j on the
newly discarded labels satisfy sum_j a_j < the initial number of labels, at
least one survives all stages and escapes. This is a conditional criterion,
not a bound we have obtained. The fresh-start estimate (FP) does not furnish
these a_j, and defining them through assumed future survival would be circular.

## 8. Small exact regressions, separate from the asymptotic argument

[`tests/test_boundary_outflow.py`](../tests/test_boundary_outflow.py) reproduces
this deliberately small table. Steps include the initial outward step.

| Fence B | Immediate exits | Steps h | Returned | Cycled outside | Still open |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 15 | 1 | 2 | 1 | 0 | 0 |
| 100 | 7 | 2 | 3 | 0 | 4 |
| 100 | 7 | 4 | 5 | 0 | 2 |
| 1000 | 65 | 2 | 10 | 0 | 55 |
| 1000 | 65 | 4 | 22 | 0 | 43 |

These are exact finite excursion classifications, not forecasts of ultimate
fate. The orbit regressions use seeds through 1000, depths through 4, and a
positive-source cap of 100000. Named example paths are checked separately.
An independent divisor-pair sum checks every evaluated aliquot edge.

The finite-band test resolves the whole *stage*, rather than imposing a short
observation time:

| First fence B | Reached above 2B first | Returned first | Cycled in band | Maximum steps to decide |
| ---: | ---: | ---: | ---: | ---: |
| 15 | 0 | 1 | 0 | 2 |
| 100 | 3 | 4 | 0 | 5 |
| 1000 | 43 | 22 | 0 | 8 |

Every evaluated source in this stage test is at most 2B<=2000; an overshooting
target is accepted exactly without iterating it. The band has B possible
values, so at most B+1 steps from an exit start suffice to decide the stage.
No factorization or source-cap failure occurred. Reaching 2B in this table
says nothing about the subsequent fate of those paths, and these small fences
do not estimate the asymptotic failure rate in (FP).

The nine regressions also check (4), label conservation, merged return edges,
an outside cycle, the inverse-source ceiling, and the semiprime bound with
primes through 499 and product sources below 250000. No new research CLI,
persisted large census, or extension of unresolved Lehmer orbits is included.

The proofs, imported theorems, and finite regressions have different roles.
Passing tests cannot establish either an asymptotic theorem or an infinite
orbit. Two read-only AI analyses agreed on the fixed-time and fixed-scale
arguments and their noncomposition limitation. Their initial proposed next
steps differed: an effective growing time horizon versus fixed-scale first
passage. After auditing the latter proof they agreed to include it, while
leaving an effective rate and the optional one-step density integral out of
scope. That agreement is not independent human review or formal certification;
human mathematical review and historical novelty checking remain outstanding.
