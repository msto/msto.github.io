---
layout: lecture
title: "MEME: Expectation and maximization steps (OOPS and ZOOPS)"
lecture: 3
course: BMI 776
date: 2019-01-29
---

# Announcements
- Read Lawrence et al
- Optional: read Durbin 11.4, Tompa, Weirach
- Homework 0 out Thursday

$$
%% Latex helpers
\newcommand{\norm}[1]{\left\lVert{#1}\right\rVert}
\newcommand{\card}[1]{\left\vert{#1}\right\vert}
\newcommand{\R}{\mathbb{R}}
\newcommand{\L}{\mathcal{L}}
\newcommand{\E}{\mathrm{E}}
\newcommand{\Var}{\mathrm{Var}}
\newcommand{\Cov}{\mathrm{Cov}}
\newcommand{\Col}{\mathrm{Col}}
\DeclareMathOperator*{\argmin}{arg\,min}
\DeclareMathOperator*{\argmax}{arg\,max}
\newcommand{\bigdot}{\boldsymbol{\cdot}}
$$

# EM overview

Recall that we are trying to find the maximum-likelihood estimate for the
parameters in our model, that is, the parameters that maximize the probability
of our observed data:

$$
\Theta_{ML} = \argmax\limits_{\Theta} P(D \mid \Theta, M)
$$

[ recap motif model and probability fn from previous lecture ] 

We want to apply EM to perform this maximization. The basic algorithm is as
follows:

```
input: motif width W, training sequences X

t = 0
initialize p(t)                # Model parameters
do
  ++t                          # Next iteration
  estimate Z(t) from p(t-1)    # E-step; update hidden states (motif positions)
  estimate p(t) from Z(t)      # M-step; max probability given hidden states
until (p(t) - p(t-1)) < eps
return p(t), Z(t)
```

# E-step: expected start positions

Recall that we are assuming our sequences are of uniform width and we defined a
$$n \times L$$ matrix $$Z$$, where $$Z_{ij} = 1$$ if the motif starts at
position $$j$$ in sequence $$i$$, and 0 otherwise. In our expectation step, we
want to compute the expected values of $$Z$$ given the set of sequences and the
previous parameters.

$$
Z^{(t)} = \E[Z \mid X, p^{(t-1)}]
$$

The expectation of an indicator variable is simple:

$$
\E[Z] = 1 \cdot P(Z=1) + 0 \cdot P(Z=0) = P(Z=1)
$$

So our matrix entries are

$$
Z_{ij}^{(t)} = \E[Z_{ij} \mid X_i, p^{(t-1)}] = P(Z_{ij} = 1 \mid X_i, p^{(t-1)})
$$

How do we compute this? We can use Bayes' rule to convert to familiar quantities:

$$
P(Z_{ij} = 1 \mid X_i, p^{(t-1)}) = \frac{P(X_i \mid Z_{ij} = 1, p^{(t-1)}) P(Z_{ij} = 1 \mid p^{(t-1)})}{P(X_i \mid p^{(t-1)})} 
$$

and then expand the denominator

$$
P(Z_{ij} = 1 \mid X_i, p^{(t-1)}) = \frac{P(X_i \mid Z_{ij} = 1, p^{(t-1)}) P(Z_{ij} = 1 \mid p^{(t-1)})}{\sum\limits_k P(X_i \mid Z_{ik} = 1, p^{(t-1)}) P(Z_{ik} = 1 \mid p^{(t-1)})}
$$

Now, if we assume the priors on our start positions are uniformly distributed,
so $$P(Z_{ij}=1) = \frac{1}{m}$$, and observe that the remaining sum in the
denominator is fixed over $$j$$, we have

$$
P(Z_{ij} =1 \mid X_i, p^{(t-1)}) \propto P(X_i \mid Z_{ij} = 1, p^{(t-1)})
$$

so for our E-step, we can compute this quantity for all positions $$j$$ and
normalize so they sum to 1.

# M-step: estimating p

Recall that $$p$$ is our position weight matrix, which is tracking the fraction
of times we observe character $$c$$ at position $$k$$ in the motif across all
sequences.

$$
p_{ck}^{(t)} = \frac{n_{ck} + d_{ck}}{\sum\limits_{b \in \{A, C, G, T\}} (n_{bk} + d_{bk})}
$$

where $$n_{ck}$$ is the expected number of times character $$c$$ is at position
$$k$$ in the motif instance, 

$$
n_{ck} = \begin{cases}
\sum\limits_i \sum\limits_{\{j \mid X_{i,j+k-1} = c\}} Z_{ij}^{(t)} & k>0 \text{ (in motif)} \\
n_c - \sum\limits_{j=1}^W n_{cj} & k=0 \text{ (background)}
\end{cases}
$$

Note that in the former case, we are summing the probability that the motif
starts at a position $$j$$ for all positions $$j$$ where the character $$c$$
exists at an offset of $$k$$. In the latter case, $$n_c$$ is the total number
of occurrences of character $$c$$ in our dataset.

Returning to the original formula for $$p_{ck}^{(t)}$$, $$d_{bk}$$ is a
pseudocount for base $$b$$ at position $$k$$. By default we will allow this
pseudocount to be 1, but we will see more intelligent ways of choosing these
pseudocounts later.

# Zero-or-one occurrences per sequences (ZOOPS)

So far, the calculations we have outlined assume exactly one occurrence of the
motif per sequence, which we call the OOPS model. We can also model the case
where we allow zero or one occurrences per sequence (ZOOPS). 

We now need to consider an alternative: that the $$i$$th sequence doesn't
contain the motif. Let $$\gamma$ denote the prior probability that any sequence
has a motif, and $$\lambda$$ denote the probability that any position is a
start position.

[[ TO FINISH ]]
