---
layout: lecture
title: Logistic regression and gradient descent
lecture: 7
course: ECE 532
date: 2019-02-14
---

# Administrative notes

- Homework 2 due Tuesday
- Midterm 1 next Thursday (Feb 21). The midterm will be entirely theory, no
  code, and will be closed book, closed note, and multiple choice. The exam
  will take up half the class period and we will have lecture the following
  half. It will draw from material covered in class through today's lecture.
  (Note that the next exam may not follow this format.)

# Summary

Today in class we discussed gradient descent and two alternatives (stochastic
gradient descent and Newton-Raphson) and showed how each algorithm can be
applied to solve the logistic regression problem.

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

# Recap: logistic regression

In the logistic regression setting we have data points $$\{(X_i, y_i)\}$$
where, unlike in linear regression, the $$y_i$$ are categorical and only take
the value 0 or 1.

The linear regression model can be defined algebraically, $$y_i = X_i' \beta +
\varepsilon_i$$. However, we define the logistic regression model
probabilistically:

$$
P(y_i = 1) = \frac{1}{1 + \exp(-X_i'\beta)} \\
P(y_i = 0) = 1 - P(y_i = 1) = \frac{\exp(-X_i'\beta)}{1 + \exp(-X_i'\beta)}
$$

These probabilities use the logistic function $$f(u) = \frac{1}{1+\exp(-u)}$$.
It might seem like this is a somewhat arbitrary choice, but we will show where
it comes from in a later lecture.

The maximum likelihood estimate for $$\beta$$ under the logistic regression
model is

$$
\begin{align*}
L_{\beta}(X, y) &= \prod P_{\beta}(X_i, y_i) \\
                &= \prod \left(\frac{1}{1 + \exp(-X_i'\beta)}\right)^{y_i} \left(\frac{\exp(-X_i'\beta)}{1 + \exp(-X_i'\beta)}\right)^{1 - y_i}
\end{align*}
$$

Note that we're using a cool "trick" that we'll see more of - when $$y_i$$ is
1, the exponents work out so that we use $$P(y_i=1)$$, and similarly for $$y_i
= 0$$.

In the last lecture, we showed that maximizing this likelihood is equivalent to
minimizing the function

$$
f(\beta) = \sum \left[(1 - y_i)X_i'\beta + \log(1 + \exp(-X_i'\beta)) \right]
$$

which we showed is convex by calculating the gradient and the Hessian, then
showing that the Hessian is positive semi-definite.

$$
\nabla^2 f = \sum \frac{\exp(X_i'\beta)}{(\exp(X_i'\beta)+1)^2}X_i X_i'
$$

Since $$f$$ doesn't have a closed-form solution, but is convex, we can solve it
using gradient descent.

# Gradient descent

At the end of the last lecture, we introduced the formula for each gradient
descent iterate:

$$
\beta^{(t)} = \beta^{(t-1)} - \eta \nabla f(\beta^{(t-1)})
$$

where $$\eta$$ is the gradient descent step size. Reminder: the gradient is the
direction of steepest increase, so we're choosing to take a step in the
opposite direction. Warning: gradient descent can overshoot if we choose a step
size that is too large (relative to the curvature of the function). One
approach can be to decrease the step size as the algorithm progresses.

# Lipschitz continuity

However, we can make a statement about a fixed step size that shows us gradient
descent will converge if a condition on the function's curvature is met. This
is a result from optimization theory that we will discuss but not prove here,
and is a common guarantee for the convergence of gradient descent.

**Theorem/** Suppose $$f : \R^n \mapsto \R$$ is convex and differentiable.
Suppose $$f$$ is _Lipschitz continuous_, meaning it satisfies the following
inequality for all $$x, y \in R^n$$:

$$
\norm{\nabla f(x) - \nabla f(y)}_2 \le L \norm{x -y}_2
$$

for some constant $$L$$. Then gradient descent with a fixed step size $$\eta
\le \frac{1}{L}$$ satisfies

$$
f(\beta^{(t)}) - f(\beta^{*}) \le \frac{\norm{\beta^{(0)} - \beta^{*}}_2^2}{2 \eta t}
$$

where $$\beta^{*}$$is the true minimizer of $$f$$. This says that as the
gradient descent algorithm progresses, our estimates are guaranteed to approach
$$\beta^{*}$$ at a rate proportional to our step size.

Note that Lipschitz continuity is a condition on the curvature of our function.
If we rearrange the formula, we have

$$
\frac{\norm{\nabla f(x) - \nabla f(y)}_2}{\norm{x - y}_2} \le L
$$

which resembles the formula for slope of a function in 1-dimension. Roughly,
$$L$$ is a bound on the "slope" of our gradient, or how quickly the gradient is
changing. This implies that the gradient is not changing too much and $$f$$ is
not too "curvy". This is a desirable condition for gradient descent, because if
$$f$$ is too steep, we can overshoot our minimum by taking too large of a step.

Now, we also have a condition on our step size: $$\eta \le \frac{1}{L}$$. This
is saying that if our function has more curvature (larger $$L$$), we need to
have a smaller step size $$\eta$$ to avoid over-shooting.

The final conclusion we can draw from our theorem is that as $$t$$ gets bigger,
the distance between the value of the function at each iterate and the true
minimum, $$f(\beta^{(t)}) - f(\beta^{*})$$, decreases. The error of our iterate
shrinks and approaches the true mean at rate $$\frac{1}{t}$$. Eventually,
$$f(\beta^{(t)})$$ will converge to $$f(\beta^{*})$$, implying that our iterate
$$\beta^{(t)}$$ will converge to $$\beta^{*}$$.

# Variants of gradient descent

Quick notes on variations of gradient descent:
1) 
