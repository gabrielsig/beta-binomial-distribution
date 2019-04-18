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

# Set up plot
plot = figure(plot_height=400, plot_width=800, title="Distribuição beta binomial",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=[0, initial_n+1], y_range=[0, 0.4]
)

plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# set up widgets
n = Slider(title="n", value=10, start=1, end=30, step=1)
alpha = Slider(title="alpha", value=1, start=0, end=40, step=0.25)
beta = Slider(title="beta", value=1, start=0, end=40, step=0.25)

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

# wire the callbacks
for w in [n, alpha, beta]:
    w.on_change('value', update_data)

# Set up layouts and add to document
inputs = column(n, alpha, beta)

curdoc().add_root(row(inputs, plot, width=800))
curdoc().title = "Beta-Binomial"