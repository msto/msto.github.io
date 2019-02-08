---
layout: lecture
title: Confidence intervals
lecture: 3
course: ECE 532
date: 2019-01-29
---

# Administrative notes

- Homework 1 is due next Tuesday (Feb 5) via Gradescope by 2:30pm 
- No class next Tuesday (Feb 5)

# Summary

Today in class we reviewed our discussion of ordinary least squares (OLS)
regression and discussed how to construct confidence intervals around the
entries of our estimated regression vector $$\hat{\beta}_{OLS}$$, primarily by
exploring the properties of the mean and covariance of a multivariate Gaussian
variable. We also began to introduce ridge regression.

$$
%% Latex helpers
\newcommand{\norm}[1]{\left\lVert{#1}\right\rVert}
\newcommand{\R}{\mathbb{R}}
\newcommand{\L}{\mathcal{L}}
\newcommand{\E}{\mathrm{E}}
\newcommand{\Var}{\mathrm{Var}}
\newcommand{\Cov}{\mathrm{Cov}}
\newcommand{\Col}{\mathrm{Col}}
\DeclareMathOperator*{\argmin}{arg\,min}
\newcommand{\bigdot}{\boldsymbol{\cdot}}
$$

# Recap: OLS

We have shown how to solve the regression problem $$\hat{\beta}_{OLS} = \argmin
\limits_{\beta} \norm{y - X\beta}_{2}^2$$ where our data is a matrix $$X \in
\R^{n \times p}$$ and our observations are a vector $$y \in \R^n$$.

We have three notable takeaways from the past two lectures:

1. The formula for our estimator $$\hat{\beta}_{OLS} = (X'X)^{-1}X'y$$
2. The observation that $$\{ X \beta : \beta \in \R^p \}$$ is the column space
   of $$X$$, and therefore the estimate $$\hat{\beta}_{OLS}$$, which minimizes
   the Euclidean distance from $$y$$ to $$X \beta$$, corresponds to the
   projection of $$y$$ onto $$\text{Col} X$$.
3. When considering the probabilistic view (or generative model), the OLS
   estimate is equivalent to the maximum likelihood estimate (MLE) if $$y_i =
   X_i' \beta + \varepsilon_i$$ where $$\varepsilon_i
   \stackrel{\text{i.i.d}}{\sim} N(0, \sigma^2)$$. This is because we defined
   the likelihood function
    
    $$
    \begin{align*}
    \L_{\beta}(X, y) &= P_{\beta}(X, y) \\
                     &= \prod\limits_{i} P_{\beta} (X_i, y_i) && \text{By our independence assumption} \\
                     &= \prod\limits_{i} \frac{1}{\sqrt{2\pi} \sigma} \exp \left( \frac{- (y_i - X_i'\beta)^2}{2\sigma^2} \right) && \text{By our Gaussian assumption}
    \end{align*}
    $$

    so maximizing $$\L$$ over $$\beta$$ is equivalent to minimizing $$\sum (y_i -
    X_i' \beta)^2$$ over $$\beta$$.

Why are we interested in the probabilistic model? For one, it permits us to
construct confidence intervals and perform hypothesis tests.

# Confidence intervals for $$\beta_j$$

In the last lecture we introduced the intuition that our confidence interval
should be our estimate plus or minus some quantity times the standard deviation
of our estimate, or $$\hat{\beta}_j \pm c \sqrt{v_j}$$ where $$v_j =
\text{Var}(\hat{\beta}_j)$$ and $$c$$ is some constant. But what are
$$\text{Var}(\hat{\beta}_j)$$ and $$c$$? Well, it depends on the distribution
of $$\hat{\beta}_j$$.

From our formula, we have

$$
\begin{align*}
\hat{\beta} &= (X'X)^{-1} X' y \\
            &= (X'X)^{-1} X' (X \beta + \varepsilon) \\
            &= \beta + (X'X)^{-1} X' \varepsilon
\end{align*}
$$

Note that the only source of randomness in our estimator is $$\varepsilon$$, as
$$\beta$$ and $$X$$ are both fixed. If $$\varepsilon$$ is a Gaussian vector,
then $$(X'X)^{-1} X' \varepsilon$$ is also Gaussian, since $$A\varepsilon$$ is
Gaussian if $$A$$ is a fixed matrix. Each $$\varepsilon_i \sim N(0,
\sigma^2)$$, so $$\varepsilon$$ is a multivariate Gaussian.

As a reminder, we say $$x \sim N(\mu, \Sigma)$$ is a multivariate Gaussian
vector in $$\R^n$$ with mean $$\mu \in \R^n$$ and covariance $$\Sigma \in \R^{n
\times n}$$ if it has the probability density function

$$
p(x) = \frac{1}{\sqrt{\det(2 \pi \Sigma)}} \exp \left( \frac{-1}{2} (x - \mu)'  \Sigma^{-1} (x - \mu) \right)
$$

So we can say that $$\varepsilon \sim N(0, \sigma^2 I_n)$$. It now remains to
compute the mean $$\mu$$ and covariance $$\Sigma$$ of $$(X'X)^{-1}X'
\varepsilon$$. 

Let's begin by simplifying the situation and calculating $$\mu$$ and $$\Sigma$$
for $$A\varepsilon$$, where $$A \in \R^{p \times n}$$ is some fixed matrix. We
will make two claims:

1. The mean is $$\E[A\varepsilon] = A \E[\varepsilon]$$
2. The covariance is $$\Cov[A \varepsilon] = A' \Cov[\varepsilon] A$$

This matches what we would expect intuitively from the 1-dimensional
equivalents:

1. The mean $$\E[ax] = a \E[x]$$
2. The variance $$\Var[ax] = a^2 \Var[x]$$

## Claim 1

Let's first verify claim 1, $$\E[A\varepsilon] = A \E[\varepsilon]$$. We will
treat $$\E$$ as an entrywise function, i.e., $$\E[x] = \begin{pmatrix} E[x_1]
&& \cdots && E[x_n] \end{pmatrix}'$$.

As with our earlier proofs of equality, we want to show that these vectors are
entry-wise equal, so we will consider the $$j$$th entry of both sides of the
equation.

On the LHS, we have the expected value of the $$j$$th entry of $$A\varepsilon$$, $$a_j' \varepsilon$$.

$$
\begin{align*}
\E[(A\varepsilon)_j] &= \E [a_j' \varepsilon] && \text{where $a_j'$ is $j$th row of $A$} \\
                     &= \E [ \sum \limits_i a_{ji} \varepsilon_i ] \\
                     &= \sum\limits_i \E[a_{ji} \varepsilon_i] && \text{Linearity of expected value} \\
                     &= \sum\limits_i a_{ji} \E[\varepsilon_i] && \text{Shown above}
\end{align*}
$$

On the RHS, we have the $$j$$th entry of $$ A \begin{pmatrix} \E[\varepsilon_1]
\\ \vdots \\ \E[\varepsilon_n] \end{pmatrix} $$, which is 

$$
a_j' \begin{pmatrix} \E[\varepsilon_1] \\ \vdots \\ \E[\varepsilon_n] \end{pmatrix} = \sum \limits_i a_{ji} \E[\varepsilon_i]
$$

So we have shown $$\E[A\varepsilon] = A \E[\varepsilon]$$. Importantly in our
case, since $$\E[\varepsilon]= 0$$, we have $$E[A\varepsilon] = A
\E[\varepsilon] = 0$$.

## Claim 2

Now let us verify claim 2, $$\Cov[A \varepsilon] = A' \Cov[\varepsilon] A$$.

A quick review of covariance - for any $$z \in \R^n$$, the covariance matrix is
a matrix $$\Sigma \in \R^{n \times n}$$, where $$\Sigma_{ij} = \Cov[z_i, z_j] =
\E[z_i z_j] - \E[z_i]\E[z_j]$$. If $$i=j$$, then $$\Cov[z_i, z_j] = \Var(z_i)$$.

We can make a useful observation: $$\Cov[z] = \E[z z'] - \E[z]\E[z]'$$. Why?
Look at the RHS. The $$ij$$th entry of $$(zz')$$ is $$z_i z_j$$. Since the
expected value is an element-wise function, the $$ij$$th entry of $$\E[zz']$$
is therefore $$E[z_i z_j]$$. 

Also, the $$ij$$th entry of $$\E[z]\E[z]'$$ is the $$ij$$th entry of
$$\begin{pmatrix} \E[z_1] \\ \vdots \\ \E[z_n] \end{pmatrix} \begin{pmatrix}
\E[z_1] && \cdots && \E[z_n]\end{pmatrix}$$. By the same logic, the $$ij$$th
entry of this matrix is $$\E[z_i] \E[z_j]$$.

Therefore the $$ij$$th entry of $$\E[zz'] - \E[z]E[z]'$$ is $$\E[z_i z_j] -
\E[z_i] \E[z_j]$$, which is exactly $$\Cov[z_i, z_j]$$ and the $$ij$$th entry
of $$\Cov[z]$$.

Using this observation, we can prove claim 2:

$$
\begin{align*}
\Cov[A \varepsilon] &= \E [ (A \varepsilon) (A \varepsilon)'] - \E [A \varepsilon] (\E [A \varepsilon])' \\
                    &= \E [ A \varepsilon \varepsilon' A'] && \E [A \varepsilon] = 0 \\
                    &= A \E [\varepsilon \varepsilon' A'] && \text{Claim 1} \\
                    &= A \E [\varepsilon \varepsilon'] A' && \text{Claim 1}
\end{align*}
$$

Note that $$\E[\varepsilon \varepsilon']$$ is $$\Cov [\varepsilon]$$, since
$$\Cov[\varepsilon] = \E [ \varepsilon \varepsilon'] -\E [\varepsilon]
\E[\varepsilon]'$$ and $$\E [\varepsilon] = 0$$. Substituting in, we then have

$$
\begin{align*}
\Cov[A \varepsilon] &= A \Cov [\varepsilon] A' \\
                    &= A \sigma^2 I A' \\
                    &= \sigma^2 AA'
\end{align*}
$$

In general, we have $$\Cov[Az] = A \E[zz'] A' - A \E[z]E[z'] A'$$ if $$\E[z]
\ne 0$$.

Returning to our formula $$\hat{\beta} = \beta + (X'X)^{-1}X' \varepsilon$$, we
have $$\hat{\beta} \sim N(\beta, \sigma^2 AA')$$ where $$A = (X'X)^{-1}X'$$.
Note that $$AA' = (X'X)^{-1}X'X (X'X)^{-T} = (X'X)^{-1}$$, so we finally have

$$
\hat{\beta}_{OLS} \sim N(\beta, \sigma^2 (X'X)^{-1})
$$

## Constructing the CI

Recall that the big picture goal is to create a confidence interval for $$\hat{\beta}_j$$. 

So if we want to construct such a CI, the variance $$\Var[\hat{\beta}_j]$$ is
just $$\sigma^2 v_j$$, where $$v_j$$ is the $$jj$$th entry of $$(X'X)^-1$$, and
the CI is

$$
\hat{\beta}_j \pm z_{\alpha / 2} \sqrt{\sigma^2 v_j}
$$

where $$z_{\alpha / 2}$$ is the quantile of the standard normal distribution
corresponding to a given $$\alpha$$. For example, in a 95% CI, $$\alpha = 1 -
0.95 = 0.05$$. 

Intuitively, we know that in the standard normal distribution, $$z_{\alpha/2}$$
standard deviations outside the mean contain $$(1-\alpha)\%$$ of the data. So
to construct a confidence interval, we shift the center of the standard normal
by our estimate for the mean, $$\hat{\beta}_j$$, and scale the size of the
standard deviation by an estimate for the SD in our data, $$\sqrt{\sigma^2
v_j}$$.

What if we don't know $$\sigma$$ (which we don't)? All the other parameters are
available, but we can't know $$\sigma$$ ahead of time. We can estimate it using
the sum of squared residuals:

$$
\hat{\sigma} = \sqrt{\frac{1}{n - p} \sum \limits_i (y_i - X_i'\hat{\beta})^2} = \sqrt{\frac{1}{n - p} \norm{y - X \beta}_{2}^2}
$$

Note that for large $$n$$, $$\frac{1}{n} \approx \frac{1}{n - p}$$.

So our final formula for the confidence interval is 

$$
\hat{\beta}_j \pm z_{\alpha / 2} \hat{\sigma} \sqrt{v_j}
$$

The point here is that generative models let us quantify uncertainty.

# Ridge regression

Ridge regression is a variant of OLS. So far, we have assumed $$X'X$$ is
invertible. What if it isn't? Intuitively, in this case, multiple solutions
exist to the minimization problem $$\min \limits_{\beta} \norm{y - X
\beta}_{2}^2$$.

Is it reasonable to assume $$X'X$$ is invertible? Sometimes, but observe that
if the columns of $$X$$ are not linearly independent, then $$X'X$$ is not
invertible. We can show this with some clever algebra.

If the columns of $$X$$ are not linearly independent, then there exists a
linear combination of the columns $$\sum v_i X_i = 0$$ with $$v_i$$ not all
zero. This corresponds to a matrix vector product $$Xv = 0$$i where $$v =
\begin{pmatrix} v_1 \\ \vdots \\ v_n \end{pmatrix} \ne 0$$.

Now suppose $$(X'X)$$ is invertible. If we left-multiply $$Xv$$ by $$(X'X)^{-1}X'$$, we have

$$
\begin{align*}
Xv &= 0 \\
(X'X)^{-1}X'Xv &= (X'X)^{-1}X' \cdot 0 \\
v &= 0
\end{align*}
$$

which is a contradiction.

From a different perspective, if the columns of $$X$$ are not linearly
independent, the projection of $$y$$ onto $$\Col X$$ might not have a unique
representation. Therefore $$\hat{\beta}_{OLS}$$ can't be unique and the form
$$\hat{\beta}_{OLS} = (X'X)^{-1}X' y$$ can't be correct.

The conclusion is that if the columns are not linearly independent, we have a
problem.

Consider the high-dimensional setting where $$p>n$$ and $$X$$ is a "wide"
matrix. The columns of $$X$$ cannot be linearly independent, because there are
$$p$$ columns in $$n$$-dimensional space, where we can obtain a maximum of
$$n$$ linearly independent vectors. So $$(X'X)$$ will never be invertible in
this setting.

What do we do? Well, we have a "simple" "fix", called ridge regression.

$$
\hat{\beta}_{\text{ridge}} = (X'X + \lambda I)^{-1} X'y
$$

We add a multiple of the identity matrix to make the matrix invertible. We rely
on the fact that $$X'X + \lambda I$$ is always invertible for any $$\lambda >
0$$, because $$X'X + \lambda I$$ is a positive definite matrix. We will review
positive definite matrices in more detail later when we discuss the singular
value decomposition and dimensionality reduction, but for now, to verify
whether a matrix $$A$$ is positive definite, check that $$v' A V > 0 \forall v
\ne 0$$.

In the next class we will explore ridge regression further.
