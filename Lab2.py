from spyre import server
import pandas as pd
import urllib2
import os
import re
from matplotlib import pyplot as plt

def pathToDirectory():
	return "/Users/pashaluchkovski/Documents/Study/Coding/Python/pyth/"

def getDataByIndex(index):
    #index = reIndex(index)
    strIndex = str(index)
    if index<10:
        strIndex = "0"+strIndex
    url="http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R"+strIndex+".txt"
    vhi_url = urllib2.urlopen(url)
    out = open('/Users/pashaluchkovski/Documents/Study/Coding/Python/pyth/f.csv', 'wb')
    out.write(vhi_url.read())
    out.close()

    print "VHI " + strIndex + " is downloaded..."


class SimpleApp(server.App):
    title = "Data Analysis/Lab 2"
    tabs = ["Plot","Table"]
    controls = [ {"type" : "button", "id" : "update_data", "label": "Calculate!"}]
	
    inputs = [
                {   "input_type":'dropdown',
                    "label": 'column', 
                    "options" : [ {"label": "VCI", "value":"VCI"},
                                  {"label": "TCI", "value":"TCI"},
                                  {"label": "VHI", "value":"VHI"}],
                    "key": 'column', 
                    "action_id": "update_data" },
                {	"input_type":'text',
                    "label": 'Year', 
                    "value":2016,
                    "key": "year_r",
                    "action_id": "update_data" },
                {   "input_type":'text',
                    "label": 'Week since', 
                    "value":1,
                    "key": "since", 
                    "action_id": "update_data" },
              	{     "input_type":'text',
                    "label": 'Week till', 
                    "value":52,
                    "key": "till",
                    "action_id": "update_data" },
                {
                    "input_type":'dropdown',
                    "label": 'Region', 
                    "key": "reg", 
                    "options" : [ {"label":"Cherkasy Oblast", "value":"1"},
								  {"label":"Chernihiv Oblast", "value":"2"},
								  {"label":"Chernivtsi Oblast", "value":"3"},
								  {"label":"Crimea", "value":"4"},
								  {"label":"Dnipropetrovsk Oblast", "value":"5"},
								  {"label":"Donetsk Oblast", "value":"6"},
								  {"label":"Ivano-Frankivsk Oblast", "value":"7"},
								  {"label":"Kharkiv Oblast", "value":"8"},
								  {"label":"Kherson Oblast", "value":"9"},
								  {"label":"Khmelnytskyi Oblast", "value":"10"},
								  {"label":"Kiev Oblast", "value":"11"},
								  {"label":"Kiev City", "value":"12"},
								  {"label":"Kirovohrad Oblast", "value":"13"},
								  {"label":"Luhansk Oblast", "value":"14"},
								  {"label":"Lviv Oblast", "value":"15"},
								  {"label":"Mykolaiv Oblast", "value":"16"},
								  {"label":"Odessa Oblast", "value":"17"},
								  {"label":"Poltava Oblast", "value":"18"},
								  {"label":"Rivne Oblast", "value":"19"},
								  {"label":"Sevastopol`", "value":"20"},
								  {"label":"Sumy Oblast", "value":"21"},
								  {"label":"Ternopil Oblast", "value":"22"},
								  {"label":"Transkarpathia Oblast", "value":"23"},
								  {"label":"Vinnytsia Oblast", "value":"24"},
								  {"label":"Volyn Oblast", "value":"25"},
								  {"label":"Zaporizhia Oblast", "value":"26"},
								  {"label":"Zhytomyr Oblast", "value":"27"}
								],
					"action_id": "update_data"
	}]
    outputs = [{	
    				"output_type" : "plot",
                    "output_id" : "plot",
                    "type" : "plot",
					"id" : "plot",
					"control_id" : "update_data",
					"tab" : "Plot"},
				{	"type" : "table",
					"id" : "table_id",
					"control_id" : "update_data",
					"tab" : "Table",
					"on_page_load" : True 
				}
			]

    def getData(self,params):
    	getDataByIndex(params['reg'])
    	os.chdir(pathToDirectory())
    	df = pd.read_csv('f.csv', index_col=False, header = 1)
    	frame = df
    	frame_columns = frame.columns.values
    	for i in range(0, len(frame.columns.values)):
    		frame_columns[i] = re.sub('[^A-Za-z0-9]+', '', frame_columns[i])
    	frame.columns = frame_columns
    	frame = frame.loc[(df['year'] == int(params['year_r']))]
    	frame = frame.loc[(df['week'] >= int(params['since']))]
    	frame = frame.loc[(df['week'] <= int(params['till']))]
    	frame = frame.loc[(df['SMN'] != -1)]
    	#print list(df['year'])
    	return frame

    def getPlot(self,params):
   		df = pd.read_csv(pathToDirectory()+"f.csv", index_col=False, header=1)
   		#frame = self.getData(params)
   		frame = df[(df['year'] == int(params['year_r']))]
   		frame = frame.loc[(frame['week']<=int(params['till']))]
   		frame = frame.loc[(frame['week']>=int(params['since']))]
   		y_axis = frame[params['column']]
   		x_axis = frame['week']
   		plt.plot(x_axis, y_axis)
   		return plt.gcf()

app = SimpleApp()
app.launch()
#a = {"since": 2014, "till": 2016}
#frame = app.getData(a)