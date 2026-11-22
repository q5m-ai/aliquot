# Trying to prove eventual evenness for 276

**Result on 276.** At offset zero, at least one leading Hankel determinant of the record indicators is odd at an order $n$ satisfying

$$10^{215}< n \le 24(10^{215}+1). \tag{1}$$

This is an existence result in a finite interval, not the computation of a determinant of that size. It uses the published orbit prefix and the [arithmetic inequalities at its last partially factored term](ALPOGE-276-RECORDS.md). It holds even if 276 eventually terminates. I did **not** prove eventual evenness or its negation.

The attempt in the other direction gives a finite sufficient test: for a proposed upper bound $K$, there is an explicit interval $(K,W(K)]$ such that evenness **throughout that interval** proves evenness forever after $K$. The interval depends on $K$, not on unknown future orbit terms. We have not found a $K$ for which that test succeeds on 276.

## From a wrong prediction to an odd determinant

Write $b_m=1$ when height $m$ is a strict record on **one fixed orbit** (seed included), and 0 otherwise. The bits are indexed by integer size, not time. Each is decided by the first term at least $m$, or by an earlier termination or repetition. Write $H_n=\det(b_{i+j})_{0\le i,j\le n}$; its **size is $n+1$**. In the calculations below work over $\mathbb F_2$: nonsingular means the integer determinant is odd.

The [pinned archive proof][kronecker] turns eventual singularity into one polynomial annihilating every shift of the bits. Try instead to build such a polynomial and test its **first failed prediction**. Suppose size $r$ is nonsingular. The invertible $r\times r$ matrix determines a unique monic $P(X)=\sum_{j=0}^r P_jX^j$ for which

$$E_i:=\sum_{j=0}^r P_j b_{i+j}=0\qquad(0\le i<r).$$

Start with the first $r$ bits and impose this recurrence forever to get a predicted sequence. Its agreement with the real bits lasts at least through $2r-1$. If $E_s=1$ is the first failure, its first wrong bit is at height $h=s+r$ and **$H_s$ is odd**. To see this, use $\ell(X^m)=b_m$ and the bilinear form $(U,V)\mapsto\ell(UV)$. In dimension $s+1$ use the monic basis

$$1,X,\ldots,X^{r-1},\ P,XP,\ldots,X^{s-r}P.$$

The two blocks are orthogonal since the cross entries are $E_i$ with $i<s$. In the second block $\ell(X^{i+j}P^2)=\sum_kP_k E_{i+j+k}$ is zero for $i+j<s-r$ and one on $i+j=s-r$. Column reversal makes this block triangular with unit diagonal. Thus the full matrix is nonsingular. In any intermediate dimension $r<t\le s$, $P$ itself gives a null vector since $E_0,\ldots,E_{t-1}$ are zero. This is a finite linear-algebra argument, not a new Lean verification.

For example, $276\to396\to696\to1104$ fixes every bit through 718. At size $r=277$, $P=X^{277}+X^{157}+X^{37}$. The first wrong prediction is **a record at 636**: the actual record after 396 is 696. In row indices, $E_{359}=b_{636}+b_{516}+b_{396}=1$ and the earlier errors are zero. Thus $H_{276}$ and $H_{359}$ are odd, and all the intervening determinants are even. Extending the initial stretch of even determinants would give the wrong answer here.

## Ruling out the cutoff $K=10^{215}$

Use $u=n_{2163}$ and $v=n_{2164}$, where $n_0=276$. The [fixed-orbit calculation](ALPOGE-276-RECORDS.md) gives **consecutive record heights** with $18\mid u$ and $u<K<v<8u$. No factorization of $u$ or exact value of $v$ is assumed.

Choose the largest nonsingular **size** $r\le K+1$. There is one: at size 277 the first 276 bits are zero and $b_{276}=1$, giving a triangular matrix after column reversal. Any failure of the predictor now gives an odd $H_{h-r}$ with $h-r>K$ by maximality. We need an *upper* bound on its first failure, not just the abstract fact that it cannot continue forever.

Factor $P=X^e Q$ with $Q(0)=1$, and put $w=r-e$. From height $e$ on, the predictor follows the width-$w$ recurrence $Q$. If $w=0$ it predicts only zeros there. Otherwise its companion matrix $T$ is invertible; extend this tail to a two-sided word $a_m$ by running $T$ backwards. Every section $a_{D j}$ obeys the characteristic polynomial of $T^D$, of degree $w$ with nonzero constant term. Thus in any **nonzero** such section, $w$ consecutive zeros are impossible: they propagate both ways. This includes the unthinned word ($D=1$).

* If $e>u$, the row $i=v-r\ge0$ has error one: its leading term hits $b_v=1$, and all lower supported terms hit heights strictly between the consecutive records $u$ and $v$. Thus a discrepancy occurs by height $v<8K$.
* Suppose $e\le u$. If the predictor is wrong at or before $u$ there is nothing further to show. Otherwise $a_u=1$ (a zero tail is already excluded), so the section on multiples of 18 is nonzero. Every such multiple $y$ satisfies $s(y)\ge7y/6$, by scaling the proper divisors of 18. A record at $y>6w$ therefore forces the next $w$ ordinary height bits to be zero. That contradicts a nonzero width-$w$ predictor. If $u>6w$, use $y=u$. Otherwise look at the first $w$ multiples of 18 strictly above $6w$. One has $a_y=1$, and $y\le24w$. Either it is not a record (a wrong bit), or the forced zeros after it contradict the predictor by $y+w$.

Thus in the second case the first failure is at $h\le\max(u+w,25w)$. Since $w\le r\le K+1$, its determinant order $h-r$ is at most $24(K+1)$. The first case also lies within this bound. This proves (1). It does not prove a later multiple-of-18 record, let alone infinitely many: the prediction can fail precisely **because the proposed height is not visited as a record**.

## A finite interval in which evenness would suffice

Here is a version for any seed $N$ and proposed integer ceiling $K\ge N$. It does not require a known multiple-of-18 record near $K$. Let $R=K+1$, $k=\lfloor\log_2 R\rfloor$, and $p_i$ be the $i$th prime ($p_1=2$). Choose the least $J$ with $\prod_{i=k+1}^J(1+1/p_i)>2$. It exists by divergence of the sum of prime reciprocals. Put

$$W(K)=\max\left(K^2,\;2R\prod_{i=1}^J p_i\right).$$

**Claim.** The orbit never exceeds $K$ if and only if $H_n$ is even for every integer $K<n\le W(K)$. This does not give a faster algorithm than following the orbit up to its first crossing or repetition. Its purpose is to specify how much *parity information alone* suffices for a given ceiling.

If there is no crossing, $b_m=0$ for all $m>K$, giving a zero last row at all orders $n>K$. Suppose the orbit does cross. Again take the largest nonsingular size $r\le R$ (size $N+1$ always works). If the predictor's tail from $e$ is zero, it misses a record no later than the first crossing. That crossing is at height at most $K^2$: its source $x\le K$ has $s(x)\le x(x-1)/2$. Since $e\le K+1$, a crossing above $K$ cannot be predicted by this tail.

For a nonzero tail, we need an abundant divisor $D$ on whose multiples the predicted word is not identically zero. We cannot simply choose 18: a binary recurrence can avoid all multiples of 18. Here is a bound independent of the predictor.

1. Any section $f(j)=a_{Dj}$ has a space of translates of dimension at most $w\le r$, from its matrix representation with $T^D$. If $f$ is nonzero, **at most $\lfloor\log_2 r\rfloor$ distinct primes $q$ can have $f(qj)=0$ for every $j$**. Indeed, choose $a$ with $f(a)=1$ and $l$ such excluded primes $q_i$. By CRT take $t_i\equiv a\pmod{q_i}$ and $t_i\equiv0$ at the other chosen primes. For subsets $S$ write $t_S=\sum_{i\in S}t_i$. The matrix $f(a+t_S-t_U)$ has ones on the diagonal and zeros whenever $U\not\subseteq S$: for $i\in U\setminus S$ its argument is divisible by $q_i$. Ordering subsets by size makes it triangular, of rank $2^l$. Its rows are evaluations of translates of $f$, so $2^l\le r$.
2. Start with $D=1$. For each of $p_1,\ldots,p_J$ in order, multiply $D$ by that prime if the new section is nonzero. A rejected prime stays excluded on the final section: all later restrictions take subsets of the same multiples. Thus at most $k$ primes were rejected. Even removing the $k$ **largest factors** $(1+1/p_i)$ leaves a product greater than 2. The accepted squarefree $D$ therefore satisfies $s(D)>D$, and its section is nonzero.
3. Among $t=r+1,\ldots,2r$ the section predicts a one at some $m=Dt$, beyond the transient $e$. If this is an actual record, $s(m)\ge t\,s(D)\ge m+t>m+r$, forcing $r$ ordinary zeros and hence a discrepancy. If it is not a record, the predictor is wrong already. The first wrong bit is consequently at $h\le 2rD+r$, yielding an odd determinant of order $h-r\le2rD\le W(K)$ and $h-r>K$.

The size bound is explicit, albeit large: for each $\varepsilon>0$, $\log W(K)=O_\varepsilon((\log K)^{2+\varepsilon})$ as $K\to\infty$. Indeed [Mertens’ product estimate][mertens] gives $\prod_{p\le x}(1+1/p)\sim c\log x$ with $c>0$, since $1+1/p=(1-p^{-2})/(1-p^{-1})$. Thus for large $k$ we may stop by $x=p_k^{2+\varepsilon/2}$. The classical estimates $p_k=O(k\log k)$ and $\sum_{p\le x}\log p=O(x)$ give the result. This size estimate is not needed for the claim or (1).

**A shorter test if the fit actually predicts zero.** Let $M(x)=\max_{1\le y\le x}s(y)$. A zero-tail fit forces $e=r$ and $b_{r-1}=1$: otherwise its last row at size $r$ would be zero. Its polynomial is therefore $P=X^r$. The first wrong bit, if any, would be the very next record after height $r-1$, at some $h\le M(r-1)$ since its source is at most $r-1$. Thus once this fit is verified and $r$ is maximal as above, evenness just for $K<n\le M(r-1)-r$ suffices. Here $M(x)\le x\log x$ by $s(y)/y=\sum_{d\mid y,\,d>1}1/d\le\log y$. For a real warning on 276, size 1873 gives exactly the zero-tail fit: the record 1872 is followed by zeros through 3745, the end of the fitting interval. The very next record is 3770, so the fit fails and $H_{3770-1873}=H_{1897}$ is odd. The zero prediction itself is not the certificate.

**Stopping point.** A proof for 276 needs *one* ceiling $K$ at which the whole indicated interval is even, or an independent argument that its zero prediction persists. A nonzero binary recurrence cannot keep fitting an actual record tail: it predicts a record on multiples of an abundant divisor and then predicts another too soon. But rejecting that recurrence only forces the next odd determinant, not the next **actual** record above an arbitrary new ceiling. The zero tail cannot be rejected without a further crossing, nor established by the absence of one in a finite prefix. Neither an infinite sequence of crossings nor a last crossing has been proved. No RH or GRH assumption, new factorization or large determinant computation is used.

[Exact checks](../tests/test_276_record_determinants.py): `python3 -m unittest discover -s tests -p 'test_276_record_determinants.py' -v`. They include direct binary elimination at orders 275–359 from independently checked aliquot steps and a small rank-four periodic word that really does reject both 2 and 3. The word is not an alleged orbit. These checks do not certify an infinite tail.

[kronecker]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/IsRatOfHankelEventuallyZero.lean#L46-L93
[mertens]: https://mathworld.wolfram.com/MertensTheorem.html
