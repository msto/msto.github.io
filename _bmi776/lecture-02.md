---
layout: lecture
title: Motif finding and expectation-maximization
lecture: 2
course: BMI 776
date: 2019-01-24
---

# Summary

Today in class we discussed the motif finding problem and began exploring the
application of expectation-maximization to it.

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

# The motif finding problem

A *motif* is some pattern occurring across a set of sequences that contains
some biological relevance. For example, motifs commonly occur in DNA at protein
binding sites.

The specific model learning task for the motif finding problem takes as input a
set of sequences of interest which putatively contain a motif. The goal is to
1) infer the motif model, i.e., the pattern with biological relevance, and 2)
identify the location of the motif within each input sequence.

We care about this problem because the genomic space is vast and we are
interested in identifying functional regions.

# Motif representation

One approach to representing motifs is to use a *position weight matrix*. Such
a matrix has one row for every possible character in the biological alphabet
and one column for each entry in the sequence. The $$ij$$th entry of this
matrix represents the probability of observing base $$i$$ at position $$j$$.

How can we construct a motif if our sequences aren't aligned, and if we don't
even know what the motif looks like?

# Expectation-maximization

Expectation-maximization (EM) can be applied to solve probabilistic models that
include some hidden state. In our setting, the hidden state is the location of
the motif start site within each sequence. Other applications that we have seen
in the past include the Baum-Welch algorithm for solving hidden Markov models,
and clustering with Gaussian mixture models.

EM is an optimization algorithm to find the maximum likelihood solution for a
given probabilistic model. Formally, we wish to find the parameters $$\theta$$
with highest likelihood given our observed data:

$$
\theta_{ML} = \argmax\limits_{\theta} P(D \mid \theta, M)
$$

where $$M$$ is our model, the previously defined position weight matrix.

EM is useful because it is difficult to directly optimize the quantity $$P(D
\mid \theta)$$. We can decompose the likelihood by introducing hidden
information $$Z$$ and creating a quantity that is easier to optimize:

$$
Q (\theta \mid \theta^+) = \sum \limits_{Z} P(Z \mid D, \theta^+) \log P(D, Z \mid \theta)
$$

where $$\theta^+$$ is some fixed setting of $$\theta$$. (TODO: review Durbin
11.6 for the derivation of this)

So we can define four steps to apply EM:

1. Define a model and a likelihood function
2. Identify the hidden variables $$Z$$
3. Write the expectation step (E-step; compute the expectation $$E[Z]$$ given current parameters)
4. Write the maximization step (M-step; compute the parameters which maximize $$Q$$ given the current state of our hidden $$Z$$)

# MEME - Multiple EM for Motif Elicitation

#### Defining our model

We define a motif to have a fixed width $$w$$ and represent it with a
probability matrix $$M \in \R^{\card{A} \times w + 1}$$, where $$\card{A}$$ is
the number of characters in our alphabet. $$M_{ck}$$ is the probability of
observing character $$c$$ at position $$k$$ if $$k \ge 1$$, and $$M_{c0}$$ is
the probability of observing character $$c$$ in the background (i.e., the bases
of the sequence not included in the motif).

We define our data to be a collection of sequences $$X = \{ X_1, \cdots, X_n
\}$$.

#### Identifying the hidden variables

We define our hidden states, the motif start positions, to be a matrix $$Z$$
such that $$Z_{ij}$$ is 1 if the motif starts at position $$j$$ in sequence
$$i$$, and 0 otherwise. (To simplify, for now we assume that all sequences are
the same length $$L$$ and $$Z$$ is $$n \times L$$.)

#### Defining the probability of an observed sequence given our model

Given a motif start position, the probability of the observed sequence can now be calculated:

$$
P(X_i \mid Z_{ij} = 1, M) = \prod\limits_{k=1}^{j-1} M_{c_k, 0} \prod\limits_{k=j}^{j+W-1} M_{c_k, k-j+1} \prod\limits_{k=j+W}^{L} M_{c_k, 0} 
$$

The first product represents the probability of the characters in the sequence
before the motif starts, based on the background probabilities; the middle
product represents the probability of the putative motif sequence based on the
motif model; and the final product represents the probability of the characters
in the sequence after the motif ends, again based on the background
probabilities.

#### Defining the EM algorithm

EM takes the maximum likelihood across all sequences, so we need a likelihood
function. EM indirectly optimizes the log likelihood of the observed data,
$$\log P(X \mid M)$$, and the M-step requires a joint log likelihood

$$
\begin{align*}
\L &= \log P(X, Z \mid M) && \text{$X$ = all sequences} \\
   &= \log \prod\limits_i P(X_i, Z_i \mid M) && \text{Sequences are independent} \\
   &= \log \prod\limits_i P(X_i \mid Z_i, M) P(Z_i \mid M) && \text{Chain rule} 
\end{align*}
$$

Note that we have already defined $$P(X_i \mid Z_i, M)$$ in our model above.
For the second term, we can assume that all positions within a sequence are
equally likely to contain the motif start position, and therefore define
$$P(Z_i \mid M) = \frac{1}{L}$$. Substituting in, we have:

$$
\begin{align*}
\L &= \log \prod\limits_i \frac{1}{L} \prod\limits_j P(X_i \mid Z_{ij} = 1, M)^{Z_{ij}}
\end{align*}
$$

Here, $$j$$ is denoting the possible indices in each sequence where the motif
could start. Recall that $$Z_{ij}$$ is 1 when the motif starts at position
$$j$$ in sequence $$i$$, so by raising this probability to the $$Z_{ij}$$, we
are keeping only the probabilities for the sites with a motif start (where
$$Z_{ij}=1$$).

A log of a product is equal to a sum of logs, and we have:

$$
\begin{align*}
\L &= \sum\limits_i \sum\limits_j Z_{ij} \log P(X_i \mid Z_{ij} = 1, M) + n \log \frac{1}{L}
\end{align*}
$$

where we will return in the next class.
