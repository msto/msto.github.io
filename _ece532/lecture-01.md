---
layout: lecture
title: Ordinary least squares regression
lecture: 1
course: ECE 532
date: 2019-01-22
---
# Course logistics and overview

- Professor Po-Ling Loh has office hours in MSC 1212 Tuesdays after class.
  Muni, the TA, has office hours Fridays 3:30-5:30.
- Homeworks are assigned biweekly and due Tuesdays at 2:30pm via PDF submission
  to gradescope.
- Expected prereqs are linear algebra, probability, stats, and familiarity with
  matlab or another matrix computing environment (e.g. Python, Julia, R)
- Grading: midterm 1 (25%), midterm 2 (25%), final (30%), homeworks (20%;
  lowest dropped)
- Texts: Bishop, Elden recommended, Hastie suggested
- Topics:
    1. Regression
    2. Dimensionality reduction
    3. Clustering
    4. Other (as time permits) - neural networks, tensor methods

Today in class we showed three different but equivalent derivations of the
ordinary least squares estimate for linear regression.

$$
%% Latex helpers
\newcommand{\norm}[1]{\left\lVert{#1}\right\rVert}
\newcommand{\R}{\mathbb{R}}
$$

# Linear regression (1-dimensional)

Goal: given data pairs $$ \{(x_i, y_i)\}_{i=1}^{n} $$, where $$x_i, y_i \in \R$$, find the best fit line
$$y = ax + b$$ through data. 

The least squares solution to this problem is:

$$
\min\limits_{a, b} \sum\limits_{i=1}^n (y_i - (a x_i + b))^2
$$

and our objective function is the sum of squared distances:

$$
f(a, b) = \sum (y_i - a x_i + b))^2.
$$

Traditionally, to solve this optimization problem, we take the partial
derivative of $$f$$ with respect to each variable, set each partial derivative
equal to 0, and solve the corresponding system of equations.

$$
\begin{align*}
\frac{\partial f}{\partial a} &= \sum -2 x_i (y_i - a x_i - b) = 0 \\
\frac{\partial f}{\partial b} &= \sum -2 (y_i - a x_i - b) = 0
\end{align*}
$$

To solve for $$a$$ and $$b$$, construct the system of equations:

$$
\begin{align*}
a \sum x_{i}^2 + b \sum x_i &= \sum x_i y_i \\
a \sum x_i + b n &= \sum y_i
\end{align*}
$$

Multiply the upper equation by $$n$$ and the lower equation by $$\sum x_i$$, and subtract to eliminate the $$b$$ term, then solve for $$a$$:

$$
\begin{align*}
a (n \sum x_{i}^2 - (\sum x_i)(\sum x_i)) &= n \sum x_i y_i - \sum y_i \sum x_i \\
a &= \frac{n \sum x_i y_i - \sum y_i \sum x_i}{n \sum x_{i}^2 - (\sum x_i)(\sum x_i)}
\end{align*}
$$

and, by the lower equation above, we have

$$
b = \frac{-a \sum x_i + \sum y_i}{n}.
$$

The point we'd like to make in the next section is that we can skip the laborious calculus and algebra with matrix methods. 

So, how do we generalize to more than one dimension?

# Linear regression (general case)

Now let us consider the case where $$y_i \in \mathbb{R}$$, but $$x_i \in
\mathbb{R}^p$$ is higher dimensional. (For example, let us consider using an
individual's height and weight to predict body mass index (BMI)). We would like
to obtain the best linear predictor of $$y_i$$ using all components of $$x_i$$.

That is,

$$
y_i = \beta_1 x_{i1} + \beta_2 x_{i2} + \cdots + \beta_p x_{ip} = \beta'x_i
$$

for some $$\beta \in \mathbb{R}^p$$. (Note that for the remainder of this
discussion, we are considering $$x_{i1}$$ to be $$1$$ and $$\beta_1$$ to be the
intercept term.)

So now let us reformulate the least squares solution to our regression problem:

$$
\min\limits_{\beta_1, \ldots, \beta_p} \sum\limits_{i=1}^{n} (y_i - x_i' \beta)^2
$$

and our new objective function is

$$
f(\beta) = \sum (y_i - x_i' \beta)^2.
$$

The naive approach we could employ from the previous section would be to take
the partial derivative of $$f$$ with respect to each $$\beta_j$$, and solve the
system of equations. Let us instead take the gradient of $$f(\beta)$$ with
respect to $$\beta$$ and set it equal to 0.

$$
\begin{align*}
\nabla_{\beta} f(\beta) &= \nabla_{\beta} \left(\sum(y_i - x_i'\beta)^2\right) \\
                        &= \sum \nabla_{\beta} [(y_i - x_i'\beta)^2] && \text{Derivation is linear} \\
                        &= \sum 2 (y_i - x_i' \beta) \nabla_{\beta}(y_i - x_i' \beta)  && \text{Chain rule} \\
                        &= \sum -2(y_i -x_i'\beta) \nabla_{\beta}(x_i'\beta) && \nabla_{\beta}y_i = 0 \\
                        &= \sum -2(y_i - x_i' \beta) x_i
\end{align*}
$$

For the final step of the above calculation, note that $$\nabla_{\beta}
x_i'\beta = x_i$$ . To show this, observe that the $$k$$-th entry of the
gradient of $$x_i'\beta$$, is the partial derivative with respect $$\beta_k$$.

$$
(\nabla_{\beta} (x_i' \beta))_k = \frac{\partial}{\partial \beta_k} x_i' \beta = \frac{\partial}{\partial \beta_k} \sum\limits_{j=1}^{p} x_{ij} \beta_j = x_{ik}
$$

So we have 

$$
\nabla_{\beta} (x_i' \beta) = \begin{pmatrix} x_{i1} \\ x_{i2} \\ \vdots \\ x_{ip} \end{pmatrix} = x_i.
$$

#### Sanity checking our math

We pause here to highlight the importance of sanity checking our calculus and
algebra by checking that the dimensions match across variables.

$$
\nabla f(\beta) = \sum -2 (y_i - x_i' \beta) x_i = 0
$$

Here, $$y_i$$ is 1-dimensional. $$x_i'$$ is $$1 \times p$$ and $$\beta$$ is
$$p$$-dimensional, so $$x_i' \beta$$ is a scalar, and therefore the
parenthetical quantity is a scalar. We can multiply $$x_i$$, a
$$p$$-dimensional column vector, by this scalar, and we are thus setting the
equation equal to the $$p$$-dimensional zero vector. This is consistent with
our knowledge that the gradient is a vector-valued function in
$$\mathbb{R}^p$$.

#### Solving the gradient for $$\beta$$

Now that we have a tractable formulation of our gradient, we can manipulate it
in a smart way to solve for $$\beta$$.

$$
\begin{align*}
\sum\limits_{i} (y_i - x_i' \beta) x_i &= 0 \\
\sum\limits_{i} y_i x_i - \sum\limits_{i} x_i' \beta x_i &= 0 \\
\sum\limits_{i} (x_i' \beta) x_i &= \sum\limits_{i} y_i x_i \\
\sum\limits_{i} x_i (x_i' \beta) &= \sum\limits_{i} y_i x_i && \text{Commutativity of scalar mult} \\
(\sum\limits_{i} x_i x_i') \beta &= \sum\limits_{i} y_i x_i \\
\beta &= (\sum\limits_{i} x_i x_i')^{-1} (\sum\limits_{i} y_i x_i) \\
      &= \hat{\beta}_{OLS}
\end{align*}
$$

The cleverness here is in observing that we can shuffle the order of the
multiplication within the summation since $$x_i' \beta$$ is a scalar and scalar
multiplication is commutative, which then allows us to factor out the
multiplication by $$\beta$$ from the summation.

#### Consistency with 1-dimensional results

Does this formula agree with the 1-dimensional case above? Note that we wanted
to obtain $$a, b$$, where $$\beta = (a \; b)'$$ and $$x_i = (x_i \; 1)'$$.

$$
\hat{\beta}_{OLS} = (\sum x_i x_i')^{-1} (\sum y_i x_i)
$$

Observe

$$
x_i x_i' = \begin{bmatrix} x_i \\ 1 \end{bmatrix} \begin{bmatrix} x_i && 1 \end{bmatrix} = \begin{bmatrix} x_i^2 && x_i \\ x_i && 1 \end{bmatrix}
$$

and

$$
y_i x_i = \begin{bmatrix} y_i x_i \\ y_i \end{bmatrix}
$$

so 

$$
\hat{\beta}_{OLS} = \begin{bmatrix} \sum x_i^2 && \sum x_i \\ \sum x_i && n \end{bmatrix}^{-1} \begin{bmatrix} \sum y_i x_i \\ \sum y_i \end{bmatrix}.
$$

Recall the formula for the inverse of a 2x2 matrix:

$$
\begin{bmatrix} a && b \\ c && d \end{bmatrix}^{-1} = \frac{1}{ad - bc} \begin{bmatrix} d && -b  \\ -c && a \end{bmatrix}.
$$

So we obtain

$$
\begin{align*}
\hat{\beta}_{OLS} &=  \frac{1}{n \sum x_i^2 - (\sum x_i)(\sum x_i)} \begin{bmatrix} n && - \sum x_i \\ - \sum x_i && \sum x_i^2 \end{bmatrix} \begin{bmatrix} \sum y_i x_i \\ \sum y_i \end{bmatrix} \\
    &= \frac{1}{n \sum x_i^2 - (\sum x_i)(\sum x_i)} \begin{bmatrix} n \sum y_i x_i - (\sum x_i) (\sum y_i) \\ - (\sum x_i) (\sum y_i x_i) + (\sum x_i^2)(\sum y_i) \end{bmatrix}.
\end{align*}
$$

and our estimator for $$a$$ is

$$
\hat{a} = \frac{n \sum y_i x_i - (\sum x_i) (\sum y_i)}{n \sum x_i^2 - (\sum x_i)(\sum x_i)}
$$

which matches our earlier results.

The moral here is that matrix manipulation is easier when we generalize to more
dimensions.

# Linear regression (matrix representation)

Let us finally move on to the matrix representation of the linear regression
problem. Define the least squares objective function:

$$
\sum\limits_{i} (y_i - x_i' \beta)^2
$$

Consider the matrix and vector

$$
X = \begin{pmatrix} x_1' \\ x_2' \\ \vdots \\ x_n' \end{pmatrix} \quad \text{and} \quad y = \begin{pmatrix} y_1 \\ y_2 \\ \vdots \\ y_n \end{pmatrix}.
$$

First, we wish to show that the least squares objective above can be written
$$\norm{ y - X \beta}_{2}^{2}$$. Recall that for any $$ v \in \R^n,
\norm{v}_{2}^{2} = \sum\limits_{i} v_i^2$$. 

Consider the $$i$$th entry of $$y - X \beta$$. Clearly, the $$i$$th entry of
$$y$$ is $$y_i$$, and the $$i$$th entry of $$X \beta$$ is $$x_i' \beta$$ since 

$$
X \beta = \begin{pmatrix} x_1' \\ \vdots \\ x_n' \end{pmatrix} \beta = \begin{pmatrix} x_1' \beta \\ \vdots \\ x_n' \beta \end{pmatrix}.
$$

So the $$i$$th entry of $$y - X \beta$$ is $$y_i - x_i' \beta$$, and by
definition of 2-norm we have shown equivalence to our least squares objective
function.

$$
\norm{y - X \beta}_{2}^{2} = \sum\limits_{i} (y_i - x_i' \beta)^2
$$

Now, we want to minimize this formulation

$$
\min\limits_{\beta} \norm{y - X \beta}_{2}^{2}.
$$

Let us take the gradient of our objective function $$f(\beta) = \norm{y - X
\beta}_{2}^{2}$$ and set it equal to 0.

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

Now, we claim that for any symmetric matrix $$A$$, $$\nabla_{\beta} (\beta ' A
\beta) = 2A \beta$$. (We will prove this claim in the next lecture.)

Using this claim, we can solve for $$\beta$$ as follows:

$$
\begin{align*}
\nabla_{\beta} f &= 0 \\
-2 X'y + 2 X'X \beta &= 0 \\
X'X \beta &= X'y \\
\beta &= (X'X)^{-1} X'y
\end{align*}
$$

which may be familiar if you have a statistics background.


