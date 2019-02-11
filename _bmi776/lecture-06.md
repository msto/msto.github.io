---
layout: lecture
title: Information theory and FIRE
lecture: 6
course: BMI 776
date: 2019-02-07
---

# Overview
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
\newcommand{\bigdot}{\boldsymbol{\cdot}}
$$

This section will focus on a particular biological question: what causes gene
differential expression?  Can we use discovered motifs to explain why genes are
up- or down-regulated under certain condtions? We will see how the authors of
FIRE employ information theoretic concepts to approach this problem.

We will become familiar with key concepts of information theory and its
application to the motif-finding problem:
- Entropy
- Mutual information (MI)
- Motif logos
- Applying mutual information to find motifs 

Analyzing a set of gene expression data (for example, Audrey Gasch's landmark
yeast datasets), we can identify sets of differentially expressed genes.
However, we don't know what might be causing some set of genes to be
up-regulated under stress. We are interested in discovering and understanding
combinations of informative patterns (motifs) upstream of genes, that may
correspond to specific configurations of bound repressors or promoters.

# Introduction to information theory

Previously, we described sequences with a probabilistic model (a motif and a
background model), and tried to maximize the likelihood of motifs under the
model. Now we will explore a different approach, information theory. In short,
information theory considers the problem of communicating information across
some channel.

Let's consider a simple example - as we watch a bike race, we'd like to
communicate the brand of each bike that passes by. To communicate this
information digitally, we could encode each brand in a bit pattern. In a sample
case where had four brands, we could encode the brands as 00, 01, 10, and 11.
So the expected number of bits we would need to communicate a brand is 2. Can
we do better than this and use fewer bits on average? Yes, if the bike brands
are distributed non-uniformly. We can choose a variable number of bits to
encode each brand, choosing a smaller number of bits for more common brands
(e.g. 1, 01, 001, 000). The optimal choice of bits, if the distribution is
known, uses $$-\log_2 P(c)$$ bits for a brand (or more generally, an event)
that we observe with probability $$P(c)$$.

Now, the expected number of bits to communicate a brand is

$$
\E[\mathrm{bits}] = - \sum P(c) \log_2 P(c)
$$

which is simply the sum of the number of bits used to encode each event
multiplied by the respective probability associated with observing each event.

# Entropy

The formula we have just derived has an important definition in information
theory - entropy. Entropy is an important quantity that measures the
uncertainty associated with a random variable. For discrete random variables,
the formula is, as above,

$$
H(X) = - \sum\limits_{x} P(X=x) \log_2 P(X=x)
$$

for all possible outcomes $$x$$.

How is entropy related to DNA sequences? We'll return to the motif sequence
logos we showed earlier (see slides). The height of each character is
proportional to the frequency of that character ($$P(c)$$). Note that the
height of each column is variable, and is determined by the decrease in entropy
$$H$$ from the background.
[[ return]]

# Mutual information

Mutual information is a central idea in information theory that is measured
with respect to two random variables, and tells us how much knowing one
variable informs us about the other. It is closely related to the independence
of the two variables.

$$
I(M; C) = H(M) - H(M \mid C)
$$

where $$H(M \mid C)$$ is the entropy of $$M$$ conditioned on $$C$$, i.e., after
observing $$C$$.

$$
\begin{align*}
H(M \mid C) &= - \sum\limits_{c} P(c) \sum\limits_m P(m \mid c) \log P(m \mid c) \\
            &= - \sum\limits_{c} \sum\limits_m P(c) P(m \mid c) \log P(m \mid c) \\
            &= - \sum\limits_{c} \sum\limits_m P(m, c) \log P(m \mid c) \\
\end{align*}
$$

Now, we can derive the common formula for mutual information:

$$
\begin{align*}
I(M; C) &= H(M) - H(M \mid C) \\
        &= - \sum\limits_m P(m) \log P(m) - (- \sum\limits_m \sum\limits_c P(m, c) \log P(m \mid c)) && \text{Defined above} \\
        &= - \sum\limits_m \left( P(m) \log P(m) - \sum\limits_c P(m, c) \log P(m \mid c) \right) && \text{Factor common summation} \\
        &= - \sum\limits_m \sum\limits_c \left(P(c \mid m) P(m) \log P(m) - P(m, c) \log P(m \mid c) \right) && \text{Trick: $P(m) = \sum\limits_c P(c \mid m) P(m)$}\\
        &= - \sum\limits_m \sum\limits_c \left(P(m, c) \log P(m) - P(m, c) \log P(m \mid c) \right) && \text{Chain rule} \\
        &= - \sum\limits_m \sum\limits_c \left(P(m, c) \log P(m) - P(m, c) (\log P(m, c) - \log P(c)) \right) && \text{Chain: $P(m \mid c) = \frac{P(m, c)}{P(c)}$} \\
        &= - \sum\limits_m \sum\limits_c P(m, c) \left(\log P(m) - \log P(m, c) + \log P(c) \right) && \text{Factor out $P(m, c)$} \\
        &= - \sum\limits_m \sum\limits_c P(m, c) \log \left( \frac{P(m) P(c)}{P(m, c)} \right) && \text{Logs}
\end{align*}
$$

Note that the formula for mutual information is symmetric, so $$I(M; C) = I(C;
M)$$.

If $$M$$ and $$C$$ are independent, then $$P(m, c) = P(m)P(c)$$, so the log
quantity goes to zero and mutual information is minimized. Mutual information
is maximized when $$H(M \mid C) = 0$$ (which corresponds to $$P(c \mid m) =
1$$).

# Finding Informative Regulatory Elements (FIRE)

So, how do we apply information theory to the motif-finding problem? Elemento _et al._ proposed the FIRE algorithm, which 
