#!/usr/bin/env python3

import os
#import PIL
import time
import json
import datetime
import subprocess

current_date = datetime.date(2021,5,1)
today = datetime.date.today()
min_x = 1000
max_x = 0
min_y = 1000
max_y = 0
datapoints = {}

while current_date < today:
	if (os.path.isfile('./collected_data/'+current_date.isoformat()+'.json')):
		distance2start = current_date - datetime.date(2021,5,1)
		if (distance2start.days < min_x):
			min_x = distance2start.days
		if (distance2start.days > max_x):
			max_x = distance2start.days
		json_filehanlder = open('./collected_data/'+current_date.isoformat()+'.json','r')
		this_days_data = json.load(json_filehanlder)
		json_filehanlder.close()
		for this_bundesland in this_days_data:
			#print(this_bundesland)
			novac = this_bundesland['population'] - this_bundesland['vacchalf']
			nofullvac = this_bundesland['population'] - this_bundesland['vaccfull']
			cases7_100k = 100000 * this_bundesland['cases7'] / this_bundesland['population']
			cases7_100k_nofullvac = 100000 * this_bundesland['cases7'] / nofullvac
			cases7_100k_novac = 100000 * this_bundesland['cases7'] / novac
			if (cases7_100k > max_y):
				max_y = cases7_100k
			if (cases7_100k_novac > max_y):
				max_y = cases7_100k_novac
			if (cases7_100k < min_y):
				min_y = cases7_100k
			if (cases7_100k_novac < min_y):
				min_y = cases7_100k_novac
			this_datapoint = { 'x' : distance2start.days, 'y1' : cases7_100k, 'y2' : cases7_100k_nofullvac, 'y3' : cases7_100k_novac }
			if (not(this_bundesland['shortname'] in datapoints)):
				datapoints[this_bundesland['shortname']] = []
			datapoints[this_bundesland['shortname']].append(this_datapoint)
		print(str(min_x)+'|'+str(min_y)+' ; '+str(max_x)+'|'+str(max_y))
	current_date = current_date + datetime.timedelta(days=1)
		
## okay now I got the minimal and maximal values for x and y
# for example today (2021-7-7) it's 14-66 for x and 0.9-198 for y
# That means a graphic might look like this:
#
#      198
#       |
#       |
#       |
#       |
#       |
#       |
#       |
#       |
#   14--+---------------------------------------------66
#       |
#      0.9
#
# In fomulas that means:
# 
# x_percent = (x-14)/(66-14)
# y_percent = (y-0.9) / (198-0.9)
#
# and for drawing:
# x_pen = x_percent*graph_width+padding

print('##########################################')
for bundesland in datapoints:
	this_sparkle = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>

<svg
   width="650"
   height="350"
   version="1.1"
"""
	this_sparkle += 'id="sparkleline_'+bundesland+'"'
	this_sparkle += """
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <g
     id="layer1">
    <path
       style="fill:none;stroke:#000000;stroke-width:0.25px;"
       d="M 25,340 25,25"
       id="vertical_axis" />
    <path
       style="fill:none;stroke:#000000;stroke-width:0.25px;"
       d="M 10,325 625,325"
       id="horizontal_axis" />
"""
	spark1 = '<path style="fill:none;stroke:#0000ff;stroke-width:0.25px;" d="M'
	spark2 = '<path style="fill:none;stroke:#009900;stroke-width:0.25px;" d="M'
	spark3 = '<path style="fill:none;stroke:#ff0000;stroke-width:0.25px;" d="M'
	for this_datapoint in datapoints[bundesland]:
		x_percent = (this_datapoint['x']-min_x)/(max_x-min_x)
		x_pen = x_percent*600 + 25
		y_percent = (this_datapoint['y1']-min_y)/(max_y-min_y)
		y_pen = 300-y_percent*300 + 25
		spark1 += ' '+str(x_pen)+','+str(y_pen)
		y_percent = (this_datapoint['y2']-min_y)/(max_y-min_y)
		y_pen = 300-y_percent*300 + 25
		spark2 += ' '+str(x_pen)+','+str(y_pen)
		y_percent = (this_datapoint['y3']-min_y)/(max_y-min_y)
		y_pen = 300-y_percent*300 + 25
		spark3 += ' '+str(x_pen)+','+str(y_pen)
	this_sparkle += spark1+'" id="cases7_100k" />'+"\n"
	this_sparkle += spark2+'" id="cases7_100k_nofullvac" />'+"\n"
	this_sparkle += spark3+'" id="cases7_100k_novac" />'+"\n"
	this_sparkle += """
  </g>
</svg>"""
	svgfilehandler = open('./images/'+bundesland+".svg", "w")
	svgfilehandler.write(this_sparkle)
	svgfilehandler.close()


subprocess.call(["git", "add", "./images/"])
