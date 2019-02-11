---
layout: lecture
title: Gibbs sampling (transition probabilities) and Dirichlet priors
lecture: 5
course: BMI 776
date: 2019-02-05
---

## Summary

Today in class we reviewed and finished our discussion of Gibbs sampling, and introduced Dirichlet priors.

$$
%% Latex helpers
\newcommand{\norm}[1]{\left\lVert{#1}\right\rVert}
\newcommand{\card}[1]{\left\vert{#1}\right\vert}
\newcommand{\R}{\mathbb{R}}
\newcommand{\L}{\mathcal{L}}
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}
\newcommand{\bigdot}{\boldsymbol{\cdot}}
$$

## Announcements

- Read Elemento et al (FIRE)
- Read Durbin 11.2
- Homework 0 is due Friday

## Recap: Gibbs Sampling

The basic idea is to draw samples from or find the mode of some distribution
$$p(x)$$. Gibbs sampling permits us to do so, even if $$p(x)$$ is untractable.

The key is to define $$p(x)$$. In our setting, the motif finding problem, it is
some distribution over the hidden motif starts. From the derivation in our last
lecture, we showed that the probability of being in a state $$u$$ is as
follows:

$$
P(u) \propto \prod\limits_c \prod \limits_{j=1}^W \left( \frac{p_{c, j}}{p_{c, 0}} \right)^{n_{c, j}(u)}
$$

where $$n_{c, j}(u)$$ is the count of $$c$$ at motif position $$j$$ across all
sequences in our current model $$u$$.

This is what's known as a _collapsed_ Gibbs sampler. Really, we could define a
distribution over our hidden motif positions $$A$$, our sequences $$X$$, and
our parameters $$p$$, $$P(A, X, p)$$, but we're choosing to sample over only
our hidden variables and integrate out the other parameters.

# Transition probabilities

We've constrained the possible transitions between our states to be those that
only change the motif start position in a single sequence, say $$i$$.

To sample a new start position for sequence $$i$$, we can describe the
following strategy:

1. Estimate $$p$$ from all sequences except $$i$$
2. Construct a probability distribution from the likelihood ratios for all possible start positions $$j$$:
   $$ \mathrm{LR}(j) = \frac{\prod\limits_{k=j}^{j+W-1} p_{c_k, k-j+1}}{\prod\limits_{k=j}^{j+W-1} p_{c_k, 0}}$$
3. Select a new position $$A_i = j$$ with probability $$\frac{\mathrm{LR}(j)}{\sum\limits_{k \in \mathrm{start pos}} \mathrm{LR}(k)}$$

# Gibbs summary

So our algorithm for Gibbs sampling looks as follows:

```
Initialize some random A
Until convergence:
    Pick some sequence X_i
    Estimate p with the current state of A from X, excluding X_i
    Sample a new start position A_i
```

Note that Gibbs sampling can get stuck in local maxima, often the correct motif
shifted by 1 or 2 bases. This is called the _phase shift problem_. It can occur
because when we sample a new start position, the probabilities over the
possible motif start locations are constrained by the motif model defined by
the other sequences. So if our model is shifted by one or two bases, the maxmum
likelihood position for our sequence will likely be shifted by the same amount.
Typically, we solve this by running Gibbs multiple times and choosing the best
results.

## Using background information to suggest what our model should look like

# Parameter tying

Many motifs are palindromic, because they are bound by a homodimer where each
constituent protein binds the same pattern (except with one side in reverse).
How can we "force" our model to prefer palindromic motifs? One strategy is
parameter tying, where we constrain two parameters to be equal, e.g. the
probability of observing $$A$$ in our first position is constrained to be equal
to that of $$T$$ in the last position, $$p_{A, 1} = p_{T, W}$$. If we're not
certain if our motif is palindromic, we can run EM or Gibbs sampling with and
without parameter tying, and then use a likelihood ratio test to determine if
tying the parameters significantly improved over the null assumption.

# Priors

Our knowledge of protein structure and amino acid characteristics can inform
our background expectations of amino acid frequencies.

Recall the MEME and Gibbs update formula

$$
p_{c, k} = \frac{n_{c, k} + d_{c,k}}{\sum\limits_{b} u_{b, k} + d_{b, k}}
$$

where $$d_{b, k}$$ was some pseudocount. How can we intelligently choose these
pseudocounts based on our background knowledge? We want to encode information
about the chemical properties of amino acids and the fact that the fall into
classes into some priors that can generate informed pseudocounts.

# Dirichlet mixture priors

We want a prior over the character frequencies, and we want a prior for each
column of the motif model, which is a multinomial distribution. We will show
that the proper and mathematically convenient choice for this prior is the
Dirichlet distribution (and in the next lecture we will explore mixtures of
Dirichlets).

# Beta distribution
For now, let's begin with exploring the Beta distribution. Let's say we'd like
to estimate the parameter $$\theta$$ of a weighted coin:

$$
P(\theta) = \frac{\Gamma(\alpha_H + \alpha_T)}{\Gamma(\alpha_H) \Gamma(\alpha_T)} \theta^{\alpha_H -1} (1 - \theta)^{\alpha_T - 1}
$$

Where the gamma function $$\Gamma$ is an generalization of the factorial
function, and $$\alpha_H$$ and $$\alpha_T$$ are the imagined number of heads
and tails we've already seen (our prior belief).

Why? This is convenient with data generated from a binomial distribution (or
from Bernoulli trials). Suppose we have a set of $$D$$ observations with
$$D_H$$ heads and $$D_T$$ tails. Then the posterior distribution has the same
form as the Beta distribution.

$$
\begin{align*}
P(\theta \mid D) &= \frac{\Gamma(\alpha_H + D_H + \alpha_T + D_T)}{\Gamma(\alpha_H + D_H) \Gamma(\alpha_T + D_T)} \theta^{\alpha_H + D_H - 1} (1 - \theta)^{\alpha_T + D_T - 1} \\
        &= \mathrm{Beta}(\alpha_H + D_H, \alpha_T + D_T)
\end{align*}
$$

Since the posterior distribution is also a Beta distribution, we call Beta
distributions a conjugate family for the binomial distribution.

# Dirichlet distribution

What if we need to encode over more than 2 outcomes? For example, over all
characters in alphabet? The Dirichlet distribution is a generalization of the
Beta distribution to more than 2 outcomes, and Dirichlet distributions are a
conjugate family for multinomial priors.

$$
P(\theta) = \frac{\Gamma(\sum \alpha_i)}{\prod \Gamma(\alpha_i)} \prod \theta_i^{\alpha_i - 1}
$$

(Note that our parameters are constrained so $$\sum \theta_i = 1$$).

Since the Dirichlet distribution is conjugated, if $$P(\theta) \sim
\mathcal{D}(\alpha_1, \cdots, \alpha_k)$$, then $$P(\theta \mid D) \sim
\mathcal{D}(\alpha_1 + D_1, \cdots, \alpha_k + D_k)$$.

Geometrically, we can think of the Dirichlet distribution as defining a density
over the simplex where $$\sum D_i = 1$$.

# Mixture of Dirichlets

We want to put a Dirichlet prior on each column of our motif model, as we'd
like to encode the functional characteristics of different subsets of amino
acids. The selection for column corresponds to 1 of the different subsets, so
we'd like to separate our columns into classes.


