---
layout: lecture
title: "Network flows: the max-flow problem"
lecture: 5
course: CS 787
date: 2019-09-19
---
## Summary

Today we began our discussion of network flow algorithms with a review of the
max-flow problem and the Ford-Fulkerson algorithm.

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


## Max-flow problem

We begin by reviewing the max-flow problem, which takes as input the following:
- a graph $$G = (V, E)$$
- a function that assigns real-valued capacities to each edge $$c(u, v) : E \mapsto \R^{+}$$
- source and sink nodes $$s, t \in V$$

The goal is to send the maximum possible flow from $$s \to t$$ without
violating the capacity constraints.

We formally define the flow as a function $$f(u, v): E \mapsto \R^{+}$$, and
the max-flow problem as

$$
\begin{align*}
\max\limits_{f} \quad & \sum\limits_{v \in V} f(s, v) - \sum\limits_{v \in V} f(v, s) \\
\textrm{s.t.} \quad & \sum\limits_{v \in V} f(u, v) - \sum\limits_{v \in V} f(u, v) = 0 \quad \forall \quad u \ne s, t \\
 \quad & 0 \le f(u,v) \le c(u, v)
\end{align*}
$$

The first constraint we have is the _flow conservation property_, which requires the flow entering a node to be the same as the flow leaving a node. The second is the _capacity_ constraint, which requires the flow along an edge 
