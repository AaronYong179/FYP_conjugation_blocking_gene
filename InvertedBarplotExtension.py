import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D

class InvertedBarplotExtension:
    plt.rcParams.update({'errorbar.capsize':3}) # sets the errorbar capsize
    
    def plot_inv_bars(self, *, limit=None, x=None, \
                         y=None, hue=None, data=None, **kwargs):
        """ Handles the plotting of bar charts that start at a custom lower limit.

        An extension of seaborn's barplot. Current barplots only allow for bars to start
        from y=0, regardless if the bar projects upwards (towards a positive value) or downwards
        (towards a negative value). In order to capture conjugation efficiency, it is important
        to represent a graph that starts from negative infinity and projects upwards.

        Of course, it is impossible to represent negative infinity, hence this behaviour
        is approximated by taking a lower y-limit of all data points, and creating
        bars that project upwards towards y=0. 

        Kwargs:
            limit (int/float) : sets lower limit of barplot
            x (string) : name of DataFrame column as x-axis (first categorical variable)
            y (string) : name of DataFrame column as y-axis
            hue (string) : name of DataFrame column as second categorical variable
            data (pandas.DataFrame) : DataFrame containing plot data
            **kwargs : other kwargs to be passed to seaborn's barplot method

        Raises:
            ValueError : If `y` and `data` are not provided as arguments.
            ValueError : If a negative infinite value is present in the given data
        """

        
        if not y or data is None:
            raise ValueError("'y' and 'data' must be provided.")

        # Sets lower limit of barplot if not provided using the integer floor of the
        # minimum value found on the y-axis
        if not limit:
            limit = np.floor(min(data[y]))
        if limit == float("-inf"):
            raise ValueError("-inf value found in data, please set a manual limit")

        heights = data[y] - limit # heights of bars to be plotted

        barplot_params = {
            'x': x,
            'y': heights,
            'hue' : hue,
            'data' : data,
            'ci' : None,
            'bottom' : limit
        }

        sns.barplot(**barplot_params, **kwargs) # call seaborn's barplot method

    def plot_inv_yerrs(self, *, x=None, y=None, \
                       hue=None, data=None, ax=None, \
                       linestyle='none', ecolor='black', **kwargs):
        """ Handles the plotting of error bars for the inverted barplot.

        Using matplotlib.pyplot's provided error bars is not viable with barplots
        that start at a custom lower limit. The calculated errors would contain
        positive values, thereby be plotted above y=0. Hence, there is a need to transform
        the error bars such that they are overlaid with the inverted bars.

        This method handles such transformations and is able to account for the presence
        or absence of a secondary categorical variable. Error bars are plotted with means
        and standard deviations.

        Kwargs:
            x (string) : name of DataFrame column as x-axis (first categorical variable)
            y (string) : name of DataFrame column as y-axis
            hue (string) : name of DataFrame column as second categorical variable
            data (pandas.DataFrame) : DataFrame containing plot data
            ax (matplotlib.pyplot.axis) : axis of subplot
            linestyle (string) : controls error bar line style, defauled at none
            ecolor (string) : controls error bar color, defaulted at black
            **kwargs : other kwargs to be passed to seaborn's barplot method

        Raises:
            ValueError : If the axis of the inverted barplot is not given. 
        """
        if ax is None:
            raise ValueError("axis of inverted barplot must be specified.")
        
        if hue:
            grouped_data = data.groupby([x, hue])[y]
            plot_cat = hue
        else:
            grouped_data = data.groupby(x)[y]
            plot_cat = x

        # calculating aggregate statistics mean and standard deviation
        categories = data[plot_cat].unique()
        agg_stats = grouped_data.agg(["mean", "std"]).reset_index()
        means, errs, transforms = [], [], []

        
        n = len(categories)
        # calculating the amount of shifting required for error bars
        dodge_amt = 0.8 / n if hue else 1
        left_shift = -(dodge_amt * ((n-1)/2)) if hue else 0

        # compile mean, standard deviation, and error bar transforms 
        for i, category in enumerate(categories):
            curr_grp = agg_stats.loc[agg_stats[plot_cat] == category]
            means.append(np.array(curr_grp["mean"]))
            errs.append(np.array(curr_grp["std"]))
            transforms.append(Affine2D().translate(left_shift + (dodge_amt*i), 0.0) + ax.transData)

        # plot all error bars
        for i in range(len(means)):
            curr_mean_arr = means[i]
            curr_std_arr = errs[i]
            curr_transform = transforms[i]
          
            ax.errorbar(x=range(len(curr_mean_arr)), y=curr_mean_arr,
                    yerr=curr_std_arr, transform=curr_transform,
                    linestyle=linestyle, ecolor=ecolor)

InvertedBarplotExtension = InvertedBarplotExtension()
