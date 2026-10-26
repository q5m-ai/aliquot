# Research notebook 08: exponent geometry, combinatorics, and certified experiments

**Status:** four concrete research tracks, exact structural deductions, and
reproducible finite experiments. **No proof/disproof, divergent sequence, or
historical novelty is claimed.** This is not a claim to have extended the
publicly known Lehmer sequences: the comparison is against this repository's
old trial-division implementation. Mathematical arguments below, experimental
observations, and unproved whole-orbit obligations are deliberately separate.

## 0. Model and deliverables

For n>0 write E(n)=(a_p)_p, where a_p=v_p(n), with finite support. Zero
coordinates are implicit; E(1)=0. The integer 0 is a separate terminal symbol,
not this zero vector. The code stores sparse **prime-labelled** pairs, not
ambiguous strings of digits and not dense arrays extending to the largest
prime. Exponents greater than nine remain unambiguous.

The aliquot map in these coordinates is the exact nonlinear dynamical system
T(E(n))=E(s(n)), for n>1. All coordinates are retained mathematically; any
small-prime projection used below is explicitly information-losing.

Deliverables, all outside the served `site/` directory:

- [`aliquot/exponent_vectors.py`](../aliquot/exponent_vectors.py): geometry
  census, modular combinatorics, certified orbit traces, controls, and paired
  whole-integer/sparse-factor comparisons.
- [`aliquot/certified.py`](../aliquot/certified.py): bounded factoring with
  replayable primality proofs, not a probable-prime backend.
- [`results/exponent-vectors.json`](results/exponent-vectors.json): compact
  exact artifact containing every computed edge, its factorization, prime
  certificates, bounds, projected patterns, and operation counts. The
  [larger-budget follow-up](results/exponent-vectors-extended.json) is separately
  labelled and retains its own complete certificates.
- [`tests/test_exponent_vectors.py`](../tests/test_exponent_vectors.py) and
  [`tests/test_certified.py`](../tests/test_certified.py): independent checks,
  exact counterexamples, corruption/budget tests, and full report reproduction.

## 1. Geometry of the exponent lattice

### 1.1 A convex growth region

For finitely supported real a_p>=0 define

```text
F(a) = sum_p log[(1-p^(-a_p-1))/(1-1/p)].
```

At integer lattice points, F(E(n))=log(sigma(n)/n). Thus s(n)>n exactly when
F(E(n))>log 2. Each coordinate contribution f_p has

```text
f'_p(a)  = log(p)/(p^(a+1)-1) > 0,
f''_p(a) = -(log p)^2 p^(a+1)/(p^(a+1)-1)^2 < 0.
```

Consequently F is concave on every finite-dimensional coordinate face. The
abundant vectors are exactly the integer points of the **convex, upward-closed
region** F>log 2. This statement concerns a continuous region and its lattice
points, not convexity of the discrete set as a subset of real space.

In particular, if E(k)=(E(n)+E(m))/2 is integral, then

```text
sigma(k)^2 >= sigma(n)*sigma(m),    k^2=n*m.
```

If both endpoints are abundant, k is abundant. Example: 24 and 54 give the
midpoint 36 in the 2--3 plane. This follows analytically; the 729 integer
midpoint pairs with endpoints <=500, including 132 abundant endpoint pairs,
are independent finite checks, not the proof.

For a fixed finite prime set S, an abundant vector supported on S exists iff
`prod_(p in S) p/(p-1)>2`: these are the increasing limiting Euler factors,
and equality at the limit is insufficient. The abundant vectors on that face
have finitely many coordinatewise minimal elements by classical Dickson's
lemma. This gives a finite antichain description for fixed-support searches,
not control of the moving support of a possible escaping orbit.

There is no unrestricted coordinatewise continuity shortcut: choose abundant
squarefree numbers supported entirely on primes exceeding j (possible by
Euler-product divergence). Their vectors tend coordinatewise to zero while
remaining abundant. See the compactness/continuity cautions and Pollack erratum
in [LITERATURE.md](LITERATURE.md).

**Use:** replace a list of abundant seeds with a curved geometric region;
search for invariant subsets or return sections inside it. **Missing:** T
need not preserve this convex region: 12 grows to deficient 16. Convexity of
F's superlevel set says nothing by itself about forward invariance under T.

### 1.2 Cancellation confines the displacement to a coordinate face

Put x=E(n), b=E(sigma(n)), y=E(s(n)), n>1. The usual valuation rule for a
difference gives

```text
y = min(x,b) + c,       c>=0,
c_p=0 whenever x_p!=b_p,
c dot |x-b| = 0.                                      (1)
```

All minima and absolute values are coordinatewise. To prove this, if two
integers have unequal p-valuations, factor out the smaller p-power; the
remaining difference is nonzero modulo p. At a tie, factor out the common
power; the remaining difference has a nonnegative additional valuation.

Equivalently, let g=gcd(n,sigma(n)), u=n/g, v=sigma(n)/g. Then

```text
s(n)=g(v-u),       gcd(u,v)=gcd(u,v-u)=gcd(v,v-u)=1.
```

The residual exponent vector E(v-u) has disjoint support from both reduced
input vectors E(u),E(v), proving (1). It need not be orthogonal to E(g): extra
powers of a retained prime can arise at a tie. At p=2 a tie necessarily adds
at least one power; at odd p it need not add any.

This is a valuation/min-plus structure with a cancellation correction, **not**
a fixed linear transformation. Coordinates absent from both x and b are also
ties, so (1) leaves room for new primes and dimension growth.

The same identity gives a prime-weighted loss/cancellation balance:

```text
y-x = c-(x-b)_+,
log(s(n)/n) = sum_p c_p*log(p) - sum_p (x_p-b_p)_+*log(p)
            = log(r)-log(u),      r=v-u.
```

Across a block, the exact gain is the product of r/u. The quantity r need not
be coprime to g: at 12, (g,u,v,r)=(4,3,7,4). The correction is not a small
perturbation; every new successor prime is contained in it.

**Use:** partition states by their balance/deficit/surplus coordinates, and
build piecewise potentials or return rules. Factoring all of sigma(n) is not
required for the implemented continuation: known source primes can simply be
stripped from s(n), leaving only the unknown support to factor.

### 1.3 Two rigorous obstructions to simple vector energies

The actual orbit contains

```text
12 -> 16 -> 15 -> 9
(2,1,0) -> (4,0,0) -> (0,1,1) -> (0,2,0),
E(12) = [E(16)+E(9)]/2.
```

If a convex V were nonincreasing on every edge of this path, convexity would
force V(12)=V(16)=V(15)=V(9). Therefore no globally convex V can be **strictly**
decreasing on every noncyclic step. A strictly convex V cannot even be weakly
nonincreasing on all these edges. This does not exclude flat regions in a
convex V, nonconvex energies, restricted invariant regions, or return maps.

There is a stronger obstruction for positive linear heights. In coordinates
2,3,5,7 take the displacements for these four actual edges:

```text
d1: 12->16 = ( 2,-1, 0, 0)
d2: 16->15 = (-4, 1, 1, 0)
d3: 30->42 = ( 0, 0,-1, 1)
d4: 42->54 = ( 0, 2, 0,-1)
3*d1+d2+d3+d4 = (2,0,0,0).
```

For a height H(x)=sum_p w_p*x_p with w_2>0, all four changes cannot be <=0:
their displayed positive combination is 2*w_2>0. This is an exact cone/separating
hyperplane obstruction, not a failure of one fitted choice of weights.

Finally, unweighted norms are not proper heights on this infinite-dimensional
lattice: E(p) has norm 1 for arbitrarily large primes p. A height must control
**prime location** as well as exponent size. For example sum a_p^2 log p has
finite lattice sublevel sets, but is convex and fails the above global
stepwise descent requirement. The natural next template is a **prime-weighted,
piecewise/nonconvex potential at selected return times**.

### 1.4 What a proof-side geometric program would have to establish

1. Choose explicit present-state return sections, including a controlled tail
   statistic rather than silently truncating all large-prime coordinates.
2. Construct a proper height on those sections: bounded height must leave only
   finitely many possible integer vectors.
3. Prove every actual positive orbit either resolves or reaches these sections
   repeatedly in finite time. A statistical tendency to return is insufficient.
4. Prove boundedness/nonincrease of the height at returns, with all intermediate
   phases justified. Repeated checkpoints in a finite set force eventual
   periodicity by determinism.

These are **open obligations**, not achieved by this notebook. The fixed-support
result in [GLOBAL.md](GLOBAL.md) explains why controlling only one fixed finite
coordinate face is not a complete escape analysis.

## 2. Direct combinatorics: the divisor box and its transfers

### 2.1 The exact object to sum

For x=(a_p), divisors correspond bijectively to lattice points

```text
B(x) = {b: 0<=b_p<=a_p for every p}.
```

The number of points is tau(n)=prod_p(a_p+1). The proper-divisor sum is the
**weighted** box sum

```text
s(n) = sum_(b in B(x), b!=x) prod_p p^b_p.
```

Its multivariate generating polynomial is

```text
P_x(z) = prod_p(1+z_p+...+z_p^a_p) - prod_p z_p^a_p;
s(n) = P_x((p)_p).
```

This is a tensor-product combinatorial description. The prime labels cannot
be discarded: 20, 28, and 44 all have exponent multiset {2,1}, but are
respectively abundant, perfect, and deficient. There is no autonomous rule
on the unlabeled exponent pattern alone.

### 2.2 A prime-factor supply hypergraph

For each source prime-power type (p,a), define the supply column

```text
B_(p,a) = E(1+p+...+p^a).
b = sum_(p:a_p>0) B_(p,a_p).
```

Equation (1) then maps this additive supply vector to the successor with its
balance-supported correction. Supply edges have a combinatorial order test:

- q=p never divides 1+p+...+p^a.
- If q|(p-1), then q divides it exactly when q|(a+1).
- Otherwise, for prime q!=p, q divides it exactly when ord_q(p)|(a+1).

Higher multiplicities require valuations, not merely a Boolean edge. The
factorization into cyclotomic values over divisors d>1 of a+1 organizes the
same supply. These are classical identities; a cycle in this supply graph is
**not** yet an invariant aliquot family because of the subtraction correction.

### 2.3 An exact residual-supply demand vector

Let m=s(n). Separate its **complete prime-power blocks** as m=m_old*R, where
m_old uses primes present in n and R uses genuinely new primes. Then
`gcd(m_old,R)=1` and `gcd(R,n*sigma(n))=1`. This R is different from the
normalized residual r=m/g, which can still contain old-prime cancellation.

For any target prime ell define

```text
d_ell = max(0, v_ell(m)+1-v_ell(sigma(m_old))).
```

Multiplicativity on these coprime blocks gives the exact equivalence

```text
v_ell(sigma(m)) > v_ell(m)
    iff v_ell(sigma(R)) >= d_ell.                      (2)
```

This isolates a specific combinatorial renewal target: can the arithmetic
producing R force its prime-power blocks to supply the next demand vector?
For 276->396, m_old=36 and R=11. The demands at both 2 and 3 are 3, while
sigma(11)=12 supplies only 2 and 1, respectively. Thus strict-surplus renewal
fails immediately, even though the sequence keeps growing. Cancellation and
phase changes cannot simply be replaced by an all-surplus assumption.

Equation (2) certifies only the requested surplus conditions, not regeneration
of all unitary-factor, coprimality, or return guards. The unmet general task is
a theorem about **factors of the new residual**, not merely the size of R.

### 2.4 Exact modular combinatorics without expanding n

For a bounded modulus m, let H_m(r) count proper divisors congruent to r mod m.
The histogram is obtained by multiplicative convolution of the prime-power
histograms, then removing the top point representing n. Thus

```text
s(n) mod m = sum_r r*H_m(r) mod m.
```

The powers p^j mod m eventually cycle, including when gcd(p,m)>1. Counting
whole cycles handles enormous a without enumerating a+1 powers. Implemented
cost is O(k*m^2) residue operations for k occupied coordinates, plus modular
power work and arithmetic on counts of up to log(tau(n)) bits. Here m<=256.
This replaces a potentially enormous product-sized divisor enumeration with
bounded-state dynamic programming.

If only s(n) mod m is needed, the faster product of geometric sums uses binary
composition of pairs (p^L, sum_(j<L)p^j), in O(sum log(a_p+1)) modular
multiplications. **No division by p-1 modulo m is used**; it need not be invertible.

For m=q^k, a nonzero residue determines v_q(s(n)) below k. A zero residue means
only v_q(s(n))>=k, not an exact exponent or an infinite valuation.

A useful exact sublattice gate follows immediately: sigma(n) is odd iff all
odd-prime exponents of n are even. In particular, an even source becomes odd
exactly on that sublattice. The census has 120 such transitions among 5,000 even
sources <=10,000. This is not a probability of escaping an individual orbit.

**Next combinatorial target:** build guarded transfer rules on supply columns,
parity/exponent phases, and modular histograms. Prove that the output reproduces
the guards. A transfer graph inferred from frequencies is only a hypothesis;
modular projections need not determine their own next state.

## 3. Lehmer-five patterns and the infinite-orbit target

### 3.1 Actual experiment and boundaries

Seeds are 276, 552, 564, 660, 966. Controls are 12, 30, 138, 318, 220, and 28.
The default run allows 256 transitions per seed, source bit length <=256,
200,000 certified-factor arithmetic units per factorization (excluding the
separately counted old-prime stripping), 32 rho restarts,
64 Lucas witness candidates per predecessor prime, and at most 200,000 divisors
in the independent edge verifier. Limits apply to sources; an already computed
successor can be the unresolved frontier.

All five stopped at a factorization budget, **not** at a detected infinite orbit.
Every displayed edge has a fully proved source factorization and independently
enumerated proper-divisor sum. The final frontier is known as an integer but
its continuation is not asserted.

| Seed | Old trial prefix | New certified prefix | Growing / shrinking steps | Longest consecutive exact-28-driver source run |
| ---: | ---: | ---: | ---: | ---: |
| 276 | 79 | 126 | 124 / 2 | 118 |
| 552 | 84 | 130 | 123 / 7 | 104 |
| 564 | 115 | 206 | 184 / 22 | 5 |
| 660 | 116 | 162 | 136 / 26 | 4 |
| 966 | 94 | 160 | 160 / 0 | 122 |

“Exact-28-driver” here means v_2(n)=2 and v_7(n)>=1; it does not mean n=28,
or demand v_7(n)=1. A **clean** 28-core additionally has v_7(n)=1, making
n=28u with gcd(u,28)=1. All checked Lehmer source terms are even. Source sizes
reach 78,85,84,97,96 bits respectively; these are not published computation
records. Counts and stopping points depend on the specified engine/budgets.

The long 28-driver runs for 276,552,966 begin at indices 8,26,38, respectively,
and reach the end of the computed source prefix. They are right-censored,
not completed lifetimes or evidence of perpetual persistence. Conversely,
564 and 660 explicitly leave that driver:

```text
1275089956 -> 1326589544,
14700 -> 34776.
```

### 3.2 A larger test breaks the tempting permanent-driver inference

The second artifact increases the step cap to 512 and certified work to
2,000,000 units per factorization; all other bounds and seed order are retained.
All five again stop at a factorization limit, with these verified edge counts:

| Seed | Extended prefix | Growing / shrinking | Longest exact-28-driver source run |
| ---: | ---: | ---: | ---: |
| 276 | 348 | 254 / 94 | 162 |
| 552 | 130 | 123 / 7 | 104 |
| 564 | 231 | 209 / 22 | 5 |
| 660 | 167 | 141 / 26 | 4 |
| 966 | 189 | 185 / 4 | 135 |

These are extensions of the same paths, not independent samples. The most
important outcome is a **falsification**, not merely longer growth:

- The 276 orbit retains the exact 28-driver at indices 8 through 169 and loses
  it on edge 169->170. Its next exact 2-exponent is 1.
- The 966 orbit retains that driver at indices 38 through 172 and loses it on
  edge 172->173, where the 2-exponent rises to 5. That successor is still a
  multiple of 28; leaving the *exact* driver does not mean immediate decline.
- Only the 552 run remains right-censored in its long exact-28-driver phase
  in this follow-up. No perpetual phase follows from that fact.

For 276 the certified loss is particularly transparent:

```text
n_169 = 7165455981799192761913565252 = 4 * 7^2 * p,
p = 36558448886730575315885537,       p mod 8 = 1,
n_170 = 7421365124006306789124764410.
```

The larger artifact contains a replayable primality certificate for p and the
entire independently checked prefix, not just a presumed-prime factor product.
Since sigma(7^2*p)=57*(p+1) has 2-valuation 1, unequal-valuation subtraction
forces v_2(n_170)=1. Thus **permanent retention of driver 28 cannot explain
276's future**, even though the shorter report made it look persistent.

### 3.3 What is worth investigating

The observed motif is **temporary protection of a small-prime core with changing
cofactor support**, rather than repetition of the full vector. Any proposed
whole-orbit mechanism must also cover breakdown, recovery, and core switching. For the 28-core,
2^2 supplies a factor 7 through sigma(4)=7, while an odd power of 7 supplies
at least three factors of 2 in its divisor sum. This protects the exact
2-exponent on that phase. The 7-exponent can spike through cancellation;
its parity and the cofactor's supply then determine whether the phase returns.
[FOUR-ADIC.md](FOUR-ADIC.md) gives the exact restoration guards and their
nonclosure. This recasts that mechanism geometrically/combinatorially; it
does not establish a new perpetual driver.

For any even perfect core D and gcd(u,D)=1,

```text
s(Du)=D*T(u),       T(u)=2*sigma(u)-u.
```

For u>1, T(u)>u. Thus a clean 28-core would give a growing orbit if the odd
cofactor repeatedly avoided 7. Reaching a cofactor divisible by 7 invalidates
the **clean factorization formula**, not necessarily the broader 28-driver.
Even-power spikes therefore need explicit additional phases, not a discarded
trajectory or an assumed reset.

The concrete disproof-side project is a finite collection of **guarded phases
with variable prime cofactors**, containing at least one explicit seed. A phase
may track a prime-power spike, supplying blocks, and modular conditions on the
remaining factorization. Its return map must prove both regeneration of these
guards and a strict increase in the whole integer. This permits changing prime
support, unlike a fixed finite coordinate-face proposal.

### 3.4 Patterns that the data already falsify

The projection (v_2,v_3,v_5,v_7) is not autonomous. Within the 276 trace:

```text
3770 and 3790 both project to (1,0,1,0),
but their successors project to (1,0,1,0) and (1,0,2,0).
```

All five traces contain such collisions; the report supplies actual witnesses.
Even outside these traces, 2 and 22 have the same four-coordinate projection,
but successors 1 and 14 have different projections. A transition matrix on
these four coordinates cannot be an exact deterministic model.

Long growth is not a separating classifier: control 318 has 30 growing steps
among its 35 transitions and nevertheless terminates. Control 138 takes 178
steps to 0; amicable 220 takes two steps to repeat; 28 is a one-step fixed point.
These controls are kept rather than filtering out counterexamples to an
attractive motif. Merged tails and repeated phases are not independent samples.

A broader abundance return class also has an exact losing first return inside
the 660 orbit. Let d_7(n) be the complete part supported on primes <=7 and let

```text
A_7 = {n: sigma(d_7(n))>=2*d_7(n), sigma(n)>2*n}.
```

Starting at orbit index 9:

```text
47952 -> 94586 -> 47296 -> 46684 -> 42524 -> 31900.
d_7: 1296,    2,       64,       4,       4,      100.
```

Only the endpoints belong to A_7, yet the return ratio is 7975/11988<1. Thus
“first return to small-prime-supported abundance always gains” is already
false on a Lehmer-five prefix. A useful next *bounded hypothesis*, not a
claim, is eventual recovery above the earlier checkpoint within a predeclared
8,32,64-step window. Fully checked failures and incomplete/censored windows
must remain distinct.

### 3.5 A sufficient infinite-orbit certificate, still missing

Supply an explicit, decidable present-arithmetic class X and n_0 in X. Prove,
for **every** n in X, that a finite positive return R(n) exists and

```text
R(n) in X,       R(n)>n.
```

This would force infinitely many distinct increasing checkpoints and hence a
nonterminating, nonperiodic aliquot orbit. Intermediate decreases and changing
cores are allowed. Defining X by “all its future returns succeed” is circular.
Finding one finite return or many right-censored examples does not prove the
universal closure statement. The Lenstra finite-growth benchmark and existing
failed supplier-renewal attempts are collected in [SYNTHESIS.md](SYNTHESIS.md).

A stronger framework can permit losing individual returns. Partition X into
finitely many guarded present-arithmetic classes X_i. Prove every input has a
finite return along one of a completely covered set of edges i->j, and give
a positive rational lower gain lambda_e for each edge. If **every directed
cycle** has product of these lower gains >1, every infinite return itinerary
grows without bound: decompose walks into simple cycles and a bounded-length
remainder, and use the positive minimum gain over the finitely many simple
cycles. A single observed profitable cycle does not suffice; total returns,
all exits, and universal edge bounds must be proved.

**Current result:** a concrete core/spike/renewal research target, with exact
positive examples and counterexamples. No suitable closed X or complete guarded
return graph has been found.

## 4. Computational scale: what exponent notation saves, and what it does not

### 4.1 Measured comparison, not an assumed compression benefit

Across the five certified prefixes in the **default** artifact:

| Quantity | Whole integer | Sparse factor representation |
| --- | ---: | ---: |
| Decimal text / compact factor-JSON bytes | 11,046 | 39,064 |
| Integer bit lengths / sum of prime+exponent bit lengths without framing | 35,788 | 40,498 |
| Paired factor arithmetic units, 779 successful paired inputs | 3,620,229 | 3,622,138 |

The last sparse count includes old-prime stripping. Both methods start each
paired input with identical prime-certificate caches; the direct run's new
proofs are not supplied to the sparse run. The common budget bounds the
factorization stage only: the sparse path additionally permits at most twice
the source-bit cap in stripping divisions. These are not equal end-to-end work
budgets. Stripping work is retained on failed rows too. There are no paired cases here where
one method finishes and the other hits its budget. Failures are reported
separately, not silently excluded from the artifact. These counts are not CPU
timings; the two storage rows describe specific encodings, not optimal coding
or Python object memory. Reusing known factors can help particular inputs but
is **not a measured aggregate speedup or compression** on these five prefixes.
The larger run agrees: 1,060 successful paired inputs take 17,818,862 direct
units versus 17,821,933 sparse units, including stripping.

The longer prefixes come from the **new certified factorization algorithm and
proof cache**, not from replacing multiplication with vector addition. The old
trial engine has its original 2,000,000 trial-work budget; its units differ from
modular arithmetic units, so their numerical budgets are not timing ratios.

### 4.2 Where the scale reduction is dramatic and genuine

For the symbolic vector [(2,10^12)], the expanded integer 2^(10^12) would need
1,000,000,000,001 binary bits (about 125 GB before object overhead). We never
construct it. The residue algorithms nevertheless compute exactly

```text
s(2^(10^12)) = 2^(10^12)-1,
s(2^(10^12)) mod 97 = 60.
```

The 97-bucket divisor histogram also counts all 10^12 proper divisors without
enumerating them. This is a real advantage for congruence searches, symbolic
families, and proving bounded-modulus guards. It is **not** a factorization of
the successor, nor a computation of its later orbit.

Python integers already avoid fixed 64-bit overflow (and browser BigInt is
available separately). Memory, bigint bit complexity, conversion budgets, and
factorization remain real limits. A single large prime has one occupied vector
coordinate but still requires storing its large prime label. Full successor
factorization cannot be inferred from its residues or its apparent sparsity.

### 4.3 Why the new factorization layer remains exact

Pollard--Brent finds candidate divisors; each must be a proper exact divisor.
Miller--Rabin is only a **compositeness filter**. Passing it never certifies a
prime at any bit size. Every accepted prime either has a trial proof through
1,000 or a complete n-1 Lucas certificate, recursively terminating at small
primes. For each certified prime q|n-1, a witness a satisfies

```text
a^(n-1) == 1 (mod n),
gcd(a^((n-1)/q)-1,n) == 1.
```

For any prime r|n, these conditions force the multiplicative order modulo r
to contain the entire q-power in n-1. Doing this for every q forces n-1|r-1,
so r>=n and n is prime. This is the classical Lucas criterion, not a new
primality result. Bounded witness search or predecessor factoring may fail
for an actual prime: the result is then **unresolved**, never probable-prime
acceptance.

The verifier replays an ascending certificate DAG with Python's built-in
modular pow, without using rho, the screening routine, or the certifier's
square-and-multiply implementation. Every orbit source is reconstructed and
its proper divisors enumerated independently. Performance/census metadata are
checked by deterministic report regeneration tests, not proved by the Lucas
certificates. Replay additionally caps prime certificates at 20,000, traces
at 32, aggregate source rows at 8,192, source/prime-proof sizes at 512 bits,
and factor-list lengths at 512. Witness lists must match factor support.
Products are checked by incremental exact division rather than constructing
untrusted oversized powers. Seeds must be positive even on empty prefixes.
The CLI reads at most 16 MiB of JSON before parsing and also caps report output;
raw seed/frontier fields have a 320-decimal-digit cap, allowing a computed
successor to exceed its source cap.

## 5. Reproduction and prioritized next work

```sh
# Default bounded evidence and compact committed artifact:
python3 -m aliquot vectors --compact > research/results/exponent-vectors.json

# Replay prime proofs and every stored orbit edge without the factor engine:
python3 -m aliquot verify-vectors research/results/exponent-vectors.json

# Reproduce the separately labelled larger artifact:
python3 -m aliquot vectors --steps 512 --max-work 2000000 --compact > research/results/exponent-vectors-extended.json
python3 -m aliquot verify-vectors research/results/exponent-vectors-extended.json

python3 -m unittest discover -s tests -v
npm test
node --check site/explorer.js
node --check site/math.js
node --check site/latex.js
```

No s(0) evaluation is permitted. All n, prime labels, ratios if added later,
and large symbolic values are exact decimal strings in persisted data; bounded
exponents, indices, counts, and arithmetic budgets are integer JSON values.
A budget-limited frontier is not a lower bound on divergence, only a verified
finite prefix with unresolved continuation.

Priority order:

1. **Guarded core-switching returns:** combine the observed runs, their now
   certified losses, and exact spike-restoration conditions. Try to prove that
   an explicit cofactor supply class regenerates across both persistence and
   core changes. Permanent 28-driver retention is already false for 276 and
   966; search controls for further counterexamples before extending a template.
2. **Combinatorial modular exclusions:** use the divisor-box residue machinery
   to reject impossible supplier/return templates cheaply before attempting
   expensive full factorizations. Retain prime identities and tie information.
3. **Piecewise proper return heights:** exploit the convex abundance boundary
   and cancellation faces, avoiding the proved global linear/convex obstructions.
   Any fitted finite-data certificate must be converted into a universal guarded
   inequality plus a finite-return theorem before it proves anything global.
4. **Scale certified continuation:** improve factor discovery and partial n-1
   certification, cache reusable prime-power supplies, and add checkpoints.
   The present implementation uses complete n-1 proofs, not an undocumented
   arbitrary-precision probabilistic primality shortcut.

These tracks connect: combinatorics proposes guards, geometry explains phases
and candidate inequalities, the Lehmer/control traces falsify weak patterns,
and certified computation supplies trustworthy examples. **The unsolved common
step is guard regeneration or universal return-height control.**

### Review scope

Two read-only AI committee analyses independently agreed on the main geometric
identities and the need for guarded supply renewal. They converged on the
primitive-triple and residual-demand formulation; the additional losing A_7
return was independently checked against a sieve and the certified 660 trace.
A subsequent single bounded static audit found verifier aggregate/domain
boundaries and omitted stripping counts on failed benchmarks; those were
corrected with regression tests. The reviewers did not run experiments or
independently replay these artifacts. Main-session software checks do that;
neither AI review nor passing tests replaces human mathematical review or
historical novelty verification.
