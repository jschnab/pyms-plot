# PyMS

Python for Mycorrhizal Symbiosis analysis (PyMS) is a graphical user interface-based program to visualize quantitative analysis of mycorrhizal fungi colonization of plant roots and perform statistical analysis of the data. It was developed to help researchers who are not familiar with command line-based softwares, or who want to increase their productivity during data analysis.

## Installation

PyMS is written in Python 3 and depends on [pandas 0.23](https://pandas.pydata.org/), [NumPy](http://www.numpy.org/), [matplotlib](https://matplotlib.org/), [SciPy](https://matplotlib.org/) and [TkInter](https://docs.python.org/3/library/tk.html). You can install them using your favourite package manager. TkInter is traditionally bundled with Python. To install PyMyS you can clone the [GitHub repository](https://github.com/jschnab/pyms.git) then follow one of the next two options.

### Windows users

To run PyMS place a shortcut of the file *pyms/pyms/run_pyms.bat* on the desktop then simply click on the shortcut. It will take a few seconds to load all the packages which are used by PyMS. In the end, the graphical user interface for PyMS will appear (along with a console window which should be kept open, it will close automatically when you exit PyMS).

### Other OS users

To run PyMS, navigate to */pyms/pyms* where *pyms.py* is located and type ``python pyms.py`` in the console. It will take a few seconds to load all the packages which are used by PyMS, then the graphical user interface for PyMS will appear.

## Input data and file format
Quantification of arbuscular mycorrhizal fungus colonization of plant roots should be done via a modified version of the grid-line
intersect method (see [Paszkowski, U., Jakovleva, L., and Boller, T. (2006). Maize mutants affected at distinct stages of the 
arbuscular mycorrhizal symbiosis. Plant J. 47 165-173](https://www.ncbi.nlm.nih.gov/pubmed/16762030)) or an equivalent method.

The input file should be a csv file with a specific formatting 
(see *test_colonisation.csv* in the same repository for an example, data from [Chiu, C. H., Choi, J., Paszkowski, U. (2018) Independent signalling cues underpin arbuscular mycorrhizal symbiosis and large lateral root induction in rice. New Phytologist. 217 552-557](https://www.ncbi.nlm.nih.gov/pubmed/29194644)).

## Generate and save a figure
* Select the graphical parameters you want by ticking options in menus "Group by" and "Color".

* Click on the "Process" menu and click on "Analyze csv file", it will open a pop-up and you can browse your file.

* Click on the "File" menu and point on "Save as" to display the file type choice. Click on the file extension name to save your file in the same folder as your csv file. If you generate several figures by clicking on "Analyze csv file" several times, it will save the last figure generated.

Here is the expected output if you use the file *test_colonization.csv*.

<img src="docs/images/test_colonization.png" width="800" alt="plot">

## Statistical analysis
PyMS allows you to perform statistical testing of inter-genotype comparisons using the Mann-Whitney test or the Kruskal-Wallis test followed by the Dunn test for post-hoc analysis (i.e. the Kruskal-Wallis test tells you if at least one genotype is different from the others while the Dunn test tells you which genotypes are different from the others). If you want to compare two genotypes, use the Mann-Whitney test. If you want to compare multiple genotypes, use the Kruskal-Wallis then Dunn tests.

* If you have not opened the csv file in PyMS yet, click on the "Process" menu and click on "Analyze csv file", it will open a 
pop-up and you can browse your file.

* Click on the "Statistics" menu and select the test you want by ticking one of 
them. You then need to select the genotypes you want to analyze in the "Select samples" menu. You can detach the menu by clicking on the top -------, so that you don't have to open the menu each time you select a genotype. Once you selected the genotypes of interest, click on "Perform statistical test" in the "Process" menu. The p-values returned by the test will be saved in a text file in the same folder as your csv file.

Here is an example if you perform the Mann-Whitney test on the genotypes *117KO* (loss-of-function mutant) and *117REV* (wild type) from the file *test_colonization.csv*. The column *Genotypes* indicates the genotypes which are compared. The other columns represent the different fungal structures. The numbers in each column represent the p-value for the difference in colonization levels for the different fungal structures.

<img src="docs/images/mann_whitney.png" width="800" alt="mann-whitney">

Here is another example if you perform the Kruskal-Wallis test followed by the Dunn tests on the genotypes *hebiba (AOC)* (loss-of-function mutant), NH WT (wild type) and PCG82-2 (complemented loss-of-function mutant). The results are displayed as for the Mann-Whitney test except there are more genotypes comparisons.

<img src="docs/images/kw_dunn.png" width="800" alt="kruskal-wallis">

## Support

If you have any question, please send an email to jonathan.schnabel31@gmail.com.

## Contributing

PyMS aims at being an evolving and collaborative project. Please contribute to make PyMS better by reporting issues and proposing enhancements and corrections through pull requests on GitHub. Please read [GitHub help pages](https://help.github.com/) for more details.

### Report issues
If you spot an issue or a bug, create a new issue in the *Issues* tab of PyMS's repository. Provide a detailed description of the issue, containing the steps needed to reproduce the issue, the software behaviour you observe, the software behaviour you expect, and the version of PyMS, Python, and dependencies.

### Pull requests
If you would like to make PyMS better, you are welcome to create a pull request after you pushed changes to a branch of the repository on GitHub.
