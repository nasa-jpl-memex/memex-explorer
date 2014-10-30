from bokeh.sampledata.iris import flowers
from bokeh.embed import components
import bokeh.resources
from bokeh.plotting import *

output_server("iris")

colormap = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}

flowers['color'] = flowers['species'].map(lambda x: colormap[x])

#setting the name kwarg will give this scatter plot a user
#friendly id, and the corresponding embed.js will have a nice name
#too

scatter(flowers["petal_length"], flowers["petal_width"],
        color=flowers["color"], fill_alpha=0.2, size=10, name="iris",
        tools="pan,wheel_zoom,box_zoom,reset,previewsave",
        plot_width=300, plot_height=300)
        
xax, yax = axis()
xax.axis_label = 'Petal Length'
yax.axis_label = 'Petal Width'

curplot().title = "Iris Morphology"

# a, b = components(curplot(), bokeh.resources.CDN)
show()