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
LAD as encouraging sparsity among our _errors_ (as opposed to among our
regression coefficients in Lasso). Essentially, it's okay if one outlier has a
large error as long as the majority of our points are well fit. Similarly, OLS
can be thought of as like ridge regression - it encourages all our residuals to
be small.

Moral: LAD gives us a more robust fit.

Our final comment will be that $$\hat{\beta}_{LAD}$$ has no closed-form
solution, but solving for $$\beta$$ involves solving a convex function, so it
is tractable to strategies such as gradient descent, which we'll discuss next
lecture. (Proof: $$y-X\beta$$ is a linear operation, so it is convex, and the
L1-norm, or absolute value, is convex, and any composition of convex functions
is convex.)

# Other loss functions

We have defined functions $$f$$ of our linear regression residuals that we have
minimized to obtain regression estimates. So far, we have chosen $$f(u) =
u^2$$, in least squares, and $$f(u) = \card{u}$$, in LAD. Other choices include
the [Tukey biweight function](http://mathworld.wolfram.com/TukeysBiweight.html)
and the [Huber loss function](https://en.wikipedia.org/wiki/Huber_loss), which
is piecewise quadratic close to 0 and linear beyond a certain threshold.

Each loss function has a generative model interpretation

$$
p_{\varepsilon}(u) \approx \exp(- f(u))
$$

Tukey has an extremely heavy tailed pdf, but it is not convex and can be
inefficient to optimize. OLS, LAD, and Huber are all convex.

The relationship between the loss functions and their respective probability
density functions can be intuited as "if the loss function grows fast, then the
pdf shrinks fast".

In the homework you will use the matlab `robustfit` package to compare
performance with different losses and convince yourself that OLS is not the
right strategy when we have outliers in our data.

# Logistic regression

We now move on to logistic regression. The reference for this material is
chapter 4 in either Bishop or Elements of Statistical Learning.

We have a new motivating context. Suppose we have data $$\{(X_i,
y_i)\}_{i=1}^n$$, where $$y_i$$ is categorical. For now, we'll restrict
ourselves to the simple case where $$y_i$$ is an indicator variable, i.e.,
$$y_i \in \{0, 1\}$$.

Applying linear regression doesn't make much sense here. In linear regression,
we are intuitively saying that if we increase the magnitude of some components
of $$X_i$$, we will observe an increase in $$y_i$$. Here, however, $$y_i$$
can't "grow" - it is either 0 or 1. Instead, we'd like to model the belief that
if we increase the magnitude of some components of $$X_i$$, $$y_i$$ is more
likely to be 1. (For example, whether BMI or blood cholesterol levels are
associated with the presence of heart disease.)

# Generative model of logistic regression

This time, we will start with the generative model, since logistic regression
doesn't have a nice algebraic or geometric perspective like OLS did (though we
will see a geometric view later). It might seem like it's coming from out of
nowhere at first, but we'll take it as given and see where it came from later.

We will assume that the $$y_i$$ are generated probabilistically from the
$$X_i$$ and a parameter $$\beta$$, with

$$
P(y_i = 1) = \frac{1}{1 + \exp(-X_i' \beta)}
$$

Note that since there are only two possible outcomes for $$y_i$$, this implies

$$
P(y_i = 0) = 1 - P(y_i=1) = \frac{\exp(-X_i'\beta)}{1 + \exp(-X_i' \beta)}
$$

The logistic function is defined as:

$$
f(u) = \frac{1}{1 + e^{-u}}
$$

and has a sigmoidal shape. By choosing this function to model our
probabilities, we are saying that larger values of $$X_i' \beta$$ are
associated with more extreme probabilities.

# MLE of logistic regression

From the generative model, we again want to find the maximum likelihood
estimate to obtain a formula for $$\hat{\beta}$$ and fit our model. We won't be
able to find a closed form solution, but we can show that the problem is
convex.

$$
\begin{align*}
L_{\beta}(X, y) &= \prod L_{\beta}(X,y) \\
                &= \prod \left( \frac{1}{1 + \exp(-X_i' \beta)}\right)^{y_i} \left(\frac{\exp(-X_i'\beta)}{1 + \exp(-X_i' \beta)}\right)^{(1-y_i)}
\end{align*}
$$

Note that we no longer have our Gaussian pdf since we're not assuming Gaussian
error terms. What are we saying here instead? The left quantity is the
probability that $$y_i$$ is 1, and the right, that $$y_i$$ is 0. Since $$y_i$$
is an indicator variable, the exponents $$y_i$$ and $$1 - y_i$$ control which
probability is "on" for each observation.

Maximizing this likelihood is equivalent to maximizing the log-likelihood:

$$
\begin{align*}
\log \L_{\beta} (X,y) &= \sum \left[ y_i \log \left( \frac{1}{1 + \exp(-X_i' \beta)} \right) + (1 - y_i) \log \left( \frac{\exp(-X_i'\beta)}{1 + \exp(-X_i' \beta)} \right) \right] \\
  &= \sum \left[ -y_i \log (1 + \exp(-X_i' \beta)) + (1 - y_i)(-X_i' \beta) - (1- y_i) \log (1 + \exp(-X_i' \beta)) \right] \\
  &= \sum \left[ (1-y_i)(-X_i' \beta) - \log (1 + \exp(-X_i' \beta)) \right] && \text{ $y_i$ terms cancel}
  &= \sum \left[ (y_i- 1)(X_i' \beta) - \log (1 + \exp(-X_i' \beta)) \right] 
\end{align*}
$$

Maxmizing this function is equivalent to minimizing its negative,

$$
f(\beta) = \sum \left[ (1-y_i)(X_i' \beta) + \log (1 + \exp(-X_i' \beta)) \right]
$$

Remember that this doesn't have a closed-form solution, so we're instead trying
to show that $$f$$ is convex. Recall from calculus that we show a function is
convex by taking a double derivative (i.e., a gradient then a Hessian).

First let's take the gradient:

$$
\begin{align*}
\nabla_{\beta} f(\beta) &= \sum \left[ (1-y_i)X_i + \frac{1}{1 + \exp(-X_i' \beta)}\exp(-X_i'\beta)(-X_i) \right] \\
  &= \sum \left[ (1-y_i)X_i - \frac{1}{1 + \exp(X_i' \beta)}(X_i) \right]
\end{align*}
$$

And our Hessian is thus:

$$
\begin{align*}
\nabla_{\beta}^{2} f(\beta) &= \sum \frac{1}{(\exp(X_i'\beta) + 1)^2}\exp(X_i' \beta) X_i X_i' \\
  &= \sum \frac{\exp(X_i' \beta)}{(\exp(X_i'\beta) + 1)^2} X_i X_i' \\
\end{align*}
$$

Note that the first $$X_i$$ in the multiplication is from the chain rule, and
the second is a carry-over from the gradient. We've used a common trick to
transpose the second $$X_i$$ so we get the matrix that's expected in the
Hessian.

You may remember that a function $$f$$ is convex if its Hessian $$\nabla^2 f$$
is positive semi-definite. We have remarked upon positive semi-definiteness in
class, and a notable characteristic is that the Hessian (or any matrix) is
positive semi-definite if the following holds:

$$
v' (\nabla^2 f) v \ge 0 ~\forall~ v \in \R^p
$$

We can verify this:

$$
\begin{align*}
v' (\nabla^2 f) v &= v' \left[ \sum \frac{\exp(X_i' \beta)}{(\exp(X_i'\beta) + 1)^2} X_i X_i' \right] v \\
  &= \sum \frac{\exp(X_i' \beta)}{(\exp(X_i'\beta) + 1)^2} v' X_i X_i' v \\ 
  &= \sum \frac{\exp(X_i' \beta)}{(\exp(X_i'\beta) + 1)^2} (X_i' v)^2 \\ 
\end{align*}
$$

Note that $$X_i' v$$ is a scalar, and its square is always non-negative, and
the fraction is an exponential (always positive) over a square of an
exponential (always positive), so this product is always non-negative and our
Hessian is positive semi-definite.

We conclude that $$f(\beta)$$ is convex. It is therefore "easy" to find the
estimate $$\hat{\beta}_{logistic} = \argmin\limits_{\beta} f(\beta)$$. How? By
applying gradient descent, which we will discuss in detail in the next lecture.

# Gradient descent

We would like an all-purpose solver for convex optimization problems (not just
logistic regression). Gradient descent is such a tool.

The idea is to start at some point $$\beta^{(0)}$$ and iteratively obtain
updates $$\beta^{(1)}, \beta^{(2)}, \cdots, \beta^{(t)}$$ by going in the
direction of steepest descent.

The formula for the gradient descent update is:

$$
\beta^{(t)} = \beta^{(t-1)} - \eta \nabla f(\beta^{(t-1)})
$$

where $$\eta$$ is a defined step size. Recall that the gradient of the function
points in the direction of steepest increase, so we choose to go in the
opposite direction.
