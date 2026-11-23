# Can the arrival of large primes stop an old prime making records?

**Two results.** A single step can introduce arbitrarily many primes, each larger than **every** prime in the seed, without dislodging 5 from any of the next prescribed number of record-making terms. The seed depends on what we prescribe. In the other direction, there is a fixed-orbit obstruction: if every term is one of finitely many cores times a coprime prime, and every finite block of the core sequence recurs arbitrarily late, the orbit must cycle. The cores need not follow a periodic schedule. Neither result assumes RH or GRH. Neither establishes a bound on reuse for general aliquot orbits.

## Test the residue-counting step from the Lean archive

We fetched the relevant Lean files at commit `9d5316ec73f5df89c4d95703ed106837b8a4060e` of the released archive. We inspected the statements and the cited modular calculation, not a build or verification of the full announced proof. Two distinct operations occur in its Behrend-set argument:

- [`TranslateMean`][mean] counts hits averaged over **all translations** of a finite set. Take the singleton $T=\{0\}$ modulo an odd prime $\ell$. For a finite set of indices $J$ (here the sources of strict new records), put $C(u)=\#\{j\in J:n_j\equiv u\pmod\ell\}$. The specialization is exactly $\sum_{u\bmod\ell} C(u)=|J|$. Repeated residues count repeatedly. The mean is $|J|/\ell$; divisibility asks for **$C(0)$**, not that mean.
- [`WindowTwo`][window] controls hits along $t_0+i h$ with a **fixed step** of sufficiently large additive order and a target satisfying its spacing hypotheses. The proof’s [`idx_eq`][index] shows why: two hits on the same point less than the order apart must have the same index. There is a direct test on one orbit. Set $x_j=(-1)^j n_j\bmod\ell$. Then $x_{j+1}-x_j=(-1)^{j+1}\sigma(n_j)\bmod\ell$. If these increments are constant and nonzero between $t$ consecutive sources, at most $\lceil t/\ell\rceil$ of those sources are divisible by $\ell$: every group of $\ell$ consecutive positions visits each residue once. In general the increment changes, or is **zero**. A zero increment can keep hitting zero rather than separating the hits.

The following result makes the zero-increment obstruction occur on actual records at the very time new large primes appear. It uses the *earlier aliquot results*, not a prime-counting conclusion from the RH announcement.

## Arbitrarily many new large factors, without losing 5

Write $s(n)=\sigma(n)-n$. A *record-making source* is a term whose **successor** exceeds every value so far. Given any $H,K\ge1$ and cutoff $Y$, there are infinitely many seeds $n_0$ such that:

1. $n_1=s(n_0)$ has at least $K$ distinct prime factors greater than both $Y$ and the largest prime factor of $n_0$;
2. $30\mid n_j$ for $0\le j\le H$, and $n_{j+1}\ge(7/5)n_j$ on all those steps. In particular, the old prime 5 divides each of $H$ consecutive record-making sources **starting with the term where the new primes arrive**.

**Keep the old factor first.** Set $r_0=1$. Use Dirichlet’s theorem to choose increasing primes $r_i>7$ with $r_i\equiv-1\pmod{30r_{i-1}^2}$ for $1\le i\le H$. Set $D=30\prod_{i=1}^H r_i$, and vary only the exponent in $n_0(e)=D7^e$, $e\ge1$. All these seeds have the **same prime factors**. If $30\mid x$ and $r_1,\ldots,r_k$ divide $x$ to exponent one, then $r_1+1\mid\sigma(x)$ keeps $30\mid s(x)$ for $k\ge1$. For $i<k$, $r_i^2\mid r_{i+1}+1\mid\sigma(x)$, so $r_i$ still divides $s(x)$ exactly once. This is the [finite supplier chain](MINIMUM-ESCAPE.md#fixed-core-prime-lifting-proposition); one guaranteed supplier is spent per step. It gives $30\mid n_0,\ldots,n_H$. Every multiple $x$ of 30 has $s(x)/x\ge s(30)/30=42/30$ by scaling the proper divisors of 30. Hence all the claimed steps set records, including the step *out* of $n_H$.

**Now force the arrivals.** [Proposition K](GLOBAL.md#proposition-k--finitely-many-adjacent-pairs-with-fixed-prime-support) says that, for each finite set $S$ of primes, only finitely many distinct sources have both source and successor supported on $S$. Its proof uses the classical S-unit theorem. Apply it with $S$ containing the seed primes and all primes up to a chosen bound. As $e\to\infty$, the largest prime factor of $n_1(e)$ therefore tends to infinity, **even along any infinite arithmetic progression of exponents**.

To force many such primes *at once*, note the exact identity

$$6 n_1(e)=(7\sigma(D)-6D)7^e-\sigma(D).$$

On the current progression choose an exponent $e_*$ with some prime $\ell\mid n_1(e_*)$ larger than $Y$, the seed primes, and all previously selected primes. Restrict the progression to $e\equiv e_*\pmod{\ell-1}$. This still leaves an infinite progression (use the least common multiple of its old period and $\ell-1$). Since $\ell>7$, Fermat’s theorem and the identity preserve $\ell\mid n_1(e)$ on it, without disturbing earlier selections. After $K$ refinements all $K$ primes occur in the **same first image**. No primality of a later term or uniform bound from the S-unit theorem is assumed.

For example, $30\cdot29\cdot7^5=14{,}622{,}090$ maps to $30\cdot53\cdot107\cdot163=27{,}731{,}190$ and then to $41{,}133{,}066$. All three incoming primes exceed 29; 5 is still present when the second record is made. In the general construction the arrival primes need not persist, and no fresh arrival at *every* subsequent step is asserted. Varying $H$ need not keep $D$, let alone the starting number, fixed. Thus no fixed cutoff and minimum count of new primes forces 5 to be absent from one of the next $H$ record-making sources for a fixed $H$. This does not bound the frequency of such bursts on a single orbit or refute a cap depending on the numerical seed.

## When a large prime really does force a return on one orbit

Consider an **infinite actual tail** $n_i=D_i p_i$, with $D_i$ in a finite set $\mathcal D$ of integers greater than 1, and each $p_i$ prime and coprime to $D_i$. A word $w=D_0D_1\cdots$ is *recurrent* if every finite prefix occurs arbitrarily far to its right. Equivalently every finite block recurs arbitrarily late: extend a block back to the start and use recurrence of that prefix. Every suffix of a recurrent word is therefore recurrent. Neither a period nor a bound on return times is required.

**Claim.** If the core word of the tail is recurrent, the aliquot values are periodic from the start of that tail. This extends [Proposition P](RECOVERY.md#proposition-p--periodic-fixed-core-schedules-cannot-escape) beyond periodic schedules, but does not retain its bound on the period. The argument below is elementary finite-group arithmetic, motivated by the fixed-step test above, not a theorem about aliquot sequences in Alpöge’s archive.

**Return lemma for changing steps.** Attach a permutation of a fixed finite set to each letter of a recurrent word. Let $P(t)$ be the composition of the first $t$ permutations, applied in time order, stopping just **before** letter $t$. For every desired prefix length there are arbitrarily late matches at times $t$ with $P(t)$ the identity.

To see this, call a permutation $a$ a return value if for every length and every lower time bound there is a matching return with product $a$. At least one exists: take successively longer, later matches and use finiteness. Return values are closed under composition. Given $a,b$, first choose a match at $k$ of the desired length $L$ with product $b$. Then choose an arbitrarily late match at $m$ of length $k+L$ with product $a$. The next $k$ maps at $m$ are exactly the original first $k$ maps. Thus $m+k$ matches the desired prefix with product $b\circ a$. Positive powers of a return value are return values, and one such power is the identity. This is why repetition of a *letter* or a single graph cycle alone does not suffice.

**Use a prime already on the orbit.** Multiplicativity gives $n_{i+1}=F_{D_i}(n_i)$ where

$$F_D(x)=\frac{s(D)}{D}x+\sigma(D).$$

Modulo any prime $\ell$ not dividing $\prod_{D\in\mathcal D} D\,s(D)$, every $F_D$ is a permutation: the denominator and the slope are units. If this tail escaped, all its terms would be distinct and tend to infinity. Since the cores are bounded, the $p_i$ would tend to infinity as well. Pick $j$ with $\ell=p_j$ outside the finite excluded set. Start the return lemma at $j$ and request a one-letter match. At some later time $k$, **both** $D_k=D_j$ and $n_k\equiv n_j\equiv0\pmod\ell$. Since $n_k=D_jp_k$ and $\ell\nmid D_j$, primality forces $p_k=\ell$. Thus $n_k=n_j$, contradicting escape. This forbids unboundedness, not genuine cycles. For the stated stronger conclusion, apply the same lemma at the recurrent start with an otherwise admissible prime larger than every value in the now bounded tail: a later congruent value must equal its starting value.

Why both parts of the return matter: $276=12\cdot23\to396\to696\to1104=48\cdot23$ revisits zero modulo 23, **not** the same integer. And if the cofactor is allowed to be composite, even a matching core and divisibility by $\ell$ need not determine it. Finiteness of a core alphabet also does not imply recurrence of any actual suffix (think of two symbols with successively longer runs between markers). A recurrent limiting word need not be the itinerary of this seed.

**Stopping point.** Infinitely many distinct primes and frequent reuse are compatible, even with the stronger finite arrival property above. A prime actually encountered on one orbit gives a contradiction in the recurrent prime-cofactor case. We have no argument that every hypothetical escape admits that description, nor a seed-dependent cap on the original record counts. [Exact example checks](../tests/test_alpoge_prime_arrivals.py) are separate from both proofs; run `python3 -m unittest discover -s tests -p 'test_alpoge_prime_arrivals.py' -v`.

[mean]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/BehrendSets/Statement.lean#L78-L80
[window]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/BehrendSets/Statement.lean#L63-L75
[index]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/BehrendSets/BehrendVariance/SpaceFreeOfBehrendFree.lean#L11-L22
