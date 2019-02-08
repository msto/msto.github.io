---
layout: lecture
title: Ridge and Lasso Regression
lecture: 4
date: 2019-01-31
---

# Administrative notes

- Muni has a regular location for office hours - Engineering Hall 2355 on
  Fridays from 3:30-5:30pm
- No class next Tuesday (Feb 5)
- Next week Professor Loh will have office hours after class on Thursday (Feb
  7) instead of Tuesday due to travel

# Summary

Today in class we continued our discussion of what to do when the matrix
$$X'X$$ is not invertible and showed two variants of OLS - ridge and lasso
regresion.

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

# Recap: Cases where $$X'X$$ is not invertible

Remember that when $$X'X$$ is not invertible, the OLS formula
$$\hat{\beta}_{OLS} = (X'X)^{-1} X'y$$ can't be computed.

On example is when the columns of $$X$$ are not linearly independent. In the
last class, we looked at a special case of this. When $$X \in \R^{n \times p}$$
is wide, i.e. $$p > n$$, the columns can't be linearly independent because they
are a set of more than $$n$$ columns in $$n$$-dimensional space. In the
homework you will see another example of a $$3 \times 3$$ matrix where $$X'X$$
isn't invertible.

We suggested one possible fix for this problem in the last lecture: add a matrix $$\lambda I$$ to $$X'X$$, i.e.

$$
\hat{\beta}_{ridge} = (X'X + \lambda I)^{-1} X'y
$$

for some $$ \lambda > 0$$. We called this solution _ridge regression_.

## Why does ridge regression fix the problem?

We rely on the fact that $$(X'X + \lambda I)$$ is always invertible if
$$\lambda > 0$$. We will show this in more detail later in the term when we
discuss singular values, but for now we can show it with eigenvalues. 

Recall that a square matrix $$X \in \R^{n \times n}$$ is invertible if all its
eigenvalues are nonzero. Also, note that $$X'X$$ only has eigenvalues $$\ge
0$$. Why? Because $$X'X$$ is a positive semi-definite matrix. We will explore
this definition more later, but for now, know that any positive semi-definite
matrix $$A$$ has the following property for all vectors $$v$$:

$$
v' A v \ge 0
$$

We can prove that $$X'X$$ has this positive semi-definite property:

$$
v' (X'X) v = (Xv)' Xv = w'w \ge 0
$$

since the inner product $$w'w$$ is the sum of squares $$\sum w_i^2$$ and
therefore cannot be negative. $$X'X$$ is therefore positive semi-definite, and
so all its eigenvalues are non-negative (take this consequence on faith for
now).

So why are the eigenvalues of $$X'X + \lambda I > 0$$? Intuitively, the
addition of $$\lambda I$$ is taking all the eigenvalues of $$X'X$$ and "pushing
them up a little". Note that the eigenvalues of $$X'X + \lambda I$$ are related
to the eigenvalues of $$X'X$$. If a vector $$v$$ is an eigenvector of $$X'X$$
with eigenvalue $$\alpha$$, then $$X'Xv = \alpha v$$. This vector remains an
eigenvector of $$X'X + \lambda I$$, as we can show:

$$
(X'X + \lambda I) v = X'X v + \lambda Iv =  \alpha v + \lambda v = (\alpha + \lambda) v
$$

So any eigenvector $$v$$ of $$X'X$$ is an eigenvector of $$X'X + \lambda I$$
with eigenvalue $$\alpha + \lambda$$. Since $$X'X$$ is positive semi-definite,
$$\alpha \ge 0$$, so the minimum eigenvalue of $$X'X + \lambda I$$ is
$$\lambda$$, which we have defined to be greater than 0. Therefore $$X'X +
\lambda I$$ only has positive eigenvalues and is invertible.

So ridge regression is actually a fix for the non-invertible problem that makes
sense for all $$\lambda > 0$$.

## Ridge regression as optimization

Another way of viewing $$\hat{\beta}_{ridge}$$ is as the solution to 

$$
\min\limits_{\beta} \{ \norm{y - X\beta}_2^2 + \lambda \norm{\beta}_2^2 \}
$$

Why? Let's take the gradient and set $$\nabla_{\beta} f = 0$$ and solve:

$$
\begin{align*}
\nabla_{\beta} f &= \nabla_{\beta} \norm{y - X\beta}_2^2 + \lambda \norm{\beta}_2^2 \\
                 &= \nabla_{\beta} \left( (y - X\beta)'(y - X\beta) + \lambda \beta' \beta \right) \\
                 &= \nabla_{\beta} (y'y - 2y'X\beta + \beta'X'X\beta + \lambda \beta'\beta) \\
                 &= \nabla_{\beta} (-2y'X\beta + \beta' (X'X + \lambda I) \beta) && \beta'\beta = \beta'I\beta \\
                 &= -2X'y + 2(X'X + \lambda I) \beta
\end{align*}
$$

Setting to zero, we have

$$
\begin{align*}
-2X'y + 2(X'X + \lambda I) \beta &= 0 \\
(X'X + \lambda I) \beta &= X'y \\
\beta &= (X'X + \lambda I)^{-1} X'y
\end{align*}
$$

which is our ridge regression estimator $$\hat{\beta}_{ridge}$$. Therefore we have shown

$$
\hat{\beta}_{ridge} = \argmin\limits_{\beta} \left \{ \norm{y - X\beta}_2^2 + \lambda \norm{\beta}_2^2 \right \}
$$

We call the 2-norm of $$\beta$$ the _ridge regularization term_ or the _ridge
penalty_. It encourages structure in our solution.

## Regularization

The idea of regularization is that we are minimizing the quantity 

$$
\text{(loss)} + \lambda \cdot \text{(penalty)}
$$

where $$\lambda$$ is a regularization parameter. In regularization, we want to
keep the loss small, but we also want to keep the penalty small. The
regularization parameter controls the trade-off between a small loss and a
small penalty.

In ridge regression, the penalty is $$\norm{\beta}_2^2$$, which encourages
small regression vectors. We use it to pick the "best" option when OLS has
multiple solutions.

As $$\lambda$$ approaches $$\infty$$, we mostly care about minimizing the
penalty, so $$\hat{\beta}_{ridge} \to 0$$. So we sometimes call this a
"shrinkage method". In the homework you'll explore the effects of different
sizes of $$\lambda$$.

## Probabilistic interpretation of ridge regression

We previously defined a generative model of linear regression:

$$
\begin{align*}
y_i = X_i' \beta + \varepsilon_i && \varepsilon_i \sim N(0, \sigma^2)
\end{align*}
$$

Now we can also assume randomness in $$\beta$$, which we can think of as
modeling in extra noise.

If we want to calculate the maximum likelihood estimate (MLE) for $$\beta$$, we
need to introduce a probability density function for $$\beta$$

$$
\begin{align*}
\L_{\beta}(X, y) &= p(\beta) \cdot P_{\beta}(X, y) \\
                 &= p(\beta) \prod\limits_{i} \frac{1}{\sqrt{2\pi}\sigma} \exp \left(\frac{-(y_i - X_i'\beta)^2}{2\sigma^2}\right) && \text{Gaussian assumption} \\
                 &= p(\beta) \prod\limits_{i} \frac{1}{\sqrt{2\pi}} \exp \left(\frac{-1}{2}(y_i - X_i'\beta)^2\right) && \text{Assume $\sigma=1$ for simplicity}\\
                 &= p(\beta) \left(\frac{1}{\sqrt{2\pi}}\right)^n \exp \left(\frac{-1}{2}\sum\limits_{i}(y_i - X_i'\beta)^2\right) \\
                 &= \left(\frac{1}{\sqrt{2\pi}}\right)^n \exp \left(\frac{-1}{2}\sum\limits_{i}(y_i - X_i'\beta)^2 + \log p(\beta)\right) \\
\end{align*}
$$

We want to maximize this likelihood with respect to $$\beta$$. Since $$(1 / \sqrt{2\pi})^n$$ is fixed with respect to $$\beta$$, we only need to maximize the exponential function, which is equivalent to minimizing the negation of the exponent

$$
\frac{1}{2} \sum (y_i - X_i' \beta)^2 - \log p(\beta)
$$

which is equivalent to minimizing

$$
\norm{y - X\beta}_2^2 - 2 \log p(\beta)
$$

Now we want to relate this problem to ridge regression. If $$\beta$$ has some
distribution, we want to reverse engineer it and show that the MLE is the same
as ridge regression, that is,

$$
- \log p(\beta) \approx \lambda \norm{\beta}_2^2
$$

Suppose $$\beta \sim N(0, \frac{1}{lambda} I)$$. Then the pdf of $$\beta$$ is

$$
\begin{align*}
p(\beta) &= \frac{1}{\sqrt{\det(2\pi\Sigma)}} \exp\left(\frac{-1}{2}(\beta - \mu)' \Sigma^{-1} (\beta - \mu) \right) \\
         &= c \cdot \exp \left(\frac{-1}{2} \beta'(\lambda I) \beta\right) && c = \frac{1}{\sqrt{\det(2\pi\Sigma)}}\\
         &= c \cdot \exp \left(\frac{-\lambda}{2} \beta'\beta\right) \\
         &= c \cdot \exp \left(\frac{-\lambda}{2} \norm{\beta}_2^2\right) \\
\end{align*}
$$

and the problem of optimizing our likelihood function becomes

$$
\begin{align*}
\max\limits_{\beta} L_{\beta}(X, y) &= \min\limits_{\beta} \norm{y - X\beta}_2^2 - 2 \log p(\beta) \\
        &= \min\limits_{\beta} \norm{y - X\beta}_2^2 - 2 \log \left[ \log c - \frac{\lambda}{2} \norm{\beta}_2^2 \right] \\
        &= \min\limits_{\beta} \norm{y - X\beta}_2^2 + \lambda \norm{\beta}_2^2  \\
\end{align*}
$$

Therefore, ridge regression with parameter $$\lambda$$ is the same as the MLE for the generative model 

$$
y_i = X_i' \beta + \varepsilon_i
$$

where $$\varepsilon_i \sim N(0, \sigma^2)$$ and $$\beta \sim N(0,
\frac{1}{\lambda}I)$$.

The generative model allows us to model uncertainty in $$\beta$$. An important
note is that the prior is centered around $$0$$, which encourages a smaller
$$\beta$$. Different values of $$\lambda$$ quantify our uncertainty. Larger
$$\lambda$$ mean our covariance matrix $$\Sigma \approx 0$$, so $$\beta$$ is
very close to 0. Note that these are the same conclusions we reached from our
algebraic model of $$\hat{\beta}_{ridge}$$.

One potential issue we can see is that we don't know how to choose $$\lambda$$.
We will discuss this in the next lecture, but the answer is by using
cross-validation.

## Lasso regression

Lasso regression uses another regularizer, or penalty.

$$
\hat{\beta}_{Lasso} = \argmin\limits_{\beta} \left\{ \norm{y - X\beta}_2^2 + \lambda \norm{\beta}_1 \right\}
$$

where $$\norm{\beta}_1$$ is the L1 norm of $$\beta$$, $$\sum \card{\beta_j}$$.

It turns out that the solutions to Lasso regression tend to be sparse (many
zero entries in $$\hat{\beta}$$).  We can demonstrate this empirically, and in
homework 2 we will see that as $$\lambda$$ increases, the number of zero
entries in $$\hat{\beta}$$ increases. This yields a more interpretable
solution, as the remaining nonzero weights in $$\hat{\beta}$$ correspond to the
relative importance of the predictor variables $$X_i$$, while ridge regression
makes $$\hat{\beta}$$ uniformly smaller.

Why does the L1 penalty make things sparse? There are many ways to answer this.
The motivation in the original paper by Tibshirani (1996) observed that in
order to make the coefficients of the regression vector small, we should solve
the following:

$$
\min\limits_{\beta} \left\{ \norm{y-X\beta}_2^2 + \lambda \cdot ( \text{# nonzero entries in $\beta$}) \right\}
$$

so our penalty counts the number of nonzero coefficients.

The issue is that this formulation is very hard to solve because it is not
convex. (We won't be discussing convexity in detail in this class, so just note
that convex functions are easier to solve with methods such as gradient
descent.) We can restrict to $$\beta$$ with a fixed number of non-zero
coefficients and exhaustively solve over all such constraints, but this is an
expensive solution. Fortunately, Lasso is convex!

We can compare the different penalty functions, like so:

1. Ridge: $$\norm{\beta}_2^2 = \sum \beta_j^2$$, penalty function $$f(x) = x^2$$
2. Lasso: $$\norm{\beta}_1 = \sum \card{\beta_j}$$, penalty function $$f(x) = \card{x}$$
2. \# nonzero: $$\norm{\beta}_0 = \sum f(\beta_j)$$, where the penalty function
$$f(x) = 0$$ if $$x=0$$ and $$1$$ otherwise.

A simplified intuition for what it means for a function to be convex is that
if we connect any two points in the function, the connecting line is always on
or above the function. Note that this is the case for the L1 and L2 norms (the
parabola of a quadratic function and the "V" of the absolute value are both
convex), but if we connect 0 with any other point on the L0 norm, the
connecting line falls below the $$f(x)=1$$ line.

The motivation for Lasso is to use the L1 norm as an approximation for the L0
norm we are interested in. Simplifying some complex math, the L1 norm is the
closest convex norm to the L0 norm.

Finally, we note that even though Lasso is convex, so we can find
$$\hat{\beta}_{Lasso}$$ efficiently, there is no closed form solution. This is
in contrast to the formulas we derived for $$\hat{\beta}_{OLS}$$ and
$$\hat{\beta}_{ridge}$$. We instead solve it with algorithms such as gradient
descent using computer packages such as `cvx` or `LASSO` in matlab.

In the next lecture we will discuss the probabilistic interpretation of Lasso
regression.

