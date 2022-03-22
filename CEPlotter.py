import seaborn as sns
import matplotlib.pyplot as plt
from statannotations.Annotator import Annotator
from InvertedBarplotExtension import InvertedBarplotExtension

class CEPlotter:
    """ Handles the plotting of a conjugation efficiency graph.

    Includes the ability to plot inverted bars, swarmplot, and
    error bars. Statistical annotation is also supported.

    Attributes:
        data (pandas.DataFrame) : data to be plotted given as an input for initialisation
        plot_data (pandas.DataFrame) : a condensed view only showing relevant plot data 
        f (pyplot.figure) : figure containing plot
        axis (pyplot.axis) : axis containing plot
        x (string) : column name containing x-axis data (categorical data)
        y (string) : column name containing y-axis data
        hue (string) : column name containing secondary categorical data
        title (string) : plot title. Optionally used for saving .png files
        palette (list) : list of hex codes for customising plot colours
        face_colour (string) : hex code for plot background colour
        apply_format (function) : formatting function called after plotting data
        global_params (dict) : contains kwargs for calling seaborn/pyplot methods
    """
    def __init__(self, data):
        """ Inits a conjugation effiency plotter object.

        Args:
            data (pandas.DataFrame) : data to be plotted
        """
        self.data = data
        self.plot_data = None
        self.f, self.axis = plt.subplots()
        self.x = None
        self.y = None
        self.hue = None
        self.title = None
        self.palette = None
        self.face_colour = None

    def edit_format(self, title, palette=None, face_colour=None, \
                    ylabel=None, xlabel=None, ylim=0, legend=True):
        """ Edits the format of the plot displayed.

        Args:
            title (string) : plot title, Optionally used for saving .png files

        Kwargs:
            palette (string) : list of hex codes for customising plot colours
            face_colour (string) : hex code for plot background colour
            ylabel (string) : y-axis title
            xlabel (string) : x-axis title
            ylim (integer/float) : upper y-limit of plot area
            legend (boolean) : sets legend visibility
        """
        
        self.palette = palette # inits palette for plotter methods
        
        def format_helper():
            plt.tight_layout()
            
            # formatting title
            plt.title(title, fontsize=9)
            self.title = title

            # formatting facecolor and axes
            self.axis.set_facecolor(face_colour)
            plt.ylabel(ylabel)
            plt.xlabel(xlabel)
            self.axis.set_ylim(top=ylim)

            """
            Note: pyplot's legend displays an idiosyncracy whereby editing visibilty
            undoes all prior legend customisation. 
            """ 
            if legend:
                """
                Duplicate legends arise due to the usage of both swarmplot and barplot.
                Removal of duplicate legends is simply performed by taking half of
                the legend labels.
                """
                plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', \
                           borderaxespad=0) # format legend 
                handles, labels = self.axis.get_legend_handles_labels() # get all handles and labels
                num_values = int(len(handles)/2) # slice into half (remove duplicate)
                self.axis.legend(handles[num_values:], labels[num_values:]) # repopulate legend
            else:
                self.axis.legend().set_visible(legend) # if legend=False, set invisible legend
            
            
        self.apply_format = format_helper


    def make_plot(self, *, x=None, y=None, hue=None, swarm=True, \
                  inv_bar=True, inv_bar_lim=None, yerr=True):
        """ Main method for handling all other plotting methods.

        Swarmplots, inverted barplots, and error bars can be toggled on/off
        individually. The use of an optional secondary categorical variable `hue`
        is supported.

        Kwargs:
            x (string) : column name containing x-axis data (categorical data)
            y (string) : column name containing y-axis data
            hue (string) : column name containing secondary categorical data
            swarm (boolean) : toggles swarmplot on/off
            inv_bar (boolean) : toggles inverted barplot on/off
            inv_bar_lim (integer/float) : sets custom lower limit for inverted barplot
            yerr (boolean) : toggles error bars on/off
        """

        # saving plot data and plot parameters
        self.plot_data = self.data[[y, x, hue]] if hue else self.data[[y, x]]
        self.y = y
        self.x = x
        self.hue = hue

        self.global_params = {
            'data' : self.plot_data,
            'x' : x,
            'y' : y,
            'hue' : hue,
            'ax' : self.axis,
            'palette' : self.palette,
        }

        # control the plotting of inverted bars, swarmplot, or error bars
        if inv_bar:
            self.plot_inv_bars(inv_bar_lim)
        if swarm:
            self.plot_swarm()
        if yerr:
            self.plot_error_bars()

        self.apply_format()
        
    def plot_swarm(self):
        """ Handles plotting of seaborn swarmplot. """
        swarmplot_params = {
            'dodge' : True,
            'linewidth' : 1,
        }
        sns.swarmplot(**self.global_params, **swarmplot_params)

    def plot_inv_bars(self, inv_bar_lim):
        """ Calls InvertedBarplotExtension for plotting of inverted bars.

        Args:
            inv_bar_lim (integer/float) : custom lower limit for inverted barplot
        """
        InvertedBarplotExtension.plot_inv_bars(limit=inv_bar_lim, \
                                               **self.global_params)

    def plot_error_bars(self):
        """ Calls InvertedBarplotExtension for plotting of error bars. """

        InvertedBarplotExtension.plot_inv_yerrs(**self.global_params)

    def annotate_stats(self, pairs):
        """ Performs statistical annotations given a list of pairs to compare.

        By default, an independent samples t-test is performed. 

        Args:
            pairs (list) : A list of comparison pairs
                e.g. [("MG1655", "ECOR A"), ("MG1655", "ECOR B"), ...] 
                or [(("MG1655", "pRK24"), ("MG1655", "F")), ...] if secondary categorical variable
        """
        annot = Annotator(self.axis, pairs, data=self.plot_data, x=self.x, y=self.y, hue=self.hue)
        annot.configure(test='t-test_ind') # modify this if a different test is used
        annot.apply_and_annotate()

    def show_and_save_plot(self, save_dir, fname=None):
        """ Shows the plot and saves it as a .png file.

        Args:
            save_dir (string) : folder to contain saved images
            fname (string) : optional file name. File will be named according to
                the plot title if no file name is given.
        """
        if fname is None:
            path = os.join(save_dir, f"{self.title}.png")
        else:
            path = os.join(save_dir, f"{fname}.png")
        plt.savefig(path)
        plt.show()

    def show_plot(self):
        """ Shows the plot without saving. """
        plt.show()
        






