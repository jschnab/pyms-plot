# PyMS
Python for Mycorrhizal Symbiosis (PyMS) is a software for quantification of mycorrhizal fungus root colonization with graphical interface. PyMS allows you to generate a
bar + scatter plot representing median and individual data values and save it in various image formats. In addition, PyMS allows you
to perform statistical testing on your data to identify differences between groups.

## System requirements
PyMS was written in Python 3.5 and requires Pandas, Numpy, Matplotlib, Scipy and home-made Mann-Whitney and Dunn's statistical 
tests which can be found in my [statistics repository](https://github.com/jschnab/statistics).
PyMS is mainly tested on Windows (a bit on MacOS but some features may not work properly).

## Input data and file format
Quantification of arbuscular mycorrhizal fungus colonization of plant roots should be done via a modified version of the grid-line
intersect method (see [Paszkowski, U., Jakovleva, L., and Boller, T. (2006). Maize mutants affected at distinct stages of the 
arbuscular mycorrhizal symbiosis. Plant J. 47 165–173](https://www.ncbi.nlm.nih.gov/pubmed/16762030)) or an equivalent method.

The input file should be a csv file with a specific formatting different from the "tidy data" specification 
(see "test_colonisation.csv" in the same repository for an example, data from [Chiu, C. H., Choi, J., Paszkowski, U. (2018) Independent signalling cues underpin arbuscular mycorrhizal symbiosis and large lateral root induction in rice. New Phytologist. 217 552-557](https://www.ncbi.nlm.nih.gov/pubmed/29194644)).

## Generate and save a figure
* Select the graphical parameters you want by ticking options in menus "Group by" and "Color".

* Click on the "Process" menu and click on "Analyze csv file", it will open a pop-up and you can browse your file. It expects to see "Genotype" or "genotype" as a column header, the rest is detected automatically.

* Click on the "File" menu and point on "Save as" to display the file type choice. Click on the file extension name to save your file in the same folder as your csv file. If you generate several figures by clicking on "Analyze csv file" several times, it will save the last figure generated.

## Statistical analysis
* If you have not opened the csv file in PyMS yet, click on the "Process" menu and click on "Analyze csv file", it will open a 
pop-up and you can browse your file. It expects to see "Genotype" or "genotype" as a column header, the rest is detected 
automatically.

* Click on the "Statistics" menu and select the test you want by ticking one of 
them. You then need to select the genotypes you want to analyze in the "Select samples" menu. You can detach the menu by clicking on the top -------, so that you don't have to open the menu each time you select a genotype. Once you selected the genotypes of interest, click on "Perform statistical test" in the "Process" menu. The p-values returned by the test will be saved in a text file in the same folder as your csv file.

