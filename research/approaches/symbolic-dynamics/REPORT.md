# Symbolic dynamics: admissibility, arithmetic lifting, and two obstructions

## 1. Verdict

**Unresolved. No candidate proof or disproof of the Catalan–Dickson conjecture is obtained.** No integer is certified to escape, and no bound is proved for every orbit. The partial mathematical arguments below are written out for review; the software checks are not independent proof review.

The substantial attempt was to encode the arithmetic into a finite symbolic system, use its recurrent paths to isolate a repeatable growth mechanism, and then prove or obstruct arithmetic realization. The strongest conclusions are negative statements about that proposed bridge:

1. **Exact finite words do not settle realization.** For every modulus `M` and duration `L`, there is an actual strictly increasing aliquot prefix of `L` steps all of whose terms are divisible by `M`. Consequently, even *all* universally valid forbidden words in the alphabet “abundance sign and residue modulo M” leave the constant growing itinerary admissible. This is a small extension/application of **Lenstra's known finite-growth construction**, not a newly discovered infinite-growth result.
2. **A concrete finite-state model without an arithmetic lift survives arbitrary fixed prime filters.** The unitary 120-core, with a prime cofactor, has exact cofactor recurrence `F(p)=2p+3`. No positive prime can remain prime under this recurrence forever. Nevertheless, for every fixed modulus `M`, its unit-residue graph has a periodic path, and infinitely many prime starting values follow that graph forever as a *formal affine sequence*. A compatible profinite orbit exists but is not an ordinary integer orbit. The report proves a general criterion for this finite-filter failure.
3. **The composite extension does not inherit the prime obstruction.** The actual cofactor block `7→17→37→77→211` over core 120 passes through the composite that invalidates the prime template and then recovers a prime. Its exact correction destroys the proposed affine modular trap. At the next cofactor, `425`, coprimality with the core fails. Neither event decides the subsequent aliquot orbit.

The periodic-core and fixed-prime-support arguments initially developed independently here were already in the repository. They are identified as such below. **No historical novelty is claimed**, including for the finite-filter criterion or its aliquot application.

## 2. Mathematical bridge and source hypotheses

### 2.1 Actual dynamics, codes, and two different admissibility notions

For `n≥1`, let `s(n)=σ(n)−n`. An orbit is followed only while positive; `s(1)=0`, and `s(0)` is never used. If a positive value repeats, determinism gives a positive periodic tail. Otherwise an infinite orbit has distinct values and eventually exceeds every fixed bound. Thus an infinite nonperiodic orbit tends to infinity, not necessarily monotonically.

Fix a finite alphabet `A` and a present-state code `c:N_{>0}→A`. For a word `w=w_0…w_{L−1}`, define

```
E_L(w) = {n≥1 : s^j(n)>0 and c(s^j(n))=w_j for 0≤j<L}.
```

There is no iteration past zero in this definition. Let `ℒ_c` be the finite words for which `E_L(w)` is nonempty. For an infinite word `w`, its prefix realization sets are nested:

```
E_1(w) ⊇ E_2(w) ⊇ ⋯.
```

*Local admissibility* means every finite subword belongs to `ℒ_c`. *Arithmetic realization* means a single positive integer lies in every prefix realization set. These are different quantifiers. Nested nonempty subsets of the discrete, noncompact set of positive integers need not intersect. If the initial seeds could all be restricted to a fixed finite set, nested nonemptiness would suffice; no such restriction is available here.

A one-step graph is weaker still: an edge `a→b` asserts only that some source realizes those two symbols. Consecutive edges can have incompatible source witnesses.

### 2.2 What transfers from symbolic dynamics

For a finite alphabet, a shift of finite type is specified by finitely many forbidden words. After a higher-block recoding it is a finite directed graph. A sofic presentation allows a finite graph with labeled edges. Infinite paths exist when compatible paths can continue indefinitely; a reachable directed cycle supplies an eventually periodic symbolic path. These statements are about the graph, not about an integer that realizes it.

The needed finite-graph fact has an elementary proof: a path longer than the number of vertices repeats a vertex; repeating the intervening cycle gives an infinite path. Compactness of the finite-alphabet product similarly produces an infinite *word* from compatible finite words. Neither argument supplies surjectivity of an arithmetic itinerary map.

A literal Markov-partition transfer would require, among other things, a specified state space, an appropriate continuous dynamical map, and a lifting theorem for all graph paths. None is established for the aliquot coding. The repository already proves that `s` has no continuous extension agreeing on all positive integers to `Z_2`, by a discontinuity at 18 ([TWO-ADIC.md, Proposition B](../../TWO-ADIC.md)). A discrete countable graph with vertex `n` and edge `n→s(n)` is exact, but its path question is just the original problem; finite-graph recurrence cannot be invoked for it.

The productive departure from the initial analogy is therefore **arithmetic analysis of lifting**, rather than an assumed conjugacy. Sections 3.1 and 3.3 prove two concrete limits on lifting, including one where the surrogate affine map really is continuous on a compact profinite space.

## 3. Results, proofs, and attribution

### 3.1 Proposition A — growing words survive every fixed residue refinement

**Statement.** For every integer `M≥1` and `L≥1`, there is an integer `n_0` such that its actual aliquot terms satisfy

```
n_0 < n_1 < ⋯ < n_L,        M | n_j  for every 0≤j≤L.
```

**Proof.** Let `p_1=2,p_2=3,…` be the successive primes. Choose `t≥2` so all prime divisors of `M` are among `p_1,…,p_t`, and put `m=t+L`.

Choose `a_1≥max(2,v_2(M))`. Recursively choose positive `a_i`, for `2≤i≤m`, such that

```
a_i ≥ v_(p_i)(M),
p_(i−1)^(a_(i−1)+1) | σ(p_i^a_i).
```

Here is a construction, not a prime-existence assumption. Put

```
B_i = p_(i−1)^(a_(i−1)+1) (p_i−1).
```

Since `gcd(p_i,B_i)=1`, Euler's theorem gives `p_i^φ(B_i)≡1 (mod B_i)`. Choose `a_i+1` to be a sufficiently large positive multiple of `φ(B_i)`. Dividing `p_i^(a_i+1)−1` by `p_i−1` proves the required divisor-sum divisibility, and a sufficiently large multiple also meets the lower bound on `a_i`.

Let `A_r` be the integers with exact exponents `v_(p_i)(n)=a_i` for `i≤r`. For `n∈A_r` and `i<r`, the unitary prime-power factor `p_(i+1)^a_(i+1)` supplies `p_i^(a_i+1)|σ(n)`. Since `v_(p_i)(n)=a_i`, subtraction gives

```
v_(p_i)(s(n))=a_i.
```

Thus `s(n)∈A_(r−1)` whenever the displayed terms are positive. Every member of `A_r`, for `r≥2`, is a multiple of 12 and is abundant: its three proper divisors `n/2,n/3,n/6` sum to `n`, and the additional divisor 1 is distinct from them. Hence `s(n)>n` and positivity is automatic at all steps needed here.

Take `n_0=∏_(i=1)^m p_i^a_i`. Inductively `n_j∈A_(m−j)` for `0≤j≤L`. These sets all fix the first `t` prime exponents, so `M|n_j`, and they all fix at least the first two exponents, so each source grows. This proves the assertion. ∎

**Attribution.** The supplying-prime chain is Lenstra's construction reproduced by Erdős (1976) and proved in [GLOBAL.md, section 1](../../GLOBAL.md). Prescribing the lower bounds needed for `M` and drawing the following language consequence are additions to this report, not a claimed new construction or historical discovery. No enormous seed from this proof was computed.

**Corollary: an obstruction even to the full forbidden-word language.** Code a positive integer by

```
c_M(n) = (sign(s(n)−n), n mod M).
```

Let `a=(+,0)`. Proposition A shows `a^r∈ℒ_(c_M)` for every finite `r`. Therefore the infinite word `a^∞` avoids **every** forbidden word that is valid for all actual finite prefixes. In particular no finite-memory approximation of this language can exclude it.

More generally, any finite labeled graph containing all these finite coded paths has an infinite path labeled entirely `a`: there are arbitrarily long all-`a` paths in its finite subgraph of `a`-labeled edges, hence a cycle there. This also covers auxiliary finite states in a graph presentation.

**Exact scope.** It is not proved that `a^∞` is unrealizable. Realizing it would give a strictly increasing infinite aliquot orbit and disprove the conjecture. Rather, the corollary proves that a strategy whose final step is “these universally valid finite-word constraints exclude every growing symbolic path” cannot work for this code. It does not exclude seed-dependent arithmetic information, infinitely many state values, or a separate descent/lifting argument. Nor is every escaping orbit required to have this constant code.

### 3.2 Periodic prime-core lifting: a closing argument, but already established

Before reading the synthesis, the most promising closing route found here was to keep the cofactor prime. If `D>1`, `p` is prime, and `p∤D`, then

```
s(Dp)=s(D)p+σ(D).
```

For a periodic schedule of cores `D_0,…,D_(r−1)`, repeated with coprime prime cofactors, composition over one period gives the checkpoint prime recurrence

```
x_(j+1)=A x_j+C,       A>0, C>0 rational.
```

Explicitly, set `r_i=s(D_i)/D_i>0`. The source step is `n'=r_i n+σ(D_i)`, so `A=∏_i r_i` and `C=(1/D_0)∑_(i=0)^(r−1) σ(D_i)∏_(h=i+1)^(r−1) r_h>0`.

This is exactly [RECOVERY.md, Proposition P](../../RECOVERY.md), not an addition here. For completeness, the closing argument can be stated briefly. The integer differences `Δ_j=x_(j+1)−x_j` obey `Δ_(j+1)=AΔ_j`. If `A=a/b` is reduced with `b>1`, integrality of every difference forces `b^j|Δ_0` for all `j`, hence `Δ_0=0`. The checkpoints are constant. If `A` is a positive integer, then `C` must also be an integer, the checkpoints strictly increase, and a late checkpoint prime `p` does not divide `A`. The affine map `z↦Az+C` permutes residues modulo `p`, so its orbit of 0 returns to 0 within at most `p` steps. A later checkpoint is a multiple of `p` larger than `p`, contradicting primality.

Thus any infinite such tail is a positive cycle with period dividing the core schedule length; there is no escape in this class. Constant checkpoints require `A<1`. The amicable cycle

```
220=20·11 → 284=4·71 → 220
```

is allowed: `A=33/40`, `C=77/40`, and `x=C/(1−A)=11`. A core 1 instead gives a prime term followed by `1→0`, not an infinite tail.

The independent fixed-prime-support route also duplicated [GLOBAL.md, Proposition K](../../GLOBAL.md), using nondegenerate S-unit finiteness after isolating a constant-containing vanishing subsum. It already implies `P⁺(n_j n_(j+1))→∞` on any escaping orbit. It supplies neither a bound on changing support nor a closing step and is not counted as a new result.

### 3.3 Proposition B — exactly when fixed prime filters miss an affine obstruction

The periodic-core argument suggests encoding prime cofactors by congruences. The following gives a sharp test of that proposal.

For integers `a≥2`, `b≥1`, put `F(x)=ax+b`. For a prime `ℓ`, call a residue `r` a *survivor* if `F^j(r)≠0 (mod ℓ)` for every `j≥0`.

**Local statement.** There is no survivor modulo `ℓ` if and only if either

```
ℓ | gcd(a,b),
or  ℓ | (a−1) and ℓ ∤ b.                         (B1)
```

**Proof.** If `ℓ|a`, every successor is `b mod ℓ`. Thus there is a survivor precisely when `ℓ∤b`. Suppose `ℓ∤a`. If `a≡1`, the map is a nonzero translation when `ℓ∤b`, and every residue visits 0; when `ℓ|b`, it is the identity and every nonzero residue survives. Finally suppose `a≠1 mod ℓ`. If `b≢0 (mod ℓ)`, the fixed point `−b/(a−1)` is nonzero and survives. If `b≡0 (mod ℓ)`, multiplication by the nonzero residue `a` preserves all nonzero residues. These cases prove the equivalence. ∎

**Global finite-filter statement.** The following are equivalent:

1. For every integer `M≥2` there is a reduced residue `r mod M` whose entire affine forward orbit is coprime to `M`.
2. `gcd(a,b)=1` and every prime divisor of `a−1` divides `b` (with no restriction from `a−1=1`).

Necessity follows by taking `M=ℓ` in (B1). For sufficiency, choose a surviving residue at each prime dividing `M`, lift it to the relevant prime power, and apply CRT. Nonvanishing modulo each prime suffices for coprimality at every time. This proves the equivalence without a primality conjecture.

Moreover, **Dirichlet's theorem** supplies infinitely many prime starting values in the resulting reduced residue class. They may be chosen larger than every prime dividing `M` and any prescribed cutoff. Every formal affine iterate then avoids the fixed test primes. Dirichlet is an imported theorem about one progression; it says nothing about primality of the later iterates.

Nevertheless **no** `F(x)=ax+b` with `a≥2,b>0` has an infinite all-prime positive orbit. If one existed it would increase without bound; choose a term `p` prime and not dividing `a`. The same affine permutation modulo `p` used in section 3.2 produces a later composite multiple of `p`. This is a seed-dependent modulus, not one fixed finite filter working for all prime starts.

For a multiperfect core `D>1` with `σ(D)=kD`, where `k≥2` is an integer, the prime recurrence is

```
p'=(k−1)p+k.
```

For `k≥3`, the finite-filter criterion becomes

```
all prime divisors of k−2 divide k
    ⇔ k−2 is a power of 2 (including 1).
```

The equivalence holds because `gcd(k−2,k)` divides 2. For perfect cores (`k=2`) the recurrence is `p↦p+2`; modulo 3 it is a nonzero translation and no residue survives forever. This classification is conditional on the existence of the stated multiperfect core; no existence claim for arbitrary `k` is made.

**Status relative to the repository.** The impossibility of an infinite prime-cofactor orbit is already contained, more generally, in [FOUR-ADIC.md, Proposition J](../../FOUR-ADIC.md). The explicit classification of fixed finite divisibility filters and the following profinite realization countermodel are not stated in the source notes inspected. Their elementary ingredients are standard. Historical novelty has not been established.

### 3.4 The 120-core gives an explicit compact model with no prime-core lift

Since `120=2^3·3·5` and `σ(120)=15·4·6=360`, for every prime `p∤120`,

```
s(120p)=120(2p+3),          F(p)=2p+3.
```

For each `M≥2`, form the finite directed graph `G_M` on unit residues modulo `M`, with edge `r→2r+3` when the target is also a unit. This is a genuine finite-state symbolic system for the **necessary congruence conditions** on the prime-core recurrence when its primes exceed every prime divisor of `M`. It is not claimed to encode sufficient conditions.

Write `M=3^e H`, with `gcd(H,3)=1`. Select

```
r_M ≡ −3 (mod H),       r_M ≡ 1 (mod 3^e),        (B2)
```

omitting a congruence when its modulus is 1. Along every formal iterate, the first component stays `−3`; the component modulo 3 stays nonzero because `F(x)≡−x (mod 3)`. Thus every iterate is a unit modulo `M`. The component modulo `H` is fixed, and the map modulo `3^e` is a permutation, so this path is periodic from its first symbol. Dirichlet supplies infinitely many primes `p≡r_M (mod M)`, which can all be taken larger than `max(5,ℓ:ℓ|M)`.

But no such prime start has a perpetual prime-core lift. For any prime `p>5`,

```
F^j(p)=2^j(p+3)−3.
```

At `h=ord_p(2)≤p−1`, this value is divisible by `p` and strictly larger than `p`, hence composite. Some earlier term might already be composite or share a core factor; the bound is an upper bound on survival of the proposed prime template, not a claim that the aliquot orbit follows it until time `h`.

There is even a compatible inverse-limit point. In

```
Z-hat = ∏ over primes ℓ of Z_ℓ,
```

let `z_ℓ=−3` for `ℓ≠3` and `z_3=1`. It reduces to (B2) modulo every `M`, and all `F^j(z)` are profinite units. The affine map is continuous here. Yet no ordinary integer equals `z`: its 2-adic component would force that integer to be exactly `−3`, whose 3-adic component is not 1. The same reasoning applies to every iterate (`F^j(z)_3=4·2^j−3≠−3`).

This exhibits precisely what a compactness argument can produce and what it cannot: a compatible arithmetic-looking formal orbit in a compact enlargement, but no positive-integer prime-core orbit. It does not define or assume an extension of `σ` to that space.

**Finite witness.** For `M=2310=2·3·5·7·11`, the selected residue cycle is

```
1537 → 767 → 1537   (mod 2310).
```

The prime `3847≡1537` has `F(3847)=7697=43·179`, already composite but coprime to 2310. All later **formal affine** terms still avoid those five test primes. The actual arithmetic is

```
461640=120·3847 → 923640=120·7697 → 1927560,
```

whereas continuing the prime formula would incorrectly give `120·15397=1847640` at the last step. These are independently checked finite identities, not a fate determination for the orbit.

### 3.5 Conditional result: exact finite realizability is itself a prime-tuples issue

For any fixed `L`, consider the linear forms

```
f_j(x)=2^j(x+3)−3,       0≤j≤L.
```

They have positive leading coefficients and are primitive: the constant coefficient `3(2^j−1)` is coprime to `2^j`. They are pairwise nonproportional. They are jointly admissible at every prime:

- at 2 take `x` odd;
- at 3 take `x≠0`;
- at every prime `ℓ≥5` take `x≡−3`, which makes all forms `−3 mod ℓ`.

**Under Dickson's prime-tuples conjecture**, these forms are simultaneously prime for infinitely many positive `x`. Discarding the finitely many small starts, the exact 120-core aliquot recurrence would then be valid for any prescribed finite duration. This is a different conjecture from the Catalan–Dickson aliquot conjecture and is **not** assumed in any unconditional conclusion here.

In particular, the following would coexist under the prime-tuples hypothesis:

```
for every L, infinitely many exact L-step prime-core prefixes;
no infinite prime-core prefix from any one integer.
```

This is a precise conditional example of the quantifier/lifting gap even when every finite word is realized by actual aliquot arithmetic. Unconditionally, section 3.4 proves only finite-filter admissibility, not arbitrarily long exact prime runs. The affine `+3` family is related to, but not the definition of, classical Cunningham chains (`2p±1`). Their literature already treats unbounded finite chain lengths as conjectural; this attempt does not mistake them for a theorem.

### 3.6 Composite revision: the exact correction is not a descending resource

The use of `δ(u)=s(u)−1` to measure prime-template failure is already explicit in [BLOCK-TRANSPORT.md](../../BLOCK-TRANSPORT.md); [RECOVERY.md](../../RECOVERY.md) also keeps composite corrections through changing cores. The identity below is an elementary specialization to the 3-perfect core 120, not a new correction method. The perpetual-core strategy itself belongs to the classical guide/driver framework discussed in [REGENERATION.md](../../REGENERATION.md).

For every `u≥1` coprime to 120, multiplicativity gives

```
s(120u)=120 T(u),
T(u)=3σ(u)−u=2u+3s(u)=2u+3+3δ(u),       δ(u)=s(u)−1.       (C)
```

For `u>1`, `δ(u)≥0`, with equality exactly when `u` is prime. Thus the formal prime map is a lower bound while the coprimality guard holds, but the correction has no fixed congruence sign and no proved finite budget. The identity for `u=1` is still valid; the assertion `δ≥0` deliberately excludes it.

The exact block

```
u:  7 → 17 → 37 → 77 → 211 → 425
n: 840 →2040→4440→9240→25320→51000
```

has five verified transitions. At `u=77`, `s(77)=19`, so `δ(77)=18` and

```
T(77)=157+54=211,       not F(77)=157.
```

Here 77 is the composite multiple of the initial prime 7 predicted by the affine trap (`ord_7(2)=3`). The next actual cofactor is prime and is not divisible by 7. Compositeness did not end the actual core block. At 425, however, `gcd(425,120)=5`; (C) may no longer be used for the next aliquot step. This is a boundary of the certified representation, not proof of decrease, termination, or divergence.

One attempted present-state refinement was

```
X={u>1 : gcd(u,120)=1, u≡2 (mod 5), σ(u)≡3 (mod 5)}.
```

The residue conditions ensure `T(u)≡2 (mod 5)`, and the class includes all primes `u>5` with `u≡2 mod5`. But `37∈X`, whereas `T(37)=77` has `σ(77)=96≡1 mod5`, so `77∉X`. The residue of the returned cofactor survives while the supply guard fails. This explicitly rejects renewal rather than merely failing to find it.

Finally, for a coprime odd input, `T(u)≡−u (mod3)` automatically avoids 3. Parity of `σ(u)` is odd exactly for a square odd `u`, so `T(u)` is even exactly when `u` is a square. Avoidance of 5 requires `3σ(u)≠u (mod5)`. Nothing proved here propagates the nonsquare condition and that divisor-sum condition together. Positive composite corrections are not a proof of their propagation.

## 4. Failed routes and revisions actually pursued

| Proposed closing step | Precise failure or counterexample | Revision and outcome |
| --- | --- | --- |
| Forbid enough words in an abundance/residue code to eliminate all growing paths. | Proposition A puts every finite constant growing word in the exact language, for every modulus. | Passed from a single transition graph to the full finite-word language; the obstruction persists. No claim that the infinite word is realized. |
| Compactness of increasingly fine congruence graphs supplies a positive seed. | The explicit profinite point in section 3.4 is compatible at every modulus but is no integer. | Verified continuity for the affine surrogate itself, not for `s`; even there compactness does not give the required lift. |
| A repeatable prime-core template can yield divergence. | Integer affine recurrences force a later multiple of an earlier prime; noninteger rational slopes consume integrality. | This closing argument works only in the restricted class and was already Proposition P/J in the repository. Cycles such as 220↔284 are not discarded. |
| Refine primality into a sufficiently large fixed collection of divisibility tests. | Proposition B classifies the obstruction exactly. Core 120 passes every such finite filter; 3847→7697 fails primality outside the chosen filter. | Seed-dependent moduli obstruct the prime template but are not a fixed finite symbolic alphabet. |
| Extend the prime trap across composites by treating its error as harmless. | `77→211` under `T` removes the trapped prime 7; the exact error is 54 in cofactor units. | Kept the error `3δ(u)` and tested a residue/supply class. Its closure fails at 37→77. |
| S-unit rigidity rules out an escaping orbit. | It rules out fixed prime support, not continually changing support; this is already Proposition K. | No replacement bound on changing prime support was established. Naming that bound would merely repackage the full problem. |

For arbitrary finite collections of cores, an escaping prime-cofactor path would have to switch aperiodically and use an expansive cycle in its recurrent transition graph, by the existing Propositions P and Q. A graph cycle need not be traversed repeatedly by that path. Nothing in finite-graph recurrence changes that distinction, and the argument here does not exclude such switching or general composite cofactors.

## 5. Remaining obligation and its relation to the full conjecture

The narrow unresolved question left by the composite revision is explicit:

> **R120.** For every `u_0>1` with `gcd(u_0,120)=1`, must some iterate of `T(u)=3σ(u)−u` fail to be coprime to 120?

This is **not asserted as a new theorem or as equivalent to the full conjecture**. If one proves R120, only perpetual retention of this particular unitary core is excluded. General escaping aliquot orbits need not ever use this core, and can change factorizations, cores, or parity.

Conversely, an explicit `u_0` with a proof of perpetual coprimality would disprove the full conjecture, since (C) would then hold at every step and

```
T(u)≥2u+3  for u>1,
T^k(u_0)≥2^k(u_0+3)−3.
```

One sufficient way to do that would be a nonempty, present-arithmetic class `X`, containing an explicit integer, with `T(X)⊆X⊆{u>1:gcd(u,120)=1}`. No such class is supplied. Defining `X` by successful future iterates would just hide the missing assertion.

The attempted difficult step was to make the prime obstruction or residue/supply guards survive the composite correction. It fails for an identified reason, not a missing computation: `δ(u)` depends on the new full factorization, can remove a previously forced divisor, and does not preserve the tested supply congruence. The finite-filter/profinite construction shows why simply adding a fixed amount of congruence information cannot repair the prime-only surrogate; it does not prove that every richer invariant fails.

For the proof direction, an additional argument covering *all* actual escaping orbits is still needed—an orbit-wise bound, a well-founded descent, or another universal contradiction that permits cycles. No new universal restriction beyond the repository's existing ones has been obtained here. The restricted R120 question is recorded to locate this attempt's boundary, not advertised as a disguised solution.

## 6. Evidence, reproducibility, and literature checks

### 6.1 Exact finite computations

Supporting files are [verify.py](verify.py), [evidence.json](evidence.json), and [tests/test_symbolic_dynamics.py](../../../tests/test_symbolic_dynamics.py). No core API, shared research note, or served file was changed.

The experiment used Python 3.12.3, exact integers, and `fractions.Fraction` for the cycle check. Factorization is the existing exact trial-division API, with **20,000 work units per call**. No probable-prime shortcuts or new dependencies were used.

| Check | Inclusive scope and limits | Outcome |
| --- | --- | --- |
| Unitary 120-core identity | `1≤u≤1000`, `gcd(u,120)=1`; additive proper-divisor sieve through `120000` | 266 cofactors; 532 factorization/product-formula comparisons against independent sieve values; no mismatch |
| Named arithmetic | 18 specified positive sources, largest 923640; independent divisor-pair enumeration with a hard source cap of 4000000 | All verified; known successors may exceed their sources, and are not automatically iterated |
| Actual 120-core block | Exactly five transitions from 840 through 51000 | Stops at cofactor overlap 425; no claim about the orbit's later fate |
| Affine-filter criterion | `2≤a≤12`, `1≤b≤12`, all 14 primes `2≤ℓ≤43`; each residue path uses at most `ℓ` transitions before failure/repetition | 1848 exact finite cases agree |
| CRT survivor cycles | Every `1≤M≤256`, plus `2310` and `2177280`; cap 1024 modular steps per modulus | 258 complete cycles checked, maximum period 162 |
| Formal modular trap tests | Every prime `7≤p≤199`; order search at most `p−1`; evaluate the explicit integer `2^h(p+3)−3` | Divisibility and strict increase checked; these values are **not** factored or treated as actual aliquot iterates |
| Additional independent checks | Pair enumeration against a sieve for `1≤n≤300`; compatible residues for all divisibility pairs `1≤d≤M≤128` | Passed |

The evidence run has **0 unresolved checks**. Separate regression tests deliberately force (i) factorization exhaustion at `n=101`, work budget 1, and (ii) a modular-cycle cap failure at modulus 9, step cap 1. Both remain unresolved; neither becomes a composite verdict or a conjectural conclusion. The evidence script records unresolved inputs if its arithmetic budget is lowered.

The proof's Lenstra seeds were **not** generated. No known hard aliquot orbit was extended, and there was no unbounded seed or prime-chain search. The modular computations enumerate small finite graphs, not whole-orbit statistics. Persisted mathematical values are decimal strings; bounded counts and limits are JSON integers.

Commands run from the assigned repository root:

```sh
python3 research/approaches/symbolic-dynamics/verify.py \
  > research/approaches/symbolic-dynamics/evidence.json
python3 -m unittest discover -s tests -p test_symbolic_dynamics.py -v
python3 -m unittest discover -s tests -v \
  > /tmp/aliquot-symbolic-full-tests.log 2>&1
node --check site/explorer.js
node --check site/math.js
node --check site/latex.js
python3 research/approaches/symbolic-dynamics/verify.py \
  > /tmp/aliquot-symbolic-evidence.json
cmp /tmp/aliquot-symbolic-evidence.json \
  research/approaches/symbolic-dynamics/evidence.json
git diff --check
```

Results: **11/11 focused tests passed; 143/143 full-suite tests passed; all three JavaScript syntax checks passed; evidence reproduced byte-for-byte.** `npm test` is the same full Python discovery command in this repository and was not invoked separately. No commit, push, PR, hosting, merge, or deployment was performed.

The additive sieve and divisor-pair algorithm do not use the factorization/product formula. They are algorithmically independent arithmetic checks, but share the Python runtime and author. They do not review the universal proofs, Dirichlet's theorem, or the conditional prime-tuples statement.

### 6.2 Prior work and public-source scope

The initial derivation preceded consultation of the synthesis. Then the following assigned-checkout notes were read: [SYNTHESIS.md](../../SYNTHESIS.md), [README.md](../../README.md), [GLOBAL.md](../../GLOBAL.md), [RECOVERY.md](../../RECOVERY.md), [FOUR-ADIC.md](../../FOUR-ADIC.md), [TWO-ADIC.md](../../TWO-ADIC.md), [BLOCK-TRANSPORT.md](../../BLOCK-TRANSPORT.md), [REGENERATION.md](../../REGENERATION.md), and [LITERATURE.md](../../LITERATURE.md). These establish the overlap with K, J, P, Q, Lenstra's construction, and the earlier residue-class failures. No other worktree, branch, agent, transcript, or shared agent memory was consulted; no work was delegated.

Public sources directly retrieved and inspected for this report:

- [Subshift of finite type](https://en.wikipedia.org/wiki/Subshift_of_finite_type), especially forbidden words, graph presentations, product topology, and sofic presentations. The finite-graph facts actually used are proved in section 2, not imported as an unchecked aliquot conjugacy.
- [Dickson's conjecture](https://en.wikipedia.org/wiki/Dickson%27s_conjecture), for the standard finite-family linear-forms statement and its attribution to L. E. Dickson, *A new extension of Dirichlet's theorem on prime numbers*, **Messenger of Mathematics 33** (1903), 155–161. The original 1903 article was not independently read; this is a checked secondary statement of an explicitly unproved hypothesis, not an imported theorem.
- E. W. Weisstein, with J. K. Andersen, [Cunningham Chain](https://mathworld.wolfram.com/CunninghamChain.html), for the `2p±1` definition and the conjectural nature of arbitrary chain lengths. The `2p+3` family here is not mislabeled as one of those standard chains. No numerical chain record is used.
- E. W. Weisstein, [Catalan's Aliquot Sequence Conjecture](https://mathworld.wolfram.com/CatalansAliquotSequenceConjecture.html), for the established target/status, not as a substitute for evaluating this argument.

Retrieval used `curl --fail --location --max-time 30 --silent --show-error URL -o FILE` and the Python standard-library HTML parser. An initial MathWorld Dickson URL returned 404; the Encyclopedia of Mathematics symbolic-dynamics page returned 502; Scholarpedia's TLS certificate verification failed and was not bypassed. None of those failed retrievals is counted as a consulted source.

Lenstra/Erdős attribution comes from the repository's written proof and source audit, citing P. Erdős, [*On Asymptotic Properties of Aliquot Sequences*](https://www.renyi.hu/~p_erdos/1976-22.pdf), **Mathematics of Computation 30** (1976), 641–645. That PDF was not reread in this session. Euler's theorem, CRT, elementary finite-field arithmetic, and Dirichlet's progression theorem are the unconditional imported number-theoretic inputs. The S-unit theorem is mentioned only when identifying the already-established route, not needed for Propositions A or B.

This was a focused attribution check, not a complete bibliographic novelty search. The known prime-chain and finite-prefix literature already supplies the central warnings. No claim that the report's precise finite-filter criterion or modular refinement is historically new is warranted.

## 7. Fruitfulness assessment

**Undetermined for resolving the conjecture.** The attempt gives two mathematically explicit diagnostics: an exact-language obstruction for abundance/residue coding, and a classified finite-filter/profinite model whose infinite paths have no prime-core lift. It also follows the prime obstruction into the actual composite correction and rejects a concrete renewal class.

These are useful safeguards against a false symbolic proof, but a restricted obstruction is not automatically progress toward Catalan–Dickson. The strongest initial orbit restrictions duplicated the repository; the added results do not yield an orbit-wise bound, a universal descending resource, or an indefinitely repeatable actual escape mechanism. The conjecture remains unresolved.
