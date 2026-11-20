# Error-correcting syndromes and aliquot dynamics

## 1. Verdict and scope

**Unresolved. No candidate proof or disproof of the Catalan–Dickson conjecture
is obtained.** In particular, no starting integer is certified to escape.
The universal partial statements below have written proofs, not independent
mathematical review or formal verification.

The principal output is a precise limitation of finite arithmetic syndromes:

1. **Real source collisions:** any realized finite residue information about
   `n, sigma(n), s(n)`, even with finitely many specified valuations of positive
   coordinates, is compatible with arbitrarily large abundancy. A constructive
   proof is below.
2. **A local-to-global gap for trajectories:** there is a complete criterion
   for an affine prime-cofactor model to survive every fixed finite prime
   sieve. The actual 120-core model satisfies it, although an infinite
   prime-cofactor trajectory in that model is impossible.
3. **The attempted composite repair fails:** a two-prime obstruction is real,
   but `637=7^2*13` evades it. Composite defects are not a monotone resource.

These are restrictions on a proposed method, not new restrictions ruling out
all escaping aliquot orbits. The report separates actual integer statements,
formal trajectories, conditional prime-tuples statements, and computations.

### Work order and overlap audit

Before reading `research/SYNTHESIS.md`, I developed the cofactor syndrome,
its rational-affine prime recurrence, and a fixed-prime-support S-unit route.
The subsequent comparison showed that both proposed orbit obstructions were
already established here:

- [GLOBAL.md, K](../../GLOBAL.md): fixed-support adjacent-pair finiteness,
  with minimal vanishing subsums handling S-unit degeneracy;
- [RECOVERY.md, P](../../RECOVERY.md): periodic schedules of arbitrary fixed
  cores and coprime prime cofactors cannot escape;
- [FOUR-ADIC.md, J](../../FOUR-ADIC.md): arbitrary switching among finitely
  many multiperfect cores cannot give an infinite prime-cofactor orbit.

They are **not additions of this attempt**. I then pursued what their adaptive
arithmetic checks cannot be replaced by: finite syndromes, and correction of
composite-cofactor errors. The general source-collision construction and the
exact affine sieve criterion are not stated in the consulted source notes.
That is a repository comparison, **not a claim of historical novelty**.

Throughout, `sigma(n)` is the positive-divisor sum, `s(n)=sigma(n)-n` for
`n>=1`, `s(1)=0`, and `s(0)` is undefined. Write `I(n)=sigma(n)/n`.
An infinite nonperiodic aliquot orbit has distinct terms and tends to infinity;
none of the arguments silently substitutes monotone growth for this fact.

## 2. A concrete bridge, and what coding theory actually supplies

### 2.1 The source theorem and its missing hypotheses

For a linear code `C=ker(H)` over a finite field, receiving `y=c+e` gives
syndrome `Hy=He`. Correction of every error in a specified set `E` requires
that `e -> He` be injective on `E`. For example, correcting every error of
Hamming weight at most `t` is possible when the code's minimum distance is at
least `2t+1`. For binary single errors, the check-matrix columns must be
nonzero and pairwise distinct. These are distinguishability conditions, not
a general assertion that a few checks reconstruct an unrestricted message.

In aliquot dynamics a natural finite signature is

```
X_M(n) = (n mod M, sigma(n) mod M).
```

It determines `s(n) mod M` but not `sigma(s(n)) mod M`. Several fixed moduli
can be replaced by their least common multiple. The equation
`next + current - sigma(current) = 0` is an exact linear consistency check on
three integers, but `sigma(current)` is a nonlinear arithmetic constraint.
We have not produced a linear code of valid aliquot trajectories with a
minimum-distance bound. Nor is there a bound on the number or size of the
prime-factor changes at a step.

The proposed error model becomes exact after choosing a coprime core.

### 2.2 Exact cofactor syndrome

Let `c>=1`, `q>=1`, and `gcd(c,q)=1`. Multiplicativity gives

```
s(cq) = s(c) q + sigma(c) s(q),                       (1)
c s(cq) - s(c) (cq) = c sigma(c) s(q).                (2)
```

For `q>1`, put `delta(q)=s(q)-1`. Then

```
s(cq) = s(c) q + sigma(c) + sigma(c) delta(q).        (3)
```

Here `delta(q)>=0`, with equality exactly when `q` is prime. Thus the exact
residual in (3) detects failure of the prime-cofactor model. If `q` is
composite, a proper divisor at least `sqrt(q)`, together with 1, gives
`delta(q)>=sqrt(q)`. This is not a bounded-magnitude noise model.

Equations (1)–(3) are proved by expanding
`(c+s(c))(q+s(q))-cq`. The assertion `s(q)=1 iff q is prime`, for `q>1`,
follows directly from the proper divisors. The case `q=1` is separate:
`s(q)=0`, not 1; assigning it a prime defect would give `delta(1)=-1`.

**What is gained:** an exact residual, a tested coprimality hypothesis, and an
explicit correction term. **What is not gained:** a cheaper way to compute
`s`, a decoder locating arbitrary changed factors, or an orbit invariant.
Even the exact values `s(39)=s(55)=17` show that this scalar residual does not
locate an unrestricted composite cofactor. Modular residuals lose more
information, as the next theorem demonstrates.

The coprimality guard cannot be dropped. For example,
`s(6*9)=66`, not `6*9+12*s(9)=102`. The same failure occurs later in the
120-core witness below. The defect notation and related composite correction
identities are already present in [BLOCK-TRANSPORT.md](../../BLOCK-TRANSPORT.md)
and [RECOVERY.md](../../RECOVERY.md).

## 3. Proved result A: invisible multiplicative perturbations

### Statement

Fix an integer `n>=1`, a modulus `M>=1`, a finite set `S` of primes, and a real
number `H>0`. There exists an integer `C>1` such that

- `gcd(C,n)=1`, and no prime in `S` divides `C`;
- `C == sigma(C) == 1 (mod M)`;
- `v_l(nC)=v_l(n)` and `v_l(sigma(nC))=v_l(sigma(n))` for every `l in S`;
- `I(nC)>H`.

Consequently `X_M(nC)=X_M(n)`, and their first successors also agree modulo
`M`. If `n>1`, any specified finite set of valuations of the first successor
can be preserved as well, by increasing the auxiliary modulus in the proof.
This is an assertion about **actual integers and actual divisor sums**.

### Proof

Choose `L` divisible by `M` and by every prime in `S`. Set
`E=L*phi(L)`, with `phi(1)=1`. For any prime `r` not dividing `nL`, Euler's
theorem and a division of the sum into `L` blocks of length `phi(L)` give

```
r^E == 1 (mod L),
sigma(r^E) = 1 + sum_(j=1)^E r^j == 1 (mod L).       (4)
```

Indeed, each block has the same residue, and `L` times that residue vanishes
modulo `L`. The assertions modulo 1 are automatic.

Take `C` to be the product of `r^E` over the primes `r<=X` not dividing `nL`.
The factors are pairwise coprime, so (4) gives
`C == sigma(C) == 1 (mod L)`. Also `C` is coprime to `nL`. This proves the
congruences and the two valuation assertions, using
`sigma(nC)=sigma(n)sigma(C)`.

The abundancy of these products is unbounded. In fact,

```
I(C) = product_(r<=X, r not dividing nL) (1+1/r+...+1/r^E)
     >= product_(r<=X, r not dividing nL) (1+1/r) -> infinity.
```

Here is an elementary justification of the last divergence. The finite Euler
product `product_(r<=X)(1-1/r)^(-1)` includes every reciprocal `1/m` with
`m<=X` in its expansion, so is at least the corresponding harmonic sum.
Also `product_(r<=X)(1-1/r^2)>=1/2`: the product over all integers
`2<=m<=floor(X)` is `(floor(X)+1)/(2 floor(X))`. Thus
`product_(r<=X)(1+1/r)` is at least half that harmonic sum. Removing finitely
many primes changes this by only a bounded positive factor. Since
`I(nC)=I(n)I(C)`, choose `X` sufficiently large to exceed `H`.

Finally, if `n>1`, then `s(n)>0`. To preserve its valuation at a specified
prime `l`, choose `L` divisible by `l^(v_l(s(n))+1)`. The congruence
`s(nC)==s(n) (mod L)` then fixes that valuation exactly. There are only
finitely many such requirements. This completes the proof. ∎

### Scope and exact collision

For every **realized** finite signature, abundancy is unbounded within its
fiber. In particular, a fixed finite collection of these residues and
valuations cannot supply an upper bound on one-step growth. This does not
exclude a factorization-aware height, an adaptive modulus, or a rule also
using the exact size. It does not preserve the condition that `q` is prime.

A small independently checked instance is

```
n=2,                    sigma(n)=3,       s(n)=1,
N=6050=2*5^2*11^2,       sigma(N)=12369,   s(N)=6319.
```

The multiplier `C=3025` has `C==sigma(C)==1 (mod 6)`. The triples agree
modulo 6, namely `(2,3,1)`, and have the same 2- and 3-adic valuations in
each coordinate. Yet `2` is deficient and `6050` is abundant:
`I(2)=3/2`, whereas `I(6050)=12369/6050>2`.

The agreement is not a multistep agreement: `1 -> 0`, while
`6319=71*89 -> 161`. No orbit conclusion follows from the collision.

This extends the kind of finite-local ambiguity in
[FOUR-ADIC.md, I](../../FOUR-ADIC.md), but with different hypotheses: that
result preserves a prime-cofactor tag and distinguishes a two-step guard;
result A allows composite perturbations and makes abundancy arbitrarily large.
Neither result implies the other's extra conditions.

## 4. Proved result B: exactly when a fixed prime sieve misses an affine model

### 4.1 Definition and classification

Let `f(x)=a*x+b`, where `a>=2` and `b>=1` are fixed integers. A residue `r`
is **M-surviving** if

```
gcd(f^j(r),M)=1 for every integer j>=0.               (5)
```

This describes only divisibility tests, not primality or an aliquot orbit.
Above every prime divisor of `M`, these unit tests are necessary for
primality, never sufficient; smaller primes themselves are finite exceptions.

For a prime `l`, there is no surviving nonzero residue modulo `l` exactly in
either of the following cases:

```
(i)  l divides both a and b;
(ii) l divides a-1 but does not divide b.             (6)
```

Therefore the following are equivalent:

- for every `M>=1` an M-surviving residue exists;
- `gcd(a,b)=1` and `rad(a-1)` divides `b`, where `rad(1)=1`.

Furthermore, under these conditions, for **each fixed** `M`, infinitely many
prime initial values `p` have every formal iterate `f^j(p)` coprime to `M`.
This last assertion uses Dirichlet's theorem, not a prime-tuples theorem.

### Proof

In (i) the next residue is zero. In (ii), the map is the nontrivial
translation `x -> x+b` on the field of `l` elements, so every orbit meets
zero within `l` steps.

In all other cases a unit orbit exists:

- If `l|a` but `l` does not divide `b`, every next residue equals the
  nonzero residue `b`; choose any nonzero initial residue.
- If `l|b` but `l` does not divide `a`, multiplication by `a` preserves
  all nonzero residues.
- In the remaining case `l` divides none of `a`, `b`, `a-1`; the fixed point
  `-b/(a-1)` modulo `l` is nonzero.

These constructions also work for the condition of being a unit modulo
`l^e`: in the first two cases any suitable lift remains nonzero modulo `l`;
in the third use the fixed point modulo `l^e`. CRT combines the choices for
the prime powers in `M`. Conversely, if a bad prime exists, taking `M=l`
prevents (5). Removing all bad primes is exactly the displayed gcd/radical
criterion.

The CRT class `r mod M` is reduced. Dirichlet's theorem supplies infinitely
many primes in it, and polynomial iteration preserves the residue orbit.
It supplies **only the initial prime**, not primality of the later values. ∎

For `a=1`, the per-prime criterion still applies, but the all-moduli radical
formulation is not used: any prime not dividing `b` detects the translation.

### 4.2 Application to a genuine aliquot core

If `sigma(D)=kD`, then for a prime `p` coprime to `D`,

```
s(Dp) = D[(k-1)p+k].                                (7)
```

For `k>=3`, the criterion for `(a,b)=(k-1,k)` reduces to

```
k-2 is a power of 2 (including 1).                   (8)
```

Indeed, `gcd(k-1,k)=1`, and `gcd(k-2,k)` divides 2. Thus every prime factor
of `k-2` can divide `k` exactly when there are no odd prime factors of `k-2`.
The perfect-core case `k=2` instead gives `p -> p+2`, detected modulo 3.

There is an actual core with `k=3`:

```
D=120=2^3*3*5,    sigma(D)=15*4*6=360.
```

Its prime-cofactor recurrence is `f(p)=2p+3`. For **every finite modulus**
`M`, apply the theorem with `lcm(M,30)`. There are infinitely many initial
primes `p>5` for which all formal cofactors remain coprime both to `M` and
to 120. Thus merely adding finitely many prime-divisibility checks, even at
higher powers, never refutes all formal infinite paths in this template.
In the formal model, residues of `n`, `sigma(n)=360(p+1)`, and `s(n)` are
also propagated consistently.

This is the precise point where the investigation follows an implication
beyond literal error-correcting codes: it becomes a local-to-global
realizability question for affine arithmetic dynamics.

### 4.3 Yet there is no infinite prime trajectory

**Lemma (standard modular obstruction; already used in the repository).**
For fixed integers `a>=2,b>=1`, an infinite sequence of primes satisfying
`p_(j+1)=a*p_j+b` is impossible.

**Proof.** The sequence would strictly increase. Choose a term `p` not
dividing `a`; only finitely many primes divide `a`. Modulo this prime,
`x -> ax+b` is a permutation, so its orbit starting at zero returns to zero
at some positive time `h<=p`. The actual recurrence started at the term `p`
has the same residues. Its term `h` steps later is divisible by `p` and
strictly greater than `p`, hence composite. Contradiction. ∎

The detecting prime here is **chosen from the actual trajectory**. It need
not belong to a previously fixed sieve. This resolves the apparent conflict
between the lemma and result B. The theorem's quantifiers are

```
for every finite M, some prime p fools that M forever in the formal model,
```

not

```
some p has only prime formal iterates forever.
```

For example, modulo 30, the residues `7,17` form a surviving 2-cycle for
`2x+3`. The positive formal sequence starts `7,17,37,77,...`. All its terms
avoid 2, 3, and 5, but the fourth is `7*11`. Modulo the **initial prime 7**,
the return occurs at time 3. Residue periodicity has not produced integer
periodicity or a realizable infinite aliquot path.

The broader periodic-core obstruction P already allows positive aliquot
cycles and contracting affine return maps. For instance `220=20*11` and
`284=4*71` form a cycle; the checkpoint cofactor map is
`p -> (33/40)p+77/40`, fixing `p=11`. Nothing here excludes that cycle.

### 4.4 Conditional result, not used in a proof

For each fixed `L`, the forms

```
F_j(x)=2^j*x+3(2^j-1),       0<=j<=L,
```

are primitive, have positive leading coefficients, and are pairwise
nonproportional. Result B shows that their product has no fixed prime
divisor: for each prime there is an input avoiding zero for *all* the forms.
The usual Dickson prime-linear-forms conjecture would therefore give
infinitely many `x` making all these finitely many values prime. Taking the
values above 5 would realize arbitrarily long finite prime-cofactor
120-core prefixes. **That conjecture is not assumed true here.**

This explains why a uniform bound on such finite prefix lengths is not an
available repair. It does not contradict the unconditional impossibility of
one infinite prime chain. Lenstra's unrestricted arbitrary finite increasing
aliquot prefixes, already discussed in GLOBAL.md, are unconditional and are
not new here. This paragraph is about a more specific, conditional template.

## 5. Trying to repair the prime model with composite syndromes

The previous obstruction kills a particular infinite prime template, not
aliquot escape. An actual trajectory can continue through the composite
term, with the positive correction in (3). I tried to force those corrections
to destroy the guarded core in finitely many steps.

For `gcd(q,120)=1`, the exact cofactor update is

```
U(q)=3 sigma(q)-q = 2q+3s(q) = 2q+3+3delta(q),
s(120q)=120 U(q).                                   (9)
```

For `q>1`, `U(q)>q`. Also `U(q)==-q (mod 3)`, so avoiding 3 is automatic.
For odd `q`, `U(q)` is odd exactly when `q` is not a square: the divisor sum
of an odd number is odd exactly when every prime exponent is even.
Divisibility by 5 is the other core guard.

### The attempted exit mechanism

In the prime model modulo 5, only the residue 2 survives indefinitely:
it is fixed, whereas `3 -> 4 -> 1 -> 0`. If a composite `q==2 (mod 5)`
necessarily knocked the output away from 2, one could try charging the
resulting residue excursions against the finite prime phases.

The following part of that proposal is provable. If `q=uv` is a product of
two distinct primes, `q==2 (mod 5)`, and `U(q)==2 (mod 5)`, then

```
sigma(q)==3 (mod 5),
u+v==0 (mod 5),
u^2==-2==3 (mod 5),
```

which is impossible. A prime square cannot be 2 modulo 5 either. This is a
restricted quadratic obstruction, similar in mechanism to the semiprime
filter N in BLOCK-TRANSPORT.md, not an unexplained probabilistic claim.

**The extension to all composites is false.** Take

```
q=637=7^2*13,    sigma(q)=57*14=798,
(q, sigma(q)) == (2,3) (mod 5),
U(q)=1757=7*251 == 2 (mod 5).
```

Both input and output are odd and coprime to 30. Here `delta(q)=160`, so the
correction `3delta(q)=480` is invisible modulo 5. This is an actual guarded
composite transition, not a formal prime replacement. It refutes the claimed
immediate-exit mechanism, although it does not show perpetual survival.
Even a departure from residue 2 would not suffice for a proof: another
composite could alter the subsequent prime-only residue itinerary.

### A defect is not an inexhaustible error budget or a decreasing height

The six checked actual aliquot steps are

```
840 -> 2040 -> 4440 -> 9240 -> 25320 -> 51000 -> 117480.
```

The first five source cofactors relative to 120 are

```
q:       7, 17, 37, 77, 211,
delta:   0,  0,  0, 18,   0.
```

Thus a composite correction can return immediately to zero at a larger
value. There is no monotone accumulation of this proposed error resource.
At the next source `q=425=5^2*17`, coprimality with 120 fails. Substituting
into the coprime formula would give `149880`, but the actual successor is
`117480`. The positive extra size at one step neither preserves unitarity
nor forces a future drop.

These counterexamples led to rejection of the exit and defect-budget
proposals, not to a claimed closed class. No expensive hard orbit was
extended; the stated trace stops after six transitions.

## 6. Remaining obligation, and why the attempt does not close

The smallest concrete unproved assertion left by the composite repair is:

> For every integer `q>1` with `gcd(q,30)=1`, does iteration of
> `U(q)=3sigma(q)-q` reach a term divisible by 2, 3, or 5 after finitely many
> steps?

The map `U` is defined on positive integers, but its interpretation as the
120-core aliquot update is valid only until the first failed coprimality
guard. A proof of this assertion would exclude a **permanently coprime
120-core** escape, not settle the full conjecture. On the other hand, an
explicit `q` rigorously shown to avoid those primes forever would disprove
the conjecture, because (9) would give the actual strictly increasing orbit
starting at `120q`.

This is deliberately a restricted arithmetic obligation, not the original
conjecture renamed as a lemma. We tried to prove its difficult part: the
prime case is obstructed, the two-prime error case has a quadratic filter,
and the proposed extension fails at `637`. Higher prime-power and multiblock
cofactors can be invisible to the very checks intended to force the exit.
Result A shows that merely adding finitely many current congruence and
valuation checks cannot bound their possible growth contribution. It does
**not** prove that every proposed future exit theorem must fail.

An adaptive checking scheme can use an actual cofactor prime to kill a
repeated affine schedule. After a composite correction or a core change,
the same fixed affine permutation is no longer being iterated, so its
zero-return proof does not apply. A finite set of possible cores also does
not force their schedule to be eventually periodic. The repository's
nonexpansive-graph result Q supplies another restriction, but leaves
aperiodic switching with expansive cycles, composite cofactors, and unbounded
cores. None is eliminated here.

Likewise, the fixed-prime-support S-unit route does not close this gap.
It is already K; bounding the prime support of each orbit after using K
would simply be another formulation of the missing global bound. The
existing proof correctly anchors a minimal vanishing subsum by its constant
term. There is no fixed S-unit group when genuinely new primes keep entering.
I did not obtain a rank-uniform substitute that forces descent.

A solution still requires control of all actual trajectories, allowing
positive cycles, or an explicit indefinitely realizable escaping seed. Neither
a residue path, a large correction, nor arbitrarily long finite prefixes
provide that control.

## 7. Literature and status of the mathematical claims

The following sources were actually consulted:

1. **Thomas W. Judson, _Abstract Algebra: Theory and Applications_, section
   8.4, especially Theorem 8.34**, in the public
   [LibreTexts edition](https://math.libretexts.org/Bookshelves/Abstract_and_Geometric_Algebra/Abstract_Algebra%3A_Theory_and_Applications_(Judson)/08%3A_Algebraic_Coding_Theory/8.04%3A_Parity-Check_and_Generator_Matrices).
   The nonzero/distinct-column condition supports the coding bridge, not a
   theorem about divisor sums.
2. **PrimePages, [Cunningham chain](https://t5k.org/glossary/page.php?sort=CunninghamChain).**
   It describes the classical `2p+1` and `2p-1` chains, the generalization to
   fixed coprime `ap+b`, and conditional finite-chain expectations. It cites
   Cunningham (1907), Lehmer (1965), and Löh (1989). Those original articles
   were not inspected here; the affine-chain subject is certainly not new.
3. **Repository synthesis and relevant proof sources:** SYNTHESIS.md,
   GLOBAL.md, RECOVERY.md sections 3–4, FOUR-ADIC.md sections 4–6,
   BLOCK-TRANSPORT.md, and LITERATURE.md. They establish the overlaps recorded
   above and document S-unit finiteness, Lenstra's construction, and related
   fixed-support amicable/sociable results in Pollack's work.

Dirichlet's theorem used in result B is the standard theorem that each
reduced residue class modulo a positive integer contains infinitely many
primes. The only application checks reducedness explicitly. It is an
imported theorem, not proved by the finite computations. The conditional
Dickson assertion is neither this theorem nor an established input.

The new partial proofs do not need the S-unit theorem. The initially proposed
fixed-support route would import it exactly as in GLOBAL.md. Its primary
papers and Pollack's corrected manuscript were not independently downloaded
and re-reviewed during this attempt; the repository literature audit is the
basis for those attributions.

The public-source check was focused, not an exhaustive novelty search.
An initial textbook-host request failed DNS resolution; the LibreTexts
edition succeeded. A proposed MathWorld Dickson URL returned 404, and its
prime-k-tuple page was only a redirect pointer; neither supplies evidence.
No claim of historical priority is made for either result A or result B.

## 8. Evidence and reproducibility

### Files and commands

Only this approach directory and
`tests/test_error_correcting_syndromes.py` were added. No shared research
notes, core API, site, deployment settings, or credentials were changed.
No commit, push, PR, hosting, or deployment was attempted.

Run from the repository root:

```sh
python3 research/approaches/error-correcting-syndromes/verify.py \
  --output research/approaches/error-correcting-syndromes/evidence.json
python3 -m unittest discover -s tests -p test_error_correcting_syndromes.py -v
```

The script is standalone, depends only on the standard library and the
existing exact aliquot module, and writes deterministic JSON. All persisted
integers, including rational numerators and denominators, are decimal strings.
The test suite rebuilds the data and compares it with the retained evidence
file. A final byte-for-byte reproduction also passed:

```sh
python3 research/approaches/error-correcting-syndromes/verify.py \
  --output /tmp/error-correcting-syndromes-evidence.json
cmp /tmp/error-correcting-syndromes-evidence.json \
  research/approaches/error-correcting-syndromes/evidence.json
```

Nothing was committed by this worker.

### Bounds declared before the main checks

| Check | Exact finite scope | Outcome |
| --- | --- | --- |
| Cofactor identity | `1<=c<=40`, `1<=q<=80`, only `gcd(c,q)=1` | 1,962 pairs; 1,087 distinct arithmetic inputs |
| Independent additive sieve | every integer `1..3200`, inclusive | supplies sums for that box; production sums compared on the used inputs |
| Affine local criterion | `1<=a,b<=12`; every prime `2..29`, inclusive | 1,440 cases, exhausting nonzero residue orbits |
| CRT examples | `M=1,30,900,30030`; at most `M+1` residue-state visits | cycles of lengths 1,2,6,2; all units |
| Semiprime filter | distinct primes at most 29; coprime to 30; product `2 mod 5` | 6 cases, also divisor-pair checked |
| Actual orbit trace | seed 840; exactly 6 transitions; source cap 100,000 inclusive | last value 117,480; no continuation attempted |
| Named arithmetic | explicit 15-value list in `verify.py` / JSON; largest source 117,480 | trial factorization plus divisor pairs, at most 342 divisor trials per input |
| Every factorization call | `max_work=100000` | 0 unresolved arithmetic cases in the evidence run |

The named list is
`2,6050,6319,840,2040,4440,9240,25320,51000,117480,637,1757,4291,20017,397`.
This includes checking the sum at the terminal trace value separately as a
named arithmetic example; it is not an additional trace or a survival claim.
A preliminary `python3 - <<'PY' ... PY` check evaluated the same list except
397, with the same 100,000-work budget and divisor-pair loop; the retained
script reproduces all those checks. No interval search for prime initial
values was performed. In particular `20017=37*541` is recorded as composite,
not accepted just because it represents a safe CRT class.

The focused regression suite additionally checks:

- divisor-pair sums for every `n=1..300`;
- adaptive modular return for `1<=a,b<=10` and primes at most 29 with
  `p` not dividing `a`, at most `p` residue steps per case;
- the prime-power neutral construction for `M=1..12` and primes at most 13,
  excluding primes dividing `M`, with exponent `M*phi(M)`;
- exact geometric sums for those prime powers, not infeasible divisor-pair
  enumeration of the large powers;
- both coprimality failures, the actual 220/284 cycle, and exact valuations
  of the 2/6050 collision;
- **two deliberately exhausted calls** on 999983 with `max_work=1`:
  the arithmetic record remains unresolved and the CRT helper propagates
  `ComputationLimit`. These expected test cases are not evidence-run failures.

**Focused result:** 9 tests passed under Python 3.12.3. Arithmetic exhaustion
is never converted into probable primality. The trace's unattempted future
is not counted as a resolved orbit.

The following additional repository checks ran:

```sh
python3 -m unittest discover -s tests -v
node --check site/explorer.js
node --check site/math.js
node --check site/latex.js
git diff --check
```

The full Python suite passed **141 tests**; all three JavaScript syntax checks
passed. `npm test` is an alias for the same full Python command and was not
separately rerun. The existing suite includes its own bounded experiments;
those are regression checks, not additional searches or new mathematical
evidence in this report. The Git check found no tracked-file changes. The
four task-owned files were also individually checked with
`git diff --no-index --check /dev/null FILE`, with no whitespace errors
(exit status 1 denotes the expected new-file difference). They remain
untracked for the coordinator.

Software independently checks finite arithmetic and the implementation of
residue tests. It does not review the universal proofs, prove Dirichlet's
theorem or Dickson's conjecture, or certify that the partial results are novel.

## 9. Fruitfulness assessment

**Not useful toward resolving the conjecture in this attempt.** There is
useful diagnostic output: explicit invisible perturbations, a complete
finite-sieve criterion for the affine model, and a checked failure of the
composite-exit repair. But the candidate closing routes either reproduce
existing results or stop at uncontrolled composite/core changes. A restricted
obstruction and a formal locally admissible path are not progress to a
whole-orbit bound or a divergent seed merely because they are exact.

**Final status: the Catalan–Dickson aliquot sequence conjecture remains
unresolved by this work.**
