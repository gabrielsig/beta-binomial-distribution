import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, TextInput
from bokeh.plotting import figure

from scipy.special import gamma 


def beta_binom_density(n, alpha, beta):
    density_list = []
    
    for k in range(n+1):
        numerator = np.float64(1.0*gamma(n+1)*gamma(alpha+k)*gamma(n+beta-k)*gamma(alpha+beta))
        denominator = np.float64(gamma(k+1)*gamma(n-k+1)*gamma(alpha+beta+n)*gamma(alpha)*gamma(beta))
       
        if denominator == 0:
            density_list.append(0)
        else:
            density = numerator / denominator 
            density_list.append(density)
        
    return density_list


# set up the data
initial_n = 10
initial_alpha = 2
initial_beta =2

x = np.arange(0, initial_n+1)
y = beta_binom_density(initial_n, initial_alpha, initial_beta)

# set up the source
source = ColumnDataSource(data=dict(x=x, y=y))

y_end = max(y)+0.1

# Set up plot
plot = figure(plot_height=400, plot_width=800, title="Distribuição Beta Binomial",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=[-1, initial_n+1], y_range=[0, y_end], 
)

plot.title.text_font_size = '20pt'
plot.title.align = 'center'

plot.xaxis.axis_label = 'k'
plot.xaxis.axis_label_text_font_size = '18pt'
plot.xaxis.axis_label_standoff = 30
plot.xaxis.major_tick_line_width = 2
plot.xaxis.major_tick_in = 0
plot.xaxis.major_tick_out = 10
plot.xaxis.major_label_text_font_size = '12pt'
plot.xaxis.minor_tick_line_width = 1


plot.yaxis.axis_label = 'P(X = k)'
plot.yaxis.axis_label_text_font_size = '18pt'
plot.yaxis.axis_label_standoff = 30
plot.yaxis.major_tick_line_width = 2
plot.yaxis.major_tick_in = 0
plot.yaxis.major_tick_out = 10
plot.yaxis.major_label_text_font_size = '12pt'
plot.yaxis.minor_tick_line_width = 1



plot.line('x', 'y', source=source, color="red", line_width=3, line_alpha=0.6, line_dash = [6, 3])
plot.circle('x', 'y', source=source, size=10, color="red", alpha=1)

# set up widgets
n = Slider(title="n", value=10, start=1, end=30, step=1)
alpha = Slider(title="alpha", value=2, start=0, end=40, step=0.1)
beta = Slider(title="beta", value=2, start=0, end=40, step=0.1)

# set up update callbacks
def update_data(attrname, old, new):
    # Get the current slider values
    curr_n = n.value
    curr_alpha = alpha.value
    curr_beta = beta.value
    # Generate the new curve
    x = np.arange(0, curr_n+1)
    y = beta_binom_density(curr_n, curr_alpha, curr_beta)
    # update the source
    source.data = dict(x=x, y=y)
    # update plot scale
    plot.x_range.end = curr_n+1
    plot.y_range.end = max(y)+ 0.1


# wire the callbacks
for w in [n, alpha, beta]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = column(n, alpha, beta)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Beta-Binomial"