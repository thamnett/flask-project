from flask import Flask, render_template, request, redirect
import simplejson as json
from pandas import *
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.palettes import Spectral11
from bokeh.embed import components
from bokeh.charts import TimeSeries, color
import requests

app = Flask(__name__)

app.debug = True

@app.route('/', methods=['GET','POST'])
def main():
    return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # request was a POST
        ticksymb = request.form['ticksymb']
        chartct = 0
        app.vars = {}
        if 'rawclose' in request.form:
            app.vars['close'] = 'Close'
            chartct = chartct + 1
        if 'adjclose' in request.form:  
            app.vars['adjclose'] = 'Adj. Close'
            chartct = chartct + 1
        if 'rawopen' in request.form:    
            app.vars['open'] = 'Open'
            chartct = chartct + 1
        if 'adjopen' in request.form:
            app.vars['adjopen'] = 'Adj.Open'
            chartct = chartct + 1
    
        api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % ticksymb
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)
                  
        jsondata = json.loads(raw_data.text)

        try:
            stockdf = DataFrame(data=jsondata['data'],columns=jsondata['column_names'])
            pass
        except KeyError:
            return render_template('ticker_error.html')
        
        if chartct > 0: pass
        else:
            return render_template('selection_error.html')
        
        stockdf['Date'] = to_datetime(stockdf['Date'], format='%Y-%m-%d')
        
        stockdf = stockdf.set_index('Date')
        
        stockdf = stockdf.iloc[:21]
        
        stockdf = stockdf.iloc[::-1]
        
        col_list = []
            
        for key in app.vars:
            col_list.append(app.vars[key])
        
        stockdf = stockdf.ix[:,col_list]
        
        numlines=len(stockdf.columns)
        mypalette=Spectral11[0:numlines]
        
        plot = figure(title='Data from Quandle WIKI set', x_axis_label='date', 
                   x_axis_type="datetime") 

        for i in range(numlines):
            plot.line(x=stockdf.index.values,y=stockdf.ix[:,i],line_color=mypalette[i],
                   line_width=5,legend=col_list[i])
                         
        script, div = components(plot)
        return render_template('graph.html', script=script, div=div, tick=ticksymb)

                         
if __name__ == '__main__':
    app.run(port=33507)
