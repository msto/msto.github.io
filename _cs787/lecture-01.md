---
layout: lecture
title: Course overview and hashing
lecture: 1
course: CS 787
date: 2019-09-06
---
## Course logistics and overview

This is the fall 2019 offering of CS 787, taught by Christos Tzamos.

An undergraduate course in algorithms typically covers simpler algorithms that
were often developed in the 90s or earlier. In this class, we will be exploring
recently published algorithms and areas under current research. We will focus
on novel techniques and general strategies with which to approach problems.

### Topics
- **Hashing** - Our discussion of hashing will include a review of probability,
  which we'll see again in randomized algorithms.
- **Flows** - Undergraduate courses cover some network flow algorithms, and we'll see more
  complex cases such as the min-cost flow problem.
- **Linear programming (LP)** - Flows are a specific case of the constraint problems seen in linear
  programming; we'll explore more general problems.
- **Approximation algorithms** - These algorithms provide tractable, "good enough" solutions for NP-hard
  problems 
- **Online algorithms** - We don't always have access to all of our input at once - online algorithms
  show us how to make decisions for input that may arrive sequentially, and how
  to handle the uncertainty around future input.
- **Randomized algorithms** - Randomized algorithms can be faster than deterministic approaches.
- **Convex/submodular optimization** - Traditional algorithms usually rely on discrete math, but we'll explore some
  methods that don't make this assumption.

### Grading 
- Problem sets (90 points). Christos will assign 6 problem sets over the course
  of the semester. Each problem set will be handed out on a Tuesday and be due
  two weeks afterwards. Collaboration on the problems sets is encouraged, but
  groups must be no more than 3 students and each student must hand in an
  individual submission and list the names of their collaborators.
- Scribing (10 points). Each student must provide scribe notes for one lecture
  during the semester, and supervise/proofread the scribe notes of another
  lecture. Scribe notes will be sent to Christos for review by the next lecture
  and will be posted publicly on Canvas.
- Grading (10 points). Each student must grade one homework problem. Problem
  sets will contain four problems, and each problem will be graded by the same
  student, so disparities in grader strictness should be applied equally and
  balance out over the semester. Christos will provide a solution key for the
  problems, but graders are expected to provide helpful feedback when scoring a
  problem. Ideally, graders will benefit from seeing the variety of approaches to
  the same problem.

Note that there are 110 total points. The 10 extra points count as a "bonus"
and provide some flexibility in grading. As a consequence, no late homeworks
will be accepted.

### Miscellaneous logistics
- Canvas will be used for file managment and Piazza for announcements, Q+A, and
  general discussion.  
- There is no textbook. Course material will consist of scribe notes along with
  papers and readings provided by Christos.
- Christos' office hours are Wednesdays from 1-2 PM in his office at CS 4375.

$$
%% Latex helpers
\newcommand{\norm}[1]{\left\lVert{#1}\right\rVert}
\newcommand{\card}[1]{\left\vert{#1}\right\vert}
\newcommand{\R}{\mathbb{R}}
\newcommand{\L}{\mathcal{L}}
\newcommand{\O}{\mathcal{O}}
\newcommand{\E}{\mathrm{E}}
\newcommand{\Var}{\mathrm{Var}}
\newcommand{\Cov}{\mathrm{Cov}}
\newcommand{\Col}{\mathrm{Col}}
\newcommand{\bigdot}{\boldsymbol{\cdot}}
$$

## Hashing

We'll consider two applications of hashing today. In the first, we'll construct
an efficient data structure for storing elements of some universe.

Suppose we have some large universe $$U$$, such as all possible IPv6 addresses.
We have elements $$x_i \in U = \{1, 2, \cdots, \card{U} \}$$. In our example,
$$\card{U} = 2^128$$, so we have quite a large universe.

Our goal is to design a data structure that can efficiently answer queries
about a subset $$S \subseteq U$$, specifically whether an element $$x_i \in U$$
is in $$S$$. A naive solution would be to define an array $$A$$ of size
$$\card{U}$$, with nonzero entries $$A_i$$ if the corresponding element $$x_i$$
exists in $$S$$. However, this has inefficient space complexity. 

We can instead use hashing to compress our array, or table, to a smaller table
of size $$m$$. In order to do so, we need to design a function that maps from
our universe to the space permitted by the smaller table, i.e. $$h : U \mapsto
\{1, \cdots , m\}$$.

**Question:** Suppose we randomly select a function $$h$$ from the set of all
functions that map $$U$$ to $$m$$. What is the probability that two elements
are assigned to the same location? That is, what is the probability that $$x_i$$
and $$x_j$$ collide,

$$
P(h(x_i) = h(x_j))
$$

for any $$x_i, x_j \in U$$ given $$x_i \ne x_j$$.

**Answer:** After assigning one element to one of $$m$$ locations, clearly the
probability that the other element will be assigned to the same location is
$$\frac{1}{m}$$.

**Question:** What is the expected number of collisions for any subset $$S
\subseteq U$$, where $$\card{S} = n$$? That is, what is the expected number of
collisions when placing $$n$$ balls into $$m$$ bins?

**Answer:** Under linearity of expectation, the expected total number of
collisions is the sum of the expected value of each possible collision, which
is simply the probability that any pair collides:

$$
\begin{align*}
\E[c] &= \sum \E[c_{ij}] \\
      &= \sum\limits_{i<j} P (h(x_i) = h(x_j)) * 1 + \sum\limits_{i<j} (1 - P(h(x_i) = h(x_j))) * 0 \\
      &= \sum\limits_{i<j} P (h(x_i) = h(x_j)) \\
      &= {n \choose 2} \frac{1}{m} \\
      &= \frac{n (n-1)}{2m}
\end{align*}
$$

so if we choose $$m$$ to be approximately $$n^2$$, we expect to have only half
a collision. (Note that this is related to the [birthday
problem](https://en.wikipedia.org/wiki/Birthday_problem).)

**Question:** What is the probability of observing at least one collision?

**Answer:** Markov's inequality states $$P(X\ge a) \le \frac{\E[X]}{a}$$, so we
have:

$$
\begin{align*}
P(c \ge 1) \le \E[c] 
\end{align*}
$$

which is no more than $$\frac{1}{2}$$ when $$m=n^2$$, as we saw in the previous
example.

## Universal hash family

A universal hash family for a universe $$U$$ is a set of functions $$H$$ that
satisfies the following property for all $$h \in H$$:

$$
\begin{align*}
P(h(x) = h(y)) \le \frac{1}{m}  \;\;\;   \forall x, y \in U \; \text{s.t.} \; x \ne y
\end{align*}
$$

Let us define the following family of functions, and we will show that this is
a universal hash family.

$$
H = \{h : h(x) = ((ax + b) \bmod p) \bmod m
$$

where $$1 \le a \le p - 1$$ and $$0 \le b \le p - 1$$, and $$p$$ is a fixed
prime such that $$\card{U} < p < 2 \card{U}$$. (Note that the upper bound is
less important; we require $$p$$ to be greater than $$\card{U}$$ but only set
the upper bound due to [Bertrand's
postulate](https://en.wikipedia.org/wiki/Birthday_problem) that there exists a
prime in this range.)

**Claim:** $$H$$ is a universal hash family.

**Proof:** 

Fix $$x, y \in U$$ s.t. $$x \ne y$$. 

Note that a random choice of $$h$$ corresponds to a random choice of $$a$$ and
$$b$$. For a given $$a$$ and $$b$$, we can define the following:

$$
s = s(a, b) = (ax + b) \bmod p \\
t = t(a, b) = (ay + b) \bmod p 
$$

We claim that for any $$s, t \in \{0, \cdots , p - 1\}$$ with $$s \ne t$$, there
exists an $$a \in \{1, \cdots, p - 1\}$$ and a $$b \in \{0, \cdots, p - 1\}$$
such that $$s = s(a, b)$$ and $$t = t(a, b)$$.

Note that without the modular arithmetic, this corresponds to a system of
linear equations which is solved with the familiar formulas for slope and
intercept, 

$$
a = \frac{s-t}{x-y} \\
b = s - ax
$$

With the modular arithmetic, since $$p$$ is prime we have a [finite field](https://en.wikipedia.org/wiki/Finite_field) upon which the multiplicative inverse is defined, and we have the solution

$$
a = (s -t)(x-y)^{-1} \bmod p \\
b = (s - ax) \bmod p
$$

Since these quantities are integers modulo $p$, they are in $$[0, p - 1]$$, and
since $$s \ne t$$ and $$x \ne y$$, $$a$$ must be nonzero, which completes our
proof of the claim.

**Question:** What is the probability of a collision for a function $$h \in H$$?

**Answer:**

$$
\underset{a, b}{P}(s(a, b) \equiv t(a, b) \bmod m) \\
= \underset{s, t \sim [0, p-1], s \ne t}{P}(s \equiv t \bmod m) \\
$$

This becomes a combinatorial problem. The denominator is the total number of
possible choices of $$s$$ and $$t$$, and the numerator is the number of choices
that satisfy the congruence modulo $$m$$, which are the number of possible
choices $$s$$ times the number of valid pairings of $$t$$.

$$
= \frac{p \left \lfloor{\frac{p-1}{m}} \right \rfloor}{p (p -1)} \le \frac{1}{m}
$$

This completes the proof that $$H$$ is a universal hash family.

## Two-level hashing

We've shown that choosing $$m \approx n^2$$ guarantees the probability of a
collision to be at most $$\frac{1}{2}$$. However, can we improve our space
complexity to be more efficient than $$\O(n^2)$$?

In two-level hashing, we define a table of size $$\O(n)$$, and, if there is a
collision, map the elements to a smaller table. This algorithm requires two
passes over the data. In the first, we count the number of collisions in each
level 1 bin.  At the end of this pass, we declare the size of each second level
table to be the square of the number of collisions in the corresponding bin,
and choose a pair $$(a_i, b_i)$$ to define a function $$h_i$$ from our
universal hash family. In the second pass, we map each element to a top level
bin, and then use the corresponding $$h_i$$ to map the element to a location in
the second level bin.

**Question:** What is the space complexity of two-level hashing?

**Answer:** The complexity is the expectation of the sum of squared collisions
over all bins in the top-level table.

$$
\begin{align*}
S(n) &= \E[\sum s_i^2] \\
     &= \sum \E [s_i^2] \\
     &\approx \sum 
