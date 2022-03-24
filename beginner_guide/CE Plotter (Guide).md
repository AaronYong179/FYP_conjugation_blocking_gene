# CE Plotter (Guide)


This serves as a guide (specifically for my amazing mentor Liyana) to use the Python plotting scripts written. No prior knowledge in programming is required, hopefully the instructions here are comprehensive enough. 

---
## Setting up
The following dependencies (packages) are required:
- pandas
- seaborn
- matplotlib.pyplot
- numpy

`pip` is the most popular tool for installing and managing Python packages, and should be included with Python. 

To install the required packages, simply run `pip install <package>` on the terminal.

For example:
```python
pip install pandas 
```
Alternatively, run: 
```python
python3 -m pip install pandas
```

Install all packages listed above in order to run the scripts provided.

---

## Quick start

The Python file `Main.py` is provided as a foundation for editing commands. Plotting the graphs should be as easy as editing the variables and running the Python script.

### Editable variables
The names of editable variables are typed in all-caps. 

1. `CSV_FILE`
    - The csv file path. The csv file must follow a specific format (details below) and should contain the data to be plotted.
    - The directory must be in the form of a string ([_what's that?_](#Data-types-a-primer))
    - Example: `CSV_FILE = "C:/User/Aaron/FYP/csv_files/master_data.csv"`
    
2. `PLOT_TITLE`
    - The title to be used for the plot.
    - If the plot is to be saved as a figure, this title will also serve as the file name.
    - Again, the title must be a string.
    - Example: `PLOT_TITLE = "pRK24 versus F plasmid conjugation efficiencies"`

3. `X_AXIS`
    - The column name to be used as the x-axis. 
    - The name must be spelt exactly as the csv file header (i.e., if the column is named Donors, "donors" or "Donor" is incorrect and will throw an error).
    - The x-axis name must be a string. 
    - Example: `X_AXIS = "Recipients"`

4. `Y_AXIS`
    - The column name to be used as the y-axis. This should be very often be "log(C/D)".
    - The y-axis name must be a string. 
    - Example: `Y_AXIS = "log(C/D)"`


5. `HUE`
    - The column name to be used as the secondary categorical variable. 
    - For example, if the `X_AXIS` contains the recipients used, I might want to further split recipient data based on the media used.
    - The secondary categorical variable name must be a string. 
    - If there is no secondary categorical variable to be plotted, simply set `HUE = None` ([_what's that?_](#Data-types-a-primer))
    - Example: `HUE = "Media"`

6. `PALETTE`
    - The colour palette to be used. You can either use predefined palettes (see: [_here_](https://matplotlib.org/3.5.1/tutorials/colors/colormaps.html) for more colour palettes ) or customise your own. 
    - Custom colour schemes must be given as a list of strings ([_what's that?_](#Data-types-a-primer))
    - Hex codes should start with a hash symbol (`#`) followed by six letters/numbers.
    - Example: `PALETTE = ["#FFFFFF", "#000000"]`


7. `FACE_COLOUR`
    - The colour of the plot area. Leave it as white (`"#FFFFFF"`) for most use cases.
    - Face colour must be a string of a hex code.
    - Example: `FACE_COLOUR = "#FFFFFF"`


8. `PAIRS`
    - Pairs for statistical analysis. By default, the statistical test performed is an independent samples t-test.
    - The pairs are a list of tuples ([_what's that?_](#Data-types-a-primer))
    - Follow the format given: `[("<value1>", "<value2>")]`
    - If a secondary categorical variable is used: `[ ( ("<value1>", "<cat1>"), ("<value1>", "<cat2>") ) ]`
    - Example: `PAIRS = [
    (("MG1655", "pRK24"), ("MG1655", "F")),
    (("ECOR C", "pRK24"), ("MG1655", "pRK24"))
]`

9. `SAVE_FIG`
    - Sets the plotter to show-and-save or show-only. 
    - Set `SAVE_FIG = True` if you would want the final plot to be saved as a png file. Otherwise, if you just want to show the plot, set `SAVE_FIG = False`.

10. `SAVE_DIR`
    - Directory to save the final plot. 
    - `"./"` simply means "save in the same folder as the Python script".

### Filters

The following section is concerned with filtering the data provided. For example, perhaps the current plot should exclude a certain recipient strain, or only include certain plasmids. This is handled by the filters that you add.

To add a filter, follow the format given: `flt.add_filter("<column_name>", ["<value1>", "<value2>", ...], include=True)`

Examples:
```
flt.add_filter("Plasmids", ["pRK24", "F"], include=True)
flt.add_filter("Recipients", ["MG1655"], include=False)
```

The `add_filter` takes in three arguments: the column to be filtered, filter values, and the decision to include or exclude the values provided. 

A few notes:
- The first argument (column name) must be a string.
- The second argument (filter values) must be in the form of a list of strings ([_what's that?_](#Data-types-a-primer))
- The third argument (filter decision) must take the form of `include=`, followed by the word `True` or `False`.

### Show plot
Note that there should not be any reason for you to modify these lines, just run the code once you have edited the editable variables.

```python=
data_handler = dh.DataHandler(pd.read_csv(CSV_FILE, encoding='utf-8')) # read csv data
data_handler.filter_data(flt) # apply filters
plotter = ce.CEPlotter(data_handler.get_data()) # send data to CEPlotter
plotter.edit_format(PLOT_TITLE, palette=PALETTE, face_colour=FACE_COLOUR) # edit plot format
plotter.make_plot(x=X_AXIS, y=Y_AXIS, hue=HUE) # pass in arguments to plot data
plotter.annotate_stats(PAIRS) # apply statistical annotations
plotter.show_plot() if not SAVE_FIG else plotter.show_and_save_plot(SAVE_DIR) # save or just show
```
---
## CEPlotter
Handles the plotting of a conjugation efficiency graph. 

Includes the ability to plot inverted bars, swarmplot, and error bars. Statistical annotation is also supported. More comprehensive documentation can be found within the code itself.

### Public methods
**edit_format**
``` edit_format(title, palette=None, face_colour=None, ylabel=None, xlabel=None, ylim=0, legend=True) ```
- Edits the format of the plot displayed. 

**make_plot**
``` make_plot(*, x=None, y=None, hue=None, swarm=True, inv_bar=True, inv_bar_lim=None, yerr=True) ```
- Main method for handling all other plotting methods.
- Swarmplots, inverted barplots, and error bars can be toggled on/off individually. The use of an optional secondary categorical variable `hue` is supported.

**annotate_stats**
``` annotate_stats(pairs) ```
- Performs statistical annotations given a list of pairs to compare.
- By default, an independent samples t-test is performed. Returns `None` and exits the method if `None` is given as an input.

**show_and_save_plot**
``` show_and_save_plot(save_dir, fname=None) ```
- Shows the plot and saves it as a .png file.

**show_plot**
``` show_plot() ```
- Shows the plot without saving.

---
## Data types (a primer)
### Strings
A string is how most programming languages deal with a _string_ of characters. However, Python does not understand plain text. You need to explicitly tell Python that this sequence of characters is a string. You can do so by enclosing them in double quotation marks.
```
"this is a string"
"strings can contain numbers too by the way, 1234"

this is not a string! (and will result in an error)
```

### Lists
You can think of lists (for now) as a collection of items. For the purposes of this plotting script, you would only need to worry about a list of strings.

Lists are denoted by square brackets, followed by a sequence of items separated by commas. 

```
["hello", "world", "from", "python"]
["ECOR A", "ECOR B"]
["MG1655"]
```
> The above are called a list of strings.
> The last item only has one element, but enclosing it in square brackets is enough to confer it the "list" type in Python. 

### Tuples
Tuples are also another way to denome a collection of items. The difference between tuples and lists? You don't have to worry about it when using this plotting script. 

Tuples are denoted by regular brackets, followed by a sequence of items separated by commas.

```
("hello", "world", "from", "python")
("ECOR A", "ECOR B")
```
> The above are called a tuple of strings.

### NoneType
`None` is a bit difficult to explain to a non-programmer, but just think of it as quite literally nothing. 

