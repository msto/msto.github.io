---
layout: lecture
title: Robust regression and logistic regression
lecture: 6
course: ECE 532
date: 2019-02-12
---

# Administrative notes

- Office hours after class today

# Summary

Today in class we introduced an alternative to least squares regression, robust
regression, that better handles noise and outliers in the dataset. We also
began to discuss logistic regression, which can be applied to classification
problems.

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

# Robust regression

The motivation for robust regression is to deal with contamination in our data
(as we'll explore in homework 2), where least squares can give us a bad fit.
All the methods we've seen so far have been variations on least squares - OLS,
ridge = OLS + L2 penalty, Lasso = OLS + L1 penalty, and even when adding a
penalty, none are robust to noise. So we need to change the least squares part
of our objective function - instead of summing squares, we need to take the sum
of some other function.

# Least absolute deviation (LAD) regression

We define the estimate for LAD by taking the sum of absolute residuals instead
of the sum of squared residuals:

$$
\hat{\beta}_{LAD} = \argmin\limits_{\beta} \left\{ \sum \card{y_i - X_i' \beta} \right \}
$$

This ends up being a robust estimator. But why? Intuitively, we can think of
the sum of squares as analogous to the mean, and the sum of absolute values as
analogous to the median, and we know that the median is a more robust measure
than the mean.

With a little more mathematical precision, it is a fact that minimizing the sum
of squared distances is equivalent to computing a mean. In the 1-dimensional
setting, if we have a collection of points on a line, the point that minimizes
the sum of squared distances to it is the mean. In other words, given a set of
$$x_i$$, we want to minimize $$f(\mu) = \sum (x_i - \mu)^2$$, which we do by
taking the derivative:

$$
\begin{align*}
f'(\mu) = \sum -2 (x_i - \mu) &= 0 \\
    \sum (x_i - \mu) &= 0 \\
    - n\mu + \sum x_i  &= 0 \\
    \mu = \frac{\sum x_i}{n}
\end{align*}
$$

which is the mean.

It is also a fact that minimizing the sum of absolute distances is equivalent
to computing a median. We won't derive this formally, but here we are trying to
minimize $$f(\mu) = \sum \card{x_i - \mu}$$. Intuitively (or proof by picture),
if we have a collection of points on a line, choosing $$\mu$$ on either side of
the points will cause some of these distances to be extreme. We want a $$\mu$$
that's in the middle so the distances are balanced, and this ends up being the
median. In higher dimensional space, you can think of this as trying to find a
line that acts as a median between our residuals.

So LAD is robust. As a note, we can more cleanly define it in matrix form:

$$
\hat{\beta}_{LAD} = \argmin\limits_{\beta} \norm{y - X\beta}_1
$$

# Probabilistic interpretation of LAD

Again our model is

$$
y_i = X_i' \beta + \varepsilon_i
$$

In our earlier discussions of ridge and Lasso regression, we kept the
assumption that our errors were normally distributed, and modeled a prior on
$$\beta$$. Now, we want to define a different distribution on the errors
$$\varepsilon_i$$. If we choose the appropriate distribution, it will give us
LAD as the maximum likelihood solution. (Note that here we are fundamentally
changing the objective function, not just adding a penalty).

Like the last time we used the L1 norm, in Lasso regression, we will choose the
Laplacian distribution. (This will be a common choice of distribution when
trying to get an absolute value inside the MLE - the Gaussian distribution is
$$\approx e^{x^2}$$, and the Laplacian is $$\approx e^{\card{x}}$$.)

So we will assume that our errors $$\varepsilon_i$$ are independently and
identically distributed with common pdf

$$
p_{\varepsilon}(u) = \frac{1}{2\sigma} \exp \left( \frac{-\card{u}}{\sigma} \right)
$$

So let us calculate the maximum likelihood estimate, letting $$P_{\beta}(X_i,
y_i)$$ denote the probability of $$X_i$$ and $$y_i$$ if the true parameter is
$$\beta$$:

$$
\begin{align*}
\L_{\beta}(X, y) &= \prod P_{\beta} (X_i, y_i) && \text{Independence of errors} \\
                 &= \prod P_{\varepsilon} (y_i - X_i' \beta) && \text{Probability of each $\varepsilon_i$} \\
                 &= \prod \frac{1}{2\sigma} \exp \left( \frac{-\card{y_i - X_i' \beta}}{\sigma} \right)
\end{align*}
$$

Maximizing this is equivalent to:

$$
\begin{align*}
\max\limits_{\beta} \L_{\beta}(X, y) &= \max\limits_{\beta} \exp \left( \sum \frac{-\card{y_i - X_i' \beta}}{\sigma} \right) \\
  &= \max\limits_{\beta} \frac{-1}{\sigma} \sum \card{y_i - X_i' \beta} && \text{Monotonicity of exponential} \\
  &= \min\limits_{\beta} \norm{y - X\beta}_1 \\
  &= \hat{\beta}_{LAD}
\end{align*}
$$

So our maximum likelihood estimate in the probabilistic interpretation is the
defined least absolute deviation estimator.

# Notes on intuition

Note that the Laplacian has "heavier tails" than the Gaussian distribution.
Eventually, if you move far enough away from 0, the pdf of the Laplacian
distribution will be above the pdf of the Gaussian. This is relevant because we
run LAD if we think there's noise in our dataset. From the model's perspective,
we're saying the errors $$\varepsilon_i$$ have a different distribution.
Specifically, by assuming they are Laplacian distributed, we are saying that
the errors "spend more time away from 0" than errors that are Gaussian
distributed - since the density is greater on the tails, you're more likely to
observe larger errors, and the error terms are more dispersed. 

Tying back in with our discussion of L1 regularization, we can also think of
LAD as encouraging sparsity among our _errors_ (as opposed to our residuals in
Lasso). Essentially, it's okay if one outlier has a large error as long as the
majority of our points are well fit. Similarly, OLS can be thought of as like
ridge regression - it encourages all our residuals to be small.

Moral: LAD gives us a more robust fit.


