---
layout: lecture
title: FIRE (cont.) and introduction to RNA-seq
lecture: 7
course: BMI 776
date: 2019-02-07
---

# Announcements
- Read Li (RSEM)
- Optionally read Wang 2009 and Conesa 2016
- HW1 is out

# Summary

Last class we showed that FIRE can find motifs without priors. This class we
discussed the inferences that FIRE can make with regards to other motif
features such as orientation or distance from transcription start site. We also
introduced RNA-seq to lay the foundation for next class's discussion of
transcriptome quantification.

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

# Review: FIRE

FIRE is a tool for motif discovery that represents the motif model as a regular
expression instead of a position weight matrix. As a consequence, there's no
notion of probability associated with a motif, just its presence or absence.

FIRE starts with 7-mers, and asks which have mutual information with some set
of sequence labels (e.g. a cluster assignment). It applies a significance test
to select only those 7-mers which are sufficiently informative, and uses these
as seeds for its generalization step. During generalization, FIRE proposes
modifications to the regex model of the motif, and greedily selects the altered
model that maximizes mutual information.

We saw an example where FIRE successfully recovered a motif previously known in
the literature.

# Conditional mutual information

One consideration is that two different seeds might converge to similar motifs.
If they generalize to the same regex, it is easy to filter duplicates, but what
if they generalize to similar motifs that aren't quite identical? FIRE
leverages a concept called conditional mutual information, which measures
whether a new motif is significantly different from an already known pattern.

Let $$M$$ be our new candidate motif, $$M'$$ be our known motif, and $$C$$ be
our cluster labels. Fire accepts a new motif if the ratio of its conditional MI
with the cluster labels given the previous motif to its mutual information with
the previous motif exceeds some threshold.

$$
\frac{I(M; C \mid M')}{I(M; M')} > r
$$

Note that intuitively, this ratio is large when there is little mutual
information between the two motifs (denominator is small), implying that
knowing the previous motif doesn't give us much additional information about
the new motif, or when the conditional MI (numerator) is large, implying that
knowing the new motif does give us additional information about the cluster
labels, even when we already know the previous motif.

The conditional mutual information is defined to be

$$
\begin{align*}
I(M; C \mid M') &= I(M; C, M) - I(M; M') \\
                &= \sum\limits_{m'} P(m') \sum\limits_m \sum\limits_c P(m, c \mid m') \log \frac{P(m, c \mid m')}{P(m \mid m') P(c \mid m')}
\end{align*}
$$

which is the weighted average of the mutual information between the new motif
and the cluster labels conditioned on observing the previous motif.

# Other motif features

The motivation behind motif discovery is to identify elements in the genome
that play a role in regulatory function. Beyond simply possessing a motif, we
might reasonably believe that motif orientation, motif position (i.e. distance
to transcription start site), or interactions between multiple motifs all play
a role in determining whether a regulator protein might bind and promote or
repress transcription. 

FIRE proposes a series of tests of mutual information between cleverly defined
random variables to determine whether any of these features might be of
regulatory significance.

#### Orientation bias

To test for significance of motif orientation, FIRE defines a new indicator
random variable 

$$
S = \begin{cases}
 1 &&  \text{Motif is present and is on the transcribed strand} \\
 0 && \text{Otherwise}
\end{cases}
$$

and tests for mutual information between this variable and the cluster labels,
$$I(S; C)$$. This test can also be used to test for the significance of the
motif being on the reverse strand by defining $$S'$$ to be 1 only when the
motif is present and on the reverse strand.

#### Position bias

To test for significance of motif position (distance from TSS), FIRE defines
two new random variables.

First, FIRE divides the promoter region into equal width bins. The first
variable, $$P$$, specifies the index of the bin that the motif falls into for a
given sequence. This serves to discretize the TSS distance.

Second, FIRE defines an over-representation indicator,

$$
O = \begin{cases}
  1 && \text{Motif is over-represented in a sequence's cluster} \\
  0 && \text{Otherwise}
\end{cases}
$$

To determine whether a motif is over-represented in a cluster, FIRE defines an
over-representation test. Let $$k$$ be the size of a given cluster, $$f$$ be
the frequency of the motif across all sequences in the dataset, and $$X$$
represent the number of motif occurrences in a given cluster. Then the
probability of observing at least $$x$$ occurrencess of the motif is the sum of
binomial probabilities

$$
P(X \ge x) = \sum\limits_{i=x}^{k} {k \choose i} f^i (1-f)^{k-i}
$$

A motif is determined to be over-represented in a cluster if this probability
is less than a Bonferroni-corrected (n=#clusters) significance level of 0.05.

This tests if the clustering assignment as a whole is associated with the
presence or absence of a motif, not whether a specific cluster is associated.

#### Multiple motifs and interactions

To test for significance of motif interactions, i.e., whether their presences
and absences are associated, FIRE tests the mutual information between the two
motifs. Specifically, FIRE defines the random variables $$M_1$$ and $$M_2$$
such that

$$
M_i = \begin{cases}
  1 && \text{Motif $i$ is in the sequence AND motif $i$ is over-represented in the sequence's cluster} \\
  0 && \text{Otherwise}
\end{cases}
$$

and tests for the mutual information $$I(M_1, M_2)$$.

Note that these mutual information tests are limited to two random variables,
and it may not be straightforward to construct random variables that permit
testing of conjunctions of these features, such as motif interaction plus
relative distance between the motifs.

Finally, although we have mostly discussed motifs in the promoter region, this
approach can be extended to look for motifs in the 3' UTR, where regulatory
signals can manage RNA stability, mostly by being bound by miRNA's that promote
degradation or translation.

# FIRE conclusions
- Uses tests of mutual information for everything
- All tests are done by constructing pairs of random variables and calculating
  MI
- k-mer generalization (in contrast with PWM)
- FIRE also incorporates sequences that lack the motif (negative sequences), by
  using clustering to detect significant associations of the motif presence

# RNA-seq

Our next section will be on RNA-seq. We'll discuss the underlying technology,
focus on the quantification problem, and on Thursday discuss how we might
approach the quantification problem with EM.

Chromosomal microarray predates RNA-seq and was the first high-throughput,
parallel assay for transcriptome quantification. The process involves designing
a chip that contains a set of probes that can bind to regions of the genome or
transcriptome. Sample DNA or RNA is fluorescently labeled, then washed across
the chip, and the abundance of each region is measured by quantifying the
intensity of the fluorescence associated with each probe.

RNA-sequencing introduces several advantages over microarray. There is no
reference needed to design probes, so it can be performed with an unknown
transcriptome and used to find novel transcripts or splice events. RNA-seq can
capture a larger range of expression, has less background noise, and higher
technical reproducibility.

In contrast to the whole-genome sequencing setting, where regions of the
sample's genome existed at a fixed relative copy state prior to sequencing, the
transcriptome exists at different levels of abundance. In RNA-seq, the
sequences are typically already known and the goal is quantifying sequencing
coverage and inferring transcript abundance. 

In short, an initial RNA sample is fragmented, the RNA fragments are subjected
to reverse transcription and amplification, and the ensuing cDNA fragments are
sequenced on a DNA sequencer.

The primary tasks in RNA-seq analysis are as follows:
- Assembly (constructing full transcript sequences from short reads)
- Quantification (estimating relative transcript abundance, or expression)
- Differential expression (identifying genes with significant variations in
  expression between two samples)

Note that RNA-seq is a relative abundance measurement, not an absolute
measurement, although we can estimate absolute abundance by adding control
spike-ins to our experiment. One issue with relative abundance can be seen in
the following table:

| Gene | Sample 1 (absolute) | Sample 2 (absolute) | Sample 1 (relative) | Sample 2 (relative) |
|------|---------------------|---------------------|---------------------|---------------------|
| 1    | 20                  | 20                  | 10                  | 5                   |
| 2    | 20                  | 20                  | 10                  | 5                   |
| 3    | 20                  | 20                  | 10                  | 5                   |
| 4    | 20                  | 20                  | 10                  | 5                   |
| 5    | 20                  | 20                  | 10                  | 5                   |
| 6    | 100                 | 300                 | 50                  | 75                  |

Note that large absolute changes in high-expressing genes can confound analyses
of relative abundance, so normalization is important.

For the next lesson, read RSEM paper.
