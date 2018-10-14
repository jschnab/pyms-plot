.. PyMS documentation master file, created by
   sphinx-quickstart on Sun Oct 14 12:34:33 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyMS's documentation!
=================================

Python for Mycorrhizal Symbiosis analysis (PyMS) is a graphical user interface-based programme to visualize quantitative analysis of mycorrhizal fungi colonization of plant roots and perform statistical analysis of the data. It was developed to help researcher who are not familiar with command line-based softwares, or who want to increase their productivity during data analysis.

Documentation
=============

Installation
------------

PyMS depends on ``pandas``, ``numpy``, ``matplotlib`` and ``scipy``. You can install them using your favourite package manager. To install PyMyS you can clone the `GitHub repository <https://github.com/jschnab/pyms.git>`_ then run ``pyms.py`` using Python's interpreter.

Input data and file format
--------------------------

Quantification of arbuscular mycorrhizal fungus colonization of plant roots should be done via a modified version of the grid-line intersect method (see `Paszkowski, U., Jakovleva, L., and Boller, T. (2006). Maize mutants affected at distinct stages of the arbuscular mycorrhizal symbiosis. Plant J. 47 165–173 <https://www.ncbi.nlm.nih.gov/pubmed/16762030>`_) or an equivalent method.

The input file should be a csv file with a specific formatting (see *test_colonisation.csv* in the same repository for an example, data from `Chiu, C. H., Choi, J., Paszkowski, U. (2018) Independent signalling cues underpin arbuscular mycorrhizal symbiosis and large lateral root induction in rice. New Phytologist. 217 552-557 <https://www.ncbi.nlm.nih.gov/pubmed/29194644>`_).

Visualize the data and save a figure
------------------------------------

* Select the graphical parameters you want by ticking options in menus "Group by" and "Color".

* Click on the "Process" menu and click on "Analyze csv file", it will open a pop-up and you can browse your file. It expects to see "Genotype" or "genotype" as a column header, the rest is detected automatically.

* Click on the "File" menu and point on "Save as" to display the file type choice. Click on the file extension name to save your file in the same folder as your csv file. If you generate several figures by clicking on "Analyze csv file" several times, it will save the last figure generated.

Statistical analysis
--------------------

* If you have not opened the csv file in PyMS yet, click on the "Process" menu and click on "Analyze csv file", it will open a pop-up and you can browse your file. It expects to see "Genotype" or "genotype" as a column header, the rest is detected automatically.

* Click on the "Statistics" menu and select the test you want by ticking one of them. You then need to select the genotypes you want to analyze in the "Select samples" menu. You can detach the menu by clicking on the dashed line at the top of the window, so that you don't have to open the menu each time you select a genotype. Once you selected the genotypes of interest, click on "Perform statistical test" in the "Process" menu. The p-values returned by the test will be saved in a text file in the same folder as your csv file.

