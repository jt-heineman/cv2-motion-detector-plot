from motion_detector import df #make available dataframe from motion detector
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import HoverTool #method expect use hover arrays
from bokeh.models import ColumnDataSource #object that provides data to bokeh, some functions use it

#create new columns with strings to pass to hover element
df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds=ColumnDataSource(df)


p=figure(x_axis_type="datetime", height=100, width=500, sizing_mode="scale_both", title="Motion Graph")  
p.yaxis.minor_tick_line_color=None
p.yaxis[0].ticker.desired_num_ticks=1

#creating hover object
hover=HoverTool(tooltips=[("Start", "@Start_string"),("End","@End_string")]) #passing decorator of dataframe
p.add_tools(hover)

#x=df["Start"]
#y=df["End"]
#q = p.quad(left=x,right=y,bottom=0, top=1,color="green")
q = p.quad(left="Start",right="End",bottom=0, top=1,color="green",source=cds) #get source info from dataframe

output_file("motiondetector3.html")

show(p)