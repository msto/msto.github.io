---
layout: lecture
title: Lasso (probabilistic view) and cross-validation
lecture: 5
course: ECE 532
date: 2019-01-31
---

# Administrative notes

- Homework 2 out today
- Office hours after class today due to travel on Tuesday

# Summary

Today in class we finished our discussion of ridge and Lasso regression,
reviewing the probabilistic view of ridge regression and exploring the
probabilistic view of Lasso regression. We also explored cross-validation.

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

# Recap: Ridge regression

We previously defined the following estimator for ridge regression:

$$
\hat{\beta}_{ridge} = (X'X + \lambda I)^{-1} X' y
$$

which we showed was equivalent to the optimization problem

$$
\hat{\beta}_{ridge} = \argmin\limits_{\beta} \left \{ \norm{y - X \beta}_2^2 + \lambda \norm{\beta}_2^2 \right \}
$$

where $$\lambda$$ is a regularization parameter that controls the trade-off
between minimizing our loss, $$\norm{y- X\beta}_2^2$$, and our penalty,
$$\norm{\beta}_2^2$$. 

In the homework we saw that ridge regression encourages our solution $$\beta$$
to be close to the origin (i.e. to have a small L2-norm). One motivation for
defining the ridge regression model is that $$X'X$$ is not always invertible,
while the ridge matrix $$X'X - \lambda I$$ is always invertible. However, we
also discussed the probabilistic interpretation, which is that ridge regression
places a Gaussian prior on $$\beta$$.

We saw that the above formulations of ridge regression also correspond to
maximizing the following likelihood function, and obtaining the _maximum a
posteriori_ (MAP) estimate for $$\beta$$ (which we erroneously referred to as the
maximum likelihood estimate (MLE) last time).

$$
\L_{\beta} (X, y) = p(\beta) P_{\beta}(X, y)
$$

where $$p(\beta)$$ is the prior PDF of $$\beta$$, and $$P_{\beta}(X, y)$$ is
the posterior probability, sometimes written $$P(X, y \mid \beta)$$.

Remember we also showed that OLS regression is equivalent to the MLE of
$$P_{\beta}(X, y)$$, i.e., finding the $$\beta$$ that maximizes this
probability. Note that this corresponds to MAP with a uniform prior. Now,
however, we are introducing a non-uniform prior, and taking the product of the
two distributions. Since our prior is Gaussian with mean 0, its density is
centered around the origin. When multiplying the two distributions, we expect
this to "adjust" the density of the posterior probability, so the density of
the product is also greater closer to 0.

# Probabilistic view of Lasso regression

We defined the Lasso regression estimator to be

$$
\hat{\beta}_{Lasso} = \argmin\limits_{\beta} \left \{ \norm{y - X \beta}_2^2 + \lambda \norm{\beta}_1 \right \}
$$

which we discussed encourages the solution to be sparse. 

Now, let's discuss the probabilistic interpretation. Again, we are placing a
prior on $$\beta$$, but instead of a Gaussian prior, we're choosing some other
distribution. For ridge regression, we wanted a sum of squares in the
exponential of our prior distribution, so it would work out to be equivalent to
minimizing the L2-norm, but now we want an absolute value, so it will be
equivalent to minimizing the L1-norm.

It turns out that the distribution that corresponds to minimizing the L1-norm
is the Laplacian distribution (or double exponential), which has the following
form:

$$
p(\beta) = \prod\limits_{j=1}^{p} \frac{\lambda}{4} \exp \left( \frac{- \lambda}{2} \card{\beta_j} \right)
$$

[[ TODO: Add pic of 1-D Laplacian ]]

If we want to obtain a sparse $$\beta$$, we want the density of our prior to be
even closer to the origin than a Gaussian. Here, a larger $$\lambda$$ will
generate a steeper curve.

# Verifying the probabilistic view of Lasso

Now let's show that a Laplacian prior does give us Lasso regression. We can
calculate the MAP (to simplify, we assume unit variance of our
$$\varepsilon_i$$, i.e. $$\sigma^2=1$$:

$$
\begin{align*}
L_{\beta}(X, y) &= p(\beta) P_{\beta}(X, y) && \text{prior $\cdot$ likelihood} \\
                &= p(\beta) \prod\limits_{i} P_{\beta} (X_i, y_i) \\
                &= \prod\limits_{j=1}^{p} \frac{\lambda}{4} \exp \left( \frac{-\lambda}{2} \card{\beta_j} \right) \prod\limits_{i=1}^n \frac{1}{\sqrt{2\pi}} \exp \left( \frac{-(y_i - X_i'\beta)^2}{2} \right)
\end{align*}
$$

Note that a product of exponentials is equivalent to the exponential of the
sum, so our maximization is equivalent to

$$
\begin{align*}
\max\limits_{\beta} L_{\beta}(X, y) &= \max\limits_{\beta} \exp \left(\frac{-\lambda}{2} \sum \card{\beta_j} - \frac{1}{2} \sum (y_i - X_i'\beta)^2 \right) \\
    &= \min\limits_{\beta} \left\{ \frac{\lambda}{2} \sum \card{\beta_j} + \frac{1}{2} \sum (y_i - X_i' \beta)^2 \right \} \\
    &= \min\limits_{\beta} \left\{ \norm{y - X\beta}_2^2 + \lambda \norm{\beta}_1 \right\}
\end{align*}
$$

So we've seen Lasso formulated as an algebraic problem, then as putting a
Laplacian prior on $$\beta$$.

Again, there is no closed form solution to the Lasso regression problem, but
many solvers exist that implement strategies such as gradient descent. An
important note for the Matlab implementation of Lasso is that it excludes the
intercept from the regularization penalty, so it solves the similar problem:

$$
\min\limits_{\beta_0, \beta} \left\{ \frac{1}{2n} \sum\limits_{i=1}^n (y_i - \beta_0 - X_i'\beta)^2 + \lambda \sum\limits_{j=1}^p \card{\beta_j} \right\}
$$

# Cross-validation

(Scribe note: All material so far can be found in chapter 3 of any of the
references. Discussion of cross-validation can be found in chapter 7 of ESL, or
chapter 1.3 of Bishop.)

So, now that we're familiar with ridge and Lasso, how do we choose the
regularization parameter $$\lambda$$? We will explore a method called
cross-validation that is effective for choosing $$\lambda$$ in these contexts
and for many other choices of parameter as we will explore later.

The idea is to calculate an estimator (let's say our ridge estimator) for
several different values of $$\lambda$$. Let's think of our estimator now as a
function of $$\lambda$$:

$$
\hat{\beta}(\lambda) = (X'X + \lambda I)^{-1} X' y
$$

How do we compare the fit of our model for each choice of $$\lambda$$? ONe idea
would be to calculate the mean square error for each $$\lambda$$, and choose
the $$\lambda$$ that minimizes.

$$
\mathrm{MSE}(\lambda) = \frac{1}{n} \norm{y - X \hat{\beta}}_2^2
$$

However, we don't just want to find the best fit for the data we have in hand.
We'd like to model the overall population, and this strategy finds the best fit
for our _training_ data, which may not generalize to other test data.

For example, consider the case of polynomial regression. Given some set of
data, we'd like to find the polynomial that best fits our data. In this
setting, our model is parameterized by the degree $$d$$ of the polynomial (e.g.
$$d=2$$ will find the best fit quadratic model). Now, if we choose a large
enough $$d$$, we can fit every point in our dataset with no error, and obtain
$$\mathrm{MSE}(d) = 0$$. However, the model that we learn won't be very likely
to predict unseen data well. 

So, we don't want to evaluate MSE just on our training data. What can we do
instead? To solve the problem of overfitting, we can calculate the MSE over a
separate set of data, a validation set, that wasn't included when we learned
our estimator. For example, we could divide our dataset $$(X, y)$$ into two
components, $$(X_{train}, y_{train})$$ and $$(X_{val}, y_{val})$$. Then
we would learn an estimator from the training set:

$$
\hat{\beta}(\lambda) = (X_{train}'X_{train} + \lambda I) X_{train}' y_{train}
$$

and compute the MSE from our validation set:

$$
\mathrm{MSE}(\lambda) = \frac{1}{n_{val}} \norm{y_{val} - X_{val}\hat{\beta}(\lambda)}_2^2
$$

We then choose the $$\lambda^{*}$$ that minimizes the MSE on the validation
set, and use the estimator $$\hat{\beta}(\lambda^{*})$$.

In cross-validation, we repeat this method many times ($$k$$-fold
cross-validation). The data is split into $$k$$ groups, and the validation
strategy described above is performed $$k$$ times, using each group as the
validation set once (and the remaining groups as the training set). We then choose the $$\lambda$$ that minimizes the average MSE over the $$k$$ validations, i.e.

$$
\lambda^{*} = \argmin\limits_{\lambda} \frac{1}{k} \sum_{i=1}^k \mathrm{MSE}_{i}(\lambda)
$$

In summary, cross-validation is implemented as follows:
1. Randomly split $$(X, y)$$ into $$k$$ chunks
2. Compute $$\mathrm{MSE}_i(\lambda)$$ for all $$i \in [1, k]$$
3. Minimize the average MSE with respect to $$\lambda$$
4. Return $$\hat{\beta}(\lambda^{*})$$, using all of $$X$$ to learn the estimator

# Leave-one-out cross-validation

The most extreme version of cross-validation is $$n$$-fold, or leave-one-out
cross-validation. Here, only a single data point is withheld to be used as the
validation set in each iteration. The benefit of this strategy is that it
reduces variability due to random re-sampling, but the trade-off is that it is
computationally expensive.

# Cross-validation in practice

In practice, we want to report the fit of our estimate on a separate set of
test data that wasn't included in training. Typically, we split the data $$(X,
y)$$ into a training set and a test set (around 20% is common for the test
set), then perform cross-validation on the training set to choose an
appropriate value of $$\lambda$$ and learn an estimator $$\hat{\beta}_{CV}$$
from the full training set.  We then report a final MSE with respect to the
test data,

$$
\mathrm{MSE} = \frac{1}{n_{test}} \norm{y_{test} - X_{test} \hat{\beta}_{CV}}_2^2
$$

Finally, if $$k$$-fold cross-validation is too expensive, we can split the data
once (say 50% training, 25% validation, and 25% test). We then learn an
estimator from our training data, choosing $$\lambda$$ by  minimizing the
$$\mathrm{MSE}(\lambda)$$ over the validation data, and finally report the
$$MSE$$ with respect to $$\hat{\beta}(\lambda^{*})$$ on the test data.
