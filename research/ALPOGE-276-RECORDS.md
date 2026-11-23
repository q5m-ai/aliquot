# A fixed open orbit: what can be proved past the factorization frontier of 276?

**Term 2164 is the first 216-digit term of the 276 sequence, and terms 2163 through 2166 all set strict records.** These conclusions use the published prefix, with 276 at index zero. They do not require the factorization of the remaining 210-digit composite or give the exact values of those four terms. I did not find a merger with a resolved orbit, a cycle, or a proof of escape.

The idea taken from [Alpöge’s Lean archive][hankel] is different from the finite digit calculation: an integer determinant can detect the difference between finitely and infinitely many records **on one seed**. Even one very large nonzero determinant can be certified here. The unresolved part is controlling the determinants at **all** sufficiently large orders.

## Four records without computing four more divisor sums

Write $s(n)=\sigma(n)-n$ and $n_0=276$. The [FactorDB snapshot][fdb] ends at the partially factored term $M=n_{2162}=DC$, where

$$D=2\cdot3^3\cdot41\cdot89=197046,\qquad A=\sigma(D)=453600.$$

Here $C$ is the exact integer in the [arithmetic fixture][checks], not an unspecified semiprime. From its decimal expansion, $C\equiv179327\pmod{201600}$ and $\gcd(C,D)=1$. The [OEIS b-file][bfile] gives the prefix through 2157; its maximum there is $n_{2157}$. The overlapping FactorDB entries agree and the next five entries increase up to $M<10^{215}$. We use this published identification and prefix maximum, **not** an independent refactorization of 2162 historical steps. The normalized prefix (ASCII `index value\n` in order, indices 0–2162) has SHA-256 `90f6782d4307f88420e78f66d8fe9430ee8e9b6c528cc276cdae2c91c79bd759`.

1. Since $C\equiv-1\pmod{24}$, it is not a square. Pair $d\mid C$ with $C/d$. Each $d$ is its own inverse modulo 24, so every pair sums to zero there. Thus $24\mid\sigma(C)$. Multiplicativity gives
   $$n_{2163}=54U,\qquad U=8400\sigma(C)-3649C\equiv29377\pmod{201600}.$$
   In particular $U$ is coprime to 54 and is 2 modulo 5. The first increase follows already from $n_{2163}=A\sigma(C)-DC>(A-D)C>M$.
2. Since $U$ is an odd nonsquare (use modulo 5), $\sigma(U)$ is even, by divisor pairing. Now $\sigma(54)=120$, so
   $$n_{2164}=6V,\qquad V=20\sigma(U)-9U\equiv7\pmod{40}.$$
   Also $n_{2164}>(11/9)n_{2163}$, using $\sigma(U)>U$.
3. The odd part of $6V$ is $3V\equiv5\pmod8$, again a nonsquare. Consequently $n_{2165}=3\sigma(3V)-6V$ is still a multiple of 6. Every multiple $x>6$ of 6 satisfies $s(x)>x$: the proper divisors $x/2,x/3,x/6$ already sum to $x$, and 1 is another. Apply this at both $n_{2164}$ and $n_{2165}$. This proves the four strict increases, hence four records because $M$ was a record.

**Which step crosses $10^{215}$?** Checking $\gcd(C,1000!)=1$ requires no factorization. Since $1001^{70}>C$, there are at most 69 distinct prime factors of $C$, so $\sigma(C)/C\le(1001/1000)^{69}$. Substitution gives the exact comparisons

$$n_{2163}\le [A(1001/1000)^{69}-D]C<10^{215}<\tfrac{11}{9}(A-D)C<n_{2164}.$$

The crossing does not skip straight to 217 digits. Indeed $U<10^{214}$, with $\gcd(U,210)=1$. At most 98 distinct prime divisors exceed 150, since $151^{99}>10^{214}$. Bounding each Euler factor for $\sigma(U)/U$ by $p/(p-1)$ gives

$$\frac{\sigma(U)}U\le \prod_{11\le p\le150\;\mathrm{prime}}\frac p{p-1}\;(151/150)^{98}<4.$$

Thus $n_{2164}/n_{2163}=(20/9)\sigma(U)/U-1<8$, enough. All comparisons above are checked by integer arithmetic in the fixture.

**Why not continue by induction?** One sufficient condition for a fifth increase is $8\mid\sigma(3V)$. Then $n_{2165}=6W$ with $W=\sigma(3V)/2-V\equiv1\pmod4$. Its odd part $3W\equiv3\pmod4$ is nonsquare, so $6\mid n_{2166}$ and $n_{2167}>n_{2166}$. This condition holds if $3\nmid V$, since then $\sigma(3V)=4\sigma(V)$ and $V\equiv7\pmod8$ is nonsquare. But the input congruence and small-prime exclusions do not even decide whether $3\mid V$. Replace $C$ by $4614527=1471\cdot3137$ or $16307327=1031\cdot15817$. Both match $C\bmod201600$ and are coprime to $1000!D$; the two exact formulas give $V=290719006007$ and $864212542407$, respectively, only the latter divisible by 3. They are controls, not the 210-digit cofactor. Nor is $V\equiv7\pmod{40}$ a permanent growth rule: $V=87$ gives $522\to648\to1167\to393$, and then reaches zero. This control starts at the $6V$ stage; it is not asserted to be a second image of $DC$ or a term of 276. Even on the actual 276 orbit an earlier retained divisor, 28, was lost at index 170 [during an increase](HILBERT-DRIVERS.md).

[Following the divisors further](276-DIVISOR-GROWTH.md) proves that the run of records must cross $1.23\times10^{215}$ before it can stop increasing. If 2167 is not another record, 2166 already exceeds twice $M$. A comparison starting at the full $197046C'$ shape loses 3 and drops on step five; it is not the actual $C$.

## An archive determinant with a hypothesis about just this seed

Fix **one** seed $N$. Put $b_m=1$ if the integer $m$ is a strict record value, including the seed as the first record, and $b_m=0$ otherwise. The index $m$ is a **height**, not a step number. Unlike “is $m$ ever visited?”, each bit has a finite decision procedure: stop at the first term $\ge m$, at zero, or at a repeated value below $m$. Only reaching exactly $m>0$ at that first crossing gives 1. There cannot be infinitely many distinct terms below $m$.

For any fixed integer offset $L\ge0$ form the ordinary power series and its leading Hankel determinants

$$B_{N,L}(z)=\sum_{j\ge0}b_{L+j}z^j,\qquad H_n=\det(b_{L+i+j})_{0\le i,j\le n}.$$

**Fixed-seed test.** The orbit terminates or repeats **if and only if** every sufficiently late $H_n$ is even. In the other case, infinitely many $H_n$ are odd. Over the complex numbers the same series is either a polynomial (termination or repetition), or has the entire unit circle as a natural boundary (escape).

Here are the two inputs to the test.

* **Aliquot arithmetic rules out an infinite periodic tail of bits.** For each $h\ge1$, choose $h$ pairwise coprime products $d_0,\ldots,d_{h-1}$ of distinct primes, each with $\prod_{p\mid d_i}(1+1/p)>3$. This is possible by divergence of the sum of reciprocals of the primes after finite exclusions. CRT supplies arbitrarily large $x>2h$ with $d_i\mid x+i$. At each of $x,\ldots,x+h-1$, the abundancy is at least that of its prescribed divisor, so $s(x+i)>2(x+i)$. If none of those heights is a record, we have $h$ consecutive zeros. If one is a record, its very next term exceeds $x+2h$, so all of $x+h,\ldots,x+2h-1$ are nonrecords. Thus arbitrarily far out there are arbitrarily long runs of zeros, for this same seed, whether or not it escapes. If it escapes there are also infinitely many ones. An eventually periodic binary word cannot have both properties.
* **Apply the pinned lemma over the two-element field.** In [the definitions][defs], `hankel c n` has size $n+1$, and `IsRat` means $Q\phi=P$ for polynomials with $Q\ne0$. The [theorem][hankel] assumes that **all** these leading determinants are zero from some order on; its [proof][annihilator] obtains one annihilating polynomial for every shift of the coefficients. Reduce our integer determinants modulo 2. Eventual evenness gives exactly its hypothesis. A rational series over $\mathbb F_2$ has eventually periodic coefficients: cancel powers of $z$ from the denominator, then its nonzero constant term gives a forward recurrence; a finite block determines the next bit and there are finitely many blocks. This contradicts the preceding paragraph on escape. Conversely, on termination or repetition the record set is finite. Beyond its last index the Hankel matrix has a zero last row. The offset $L$ is held fixed in both directions.

The analytic conclusion is the classical finite-alphabet theorem of Szegő ([Breuer–Simon, Theorem 5.1][szego]), **not** a deduction from RH. An infinite, non-eventually-periodic binary series cannot be continued analytically across even one open arc of the unit circle. It would therefore suffice to continue $B_{276,0}$ across a neighborhood of, say, $-1$. A value or radial limit at one point is not such a continuation.

**A nonzero determinant proved on 276 itself.** Put $g=(A-2D)C=59508C>2\cdot10^{214}$ and choose the fixed offset $L=M-g>0$. The lower bound for $n_{2163}$ proves that the record $M$ is followed by a jump **past** $M+g$. Thus $b_M=1$ and $b_{M+1}=\cdots=b_{M+g}=0$, irrespective of later drops. At order $g$ the anti-diagonal is all ones and everything beyond it is zero. Reversing the columns proves

$$H_g=(-1)^{g(g+1)/2}=1.$$

There is no enormous matrix computation here. The same argument at the early record $1872\to3770>2\cdot1872$ gives $H_{1872}=1$ at offset zero. Neither is evidence for infinitely many odd determinants. In fact even on a **resolved** orbit with largest record $R$, the determinant at offset zero and order $R$ is $\pm1$, followed exclusively by zeros. In particular the cutoff has an exact interpretation: at offset zero, for each $K\ge0$, **all $H_n$ with $n>K$ are even if and only if no term exceeds $K$**. This is not a shorter search for a cutoff. To use it one needs a parity argument independent of the orbit maximum. The CRT intervals alone do not force nonzero determinants either: this orbit might skip a prescribed interval altogether.

## The missing arithmetic, not a larger determinant calculation

The archive’s [Landau positivity lemma][landau] needs an **independent analytic continuation** matching the initial transform; in [the zeta application][phi] a logarithmic-derivative identity provides it. For the record bits one can literally set $h(x)=b_m$ on $[2^m,2^{m+1})$ for $m\ge0$. For $\Re w>0$, its positive-input Mellin transform is $(1-2^{-w})B_{276,0}(2^{-w})/w$. At $w=0$ each record contributes exactly $\log 2$ to the integral. This detects escape, but supplies no independent continuation.

There is a specific obstruction to substituting a finite list of multiplicative functions for the aliquot step in this transform. Even for the **first** record after $Dpq$, with $D=197046$ as above and $p,q$ distinct new primes, the weight $2^{-s(Dpq)}$ is not a finite linear combination of multiplicative functions of $Dpq$ on this family. Indeed every $Dpq$ is abundant. Taking $p,q$ in two disjoint infinite sets of primes away from $D$, the rows indexed by $p$ are

$$q\longmapsto 2^{-A(p+1)}\bigl(2^{-((A-D)p+A)}\bigr)^q.$$

Arbitrarily many rows are linearly independent: in a proposed relation divide by the largest exponential base with nonzero coefficient and let $q$ tend to infinity along its prime set. In contrast a sum of $k$ multiplicative functions gives a matrix of rank at most $k$ by separation at $D,p,q$. This rules out that particular global shortcut, **not** an orbit-specific identity; it does not assume that the real $C$ has two prime factors.

To settle 276 this way would require an arithmetic reason that its leading determinants eventually vanish modulo 2, or remain odd at infinitely many orders at one fixed offset. We have neither. The four records and the digit crossing are statements about the actual sequence; the infinite alternatives are a criterion, not a verdict. No RH/GRH or prime-tuples assumption is used, and we did not build or verify the announced RH proof.

[Follow-up: an attempt to prove eventual evenness](ALPOGE-276-PARITY.md) fits a recurrence over the two-element field and uses the aliquot map to force its first error. It gives an explicit finite parity test for each proposed ceiling and a finite interval containing an odd leading determinant at offset zero on 276; it does not establish eventual parity.

[Offline exact checks][checks]: `python3 -m unittest discover -s tests -p 'test_276_record_determinants.py' -v`. They check the two published decimal fields against one another, partial-factor bounds, small control orbits by both factorization and divisor pairs, and small Hankel matrices over the binary field. They do not factor $C$, audit the whole database prefix, or check an asymptotic criterion by sampling.

[fdb]: https://factordb.com/sequences.php?se=1&aq=276&action=last20&fr=0&to=100
[bfile]: https://oeis.org/A008892/b008892.txt
[checks]: ../tests/test_276_record_determinants.py
[defs]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Development/AbelianVarietyTheory/Definitions/Divisors/IsAdmissibleIntegralBasisChangeOne.lean#L53-L56
[hankel]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/IsRatOfHankelEventuallyZeroStatement.lean#L10-L11
[annihilator]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/IsRatOfHankelEventuallyZero.lean#L66-L93
[szego]: https://arxiv.org/abs/1002.0823
[landau]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/ZetaRealNonvanish.lean#L20-L27
[phi]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/ZetaNonvanishing/ZetaLandau.lean#L100-L113
