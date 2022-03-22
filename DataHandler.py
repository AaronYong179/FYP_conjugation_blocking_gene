import pandas as pd

## CONSTANTS
## Make sure that the csv file headers match the following headers
COLUMN_HEADERS = ["Donors",
                  "Recipients",
                  "Plasmids",
                  "Media",
                  "Temperature",
                  "Duration",
                  "C/D",
                  "log(C/D)"]


class DataFilter:
    """ Contains a list of filters to apply to a dataframe.

    The DataFilter class is given as an input to the DataHandler class.
    Inclusion/exclusion criteria are interpreted and applied to a dataframe
    encapsulated by the DataHandler class.

    Attributes:
        filters : A list of filtering criteria. 
    """
    def __init__(self):
        """ Inits DataFilter with an empty list """
        self.filters = []

    def add_filter(self, column, values, include=False):
        """ Method to add a filter into the list of filters.

        A filter is represented by the column name to be filtered, a list of values
        to exclude/include, and a boolean representing the decision to exclude or
        include the list of values provided.
        
        Args:
            column (str): Column name to be filtered. The name must be an element of
                global constant :COLUMN_HEADERS:
            values (list): A list of strings, containing values to include or exclude.
                Does not work with numeric values.
            include (bool): Excludes or includes the strings within arg :values:
        """
        self.filters.append((column, values, include))

    def get_filters(self):
        """ Returns a list of added filters. """
        return self.filters


class DataHandler:

    """ A list of categorical variables within the gloabl constant :COLUMN_HEADERS: """
    CATEGORICAL_DATA = [x for x in COLUMN_HEADERS if \
                        (x != "C/D" and x != "log(C/D)")]
    
    def __init__(self, df):
        """ Inits DataHandler with a pandas DataFrame.

        Args:
            df (pandas.DataFrame) : pandas DataFrame of data to be plotted 
        """
        self.data = df

        # A boolean flag; set to true once method :__prepare_categorical_data
        # is run. 
        self.is_categorical = False

    def __prepare_categorical_data(self):
        """ Converts columns in :CATEGORICAL_DATA: into into pandas' representation
        of categorical data.

        In order to plot data correctly, the pandas DataFrame needs to know which column
        contains categorical data. The conversion to categorical data occurs after filtering,
        to avoid wasting resources on data that is meant to be excluded in the first place.
        """
        self.is_categorical = True
        for cat_var in self.CATEGORICAL_DATA:
            self.data[cat_var] = pd.Categorical(self.data[cat_var], \
                                                self.data[cat_var].unique())
            
    def get_data(self):
        """ Converts relevant data into categorical data (if not already done) before
        returning a DataFrame of cleaned plot data. """
        if not self.is_categorical:
            self.__prepare_categorical_data()
        return self.data

    def filter_data(self, data_filter_obj):
        """ Applies filter criteria from an input DataFilter object.

        Args:
            data_filter_obj (DataFilter): DataFilter containing inclusion/exclusion criteria
        """
        for flt in data_filter_obj.get_filters():
            col, val, include = flt
            # Note that only filtering by string values are implemented at the moment.
            if include:
                self.data = self.data.loc[self.data[col].isin(val)]
            else:
                self.data = self.data.loc[~self.data[col].isin(val)]


