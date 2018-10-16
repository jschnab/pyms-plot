#script which generates a barplot from colonization data
#written by Jonathan Schnabel, December 2017 (last update October 2018)
#licence GPLv3

#TO DO: change window icon
#TO DO: put error handlers

### --- history --- ###
# 15/02/2018: addition of number_rep.reindex() to re-establish original data order

# 24/02/2018: addition of Mann-Whitney test

# 25/02/2018: test of "pad" in xlim for up to 9 genotypes with group by genotype
#             addition of colors to group by structure with up to 9 genotypes
#             test with 3 structures for up to 9 genotypes
#             test with 3 structures from 5 to 9 genotypes and group by structure

# 01/03/2018: Mann-Whitney test in Python 3.5.2 does not calculate exact p-value
#             but uses normal distribution approximation, hence n > 20 is required
#             addition of calculation of exact p-value (mannwhitney_exact in scipy.stats)

# 02/03/2018  to account for ties, the statistical test only indicates if p-value <= alpha
#             the exact test does not work for samples with different sizes

# 03/03/2018  update of the Mann-Whitney exact test, now works for any sample size < 10
#             above 10 data points the calculation time becomes very high

# 04/03/2018  update of the Mann_whitney exact test, the script gets
#             critical U statistics and cumulated W statistics frequencies
#             from a text file to avoid calculating data on the fly

# 05/03/2018  modified the way the legend is handled, removed "pad", set "loc" as "center left" and
#             added the bbox_to_anchor parameter. To avoid cutting the legend, 
#             added "bbox_inches ='tight'" argument when saving the figure.

# 17/03/2018  addition of "Save as" options, the figure is stored in the new "Global" class
#             and the "saveas" functions in the "Application" class calls it to save the figure

# 20/03/2018  added statistical tests in a separate menu

# 22/03/2018  optimization of figure display so figure is not cut

# 30/04/2018 dunn.test method='bh' in R is 'fdr_bh' in Python
#            process_csv can read index "Genotype" and "genotype"

# 02/08/2018 add instructions to remove NaN from dataframe before processing
#            the name of the index is not a problem now (cf 30/04/2018)

# 06/08/2018 modified to comply with PEP8 (spaces around commas and '=')

# 13/10/2018 Mann-Whitney test from scipy.stats is now used

from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from scipy.stats import mannwhitneyu as mw
import dunn_test 
from itertools import combinations

class Global(object):
    """Class for global data"""
    #dataframe data
    struct = None
    geno = None
    col = None
    #figure data
    figure = None
    ax = None
    #file name from "filedialog.askopenfilename()"
    file_name = None
    #counter for file extension
    export_number_fig = 0
    export_number_stats = 0
    
class MenuBar(Frame):
    """drop-down menu bar"""
    def __init__(self, boss=None):
        Frame.__init__(self, borderwidth=2)

        ### <File> menu ###
        fileMenu = Menubutton(self, text='File')
        fileMenu.pack(side=LEFT, padx='3')
        #drop-down part
        me1 = Menu(fileMenu)
        #sub-menu for "save as" menu
        me4 = Menu(me1)
        me4.add_command(label='pdf', underline=0,
                        command=boss.saveas_pdf)
        me4.add_command(label='png', underline=0,
                        command=boss.saveas_png)
        me4.add_command(label='svg', underline=0,
                        command=boss.saveas_svg)
        me4.add_command(label='eps', underline=0,
                        command=boss.saveas_eps)
        #sub-menu integration
        me1.add_cascade(label='Save as', underline=0, menu=me4)
        #add quit button
        me1.add_command(label='Quit', underline=0, command=boss.quit)
        #menu integration
        fileMenu.configure(menu=me1)

        ### <Group by> menu ###
        groupbyMenu = Menubutton(self, text= 'Group by')
        groupbyMenu.pack(side=LEFT, padx='3')
        self.me1 = Menu(groupbyMenu)
        #tkinter variable
        self.group_by = IntVar()
        #drop-down part
        for (v, lab) in [(0, 'Genotype'), (1, 'Structure')]:
            self.me1.add_radiobutton(label=lab, variable=self.group_by,
                                     value=v, command=None)
        #integrate to menu
        groupbyMenu.configure(menu=self.me1)

        ### <Color menu ###
        colorMenu = Menubutton(self, text='Color')
        colorMenu.pack(side=LEFT)
        self.me3 = Menu(colorMenu)
        #tkinter variables
        self.color = IntVar()
        #drop-down part of the menu
        for (v, lab) in [(0, 'Blues'), (1, 'Color blind'), (2, 'Rainbow')]:
            self.me3.add_radiobutton(label=lab, variable=self.color,
                                     value=v, command=self.changeCol)
        #integrate to menu
        colorMenu.configure(menu=self.me3)

        ### <Process> menu ###
        open_csvMenu = Menubutton(self, text='Process')
        open_csvMenu.pack(side=LEFT, padx='3')
        me2 = Menu(open_csvMenu)
        #drop-down part
        me2.add_command(label='Analyze csv file', command=boss.process_csv)
        me2.add_command(label='Perform statistical test', command=boss.do_stat_test)
        #integrate to menu
        open_csvMenu.configure(menu=me2)

        ### <Statistics> menu ###
        self.samples = {} #dictionary for samples
        self.statMenu = Menubutton(self, text="Statistics")
        self.statMenu.pack(side=LEFT, padx='3')
        #drop-down part
        self.me5 = Menu(self.statMenu)
        #tkinter variable
        self.stat_test = IntVar()
        #dropdown part
        for (v, lab) in [(0, 'Mann-Whitney test'),
                         (1, 'Kruskal-Wallis-Dunn test')]:
            self.me5.add_radiobutton(label=lab, variable=self.stat_test,
                                     value=v, command=None)
        #integrate to menu
        self.statMenu.configure(menu=self.me5)
        
        self.palettes = (((00, 00, 1), #blues
                  (.125, .125, 1),
                  (.25, .25, 1),
                  (.375, .375, 1),
                  (.5, .5, 1),
                  (.625, .625, 1),
                  (.75, .75, 1),
                  (.875, .875, 1),
                  (.975, .975, 1)),
                ((.5, .5, .5), #color blind
                  (.9, .6, 00),
                  (.35, .7, .9),
                  (00, .6, .5),
                  (.95, .9, .25),
                  (00, .45, .7),
                  (.8, .4, .00),
                  (.8, .6, .7),
                  (.14, 1, .14)),
                ((.5, .5, .5), #rainbow
                  (.93, .51, .93),
                  (.6, .2, .9),
                  (00, 00, 1),
                  (00, 1, 00),
                  (1, 1, 00),
                  (1, .55, 00),
                  (1, 00, 00),
                  (.7, .13, .13)))

    def changeCol(self):
       self.col = []
       c = self.color.get()
       for i in self.palettes[c]:
           self.col.append(i)

class Application(Frame):
    """main application"""
    def __init__(self, boss=None):
        Frame.__init__(self)
        self.master.title('PyMS 0.8.1')
        self.mBar = MenuBar(self)
        self.mBar.me1.invoke(1)
        self.mBar.me3.invoke(2)
        self.mBar.pack()
        self.can = Canvas(self, bg='light grey', height=0, width=250,\
                          borderwidth=2)
        self.can.pack()
        self.pack()

    def saveas_pdf(self):
        """Save plot as pdf file"""
        fi_name = Global.file_name.split('.')[0] + '-' \
                             + str(Global.export_number_fig) + '.pdf'
        plt.savefig(fname=fi_name, bbox_inches='tight')

    def saveas_png(self):
        """Save plot as png file"""
        fi_name = Global.file_name.split('.')[0] + '-' \
                             + str(Global.export_number_fig) + '.png'
        plt.savefig(fname=fi_name, bbox_inches='tight', dpi=300)

    def saveas_eps(self):
        """Save plot as eps file"""
        fi_name = Global.file_name.split('.')[0] + '-' \
                             + str(Global.export_number_fig) + '.eps'
        plt.savefig(fname=fi_name, bbox_inches='tight')

    def saveas_svg(self):
        """Save plot as svg file"""
        fi_name = Global.file_name.split('.')[0] + '-' \
                             + str(Global.export_number_fig) + '.svg'
        plt.savefig(fname=fi_name, bbox_inches='tight')

    def do_stat_test(self):
        """Perform the statistical test of choice"""
        Global.export_number_stats += 1
        
        if self.mBar.stat_test.get() == 0:
            self.mann_whitney()
        elif self.mBar.stat_test.get() == 1:
            self.dunn()

    def mann_whitney(self):
        "Perform Mann-Whitney test on data"""
        #set alpha
        alpha = 0.05

        #extracts selected samples for statistical test
        geno_select = []
        for key, value in self.mBar.samples.items():
            if value.get() == 1:
                geno_select.append(key)

        #re-establish the original order of genotypes
        geno_test = []
        for i in Global.geno:
            for j in geno_select:
                if i == j:
                    geno_test.append(j)
        
        #generates all combinations of genotype pairs
        comp = tuple(combinations(geno_test, 2))

        #calculate p-values from Mann-Whitney test and put them into list
        p_val = []
        for _, (ii, jj) in enumerate(comp):
            for s in Global.struct:
                p_val.append(mw(Global.col[s][Global.col.index == ii],
                                          Global.col[s][Global.col.index == jj])[1])
        
        #put p-values in array then dataframe
        p_val = [round(i, 4) for i in p_val]
        p_arr = np.array(p_val).reshape(len(comp), len(Global.struct))

        df = pd.DataFrame(p_arr, columns=Global.struct)

        df_row = []
        for pp, (ii, jj) in enumerate(comp):
            df_row.append([ii, jj])
        df.insert(loc=0, column='Genotypes', value=df_row)
        df = df.set_index('Genotypes')


        #saves p-values dataframe in text file
        with open(Global.file_name.split('.')[0] + '_MW_pval' + '-' \
                  + str(Global.export_number_stats) + '.txt', 'w') as outfile:
            outfile.write('Mann-Whitney two-sided test for genotype \
combinations indicated in the \n"Genotypes" columns and fungal structures \
indicated as column headers.\nValues indicate p-value.\n\n')
            df.to_string(outfile)

    def dunn(self):
        """Perform Dunn's test on data"""
        #get selected samples
        geno_select = []
        for key,value in self.mBar.samples.items():
            if value.get() == 1:
                geno_select.append(key)

        #re-establish the original order of genotypes
        geno_test = []
        for i in Global.geno:
            for j in geno_select:
                if i == j:
                    geno_test.append(j)
        
        #calculate p-values from Dunn's test and put them into list
        p_val = []
        for s in Global.struct:
            data = []
            for g in geno_test:
                data.append(list(Global.col[s][Global.col.index == g]))
            p_val.append(dunn_test.kw_dunn(data, method='fdr_bh')[3])

        #generates all combinations of genotype pairs
        comp = tuple(combinations(geno_test, 2))

        df = pd.DataFrame()
        i = 0
        while i < len(Global.struct):
            df.insert(loc=i, value=p_val[i], column=Global.struct[i])
            i += 1
        
        df_row = []
        for pp, (ii, jj) in enumerate(comp):
            df_row.append([ii, jj])
        df.insert(loc=0, column='Genotypes', value=df_row)
        df = df.set_index('Genotypes')

        #saves p-values dataframe in text file
        with open(Global.file_name.split('.')[0] + '_Dunn_pval' + '-' \
                  + str(Global.export_number_stats) + '.txt', 'w') as outfile:
            outfile.write('p-values of Dunn\'s test for genotype \
combinations indicated in the \n"Genotypes" columns and fungal structures \
indicated as column headers.\n\n')
            df.to_string(outfile)

    def process_csv(self):
        """Read csv file containing arbuscular mycorrhizal fungi colonization
data, calculate median, display bar chart and perform Mann-Whitney test on each genotype
combination"""
        
        Global.export_number_fig += 1

        if self.mBar.group_by.get() == 0:    #group by genotype
            #=== PREPARATION ===#
            #browse file name
            Global.file_name = filedialog.askopenfilename()

            #read the csv file
            Global.col = pd.read_csv(Global.file_name)

            #remove NaN values from data frame
            index_name = Global.col.columns[0]
            Global.col = Global.col.loc[~pd.isna(Global.col[index_name])]
            Global.col = Global.col.dropna(1)

            #set index as first column
            Global.col = Global.col.set_index(index_name)

            #collect genotype names
            geno = []
            for g in Global.col.index:
                if g not in geno:
                    geno.append(g)
            Global.geno = geno

            #count the number of repetitions for each genotype
            number_rep = Global.col.index.value_counts()
            number_rep = number_rep.reindex(geno)

            #collect names of fungal structures
            Global.struct = Global.col.columns[:]

            #calculate medians
            col_group = Global.col.groupby(Global.col.index) # group data by genotype
            medians = col_group.median()
            medians = medians.reindex(geno)

            #=== GRAPHICS ===#
            #set positions and width for bars
            pos = list(range(len(geno)))
            width = 1 / (len(Global.struct) + 1)

            #plotting bars
            Global.figure = plt.figure(figsize=(10, 5))
            Global.ax = Global.figure.add_axes([0.1, 0.1, 0.75, 0.85])

            #draw bar plot from medians
            colors = self.mBar.col

            s = 0
            while s < len(Global.struct):
                plt.bar([p + s * width for p in pos], medians[Global.struct[s]], width,
                        alpha=1, color=colors[s], edgecolor='black',
                        linewidth=.5, zorder=3)
                s += 1
                #add legend
                Global.ax.legend(Global.struct, bbox_to_anchor=(1, 0.5),
                                 loc='center left')

            #draw scatter plot from individual data points
            #first you need a list with data coordinates from the 'col' DataFrame
            start = [0]
            end = [number_rep[0] - 1]
            counter = 1
            while counter < len(geno):
                start.append(end[counter - 1] + 1)
                end.append(end[counter -1] + number_rep[counter])
                counter += 1

            #browse data and add individual points on the graph
            s = 0
            while s < len(Global.struct):
                i = 0
                while i < len(geno):
                    for k in range(start[i], end[i] + 1):
                        plt.plot(i + s * width, Global.col[Global.struct[s]].values[k],
                                 c='black', marker='o', fillstyle='full',
                                 zorder=4, mew=.5, markersize=1.5,
                                 clip_on=False)
                    i += 1
                s += 1

            #set y axis label
            Global.ax.set_ylabel('Total root length colonization (%)')

            #set position of x ticks but no display
            Global.ax.set_xticks([p + width * ((len(Global.struct) - 1) / 2) for p in pos])
            Global.ax.tick_params(axis='x', color='white')

            #set label for x ticks
            Global.ax.set_xticklabels(geno)

            #set y axis limits
            plt.ylim([0, 100])
            plt.xlim([min(pos) - width, max(pos) + len(Global.struct) * width])

            #remove figure frame
            Global.ax.spines['top'].set_visible(False)
            Global.ax.spines['right'].set_visible(False)
            Global.ax.spines['bottom'].set_visible(False)

            #shows figure
            Global.figure.show()

            #=== STATISTICS ===#
            #adapts the menu to data (allow to select individual samples)
            #creates a check_button menu with names of genotypes
            #re-builds the stats menu for subsequent analysis
            if Global.export_number_fig > 1: 
                self.mBar.me5.destroy()
            #drop-down part
            self.mBar.me5 = Menu(self.mBar.statMenu)
            #tkinter variable
            self.mBar.stat_test = IntVar()
            for (v, lab) in [(0, 'Mann-Whitney test'),
                             (1, 'Kruskal-Wallis-Dunn test')]:
                self.mBar.me5.add_radiobutton(label=lab, variable=self.mBar.stat_test,
                                              value=v, command=None)
            self.mBar.me6 = Menu(self.mBar.me5)
            self.mBar.samples = {} #re-initialize dictionary
            for (v, lab) in list(zip(range(len(geno)), geno)):
                self.mBar.samples['{0}'.format(lab)] = IntVar()
                self.mBar.me6.add_checkbutton(label=lab, variable=self.mBar.samples[lab], command=None, onvalue=1, offvalue=0)
            self.mBar.me5.add_cascade(label='Select samples', menu=self.mBar.me6)
            self.mBar.statMenu.configure(menu=self.mBar.me5)
            self.mBar.pack()

        elif self.mBar.group_by.get() == 1:    #group by structure
            #=== PREPARATION ===#
            #browse file name
            Global.file_name = filedialog.askopenfilename()

            #read the csv file
            Global.col = pd.read_csv(Global.file_name)

            #remove NaN values from data frame
            index_name = Global.col.columns[0]
            Global.col = Global.col.loc[~pd.isna(Global.col[index_name])]
            Global.col = Global.col.dropna(1)

            #set index as first column
            Global.col = Global.col.set_index(index_name)

            #collect genotype names
            geno = []
            for g in Global.col.index:
                if g not in geno:
                    geno.append(g)
            Global.geno = geno

            #count the number of repetitions for each genotype
            number_rep = Global.col.index.value_counts()
            number_rep = number_rep.reindex(geno)

            #collect names of fungal structures
            Global.struct = Global.col.columns[:]

            #calculate medians and invert axes of dataframe
            col_group = Global.col.groupby(Global.col.index) # group data by genotype
            medians = col_group.median()
            medians_trans = medians.transpose()

            #=== GRAPHICS ===#
            #set positions and width for bars
            pos = list(range(len(Global.struct)))
            width = 1 / (len(geno) + 1)

            #plotting bars
            Global.figure = plt.figure(figsize=(10, 5))
            Global.ax = Global.figure.add_axes([0.1, 0.1, 0.75, 0.85])

            #draw bar plot from medians
            colors = self.mBar.col

            s = 0
            while s < len(geno):
                plt.bar([p + s * width for p in pos], medians_trans[geno[s]],
                        width, alpha=1, color=colors[s], edgecolor='black',
                        linewidth=.5, zorder=3)
                s += 1
                #add legend
                Global.ax.legend(geno, bbox_to_anchor=(1, 0.5), loc='center left')

            #draw scatter plot from individual data points
            #first you need a list with data coordinates from the 'col' DataFrame
            start = [0]
            end = [number_rep[0] - 1]
            counter = 1
            while counter < len(geno):
                start.append(end[counter - 1] + 1)
                end.append(end[counter - 1] + number_rep[counter])
                counter += 1

            #browse data and add individual points on the graph
            s = 0
            while s < len(Global.struct):
                i = 0
                while i < len(geno):
                    for k in range(start[i], end[i] + 1):
                        plt.plot(s + i * width, Global.col[Global.struct[s]].values[k],
                                 c='black', marker='o', fillstyle='full',
                                 zorder=4, mew=.5, markersize=1.5,
                                 clip_on=False)
                    i += 1
                s += 1

            #set y axis label
            Global.ax.set_ylabel('Total root length colonization (%)')

            #set position of x ticks but no display
            Global.ax.set_xticks([p + width * ((len(geno) / 2 - .5)) for p in pos])
            Global.ax.tick_params(axis='x', color='white')

            #set label for x ticks
            Global.ax.set_xticklabels(Global.struct)

            #set y axis limits
            plt.ylim([0, 100])
            plt.xlim([min(pos) - width, max(pos) + len(geno) * width + width / 2])

            #remove figure frame
            Global.ax.spines['top'].set_visible(False)
            Global.ax.spines['right'].set_visible(False)
            Global.ax.spines['bottom'].set_visible(False)

            Global.figure.show()

            #=== STATISTICS ===#
            #adapts the menu to data (allow to select individual samples)
            #creates a check_button menu with names of genotypes
            #re-builds the stats menu for subsequent analysis
            if Global.export_number_fig > 1: 
                self.mBar.me5.destroy()
            #drop-down part
            self.mBar.me5 = Menu(self.mBar.statMenu)
            #tkinter variable
            self.mBar.stat_test = IntVar()
            for (v, lab) in [(0, 'Mann-Whitney test'),
                             (1, 'Kruskal-Wallis-Dunn test')]:
                self.mBar.me5.add_radiobutton(label=lab, variable=self.mBar.stat_test,
                                              value=v, command=None)
            self.mBar.me6 = Menu(self.mBar.me5)
            self.mBar.samples = {} #re-initialize dictionary
            for (v, lab) in list(zip(range(len(geno)), geno)):
                self.mBar.samples['{0}'.format(lab)] = IntVar()
                self.mBar.me6.add_checkbutton(label=lab, variable=self.mBar.samples[lab], command=None, onvalue=1, offvalue=0)
            self.mBar.me5.add_cascade(label='Select samples', menu=self.mBar.me6)
            self.mBar.statMenu.configure(menu=self.mBar.me5)
            self.mBar.pack()

if __name__ == '__main__':
    app = Application()
    app.mainloop()
    app.master.destroy()
