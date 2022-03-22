import os
import pandas as pd
import DataHandler as dh
import CEPlotter as ce

flt = dh.DataFilter() # do not edit unless you know what you are doing!

#############################
## EDITABLE VARIABLES HERE ##
#############################

## RAW DATA LOCATION
CSV_FILE = "./csv_files/master_data.csv"

## PLOT DETAILS
PLOT_TITLE = "pRK24 versus F plasmid transfer"

# Make sure these follow the column name in the csv file!
# If the column name is "Donors" spell it exactly the same way, not "Donor" or "donors".
X_AXIS = "Recipients" 
Y_AXIS = "log(C/D)"
HUE = "Plasmids"

## FORMATTING
PALETTE = ['#A9D18E', '#5A747D']
FACE_COLOUR = '#F4F4F4'

## STATISTICS
# Follow the format given: [("<value1>", "<value2>")]
# If a secondary categorical variable is used: [ ( ("<value1>", "<cat1>"), ("<value1>", "<cat2>") ) ]
PAIRS = [
    (("MG1655", "pRK24"), ("MG1655", "F")),
    (("ECOR C", "pRK24"), ("MG1655", "pRK24"))
]

## FILTERS
# Follow the format given: flt.add_filter("<column_name>", ["<value1>", "<value2>", ...], include=True
# Examples are given below:
# >>> flt.add_filter("Plasmids", ["pRK24", "F"], include=True)
# >>> flt.add_filter("Recipients", ["MG1655"], include=False) # this excludes MG1655

flt.add_filter("Plasmids", ["pRK24", "F"], include=True)
flt.add_filter("Media", ["M9"], include=True)
flt.add_filter("Donors", ["MG1655"], include=True)
flt.add_filter("Recipients", ["MG1655", "ECOR C"], include=True)

#################
## RUN PLOTTER ##
#################

data_handler = dh.DataHandler(pd.read_csv(CSV_FILE, encoding='utf-8')) # read csv data
data_handler.filter_data(flt) # apply filters
plotter = ce.CEPlotter(data_handler.get_data()) # send data to CEPlotter
plotter.edit_format(PLOT_TITLE, palette=PALETTE, face_colour=FACE_COLOUR) # edit plot format
plotter.make_plot(x=X_AXIS, y=Y_AXIS, hue=HUE) # pass in arguments to plot data
plotter.annotate_stats(PAIRS) # apply statistical annotations
plotter.show_plot() # show the final plot
