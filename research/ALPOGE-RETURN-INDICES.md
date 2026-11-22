# Comparing two stretches of one aliquot orbit

Two operations in Alpöge's pinned Lean archive give restrictions on a *single* orbit of the form $6p_iq_i$, where $3<p_i<q_i$ are primes. First, a long initial list of smaller primes cannot start again too soon, even if the list uses unboundedly many different primes as its length grows. Second, if the two prime factors stay comparable, every sufficiently large doubling forces some smaller prime to lead to many **different** next smaller primes. Neither argument assumes that the orbit is random. Neither forces it to leave this form.

The source operations are the [signed lattice index `IdxAdd` and `IdxDet`][idx] (with the [additivity][idx-add] and [determinant proofs][idx-det]), and the [Vandermonde split][split] into within-group and between-group differences. The archive also [performs such a split][split-proof] in its compact/noncompact torus calculation. These are classical identities used inside the archive. The choice to apply them to **differences of aliquot values**, the prime weights below, and the doubling estimate are the adaptations here; they are not claims in the archive. We inspected the linked sources at `9d5316ec73f5df89c4d95703ed106837b8a4060e`, not a build of the full announced proof. Neither RH nor Dirichlet GRH is needed.

## What cancels when an ordered list repeats?

Divide each term by 6 and write $u_i=p_iq_i$. At such a source the [exact aliquot step](SIX-SEMIPRIME-RETURNS.md) in cofactor coordinates is

$$u_{i+1}=F_{p_i}(u_i),\qquad F_p(x)=\frac{p+2}{p}x+2(p+1).$$

For a list $w=(p_0,\ldots,p_{h-1})$ of smaller primes write $S_j=\prod_{i<j}(p_i+2)/p_i$, including $S_0=1$. If entries $x,y$ follow the **same ordered list**, their difference after $j$ steps is exactly $S_j(y-x)$: the translation cancels at each step. The output at the end need not be a semiprime. Write $S_j=A_j/B_j$ in lowest terms. Then $B_j\mid y-x$ for every $j\le h$.

This is where the signed index matters. For each prime $r$, take the discrete valuation ring $O=\mathbb Z_{(r)}$ inside $\mathbb Q$, in dimension one. The archive's convention gives $\operatorname{idx}(O,S_jO)=v_r(S_j)$: a positive index for multiplication by $r$, a negative one for division by $r$. By additivity along the successive lattices,

$$v_r(S_j)=\sum_{i<j}\big(v_r(p_i+2)-\mathbf1_{p_i=r}\big).$$

Only **after** that sum is it legitimate to take the negative part for $v_r(B_j)$. Given one integral realization, the allowed starting differences for integrality of *all* formal steps are exactly the multiples of $\operatorname{lcm}_{j\le h}B_j$; this is not sufficient for primality. For example the actual steps $7\cdot11\to5\cdot23\to173$ have prefix slopes $9/7,9/5$: the final denominator is 5, not 35, although both prefixes together require 35.

### A denominator large enough to beat real growth

For **every** length-$h$ list of primes $>3$, whether realized or not, we have

$$\boxed{\quad B_h\ \ge\ c^h S_h,\qquad c=507/400>1.\quad} \tag{1}$$

In particular the bound is independent of the number and size of the primes in the list. To prove it, take a completely multiplicative positive weight $d$ with $d(2)=2$, $d(3)=3$, $d(7)=4$. For other primes $r>3$ use $d(r)=3/2$ if $r\equiv2\pmod3$ and $d(r)=8/3$ if $r\equiv1\pmod3$. Then $H(n)=n/d(n)$ satisfies $1\le H(n)\le n$. By multiplicativity,

$$\frac{B_h}{S_h}\ \ge\ \frac{H(B_h)}{H(A_h)S_h}=\prod_{i<h} K(p_i),\qquad K(p)=\left(\frac p{p+2}\right)^2\frac{d(p+2)}{d(p)}.$$

The five rows exhaust the letters. In the composite row all prime factors of $p+2$ exceed 3. In the last row $(p+2)/3>1$ has weight at least $3/2$.

| Smaller prime $p$ | Lower bound for $K(p)$ |
|---|---:|
| $5$ | $(5/7)^2(8/3)=200/147$ |
| $7$ | $(7/9)^2(9/4)=49/36$ |
| $p\equiv2\pmod3$, $p>5$, $p+2$ prime | $(11/13)^2(16/9)=1936/1521$ |
| $p\equiv2\pmod3$, $p+2$ composite (so $p\ge23$) | $(23/25)^2(3/2)=1587/1250$ |
| $p\equiv1\pmod3$, $p>7$ (so $p\ge13$) | $(13/15)^2(27/16)=507/400$ |

Taking the minimum proves (1). No optimality of the constant is claimed.

### How soon can one seed repeat its prefix?

Suppose the first $h$ smaller primes of a given run appear again starting at step $k>0$, and the run stays in the required form through both lists of sources. All $S_j$ below refer to the list read from that seed. Strict growth and the difference identity give $0<B_h\le u_k-u_0$. For the real size, $u_{i+1}=(p_i+2)(q_i+2)-2<(1+2/p_i)^2u_i$, so $\sqrt{u_i}/S_i\le\sqrt{u_0}$. Hence

$$\frac{u_{i+1}}{S_{i+1}}-\frac{u_i}{S_i}=\frac{2p_i(p_i+1)}{(p_i+2)S_i}<\frac{2p_i}{S_i}\le 2\sqrt{u_0}.$$

Since each slope is at most $7/5$, summing and combining with (1) gives the **finite, seed-specific test**

$$\boxed{\quad c^h<(u_0+2k\sqrt{u_0})\,(7/5)^{\max(k-h,0)}.\quad} \tag{2}$$

Thus at a fixed seed only bounded lengths can occur twice back-to-back ($k=h$), or overlap ($k<h$). More generally on a hypothetical infinite run let $R(h)$ be the first positive starting step of a matching prefix, or $\infty$ if it never matches. Taking logs in (2) along any subsequence with $R(h)/h$ bounded gives

$$\liminf_{h\to\infty}\frac{R(h)}h\ \ge\ 1+\frac{\log(507/400)}{\log(7/5)}\ >\ 1.7.$$

This is a start-to-start delay, not a gap of $1.7h$ *after the end* of the first block. It excludes nonperiodic schedules with arbitrarily many distinct smaller primes: for example, take distinct primes $r_0,r_1,\ldots>3$ and prescribe the label $r_{v_2(i+1)}$ at step $i$. Its length-$(2^t-1)$ prefix repeats at lag $2^t$, since $v_2(2^t+j)=v_2(j)$ for $1\le j<2^t$. No seed can follow that whole schedule. Nor can two **distinct** integer entries realize the same infinite ordered list: their nonzero difference would have to be at least $B_h\ge c^h$ for every $h$.

There is also a conditional answer about **one fixed prime**. If $R(h)\le Kh$ for infinitely many $h$ and one fixed $K$, some fixed prime must occur with positive upper frequency, in infinitely many separate visits. Otherwise, if every fixed prime has upper frequency zero, split $\log(u_k/u_0)<\sum_{i<k}4/p_i$ at a fixed prime cutoff $L$. The finitely many small primes contribute $o(k)$; the rest contribute at most $4k/L$. Let $L\to\infty$ to get $\log u_k=o(k)$. But for $k=R(h)\le Kh$, the input difference requires $u_k> B_h\ge c^h$, a contradiction. The visits cannot all end in an infinite constant block, by the infinite-list uniqueness just proved. Thus if every prime makes only finitely many visits, the prefix return time divided by $h$ must tend to infinity. We have not proved the linear-return hypothesis for an arbitrary orbit.

Short matches really occur. At $u_0=235$ the successive cofactors are $235,341,427,565,803,973,1267$: the smaller-prime list $(5,11,7)$ occurs twice back-to-back. Its slope is $117/55$, and the difference of inputs $565-235=330$ is taken to $1267-565=702$. **Order cannot be discarded.** At $18293\to21643\to23573\to27883$, the lists $(11,23)$ and $(23,11)$ have the same slope $325/253$, but $253\nmid21643-18293$. Different orders have different translations.

## When the same prime returns with different continuations

At each occurrence of smaller prime $p$, label its partner $q$ by the *next* smaller prime $r$, if the next term is still of the required form. Then $r\mid(p+2)q+2(p+1)$, and $r\nmid p+2$ since otherwise this expression is $-2\bmod r$. Thus **every visit with the same ordered pair $p\to r$ puts $q$ in a single residue class modulo $r$**, also when $r=p$. All those partners are distinct on our growing run.

To combine this information, form the Vandermonde determinant in the partners at a fixed $p$, whose absolute value is $|V|=\prod_{i<j}|q_j-q_i|$. [Split it by labels][split]: write $t_r$ for the number carrying label $r$. Each within-label difference contributes a factor $r$; the cross-label differences are integers. Repeated splitting gives $\prod_r r^{\binom{t_r}{2}}\mid V$. One must not count a factor from every pair regardless of label. For instance, $15095\to21145\to29615\to41473$ has visits at $p=5$ with partners $3019,4229,5923$ and labels $5,5,67$. Only the first pair's difference is divisible by 5; none is divisible by 67.

Even counting shared factors of the *whole* successors need not help. Set $L_p(q)=(p+2)q+2(p+1)$. Since $\gcd(L_p(q),p+2)=1$, subtracting the two outputs gives $\gcd(L_p(q),L_p(z))=\gcd(L_p(q),z-q)$. On the [actual run from $6\cdot3707$](SIX-SEMIPRIME-RETURNS.md), the three cofactors following visits to 11 are $5\cdot881$, $73\cdot107$, and $23\cdot421$. They are pairwise coprime. Thus not one shared output prime can be charged to those three pairs of visits.

**A restriction on one doubling.** Suppose we have a run from $u_0$ through the first crossings $a,b$ of $X,2X$, respectively, with the two-prime form still valid at $b$. Take $X>\max(u_0,120)$. Let $H_X=\max_{a\le i\le b} q_i/p_i$ measure how unequal the partners are. Let $D_X$ be the maximum, over $p$, of the number of **distinct** labels $r$ following it in $a\le i<b$. Then for an absolute constant $c_0>0$ and all sufficiently large such $X$,

$$\boxed{\qquad D_X H_X\ \ge\ c_0\log X.\qquad} \tag{3}$$

Here the useful part of the split is already visible in each pair of columns: partners with the same label are spaced at least $r$ apart. In $[X,2X)$ an edge $p\to r$ therefore occurs at most $1+X/(pr)$ times. Put $P=\sqrt{X/H_X}$. If $H_X>\sqrt X$, (3) holds since $D_X\ge1$ (the crossings are distinct as shown below). Otherwise $P\ge X^{1/4}$, and both $p$ and $r$ are at least $P$ because their cofactors are at least $X$. This is why $b$ is included in the definition of $H_X$.

There is no large overshoot at entry: $F_p(pq)\le F_5(pq)$ since the difference is $2(p-5)(q/5-1)\ge0$. Thus $u_a<(7/5)X+12<3X/2$ and the log gain to $u_b$ exceeds $\log(4/3)$. Each step contributes less than $4/p$ since $q>p+1$. Sum over admissible labels, using $p\le\sqrt{2X}$, so $1\le\sqrt2\,X/(pP)$:

$$\log(4/3)<4D_X\sum_{P\le p\le\sqrt{2X}}\frac1p\left(1+\frac X{pP}\right)\ \ll\ \frac{D_X X}{P}\sum_{p\ge P}\frac1{p^2}\ \ll\ \frac{D_X H_X}{\log P}.$$

Both sums are over primes. The last inequality uses only the classical upper bound $\pi(t)\ll t/\log t$: summing over $[2^jP,2^{j+1}P)$ gives $\sum_{p\ge P}p^{-2}\ll1/(P\log P)$. Since $\log P\ge(\log X)/4$, this proves (3). In particular, an infinite run with uniformly comparable factors would need some smaller prime to lead to at least a constant times $\log X$ **different** smaller primes during each large doubling. All but at most one of those labels end a consecutive stretch at that $p$: a surviving $p$ is still the smaller prime. Thus the bound demands many **separate visits in the same doubling**, although the prime witnessing it can change with $X$. This is not a distribution statement over starting seeds.

**What's still missing.** The [previous necessary condition](SIX-SEMIPRIME-RETURNS.md) counts *separate visits to one prime*. Long matching lists are much stronger. Even symbolically a list $5,r_1,5,r_2,\ldots$ with distinct fresh $r_i\ne5$ revisits 5 without repeating any ordered pair; this is not asserted to be an aliquot orbit. The split estimates visits that share a next label and trades the number of labels against factor imbalance; it does not bound either quantity from the seed.

We also checked a more specialized symmetry in the same source: [`CayleyDifference` and `ResultantConjugate`][conjugate]. The Cayley coordinate $(g-1)/(g+1)$ of a forward slope $g=(p+2)/p$ is exactly $1/(p+1)$. But `ResultantConjugate` requires a field endomorphism to permute the slopes in each list into their reciprocals. These slopes are rational, hence fixed by any such endomorphism, and all are greater than 1. No nonempty forward list has that symmetry. Inserting inverse maps would add steps not known to occur on the orbit. This rules out that direct use of the stronger identity, not a different encoding. We have neither a perpetually surviving seed nor a general exit proof.

[Independent finite arithmetic checks](../tests/test_alpoge_return_indices.py): `python3 -m unittest discover -s tests -p 'test_alpoge_return_indices.py' -v`. They verify the examples and boundary computations, not the infinite-orbit conclusions.

[idx]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/LogFactorialIndices/StatementIdx.lean#L24-L54
[idx-add]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/LogFactorialIndices/SignedSubspaceIndex/IdxBase.lean#L159-L171
[idx-det]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/LogFactorialIndices/SignedSubspaceIndex/IdxDet.lean#L271-L292
[split]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/ResultantValuation/ResultantConjugate.lean#L35-L39
[conjugate]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/ResultantValuation/ResultantConjugate.lean#L13-L25
[split-proof]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/VandermondeSplitsCompactNoncompact.lean#L59-L85
