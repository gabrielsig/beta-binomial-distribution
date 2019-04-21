import numpy as np

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, Div
from bokeh.plotting import figure

from scipy.special import gamma 
from scipy.stats import beta


# def beta(alpha, beta):
#     density_list = []
#     for p in np.linspace(0.01, 1, 100):
#         density = gamma(alpha+beta)/(gamma(alpha)*gamma(beta)) * x**(alpha-1)*(1-x)**(beta-1)
#         density_list.append(density)
    
#     return density_list

def beta_binom(n, alpha, beta):
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
pdf_y = beta_binom(initial_n, initial_alpha, initial_beta)
cdf_y = list(np.cumsum(pdf_y))

beta_x =  np.linspace(0, 1.0, 100)
beta_pdf_y =  beta.pdf(beta_x , initial_alpha, initial_beta)
beta_cdf_y =  beta.cdf(beta_x , initial_alpha, initial_beta)


# set up the source
pdf_source = ColumnDataSource(data=dict(x=x, y=pdf_y))
cdf_source = ColumnDataSource(data=dict(x=x, y=cdf_y))
beta_pdf_source = ColumnDataSource(data=dict(x=beta_x, y=beta_pdf_y))
beta_cdf_source = ColumnDataSource(data=dict(x=beta_x, y=beta_cdf_y))


# Set up plot
pdf_plot = figure(
    plot_height=300, 
    plot_width=600, 
    title="PDF",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=[-1, initial_n+1], y_range=[0,  max(pdf_y)+0.1], 
)

cdf_plot = figure(
    plot_height=300, 
    plot_width=600, 
    title="CDF",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=[-1, initial_n+1], y_range=[0.0,  1.05], 
)

beta_pdf_plot = figure(
    plot_height=300, 
    plot_width=600, 
    title="Beta Distribution",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=[-0.05, 1.05], y_range=[0.0, max(beta_pdf_y)+0.1], 
)

beta_cdf_plot = figure(
    plot_height=300, 
    plot_width=600, 
    title="Beta Distribution",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=[-0.05, 1.05], y_range=[0.0,  1.05], 
)

pdf_plot.title.text_font_size = '16pt'
pdf_plot.title.align = 'center'
pdf_plot.xaxis.axis_label = 'k'
pdf_plot.yaxis.axis_label = 'P(X = k)'
pdf_plot.axis.axis_label_text_font_size = '14pt'
pdf_plot.axis.axis_label_standoff = 20
pdf_plot.axis.major_tick_line_width = 2
pdf_plot.axis.major_tick_in = 0
pdf_plot.axis.major_tick_out = 10
pdf_plot.axis.major_label_text_font_size = '10pt'
pdf_plot.axis.minor_tick_line_width = 1

cdf_plot.title.text_font_size = '16pt'
cdf_plot.title.align = 'center'
cdf_plot.xaxis.axis_label = 'k'
cdf_plot.yaxis.axis_label = 'F(X < k)'
cdf_plot.axis.axis_label_text_font_size = '14pt'
cdf_plot.axis.axis_label_standoff = 20
cdf_plot.axis.major_tick_line_width = 2
cdf_plot.axis.major_tick_in = 0
cdf_plot.axis.major_tick_out = 10
cdf_plot.axis.major_label_text_font_size = '10pt'
cdf_plot.axis.minor_tick_line_width = 1

beta_pdf_plot.title.text_font_size = '16pt'
beta_pdf_plot.title.align = 'center'
beta_pdf_plot.xaxis.axis_label = 'p'
beta_pdf_plot.yaxis.axis_label = 'PDF'
beta_pdf_plot.axis.axis_label_text_font_size = '14pt'
beta_pdf_plot.axis.axis_label_standoff = 20
beta_pdf_plot.axis.major_tick_line_width = 2
beta_pdf_plot.axis.major_tick_in = 0
beta_pdf_plot.axis.major_tick_out = 10
beta_pdf_plot.axis.major_label_text_font_size = '10pt'
beta_pdf_plot.axis.minor_tick_line_width = 1

beta_cdf_plot.title.text_font_size = '16pt'
beta_cdf_plot.title.align = 'center'
beta_cdf_plot.xaxis.axis_label = 'p'
beta_cdf_plot.yaxis.axis_label = 'CDF'
beta_cdf_plot.axis.axis_label_text_font_size = '14pt'
beta_cdf_plot.axis.axis_label_standoff = 20
beta_cdf_plot.axis.major_tick_line_width = 2
beta_cdf_plot.axis.major_tick_in = 0
beta_cdf_plot.axis.major_tick_out = 10
beta_cdf_plot.axis.major_label_text_font_size = '10pt'
beta_cdf_plot.axis.minor_tick_line_width = 1


pdf_plot.line('x', 'y', source=pdf_source, color="red", line_width=3, line_alpha=0.6, line_dash = [6, 3])
# pdf_plot.step('x', 'y', source=pdf_source, color="red", line_width=3, line_alpha=0.6, line_dash = [6, 3], mode="after")
pdf_plot.circle('x', 'y', source=pdf_source, size=10, color="red", alpha=1)

# cdf_plot.line('x', 'y', source=cdf_source, color="red", line_width=3, line_alpha=0.6, line_dash = [6, 3])
cdf_plot.step('x', 'y', source=cdf_source, color="red", line_width=3, line_alpha=0.6, line_dash = [6, 3], mode="after")
cdf_plot.circle('x', 'y', source=cdf_source, size=10, color="red", alpha=1)

beta_pdf_plot.line('x', 'y', source=beta_pdf_source, color="blue", line_width=3 )
beta_cdf_plot.line('x', 'y', source=beta_cdf_source, color="blue", line_width=3 )


# set up widgets
n_slider = Slider(title="n", value=10, start=1, end=30, step=1)
alpha_slider = Slider(title="alpha", value=2, start=0.1, end=40, step=0.1)
beta_slider = Slider(title="beta", value=2, start=0.1, end=40, step=0.1)

# set up update callbacks
def update_data(attrname, old, new):
    # Get the current slider values
    curr_n = n_slider.value
    curr_alpha = alpha_slider.value
    curr_beta = beta_slider.value
    # Generate the new curve
    x = np.arange(0, curr_n+1)
    pdf_y = beta_binom(curr_n, curr_alpha, curr_beta)
    cdf_y = list(np.cumsum(pdf_y))
    beta_x =  np.linspace(0, 1.0, 100)
    beta_pdf_y =  beta.pdf(beta_x , curr_alpha, curr_beta)
    beta_cdf_y = beta.cdf(beta_x , curr_alpha, curr_beta)
    # update the source
    pdf_source.data = dict(x=x, y=pdf_y)
    cdf_source.data = dict(x=x, y=cdf_y)
    beta_pdf_source.data = dict(x=beta_x, y=beta_pdf_y)
    beta_cdf_source.data = dict(x=beta_x, y=beta_cdf_y)
    # update plot scale
    beta_pdf_plot.y_range.end = max(beta_pdf_y)+0.1
    pdf_plot.y_range.end = max(pdf_y)+ 0.1
    pdf_plot.x_range.end = curr_n+1
    cdf_plot.x_range.end = curr_n+1


# wire the callbacks
for w in [n_slider, alpha_slider, beta_slider]:
    w.on_change('value', update_data)


# div = Div(text="""Your <a href="https://en.wikipedia.org/wiki/HTML">HTML</a>-supported text is initialized with the <b>text</b> argument.  The
# remaining div arguments are <b>width</b> and <b>height</b>. For this example, those values
# are <i>200</i> and <i>100</i> respectively.""",
# width=200, height=100)

# Set up layouts and add to document
line1 = row( n_slider, alpha_slider, beta_slider)
line2 = row(pdf_plot, cdf_plot)
line3 = row(beta_pdf_plot, beta_cdf_plot)

curdoc().add_root(column(line1, line2, line3, width=800))
curdoc().title = "Beta-Binomial"