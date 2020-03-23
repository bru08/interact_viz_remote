"""
Create One plot with two callback froma slider: geneerate n random points
, the button regenerate the random points
Selected points are represented also in the smaller plot in the upper right corner
"""

from random import random
from bokeh.layouts import column, row
from bokeh.models import Button, Slider
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, BoxSelectTool

# create a plot and style its properties
sigma = 10
mean = 5
n = 10  # numer of points to genereate
color = ['blue', 'green', 'red']
p = figure(
    tools="pan,lasso_select,box_select,tap",
    plot_width=600, plot_height=600, 
    toolbar_location='above'
    )
# add a scatter renderer to our plot (no data yet)
r = p.scatter(x= [], y= [], fill_color = [], size=10)
ds = r.data_source


p2 = figure(
    tools="pan,lasso_select,box_select,tap",
    plot_width=200, plot_height=200, 
    toolbar_location='above'
    )
# add a scatter renderer to our plot (no data yet)
r2 = p2.scatter(x= [], y= [], fill_color = [], size=10)
ds2 = r2.data_source



# create a callback that will add a number in a random location
def slider_callback(attr, old, new):
    # regenerate points and add new ones
    n = slider.value
    new_data = dict()
    new_data['x'] = [(random()-.5)*sigma + mean for _ in range(n)]
    new_data['y'] = [(random()-.5)*sigma + mean for _ in range(n)]
    new_data['fill_color'] = [color[int(random()*3)] for _ in range(n)]
    ds.data = new_data

def button_callback():
    # regenerate the same number of points
    n = len(ds.data['x'])
    new_data = dict()
    new_data['x'] = [(random()-.5)*sigma + mean for i in range(n)]
    new_data['y'] = [(random()-.5)*sigma + mean for i in range(n)]
    new_data['fill_color'] = [color[int(random()*3)] for _ in range(n)]
    ds.data = new_data

def plot_selected_callback(attr, old, new):
    indices = ds.selected.indices
    print('sono in seelection callback')
    print(indices)
    for ind in indices:
        print(f"index {ind} x {ds.data['x'][ind]} y {ds.data['y'][ind]} color {ds.data['fill_color'][ind]}")
    new_data = dict()
    new_data['x'] = [ds.data['x'][ind] for ind in indices]
    new_data['y'] = [ds.data['y'][ind] for ind in indices]
    new_data['fill_color'] = [ds.data['fill_color'][ind] for ind in indices]
    ds2.data = new_data

# add a button widget and configure with the call back
button = Button(label="Re-generate random points")
slider = Slider(
    start=0, end=100, value=1, step=1, 
    title="How many points", orientation='vertical',
    bar_color ='blue', direction='rtl'
    )

button.on_click(button_callback)
slider.on_change('value', slider_callback)
ds.selected.on_change('indices', plot_selected_callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(row(column(button, p), slider, p2))
