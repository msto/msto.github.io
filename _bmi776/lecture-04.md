---
layout: post
title: Lecture 04
date: 2019-01-31
header-includes:
  - \usepackage{algorithm2e}
---

## Summary

Today in class we reviewed and finished our discussion of applying EM to the
motif finding problem, and introduced a second approach - Gibbs sampling.

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

- Read the Gibbs paper for next class (Lawrence et al.)
- Explore the ipython notebook with examples of the gamma function and the
  Dirichlet distribution

## Lecture goals

We've discussed the OOPS (One Occurrence Per Sequence) and ZOOPS (Zero Or more
Occurrences Per Sequence) models for EM. Now, we want to extend to any number
of motifs and handle motifs of uncertain width.

Additionally, we want to choose our initial parameters intelligently. Can we
incorporate background information, so not all motif models are equally likely?

## MEME
# Review EM algorithm

Recall that in the EM algorithm, we begin our search from an initial estimate
of the parameters $$p^{(0)}$$. However, EM can only obtain a local maximum of
the likelihood function reachable from $$p^{(0)}$$. One approach to find the
global maximum could be to take multiple initializations of $$p^{(0)}$$ and
choose the best final result. Unfortunately, in the high-dimensional setting, it is
computationally infeasible to exhaustively search this space.

However, there are some easy heuristics that can get us close to the global
maximum. We can observe that the true motif must be similar to some subsequence
in our set of sequences. Intuitively, the motif can't be a sequence that isn't
represented in our dataset. This insight suggests the following strategy:

```
For each distinct subsequence S with length W
    Derive p_(0) from S
    Run EM for 1 iteration
End
Choose the motif model that yielded the highest likelihood
Run EM from the corresponding p_(0) until convergence
```

This heuristic generally approximates the global maximum well.

## Learning Sequence Motifs with Gibbs Sampling

# Goals
- Discuss Gibbs sampling, a specific instance of Markov chain Monte Carlo
- Apply Gibbs sampling to the motif funding problem. This is a stochastic
  method, in contrast to the deterministic MEME and its fuzzy heuristic.
- Parameter tying (for example, when assuming a palindromic motif)
- Priors on our model (incorporating background information, such as the
  knowledge that some amino acids behave similarly)

# Motivation for Gibbs sampling
Deterministic algorithms, like EM, can get stuck in local maxima. Gibbs
sampling searches with randomness to escape local maxima, and can be thought of
as a stochastic analog of EM.

# Gibbs sampling approach

In EM, we maintained a distribution $$Z_{i}^{(t)}$$a over the possible motif
start positions. In Gibbs sampling, we will maintain a specific motif start
position $$a_i$$ for each sequence, but will randomly resample $$a_i$$ at each
iteration.

The algorithm is as follows:
```
Input: motif width W, set of sequences X
Initialize a random vector of motif start positions a
do
    Pick any sequence X_i
    Estimate p with the current motif locations a (holding out a_i)
    Compute the probability that the motif starts at each position in X_i
    Randomly sample a new motif start position a_i for X_i from this distribution
until convergence
```

# Markov chain Monte Carlo
Markov chains representing transition probabilities have a stationary
distribution if after sufficient iterations, $$p^{(t)}(\text{state})$$
converges to a stable distribution and approximates the actual probability of
being in that state. Mathematically,

$$
p^{(t)}(u) \approx p^{(t +1)}(u)
$$

In matrix form, let $$T$$ be the transition matrix such that $$T_{uv} = \tau(u
\mid v)$$, where $$\tau(u \mid v)$$ is the transition probability of moving
from state $$u$$ to state $$v$$. Let $$p^{(t)}$$ denote the vector of
probabilities of being in a given state. Then the stationary distribution has
the form:

$$
p^{(t+1)} = T p^{(t)}
$$

Note that this formulation is consistent with the intuition that $$p^{(t+1)}(u) =
\sum\limits_{v} p^{(t)}(v) \tau(u \mid v)$$.

So the states of our Markov chain correspond to some configuration of our
probabilistic model. In motif finding, this corresponds to some configuration
of our motif start positions, $$a$$. The transitions correspond to a change in
our start positions. For our purposes, a transition is permitted only if it
corresponds to changing the motif start position in a single sequence (i.e.,
updating multiple sequences in a single iteration is not permitted.)

# What does this get us?

We're trying to take some distribution $$P(a)$$, and we want to find the mode
of this distribution, which corresponds to the configuration of $$a$$ that
maximizes $$P(a)$$. We'd also like to sample from this distribution.

In large models, it is difficult to do either of these directly. MCMC works
around this. The main idea is that we construct a Markov chain where the states
correspond to configurations of the motif positions $$a$$, and the stationary
distribution of this chain is the distribution $$P(a)$$ of interest. So we need
to define a transition probability matrix $$T$$ that will give us the desired
stationary distribution.

# Building a Markov chain with the desired stationary distribution

So how do we do this? We set our transition probabilities so that a property
called _detailed balance_ holds. This guarantees a stationary distribution.

Transition probabilities satisfy detailed balance if the following is true:

$$
P(u) \tau (v \mid u) = P(v) \tau(u \mid v)
$$

Note that if we assume detailed balance, we can show that our distribution is stationary:

$$
\begin{align*}
\sum\limits_{v} P(u) \tau(v \mid u) &= \sum\limits_{v} P(v) \tau (u \mid v) \\
P(u) \sum\limits_{v} \tau(v \mid u) &= \sum\limits_{v} P(v) \tau (u \mid v) && \text{$P(u)$ constant for all $v$} \\
P(u) &= \sum\limits_{v} P(v) \tau (u \mid v) && \text{Sum of transition probs is 1} 
\end{align*}
$$

which matches our early definition of a stationary distribution, $$P=TP$$.

Suppose we draw $$n$$ samples from such a Markov chain, and let
$$\mathrm{count}(u)$$ denote the number of times the chain was in state $$u$$.
Then $$\lim\limits_{n \to \infty} \frac{1}{n} \mathrm{count}(u) = P(u)$$.

Gibbs sampling is a specific choice of our transition probabilities $$T$$. It
is a special case where we only permit transitions that change a single
variable, say $$a_{\Delta}$$, and we define a transition probability $$\tau$$
to be the conditional probability $$P(a_{\Delta} \mid a_{i \ne \Delta})$$.

Why does this choice of $$T$$ give us detailed balance? Suppose we have two
states, or configurations of our motif start positions, that differ for only a
single sequence, $$X_i$$. Let's call them $$a$$ and $$a'$$, and let's denote
the set of all possible sequence indices as $$I$$, so $$a_{i} \ne a_{i}'$$, but
$$a_{I \setminus i} = a_{I \setminus i }'$$. (Also let $$A$$ denote the random variable
corresponding to our motif start positions.)

$$
\begin{align*}
&= P(A = a) P(A_i = a_i' \mid A_{I \setminus i} = a_{I \setminus i}) \\
&= P(A_i = a_i \mid A_{I \setminus i} = a_{I \setminus i}) P(A_{I \setminus i} = a_{I \setminus i}) P(A_i = a_i' \mid A_{I \setminus i} = a_{I \setminus i}) \\
&= P(A_i = a_i \mid A_{I \setminus i} = a_{I \setminus i}) P(A_i = a_i', A_{I \setminus i} = a_{I \setminus i}) \\
&= P(A_i = a_i \mid A_{I \setminus i} = a_{I \setminus i}) P(A = a') \\
\end{align*}
$$

which is our definition of detailed balance.

# Probability of being in a state

We can define the probability of being in a state $$u$$ as follows:

$$
P(u) \propto \prod\limits_{c} \prod\limits_{j=1}^{W} \left ( \frac{p_{c,j}}{p_{c,0}} \right ) ^{n_{c,j}(u)}
$$

where $$n_{c, j}(u)$$ is the number of times character $$c$$ was observed at
position $$j$$ across all motifs, given the motif start positions in state
$$u$$. So we're taking the product of the probabilities of observing character
$$c$$ at position $$j$$ in our motif model over the probabilities from our
background model.

The full derivation can be found in Liu et al. (JASA 1995) but we can show that
this is proportional to the likelihood of our data to obtain some intuition for
this formula.

Remember that the state $$u$$ is some configuration of our hidden variables,
the motif start positions in $$A$$, and we're interested in the probability of
these start positions given our observed data, $$P(A \mid X)$$. (Note that in
the lecture notes for MEME, we used $$Z$$ instead of $$X$$ to refer to our
data.) By Bayes' Theorem, we have

$$
P(A \mid X) = \frac{P(X \mid A) P(A)}{P(X)}
$$

Since $$X$$ is fixed, that means our probability is proportional to the numerator

$$
P(A \mid X) \propto P(X \mid A) P(A)
$$

And if we assume a uniform prior over the possible motif start positions, that
means $$P(A)$$ is constant and this is simply proportional to the probability
of the data given the motif start positions:

$$
P(A \mid X) \propto P(X \mid A)
$$

Now, without being too rigorous, since we're just trying to provide intuition
for the formula above, $$P(X \mid A)$$ is some product of character
probabilities:

$$
P(X \mid A) = P(\text{all motif positions according to our motif model}) P(\text{all non-motif positions according to our background model})
$$

We can multiply this by the fraction $$\frac{P(\text{all motif positions according to our background model})}{P(\text{all motif positions according to our background model})}$$, which is 1, and obtain

$$
P(X \mid A) = \frac{P(\text{all motif positions according to our motif model})}{P(\text{all motif positions according to our background model})} P(\text{all positions according to our background model})
$$

Note that the second quantity is our null model and is independent of our motif
model, so it is constant, and $$P(X\mid A)$$ is then proportional to the first
quantity:

$$
P(X \mid A) \propto \frac{P(\text{all motif positions according to our motif model})}{P(\text{all motif positions according to our background model})}
$$

which is consistent with the formula above for the probability of a state in
the stationary distribution of our Markov Chain.

Next lecture we will discuss transition probabilities.
