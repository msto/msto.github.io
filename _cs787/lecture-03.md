---
layout: lecture
title: Hashing
lecture: 3
course: CS 787
date: 2019-09-12
---
## Summary

Today we considered the motivational problem of counting the number of distinct
elements in a stream, and applying the concentration inequalities we learned in
the last lecture to bound an estimator for this count.

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
Last lecture we discussed three concentration inequalities:

1. Markov's inequality
2. Chebyshev's inequality
3. Chernoff's bound

We saw that Chernoff's bound is the most powerful, and will be applying it
again today. To review, Chernoff's bound states the following:

Let $$X_i$$ be independent Bernoulli random variables, i.e. $$X_i \in \{0, 1\}$$, with $$\E[\sum X_i] = \mu$$. Then

$$
P(\sum X_i \ge (1 + \delta) \mu) \le \exp\left(\frac{-\delta^2 \mu}{2 + \delta}\right)
$$

Note that this holds in the other direction:

$$
P(\sum X_i \le (1 - \delta) \mu) \le \exp\left(\frac{-\delta^2 \mu}{2 + \delta}\right)
$$

## Estimating the parameter of a Bernoulli variable

**Question:** Suppose we have 1 coin that lands heads (H) with probability
$$\bar\mu$$ (and therefore tails with probability $$1 - \bar\mu$$). How many
coin tosses are required to estimate $$\mu$$ within accuracy $$\varepsilon$$ with
confidence $$1 - q$$?

We define the _accuracy_ of an estimator to be its distance from the true
value, i.e. $$\card{ \hat\mu - \bar\mu} \le \varepsilon$$. We define the
_confidence_ to be the probability of achieving a minimum accuracy, i.e.
$$P(\card{\hat\mu - \bar\mu} \le \varepsilon) = 1 - q$$. (This is commonly
referred to as an epsilon-delta guarantee; but we are using $$q$$ here to avoid
confusion with the $$\delta$$ of the Chernoff bound.)

It is easy to construct an estimator for this parameter - we can simply compute
the fraction of heads in all tosses. Let $$X_i$$ be the $$i$$th throw, and we
have the estimator for $$n$$ throws

$$
\hat\mu = \frac{\sum X_i}{n}
$$

We want to compute a probability bound for the accuracy of this estimator in
terms of $$n$$. Namely, we are interested in the probability that this
estimator is within $$\varepsilon$$ of the true parameter.

$$
P(\hat\mu \ge \bar\mu + \varepsilon)
$$

If we set $$\varepsilon = \delta \bar\mu$$, we can transform this into the
Chernoff bound formula:

$$
\begin{align}
P( \hat\mu \ge \bar\mu + \varepsilon) &= P (\hat\mu \ge (1 + \delta) \bar\mu) \\
        &= P(\frac{\sum X_i}{n} \ge (1+\delta) \bar\mu) \\
        &= P(\sum X_i \ge (1+\delta) \bar\mu n) \\
        &\le \exp\left(\frac{-\delta^2 \bar\mu n}{2 + \delta} \right) \\
        &= \exp\left(\frac{-\delta^2 \bar \mu}{2+ \delta} \cdot \frac{\bar\mu}{\bar\mu} n \right) \\
        &= \exp\left(\frac{-\varepsilon^2}{2\bar\mu + \varepsilon} n \right)
\end{align}
$$

which is at most $$\frac{q}{2}$$ if we choose $$n = \Theta\left(\frac{\bar\mu +
\varepsilon}{\varepsilon^2} \log \frac{1}{q}\right)$$. Since the Chernoff bound
is symmetric, the probability that our estimator is further than
$$\varepsilon$$ from the true parameter is at most $$q$$.

This completes our discussion of probabilistic bounds, which showed us how to
estimate the likelihood of an event. Now, we will apply these tools to the
design of an algorithm.

## The [Count-Distinct Problem](https://en.wikipedia.org/wiki/Count-distinct_problem)

Let us consider the following motivating problem. Suppose we observe a large
stream, i.e., some sequence of different objects $$X_1 \dots X_n$$. How many
distinct elements appear in this sequence?

A naive approach would be to sort the elements and filter duplicates, but this
is $$\O(n)$$ in the number of unique words. Today we will show that, using only
5 words, this problem can be solved with an accuracy of 5%. 

The key idea is to hash every observed element of the sequence, using a hash
function that randomly assigns each element to a real number between 0 and 1,
i.e. $$h(x_i) \in [0, 1]$$, and to keep track of the minimum observed hash
value, $$y = \min\limits_i \{h(X_i)\}$$. 

This is cheap in space, since we only need to store the current minimum hash
and the curent element! We can also assume there will be no collisions, since
the range $$[0, 1]$$ is a sufficiently large domain, so the number of distinct
hashes corresponds to the number of distinct elements.

Now, if there are $$n$$ distinct elements, what is $$\E[y]$$?

**Proof:**

$$
\begin{align}
\E[y] &= \int_0^1 z P(y \le z) dz \\
      &= \int_0^1 P(y \ge z) dz \\ 
      &= \int_0^1 (1 - z)^n dz \\
      &= \frac{1}{n+1}
\end{align}
$$

So, if we have a value for $$y$$, we can solve for $$n$$ here and obtain the
estimator $$\hat n = \frac{1}{y} - 1$$. However, this estimator may be far from
the true count. Let's first try to bound it by applying Chebyshev's inequality.

$$
P(\card{y - \E[y]} \ge k \sigma) \le \frac{1}{k^2}
$$

To do so, we need to estimate the variance $$\sigma^2$$ of $$y$$. Recall the
formula for variance,

$$
\Var[y] = \E[(y - \E[y])^2] = \E[y^2] - \E[y]^2
$$

We can compute $$\E[y^2]$$:

$$
\E[y^2] = \int_0^1 y^2 n(1-y)^{n-1} dy = \frac{2}{(n+1)(n+2)}
$$

Substituting this into the variance formula, we have

$$
\begin{align}
\Var[y] &= \E[y^2] - \E[y]^2 \\
        &= \frac{2}{(n+1)(n+2)} - \left( \frac{1}{n+1} \right)^2 \\
        &\le \frac{2}{(n+1)^2} - \frac{1}{(n+1)^2} \\
        &= \frac{1}{(n+1)^2}
\end{align}
$$

and so we have $$\sigma \le \frac{1}{n+1}$$. Note that the standard deviation
of our estimator is equal to its expected value, and so we have a noisy
estimator that can't tell us much. We can't apply the Chernoff bound since we
don't have a sum of independent Bernoulli variables, so how else can we improve
our estimator? Instead of using a single noisy random variable, we can try
repeating the experiment.

## Improving the estimator with repetition

Our initial idea was to choose a random hash function $$h: \{X_1, \dots X_n\}
\mapsto [0, 1]$$ and store the minimum observed hash value $$y$$. Suppose we
instead choose $$m$$ random hash functions that all map the observed elements
to $$[0, 1]$$ and store the minimum observed hash values for each function
$$y_1 \dots y_m$$.

Now we have the mean observed hash value $$\bar y = \frac{\sum y_j}{m}$$, with the following variance.

$$
\begin{align}
\Var[\bar y] &= \Var [\frac{1}{m} \sum y_j] \\
        &= \frac{1}{m^2} \Var [\sum y_j] \\
        &= \frac{1}{m^2} \sum \Var [y_j] \\
        &\le \frac{1}{m^2} \sum\limits_{j=1}^m \frac{1}{(n+1)^2} \\
        &= \frac{1}{m} \cdot \frac{1}{(n+1)^2}

\end{align}
$$

We can now apply Chebyshev's inequality, using $$\sigma = \frac{1}{\sqrt{m}}
\cdot \frac{1}{(n+1)}$$.

$$
P\left(\card{\bar y - \E[\bar y]} \ge k \frac{1}{n+1} \cdot \frac{1}{\sqrt{m}}\right) \le \frac{1}{k^2}
$$

<!-- TODO: figure out why Christos derived this as well -->
<!-- Here, our accuracy is thus $$\varepsilon = k \frac{1}{n+1} \cdot -->
<!-- \frac{1}{\sqrt{m}}$$. Solving for $$k$$, we have $$k= -->
<!-- \varepsilon(n+1)\sqrt{m}$$.  -->

<!-- Note that if we choose $$\varepsilon = k \frac{1}{\sqrt{m}}$$ we have $$k= -->
<!-- \varepsilon \sqrt{m}$$ and can substitute into Chebyshev's inequality. (Recall $$\E[\bar -->
