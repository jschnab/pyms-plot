---
title: 'PyMS: Python for Mycorrhizal Symbiosis data analysis'
tags:
  - data analysis
  - statistics
  - mycorrhiza
authors:
  - name: Jonathan Schnabel
    orcid: 0000-0002-9515-332X
    affiliation: "1"
affiliations:
  - name: Department of Plant Sciences, University of Cambridge, UK.
    index: 1
date: 14 October 2018
bibliography: paper.bib
---

# Summary

Python for Mycorrhizal Symbiosis (PyMS) aims at providing an easier way for researchers and students to analyze quantitification of mycorrhizal symbiosis root colonization and produce publication-quality figures without having to use command line-based softwares. PyMS is routinely used in our laboratory for various research projects. Input data should be collected via the line intersect method [@Paszkowski] or an equivalent method. PyMS accepts csv files and is provided with an example from a recent research article [@Chiu].

PyMS allows users to plot data according to the representation most widely used (bar-plot showing the median of data and scatter-plot displaying individual data points) and select a few graphical parameters (two different modes of data grouping and bar face color including a color-blind-friendly palette). Figures can be saved in different image formats depending on downstream application.

To test the hypothesis of different colonization levels between groups, PyMS uses the Mann-Whitney test or its own implementation of the Kruskal-Wallis test with post-hoc analysis using Dunn's test. These tests were chosen because the small sample sizes obtained during mycorrhizal colonization of roots makes the use of parametric tests less reliable.

PyMS relies on pandas [@pandas] to manipulate data, matplotlib [@matplotlib] to build plots, SciPy [@SciPy] and statsmodels [@seabold] for statistics and TkInter to build the graphical user interface.

# Acknowledgements

This work was supported by a BBSRC grant (project reference BB/P003419/1) granted to Uta Paszkowski (Department of Plant Sciences, University of Cambridge, UK).

# References
