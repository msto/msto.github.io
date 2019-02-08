---
layout: lecture
title: Algebraic, geometric, and probabilistic views of OLS
lecture: 2
course: ECE 532
date: 2019-01-24
---
# Administrative notes

- Homework 1 will be uploaded by EOD today
- Readings will be assigned as the term progresses; for now, review chapter 3
  in any of the references 

# Summary

Today in class we discussed the three views of ordinary least squares (OLS)
regression:
1. Algebraic (using matrices and gradients)
2. Geometric (considering our solution to be a projection of $$y$$ onto the
   column space of $$X$$)
3. Probabilistic (a generative model)

$$
%% Latex helpers
\newcommand{\norm}[1]{\left\lVert{#1}\right\rVert}
\newcommand{\R}{\mathbb{R}}
\newcommand{\L}{\mathcal{L}}
\DeclareMathOperator*{\argmin}{arg\,min}
\newcommand{\bigdot}{\boldsymbol{\cdot}}
$$

# Recap: OLS

Recall that our goal is to take a set of observations $$\{(X_i,
y_i)\}_{i=1}^{n}$$, where $$X_i \in \R^p$$ and $$y_i \in \R$$, and find the
best fit for $$y_i \approx X_i' \beta$$ for some regression vector $$\beta$$.
Our motivating example considered the case where $$p=3$$, $$X_i$$ contained an
individual's height, weight, and an intercept term, and $$y_i$$ represented an
individual's body mass index (BMI).

In matrix form:

$$
\hat{\beta}_{OLS} = \argmin\limits_{\beta} \norm{y - X\beta}_{2}^{2}
$$

From this equation, we differentiated directly with respect to $$\beta$$ and solved:

$$
\begin{align*}
\nabla_{\beta} f &= \nabla_{\beta} \norm{y - X\beta}_{2}^{2} \\
                 &= \nabla_{\beta} [ (y-X\beta)'(y - X\beta) ] && \norm{v}_{2}^{2} = v'v \\
                 &= \nabla_{\beta} [y'y - (X\beta)'y - y' X \beta + (X \beta)' (X \beta) ] && \text{FOIL} \\
                 &= \nabla_{\beta} [y'y - 2 y' X \beta + \beta' X' X \beta] && v'w = w'v \\
                 &= 0 - \nabla_{\beta} 2 y'X \beta + \nabla_{\beta} \beta' X' X \beta && \nabla_{\beta} c = 0 \\
                 &= - 2 X'y + \nabla_{\beta} \beta' X' X \beta && \nabla_{\beta} v'\beta = v \\
\end{align*}
$$

Last class, we continued our solution by relying on the following claim:

$$
\nabla_{\beta} (\beta' A \beta) = 2 A \beta
$$

if $$A$$ is symmetric. To prove this claim, we want to think about both sides
of this equation, which are $$p$$-dimensional vectors, and show that the
$$j$$th components of each are equal.

On the left hand side (LHS), the $$j$$th component is the partial derivative
with respect to $$\beta_j$$:

$$
\frac{\partial}{\partial \beta_j} (\beta' A \beta) = \frac{\partial}{\partial \beta_j} \sum\limits_{k, l} \beta_k a_{kl} \beta_l
$$

Here, we are letting $$A = \begin{pmatrix} a_{kl} \end{pmatrix}$$. Let
$$a_{k \bigdot}$$ denote the $$k$$th row of $$A$$. To obtain the above
equivalence, recall that the $$i$$th entry of the matrix-vector product $$Ax$$ is the dot product of the $$i$$th row of $$A$$ with $$x$$, that is:

$$
\begin{align*}
A \beta &= \begin{pmatrix} {a_{1\bigdot}}'\beta \\ \vdots \\ {a_{p \bigdot}}' \beta  \end{pmatrix} \\
        &= \begin{pmatrix} \sum\limits_{l} a_{1l} \beta_l \\ \vdots \\ \sum\limits_{l} a_{pl} \beta_l \end{pmatrix}
\end{align*}
$$

so we have:

$$
\begin{align*}
\beta' A \beta &= \begin{pmatrix} \beta_1 && \cdots && \beta_p \end{pmatrix} \begin{pmatrix} \sum\limits_{l} a_{1l} \beta_l \\ \vdots \\ \sum\limits_{l} a_{pl} \beta_l \end{pmatrix} \\
              &= \beta_1 \sum\limits_l a_{1l} \beta_l + \cdots + \beta_p \sum\limits_{l} a_{pl} \beta_l \\
              &= \sum\limits_{k} \beta_k \sum\limits_l a_{kl} \beta_l \\
              &= \sum\limits_{k, l} \beta_k a_{kl} \beta_l
\end{align*}
$$

as above. Now let us continue with our proof:

$$
\begin{align*}
\frac{\partial}{\partial \beta_j} (\beta' A \beta) &= \frac{\partial}{\partial \beta_j} \sum\limits_{k, l} \beta_k a_{kl} \beta_l \\
        &= \frac{\partial}{\partial \beta_j} \left( \sum\limits_{k \ne j} a_{kj} \beta_k \beta_j + a_{jj} \beta_{j}^2 + \sum\limits_{k \ne j} a_{jk} \beta_j \beta_k \right) \\
        &= \frac{\partial}{\partial \beta_j} \left( 2 \sum\limits_{k \ne j} a_{kj} \beta_k \beta_j + a_{jj} \beta_j^2 \right) && A \text{ is symmetric} \\
        &= 2 \sum\limits_{k \ne j} a_{kj} \beta_k + 2 a_{jj} \beta_j \\
        &= 2 \sum\limits_{k} a_{kj} \beta_k
\end{align*}
$$

Is this equal to the $$j$$th component of the right hand side (RHS) of our
equation, $$2A\beta$$? We showed above that 

$$
A \beta = \begin{pmatrix} \sum\limits_{l} a_{1l} \beta_l \\ \vdots \\ \sum\limits_{l} a_{pl} \beta_l \end{pmatrix}
$$

whose $$j$$th component is $$\sum\limits_{l} a_{jl} \beta_l$$. Twice this
quantity is indeed equal to the $$j$$th component of the LHS we derived
earlier, $$2 \sum\limits_k a_{kj} \beta_k$$. 

Having shown that $$\nabla_{\beta} (\beta' A \beta) = 2 A \beta$$, we can
complete our derivation of the ordinary least squares estimate for $$\beta$$:

$$
\begin{align*}
\nabla_{\beta} f &= - 2 X'y + \nabla_{\beta} \beta' X' X \beta \\
                 &= - 2 X'y + 2 X' X \beta \\
\end{align*}
$$

Setting this equal to 0, we can solve:

$$
\begin{align*}
- 2 X'y + 2 X' X \beta &= 0 \\
  X'X \beta &= X'y \\
  \beta &= (X'X)^{-1} X'y
\end{align*}
$$

which is our estimate $$\hat{\beta}_{OLS}$$.

# Geometric interpretation of OLS

The OLS estimate finds a projection of $$y \in \R^n$$ onto the column space of
$$X$$.

Observe that the columns of $$ X \in \R^{n \times p} $$ are $$\{ X^1, \cdots,
X^p \}$$ and all $$X^j \in \R^n$$.

Recall that the column space of a matrix $$X$$ is 

$$
\text{Col} X = \text{span} \{X^1, \cdots, X^p\} = \{ \sum\limits_{j} \alpha_j X^j \mid \alpha_j \in \R \}
$$

If we consider $$X \beta$$, for different choices of $$\beta$$ we get different
linear combinations of the columns $$\{ X^1, \cdots, X^p \}$$. (Recall that the
matrix-vector product $$Ax$$ can be computed as a linear combination of the
columns of $$A$$ using the entries in $$x$$ as weights, $$Ax = \sum x_i A^i$$.)

$$
X \beta = \begin{pmatrix} X^1 && \cdots && X^p \end{pmatrix} \begin{pmatrix} \beta_1 \\ \vdots \\ \beta_p \end{pmatrix} = \sum\limits_{j} \beta_j X^j = \text{Col} X
$$

Therefore the set $$\{ X \beta \mid  \beta \in \R^p \}$$ is exactly the set of
vectors in $$\text{Col} X$$.

Since the 2-norm is Euclidean distance, the $$\hat{\beta} \in \R^p$$ that
minimizes $$\norm{y - X\beta}_{2}^2$$ is finding the closest point $$X
\hat{\beta} \in \text{Col} X$$.

# Probabilistic interpretation of OLS

Let us visit an idea that will recur throughout this course. Instead of
thinking in terms of data points $$(X_i, y_i)$$ or matrices $$(X, y)$$,
consider a generative model. Consider the setting where the $$(X_i, y_i)$$ are
generated in a random way:

$$
y_i = X_{i}' \beta + \varepsilon_i
$$

where $$X_i$$ is a fixed vector in $$\R^p$$ and $$\varepsilon_i \sim N(0,
\sigma^2)$$. That is, begin with fixed data points $$X_i$$, generate random
error terms $$\varepsilon_i$$, and construct our $$y_i$$, then estimate
$$\beta$$ using the observed and constructed $$(X_i, y_i)$$.

We can use maximum likelihood estimation (MLE) to find an estimate for
$$\beta$$. To recap MLE, we write the probability of observing $$(X_i, y_i)$$
assuming $$\beta$$ was our true regression vector, and then maximize over
$$\beta$$.

Let us define a likelihood function (the probability of observing our data):

$$
\begin{align*}
\L_{\beta}(X,y) &= \prod\limits_{i} P_{\beta} (X_i, y_i) && \text{Assuming independent observations} \\
                &= \prod\limits_{i} \frac{1}{\sqrt{2\pi} \sigma} \exp\left({\frac{- (y_i - x_i' \beta)^2}{2 \sigma^2}}\right) && \text{Using normal PDF}
\end{align*}
$$

To view how we obtained this, recall that the probability density function
(PDF) of a normally distributed random variable $$X \sim N(\mu, \sigma^2)$$ is

$$
p(x) = \frac{1}{\sqrt{2\pi}\sigma} \exp \left( { \frac{-(x - \mu)^2}{2\sigma^2} } \right)
$$

and if $$\mu = 0$$, this becomes

$$
p(x) = \frac{1}{\sqrt{2\pi}\sigma} \exp \left( { \frac{-x^2}{2\sigma^2} } \right)
$$

Above we stated that $$y_i = X_i' \beta + \varepsilon_i$$. Rearranging, we have
$$\varepsilon_i = y_i - X_i' \beta$$, and we know from the definition of our
model that $$\varepsilon_i \sim N(0, \sigma^2)$$. We can therefore simply
substitute $$y_i - X_i' \beta$$ for $$x$$ in the normal PDF, and obtain the
above formulation

$$
\begin{align*}
\L_{\beta}(X,y) &= \prod\limits_{i} \frac{1}{\sqrt{2\pi} \sigma} \exp\left({\frac{- (y_i - x_i' \beta)^2}{2 \sigma^2}}\right) 
\end{align*}
$$

Now we want to maximize this likelihood function with respect to $$\beta$$.
First, let's re-order our equation.

$$
\begin{align*}
\L_{\beta}(X,y) &= \prod\limits_{i} \frac{1}{\sqrt{2\pi} \sigma} \exp\left({\frac{- (y_i - x_i' \beta)^2}{2 \sigma^2}}\right)  \\
                &= \left(\frac{1}{\sqrt{2\pi} \sigma} \right)^n \prod\limits_{i} \exp\left({\frac{- (y_i - x_i' \beta)^2}{2 \sigma^2}}\right) \\
                &= \left(\frac{1}{\sqrt{2\pi} \sigma} \right)^n \exp\left({\sum\limits_{i} \frac{- (y_i - x_i' \beta)^2}{2 \sigma^2}}\right) \\
                &= \left(\frac{1}{\sqrt{2\pi} \sigma} \right)^n \exp\left({ \frac{-1}{2\sigma^2} \sum\limits_{i} (y_i - x_i' \beta)^2}\right) \\
\end{align*}
$$

Note that the quantity $$\left( \frac{1}{\sqrt{2\pi}\sigma} \right)^n$$ is
fixed with respect to $$\beta$$. Additionally, the exponential function is
monotonically increasing, so to maximize the likelihood function we only need
to maximize the exponent. The quantity $$\frac{-1}{2\sigma^2}$$ is also fixed
with respect to $$\beta$$, and its product with the always-positive sum of
squares will always be negative, so maximizing the exponent is equivalent to
minimizing the sum of squares. We have thus shown that maximizing the
likelihood function $$\L_{\beta}$$ with respect to $$\beta$$ is the same as
minimizing $$\sum (y_i - X_i'\beta)^2$$, which is our ordinary least squares
estimate.

Note that unlike our considerations of the algebraic and geometric forms of the
least squares problem, our probabilistic from required to make certain
assumptions about our data - namely that the data points were independent and
had Gaussian error terms. Despite this constraint, the generative model permits
us to use a whole family of estimators for different distributions, and permits
inference, such as constructing confidence intervals or performing hypothesis
tests.

# Constructing confidence intervals

Suppose we ran OLS to obtain the estimate $$\hat{\beta} = (X'X)^{-1}X'y$$.

1. What is the best estimate for $$\beta_j$$? Obviously $$\hat{\beta}_j$$.
2. But what if I want error bars for my estimate? Error bars can indicate
uncertainty or variability depending on the distribution of $$\beta_j$$.

If we use the generative model $$y = X \beta + \varepsilon$$, then there is
some variability in $$\hat{\beta}$$:

$$
\begin{align*}
\hat{\beta} &= (X'X)^{-1} X'y \\
            &= (X'X)^{-1} X' (X \beta + \varepsilon) \\
            &= (X'X)^{-1} X'X \beta + (X'X)^{-1} X' \varepsilon \\
            &= \beta + (X'X)^{-1} X' \varepsilon \\
\end{align*}
$$

Therefore $$\hat{\beta}_j$$ is distributed as $$\beta_j + [(X'X)^{-1}X' \varepsilon]_j$$.
(Since $$X$$ and $$\beta$$ are fixed, note that the only randomness is coming
from our error terms $$\varepsilon$$.)

Intuitively, our confidence interval will then be $$\beta_j \pm c \sqrt{v_j}$$
for some constant $$c$$, where $$v_j$$ is the $$j$$th component of the variance
of $$(X'X)^{-1} X' \varepsilon$$. We will explore this more in the next
lecture, but here's a quick preview of the result:

$$
(X'X)^{-1}X' \varepsilon \sim N(0, \Sigma^2)
$$

where $$\Sigma^2 = \sigma^2 (X'X)^{-1}$$. Therefore we should take $$v_j =
\sigma^2 \cdot [(X'X)^{-1}]_j$$.
