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
