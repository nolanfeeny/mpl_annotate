# NECESSARY IMPORTS
import matplotlib.pyplot as plt
import matplotlib.image as img
import mpld3
from mpld3 import plugins
mpld3.enable_notebook()


# PLOTS THE IMAGE IN THE NOTEBOOK
def plot(imgname):
    fig, ax = plt.subplots()
    im = img.imread(imgname)
    plt.imshow(im, origin='lower')
    return fig

def pickpoints(fig='', radius=4, color="white", x = 'x', y = 'y'):
    if not fig:
        fig = plt.gcf()
    plugins.connect(fig, Annotate(radius, color, x = x, y = y)) # color='htmlcolorname', radius=int
    plugins.connect(fig, plugins.MousePosition())

# FORMATS x AND y LISTS INTO SHORTER DECIMALS, SO THEY'RE NOT TOO LENGTHY
def cleanformat(var):
    varlist = []
    if type(var) == float:
        varlist = '{:05.2f}'.format(var)
    else:
        for i in range(len(var)):
            varlist.append('{:05.2f}'.format(var[i]))
    return varlist
        
    
        
# MAIN CLASS THAT CONTAINS JAVASCRIPT CODE TO CREATE CIRCLES AND DRAG CIRCLES  
class Annotate(plugins.PluginBase):
    """A plugin that creates points in a figure by clicking the mouse"""
   
    JAVASCRIPT = r"""
    mpld3.register_plugin("annotate", Annotate);
    Annotate.prototype = Object.create(mpld3.Plugin.prototype);
    Annotate.prototype.constructor = Annotate;
    Annotate.prototype.requiredProps = [];
    Annotate.prototype.defaultProps = {radius: 4, color: "white"};
    function Annotate(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    Annotate.prototype.draw = function(){
        
        /// NECESSARY STARTUP VARIABLES ///
        
        var fig = this.fig;
        var ax = fig.axes;
        var dataset = [];
        var x = 0;
        var y = 0;
        var svg = d3.select(".mpld3-figure");   // existing svg element
        var radius = this.props.radius;
        var color = this.props.color;
        var ax = fig.axes[0];
        
        
        /// INDEXES HTML DOC TO PULL VALUES FOR x,y CALIBRATION ///
        
        var xcal = document.getElementsByClassName('mpld3-baseaxes')[0].transform.animVal[0].matrix.e;
        var ycal = document.getElementsByClassName('mpld3-baseaxes')[0].transform.animVal[0].matrix.f;
        console.log(xcal);
        console.log(ycal);
        
        var xcommand = "x = []";
        IPython.notebook.kernel.execute(xcommand);
        var ycommand = "y = []";
        IPython.notebook.kernel.execute(ycommand);
        
        
        ////////// CREATE POINT COMPONENT //////////
        
        var update_coords = function() {
        
            return function() {
                var pos = d3.mouse(this),
                    x = ax.x.invert(pos[0]),
                    y = ax.y.invert(pos[1]);
                    
                var newpoint = {
                    cx: pos[0] + xcal,
                    cy: pos[1] + ycal,
                    r: radius,
                    fill: color
                };
                dataset.push(newpoint);
                
                var circles = svg.selectAll("circle")
                    .data(dataset)
                    .enter()
                    .append("circle")
                    .attr(newpoint)
                    .call(drag);
                       
                var xcommand = "x.append("+x+")";
                IPython.notebook.kernel.execute(xcommand);
                console.log(xcommand);
                var ycommand = "y.append("+y+")";
                IPython.notebook.kernel.execute(ycommand);
                console.log(ycommand);
                   
            };
        }();
        ax.baseaxes
            .on("mousedown", update_coords);

        
        
        ////////// DRAG POINT COMPONENT //////////
        
        var drag = d3.behavior.drag()
            .on("dragstart", dragstarted)
            .on("drag", dragged)
            .on("dragend", dragended);
            
        function dragstarted(d) {
             d3.event.sourceEvent.stopPropagation();
             d3.select(this).classed("dragging", true);
        }
        
        function dragged(d) {
             d3.select(this).attr("cx", d3.event.x)
                            .attr("cy", d3.event.y);             
        }

        function dragended(d, i) {
             d3.event.sourceEvent.stopPropagation();
             d3.select(this).classed("dragging", false);
             var calib_cx = d3.select(this)[0][0].cx.animVal.value - xcal;
             var calib_cy = d3.select(this)[0][0].cy.animVal.value - ycal;
             var xcommand = "x["+i+"] = "+ax.x.invert(calib_cx);
             var ycommand = "y["+i+"] = "+ax.y.invert(calib_cy);
             IPython.notebook.kernel.execute(xcommand);
             IPython.notebook.kernel.execute(ycommand);
             console.log(xcommand);
             console.log(ycommand);
        }


    };"""

    def __init__(self, radius=4, color="white", x = 'x', y = 'y'):
        self.dict_ = {"type": "annotate",
                      "radius": radius,
                      "color": color};
        self.x = x;
        self.y = y;