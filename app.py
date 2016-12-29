from flask import Flask, render_template, request, redirect
import simplejson as json
from pandas import *
from bokeh.io import push_notebook, show, output_notebook
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.embed import components 
import requests

app = Flask(__name__)

app.vars = {}
chartct = 0

@app.route('/', methods=['GET'])
def main():
    return redirect('/index')

@app.route('/index', methods='GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        # request was a POST
        app.vars['tick'] = request.form['ticksymb']
        if request.form['close']:
            app.vars['close'] = request.form['close']
            chartct = chartct + 1
        if request.form['adjclose']:    
            app.vars['adjclose'] = request.form['adjclose']
            chartct = chartct + 1
        if request.form['open']:    
            app.vars['open'] = request.form['open']
            chartct = chartct + 1
        if request.form['adjopen']:
        app.vars['adjopen'] = request.form['adjopen']
            chartct = chartct + 1
        
        api_url = 'https://www.quandl.com/api/v1/datasets/WIKI/%s.json' % 'GOOG'
        session = requests.Session()
        session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
        raw_data = session.get(api_url): pass
                         
        if chartct > 0: pass
        else:
            return render_template('selection_error.html')
                         
        jsondata = json.loads(raw_data.text)

        try:
            stockdf = DataFrame(data=jsondata['data'],columns=jsondata['column_names'])
            stockdf
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
