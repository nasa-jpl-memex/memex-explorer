linspace = (start, end, n) ->                
  L = new Array()
  d = (end - start)/(n-1)
  i = 0
  while i < (n-1)
    L.push(start + i*d);
    i++
  L.push(end)
  return L

N = 50 + 1
r_base = 8
theta = linspace(0, 2*Math.PI, N)
r_x = linspace(0, 6*Math.PI, N-1)
rmin = (r_base - Math.cos(r) - 1 for r in r_x)
rmax = (r_base + Math.sin(r) + 1 for r in r_x)

color = _.flatten((["FFFFCC", "#C7E9B4", "#7FCDBB", "#41B6C4", "#2C7FB8", "#253494", "#2C7FB8", "#41B6C4", "#7FCDBB", "#C7E9B4"] for i in [0..4]))

#
# Create the Bokeh plot
# 

window.source = Bokeh.Collections('ColumnDataSource').create(
  data:
    x: (0 for i in [0...rmin.length])
    y: (0 for i in [0...rmin.length])
    inner_radius: rmin
    outer_radius: rmax
    start_angle: theta.slice(0,-1)
    end_angle: theta.slice(1)
    color: color
)

glyph = {
  type: 'annular_wedge'
  x: 'x'
  y: 'y'
  inner_radius: 'inner_radius'
  outer_radius: 'outer_radius'
  start_angle: 'start_angle'
  end_angle: 'end_angle'
  fill_color: 'color'
  line_color: 'black'
}

options = {
  title: "Animation Demo"
  dims: [600, 600]
  xrange: [-11, 11]
  yrange: [-11, 11]
  xaxes: "below"
  yaxes: "left"
  tools: "pan,wheel_zoom,box_zoom,reset,resize"
}

plot = Bokeh.Plotting.make_plot(glyph, window.source, options)
Bokeh.Plotting.show(plot)

#
# Update the plot data on an interval
# 

update = () ->
  data = window.source.get('data')
  rmin = data["inner_radius"]
  tmp = [rmin[rmin.length-1]].concat(rmin.slice(0, -1))
  data["inner_radius"] = tmp
  rmax = data["outer_radius"]
  tmp = rmax.slice(1).concat([rmax[0]])
  data["outer_radius"] = tmp
  window.source.set('data', data)
  window.source.trigger('change', source, {})

setInterval(update, 100)