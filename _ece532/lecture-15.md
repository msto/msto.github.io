---
layout: lecture
title: Dimensionality reduction
lecture: 15
course: ECE 532
date: 2019-03-19
---

# Administrative notes

- Midterm 2 next Tuesday (April 2). Same format as midterm 1.
- Midterm review Friday 3:30-5:30

# Summary

Today in class we discussed linear dimensionality reduction, specifically
principal components analysis.

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
\newcommand{\bigdot}{\boldsymbol{\cdot}}
$$

# Motivation

We can think of three primary motivations to reduce the dimensionality of our data:

1. Computational savings - Algorithms generally cost more in higher dimensions
or take longer to converge. By compressing our data, we can improve
time/space efficiency.
2. Statistical benefits - Fewer dimensions can yield more generalizable models.
For example, in logistic regression, it's typically possible to find a linearly
separating hyperplane for any collection of data points in high enough
dimensions.
3. Visualization - We can't visualize data points in more than three
dimensions. Dimensionality reduction allows us to create interpretable 2D and
3D visualizations of high-dimensional data.

# Principal components analysis (PCA) 

PCA is an unsupervised dimensionality reduction technique. (See Bishop ch. 12 or ESL ch. 14 for a detailed reference.)

Again, our setting is a collection of $$p$$-dimensional feature vectors,
$$\{X_i\}_{i=1}^n \in \R^p$$. Our goal is to find the "best" linear
transformation to a lower dimensional space, $$f : \R^p \mapsto \R^q, q< p$$.
Here, when we say "best", we mean we want to choose the transformation $$f$$
that maximally captures the variation in our data._ 
(Later we'll see another approach, Johnson-Lindenstrauss embedding, where the
"best" projection is one that best preserves distance between points.)

Consider the 1-dimensional projection case $$q=1$$.
As in LDA, we want to find a direction (i.e. unit vector) $$u \in \R^p$$ that
maximizes variances, and consider projecting our points onto $$\{u' X_i\}$$.

Recall the estimate of variance in a sample $$\{y_i\}$$ is 

$$
\Var[y] = \frac{1}{n} \sum (y_i -\bar{y})^2
$$

Here, our $$y_i = u' X_i$$, so we have

$$
\bar{y} = \frac{1}{n} \sum u'X_i = u'(\frac{1}{n} \sum X_i) = u' \bar{X}
$$

## PCA objective function and algorithm

We write the objective function to maximize the variance of the projected points.

$$
\begin{align}
J &= \frac{1}{n} \sum (u'X_i - u'\bar{X})^2 \\
  &= \frac{1}{n} \sum (u' (X_i - \bar{X})^2 \\
  &= \frac{1}{n} \sum \left(u' (X_i - \bar{X})(X_i-\bar{X})' u \right) \\
  &= u' \left(\frac{1}{n} \sum (X_i - \bar{X})(X_i-\bar{X})' \right) u \\
  &= u' S u
\end{align}
$$

where $$S$$ is a matrix that can be defined entirely from our original data.

So PCA solves the problem

$$
\max\limits_{\norm{u} = 1} u' Su, \quad S = \frac{1}{n} \sum (X_i - \bar{X})(X_i - \bar{X})'
$$

The solution to this problem is the top eigenvector of $$S$$, i.e., the eigenvector corresponding to the maximum eigenvalue. (We will show why momentarily).

The PCA algorithm for $$q=1$$ is therefore the following:
1. Construct $$S = \frac{1}{n} \sum (X_i - \bar{X})(X_i - \bar{X})'$$
2. Compute the top eigenvector $$u$$ of $$S$$
3. Project all data onto $$\{u'X_i\}$$

TODO: aside about re-centering and re-writing

## Digression on singular value decomposition (SVD)

So, why is the optimization problem $$\max\limits_{\norm{u}=1} u'Su$$ solved by
the maximum eigenvector of $$S$$?_

_Fact:_ Any real, symmetric matrix has an orthonormal basis of eigenvectors. (And note that $$X'X$$ is symmetric for all matrices $$X$$.)

A more basic fact: for all matrices $$A \in \R^{m \times n}$$, it is always possible to construct the singular value decomposition (SVD) of $$A$$:

$$
A = U \Sigma V' = U \begin{pmatrix} D && 0_{r \times (n-r)} \\ 0_{(m-r) \times r} && 0 \end{pmatrix} V'
$$

where $$U \in \R^{m \times m}, V \in \R^{n \times n}$$, the columns of $$U$$
are orthonormal, the columns of $$V$$ are orthonormal, and $$D$$ is diagonal
with positive entries.

The columns of $$U$$ are the left singular vectors of $$A$$, the columns of
$$V$$ are the right singular vectors of $$A$$, and the values in $$D$$ are the
singular values of $$A$$. 

If $$A$$ is symmetric, then $$U=V$$ and their columns are the eigenvectors of
$$A$$.
