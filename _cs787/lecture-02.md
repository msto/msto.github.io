---
layout: lecture
title: Hashing
lecture: 2
course: CS 787
date: 2019-09-10
---
## Summary

Today we considered the motivational problem of load balancing - assigning $$n$$
jobs to $$n$$ machines - and attempted to bound the maximum expected number of
jobs on a single machine. We learned three probabilistic tools - Markov's
inequality, Chebyshev's inequality, and the Chernoff bound - and saw how each
could identify a successively tighter bound.

$$
%% Latex helpers
\newcommand{\norm}[1]{\left\lVert{#1}\right\rVert}
\newcommand{\card}[1]{\left\vert{#1}\right\vert}
\newcommand{\R}{\mathbb{R}}
\newcommand{\L}{\mathcal{L}}
\newcommand{\O}{\mathcal{O}}
\newcommand{\E}{\mathrm{E}}
\newcommand{\Var}{\mathrm{Var}}
\newcommand{\Cov}{\mathrm{Cov}}
\newcommand{\Col}{\mathrm{Col}}
\newcommand{\bigdot}{\boldsymbol{\cdot}}
$$


## Recap
Last lecture we discussed a universal hash function family:

$$
H = \{h_{a, b} \mid a \in \{1, \cdots, p - 1\}, b \in \{0, \cdots, p - 1\}, h_{a, b} = ((ax+b) \bmod p) \bmod m \}
$$

We discussed that a perfect hashing strategy required space $$m = \O(n^2)$$, and
saw that we could improve this to $$O(n)$$ by using a two-level hashing. Proving
these bounds required only linearity of expectation and the universal hash
property. Today we will discuss more powerful probabilistic tools for random
variables.

## Motivation - load balancing and maximum load
The motivating problem we consider is load balancing. We have $$n$$ equal sized
jobs that must be assigned to $$n$$ machines. Clearly, we may have a collision
where two jobs are assigned to the same machine if job assignment is not
coordinated. (Note that we are not considering a random permutation of the
jobs, which would constrain each machine to accept only one job, but rather the
scenario where the choice of machine is drawn randomly with replacement for
each job.)

A simple question to ask is what the expected load for a random machine is,
which is 1 job. However, we are interested in investigating what the worst case
load for a machine is. To do so, expectation won't suffice and we'll need to
consider other probabilistic tools.

## Markov's inequality

The first tool we will apply is Markov's inequality, which we saw briefly in
the last lecture.

For any random variable $$X \ge 0$$ and any positive constant $$a > 0$$, it holds that:

$$
P(X \ge a) \le \frac{\E[X]}{a}
$$

**Proof:**

Let $$1_{X \ge a}$$ be an indicator variable; 1 when $$X \ge a$$ and 0
otherwise. The probability $$P(X \ge a)$$ is then the expectation of this
random variable. Observe that the following is true:

$$
\E[1_{X \ge a}] \le \E\left[\frac{X}{a}\right]
$$

Since if $$X \ge a$$, then LHS = 1 and RHS $$\ge 1$$; otherwise LHS = 0 and 0
$$<$$ RHS $$<$$ 1. 

By linearity of expectation, $$\E\left[\frac{X}{a}\right] = \frac{E[X]}{a}$$,
which completes the proof.

**Applying to find a bound:**

Let $$M_i$$ be the number of jobs assigned to machine $$i$$. Using Markov's
inequality, we can bound the probability that the maximum load of a single
machine exceeds $$k$$ jobs.

$$
P(M_i \ge k) \le \frac{\E[M_i]}{k} = \frac{1}{k}
$$

(since we noted above the expected load per machine is 1 job.)

However, we would like to bound the maximum load over all machines, i.e. the
probability that no machine receives more than $$k$$ jobs. To do so, we will
apply the [union bound](https://en.wikipedia.org/wiki/Boole%27s_inequality),
which states that the probability of a union of events is no more than the sum
of their probabilities.

$$
\begin{align*}
P( \exists i : M_i \ge k) &\le \sum\limits_i P(M_i \ge k) \\
 &\le \sum\limits_i \frac{1}{k} \\
 &= \frac{n}{k}
\end{align*}
$$

So we have proven that the probability that any machine . [TODO: write a better statement about triviality here]

However, if we apply a more powerful inequality, we can obtain a better bound
and therefore a better understanding of the behavior of the problem.

## Chebyshev's inequality

Let $$X$$ be a random variable with mean $$\mu = \E[X]$$ and variance
$$\sigma^2 = \E[(X - \mu)^2]$$. Then

$$
P( \card{X - \mu} \ge k \sigma) \le \frac{1}{k^2}
$$

Qualitatively, Markov's inequality bounds the value of a random variable with
its expectation. A random variable is unlikely to take a value that is several
multiples of its expectation. Chebyshev's inequality is more fine grained and
places a tighter bound on the mean. [TODO: elaborate?]

**Proof:**

We can prove Chebyshev's inequality using Markov's inequality. Let us define a
random variable $$z = (X - \mu)^2$$. Then we have
    [TODO: write out and add proof]


**Applying to find a bound:**

In our context, this allows us to place a tighter bound on the maximum load of a machine:

$$
P(M_i \ge k) = P(\abs{M_i - 1} \ge k - 1)
$$

Note that the random variable $$M_i$$ is the sum of indicator variables
$$y_{ji}$$, where $$y_{ji}=1$$ if job $$j$$ is assigned to machine $$i$$.

$$
M_i = \sum\limits_{j=1}^n y_{ji}
$$

Since the jobs are assigned randomly the variables $$y_{ji}$$ are independent,
and we have

$$
\begin{align*}
\Var[M_i] &= \sum \Var[y_{ij}] \\
          &= n \Var[y_{11}] \\
         &= n \left( \frac{1}{n} \left(1 - \frac{1}{n}\right)^2 + \left(1 - \frac{1}{n}\right)\left(0 - \frac{1}{n}\right)^2 \right) \\
        &= 1 - \frac{1}{n} \\
        < 1
\end{align*}
$$

Since the variance is less than 1, we can bound $$\sigma$$ at 1 in Chebyshev's inequality and obtain

$$
P(\card{M_i - 1} \ge k - 1) \le \frac{1}{(k -1)^2}
$$

Applying the union bound again, we now have the new bound on our maximum load

$$
P(\exists i : M_i \ge k) \le \frac{n}{(k-1)^2}
$$

which is no longer a trivial bound! In fact, we can observe that for
$$k=\O(\sqrt{n})$$, this probability is at most 0.01. [TODO: why?] which gives
us a reasonable confidence that no machine should have more than $$\sqrt{n}$$
jobs piling up.

But 

