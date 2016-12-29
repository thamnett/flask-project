from flask import Flask, render_template, request, redirect
import simplejson as json
from pandas import *
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.embed import components 
import requests

app = Flask(__name__)

app.debug = True

app.vars = {}


@app.route('/', methods=['GET','POST'])
def main():
    return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # request was a POST
        app.vars['tick'] = request.form['ticksymb']
        chartct = 0
        if 'close' in request.form:
            app.vars['close'] = 1
            chartct = chartct + 1
        if 'adjclose' in request.form:  
            app.vars['adjclose'] = 1
            chartct = chartct + 1
        if 'open' in request.form:    
            app.vars['open'] = 1
            chartct = chartct + 1
        if 'adjopen' in request.form:
            app.vars['adjopen'] = 1
            chartct = chartct + 1
    
        api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/GOOG.json' #% 'GOOG'
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url)
                         
        if chartct >= 0: pass
        else:
            return render_template('selection_error.html')
                         
        jsondata = json.loads(raw_data.text)

        try:
            stockdf = DataFrame(data=jsondata['data'],columns=jsondata['column_names'])
        #stockdf
            return render_template('ticker_error.html')
        except KeyError:
            return render_template('ticker_error.html')
        
                         
       # plot = figure(tools=TOOLS,
        #      title='Data from Quandle WIKI set',
         #     x_axis_label='date',
          #    x_axis_type='datetime')
                         
        #script, div = components(plot)
        #return render_template('graph.html', script=script, div=div)

                         
if __name__ == '__main__':
    app.run(port=33507)
