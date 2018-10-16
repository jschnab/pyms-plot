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

Python for Mycorrhizal Symbiosis (PyMS) aims at providing an easier way for researchers and students to analyze quantitification of mycorrhizal symbiosis root colonization levels and produce publication-quality figures without having to use command line-based softwares. PyMS is routinely used in our laboratory for various research projects.

PyMS allows users to plot data according to the representation most widely used (bar-plot showing the median of data and scatter-plot displaying individual data points) and select a few graphical parameters (two different modes of data grouping and bar face color including a color-blind-friendly palette). Figures can be saved in different image formats depending on downstream application.

To test the hypothesis of different mycorrhizal colonization levels between groups, PyMS uses the Mann-Whitney test or its own implementation of the Kruskal-Wallis test with post-hoc analysis using the Dunn's test. These tests were chosen because the small sample sizes obtained during mycorrhizal colonization of roots makes less reliable the use of parametric tests.

PyMS uses the module tkinter to provide a graphical user interface for data visualization and to perform statistical tests. PyMS relies on [@pandas] to manipulate data, [@matplotlib] to build plots and [@SciPy] for statistics. 

# Acknowledgements

This work was supported by a BBSRC grant (project reference BB/P003419/1) granted to Uta Paszkowski (Department of Plant Sciences, University of Cambridge, UK).

# References
