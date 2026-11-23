# A determinant bound, and what it takes for one aliquot orbit to set records

**Fixed-seed result.** If each odd prime divides at most $L$ of the terms whose **next** step sets a new all-time high, with the same $L$ for every odd prime, that orbit is bounded. There is no restriction on powers of 2, on prime exponents in a term, or on what happens between records. More quantitatively, before an orbit from a fixed seed can first reach a large level $B$, some odd prime must have divided at least $(1/2-o(1))\log B/\log\log B$ such sources, counting the step that crosses $B$. The prime may depend on $B$.

We got here in two stages. The determinant calculation below uses a specific rule in Alpöge’s released proof work: it gives a genuine size saving on a large set of characters, but not on the character we need. Factoring the divisor operator **on that character** gives the record bound. The latter argument is elementary aliquot arithmetic plus Mertens’ theorem; it is not an automorphic height theorem. Neither part assumes RH or GRH, verifies the announced proof, or settles the aliquot conjecture.

## What happens to the determinant?

Use the [previous fixed-orbit construction](ALPOGE-ORBIT-LIFT.md): $n_0=N$, $n_{j+1}=s(n_j)=\sigma(n_j)-n_j$ for $0\le j<h$, with $h\ge1$ and all sources $n_j>1$. Put $Q=\prod_{j<h}n_j$. Choose a prime $q>Q$ with $q\equiv-1\pmod{\operatorname{lcm}(8,Q)}$ by Dirichlet’s theorem. Every prime factor of $Q$ is a square modulo $q$ by quadratic reciprocity. The squares $H$ have odd order $b=(q-1)/2$; the odd characters modulo $q$ restrict bijectively to the $b$ characters of $H$, since $-1\notin H$. The quadratic character $\xi$ is the odd extension of the trivial character of $H$.

Write $R_df(x)=f(dx)$ on the units modulo $q$. On the space of odd functions each Gauss/adjoint pair acts by $q$. After removing this known scalar from each step, the chain is $T_h=\prod_{j<h}K_{n_j}$ with

$$K_n=\sum_{d\mid n,\ d<n}\frac d n R_d,\qquad k_n(\chi)=\sum_{d\mid n,\ d<n}\frac d n\chi(d).$$

The $k_n(\chi)$ are its one-step multipliers. In particular $T_h\xi=(n_h/N)\xi$ and $\|T_h\|=n_h/N$. We now use the archive’s [block and chain determinant rules][det]: the character lines form an internal direct sum, each of dimension one, preserved by every step. The determinant on any sum of these lines is the product of the corresponding multipliers, with the products over steps and characters interchangeable.

There is an independent bound for this product. Proper divisors of each source are distinct in $H$ (they are positive and smaller than $q$). Expanding the square and summing over characters kills every off-diagonal term:

$$\frac1b\sum_{\chi\ {\rm odd}} |k_n(\chi)|^2
  =\sum_{d\mid n,\ d<n}\frac{d^2}{n^2}
  =\sum_{a\mid n,\ a>1}\frac1{a^2}
  < \rho^2:=\zeta(2)-1 < \frac34.$$

For the last inequality even $1/4+\sum_{a\ge3}1/[a(a-1)]=3/4$ suffices. Take **any** nonempty set $S$ of $r=\theta b$ odd characters, the same set throughout the chain, and let $V_S$ be their span. Its one-step mean square is at most $\rho^2/\theta$. The geometric mean of the magnitudes is at most their root mean square. Multiplying over steps therefore gives

$$\boxed{\left|\det(T_h|_{V_S})\right|^{1/r}\ \le\ (\rho/\sqrt{\theta})^h.}$$

It holds even when some multiplier is zero. For all $b$ odd characters the base is about $0.8031$; even the $\lceil 3b/4\rceil$ with the largest chain multipliers (in magnitude) have base below $0.928$. This is a bound on a **geometric mean**, not a claim of independent random characters at successive steps, nor that every individual multiplier shrinks.

**Why the archive’s height step does not turn this into a ceiling.** Its [`DescentCut`][cut] has two relevant hypotheses: a supplied **map-height bound**, and a projection losing at most $3\delta$ of the rank, with $\delta\le1/12$. Inspect the [definition of map height][height]: it averages the logarithm of the **squared operator norm** at the infinite places, not the logarithm of the determinant per dimension. For our $T_h$, take the field $\mathbb Q(i)$ and identity metrics in the square-coordinate basis (an odd function is determined by its restriction to $H$). All divisor translations are rational permutation matrices there. There is one complex place; the specified archimedean map height is exactly $2\log(n_h/N)$. Assuming a uniform upper bound for it would already assume the desired conclusion.

Nor can we just project the whole odd space onto the modes attaining the peak. Equality in each triangle inequality for $k_n(\chi)$ requires $\chi(d)=1$ for **every** proper divisor: all weights are positive and $d=1$ fixes the phase. Equality for the whole product requires this at every step. If even one source is composite, some prime proper divisor $p$ has nonidentity residue in $H$, of odd order at least three. At most $b/3$ characters are trivial on that residue. Keeping only the peak would discard at least two thirds of the rank, not at most one quarter. This checks the proposed full-space application, not every possible choice of lattices and metrics. As a simple sanity check, in the actual orbit $6\to6\to\cdots$ the peak is 1 forever, whereas the one-step mean square is only $14/36$ and the geometric mean of the chain decays exponentially.

## A bound for the particular character: charge just the new records

The determinant averages away the orbit. Instead add back the omitted divisor after reversing each translation. The operator then factors **exactly**:

$$ I+R_n^{-1}K_n=\sum_{a\mid n}\frac{R_a^{-1}}{a}
   =\prod_{p^e\parallel n}\left(\sum_{k=0}^{e}\frac{R_p^{-k}}{p^k}\right).$$

Indeed $a=n/d$ turns $d/n$ into $1/a$; the added identity is $a=1$. On $\xi$ the full multiplier is $\alpha(n):=\sigma(n)/n$, and the growth factor we need is $\alpha(n)-1$. From here on **no character or probe prime is needed**.

Split a source $n=D u$ with $\gcd(D,u)=1$ and $\alpha(D)\le2$. The choice of $D$ can change at every step. The product identity, or ordinary multiplicativity, gives the pointwise inequality

$$ \frac{s(n)}n=\alpha(D)\alpha(u)-1\ \le\ 2\alpha(u)-1\ \le\ \alpha(u)^2
    \ \le\ \prod_{p\mid u}\left(\frac p{p-1}\right)^2. \tag{1}$$

The middle inequality is $(\alpha(u)-1)^2\ge0$. The last bound charges a prime only **once per source**, even if its exponent is large.

Fix a threshold $B>N$ and suppose $n_h$ is the **first** term at least $B$. Set $M_j=\max_{0\le i\le j}n_i$. Count only the steps $j<h$ for which $n_{j+1}>M_j$. For each such step choose a split as in (1), and let $c_p$ count how many of their $u_j$ are divisible by $p$. At a new record $M_{j+1}/M_j=n_{j+1}/M_j\le n_{j+1}/n_j$; at every other step $M_{j+1}/M_j=1$. Multiplying (1) at just the new records gives

$$\boxed{\frac BN\ \le\ \frac{n_h}N\ \le\ \prod_{p<B}\left(\frac p{p-1}\right)^{2c_p}.} \tag{2}$$

The prime cutoff is $B$, **not** the unknown overshoot $n_h$, because every source was smaller than $B$. Nothing presumes a monotone orbit or charges a rise that merely recovers from a dip.

**Unconditional restriction on escape.** At every source choose $D=2^{v_2(n)}$, including $D=1$ at odd sources. Its abundancy is $2-2^{-v_2(n)}<2$. Thus $c_2=0$. If $L(B)=\max_{p\text{ odd}}c_p$, (2) gives

$$ B/N\le E(B)^{2L(B)},\qquad E(B)=\prod_{3\le p<B}\frac p{p-1}\quad(p\text{ prime}). \tag{3}$$

[Mertens’ product theorem][mertens] gives $E(B)\sim(e^\gamma/2)\log B$. For a fixed seed reaching arbitrarily high levels this forces

$$ \liminf_{B\to\infty}\frac{L(B)\log\log B}{\log B}\ \ge\ \tfrac12.$$

In particular, with an independently known uniform cap $L$ one can choose **in advance** any $B>N$ such that $N E(B)^{2L}<B$; the orbit cannot cross it. Such a $B$ exists for every finite $L$. A bounded integer orbit must terminate or repeat. We have **not** obtained $L$ from $N$. Each bounded orbit has only finitely many record-setting steps anyway; the substance of (3) is the quantitative restriction on the prime factors of *record-makers* if the orbit is unbounded. It does not prove that a single fixed odd prime occurs infinitely often.

**Check on one prescribed orbit.** For $N=276$, $B=25{,}000$, exact rational multiplication gives $E(B)<19/2$. If no odd prime were used twice at record-making sources, the first crossing would be at most $276(19/2)^2=24{,}909$, a contradiction. This prediction needs no later orbit terms. The actual first crossing is $22{,}876\to26{,}404$ at step 15; the prime 3 divided eight of the twelve record-making sources. The intervening increase $2716\to2772$ did **not** set a record and is not charged. No conclusion about the ultimate fate of 276 is used or obtained.

**What if 6 is always available?** On a block $n_j=6u_j$ with $u_j>1$ coprime to 6 at every **source**, take $D=6$, since $\alpha(6)=2$. The cofactors satisfy $u_{j+1}=2\sigma(u_j)-u_j=u_j+2s(u_j)\ge u_j+2$. Thus an infinite run of this shape would be strictly increasing. Applying (2) from the start of that run, neither 2 **nor 3** is charged: primes greater than 3 would have to be reused with unbounded multiplicity across its sources. In particular such a run with pairwise coprime cofactors is impossible, even though they need not be prime or have boundedly many factors. The assumption $\gcd(6,u_j)=1$ is essential; the ever-present 6 in a general multiple of 6 need not be a coprime factor. Short runs really can use fresh primes: $47\to49\to65\to103\to105$ in cofactor coordinates has pairwise coprime sources, then leaves the coprimality condition. Leaving it need not settle the orbit.

**Stopping point.** We can now rule out escape driven by fresh odd primes with uniformly bounded reuse at record-making steps. We cannot rule out the required reuse: the [finite supplier construction](MINIMUM-ESCAPE.md#52-the-perfect-core-exception-permits-fresh-finite-recharge-too) can preserve factors through arbitrarily long growing runs on **different** seeds. What is missing is an independent limit on that supply, or a way to prove descent below the starting seed in a minimal-counterexample argument. The determinant estimate controls the wrong size to provide it.

[Follow-up on the proposed supply limit](ALPOGE-PRIME-ARRIVALS.md): even a burst of arbitrarily many primes larger than every seed factor need not dislodge an old prime from a prescribed finite run of records. Recurrent single-prime-cofactor schedules, however, force a return to an actual previous value.

[Exact finite checks](../tests/test_alpoge_record_height.py): `python3 -m unittest discover -s tests -p 'test_alpoge_record_height.py' -v`. These check the local operators, a first crossing, and the clean-6 example, not an asymptotic claim.

[det]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/ThetaLiftIndependence/Statement.lean#L260-L278
[cut]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/MeanHeightDescent/DescentCut.lean#L23-L46
[height]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/HarderNarasimhan/StatementPl.lean#L55-L62
[mertens]: https://mathworld.wolfram.com/MertensTheorem.html
