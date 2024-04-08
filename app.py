import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg before importing any other Matplotlib modules

from flask import Flask, after_this_request, render_template, request
import math
import numpy as np
import os
import atexit
from python_scripts.Curva import Curva

app = Flask(__name__)

plot_path = 'static/curva_plot.png'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST']) #only runs when a post happens !
def calculate():
    # Get input values from the form
    funcX_expr = request.form['funcX'] 
    funcY_expr = request.form['funcY']
    interval_start = float(request.form['interval_start'])
    interval_end = float(request.form['interval_end'])
    interval_step = float(request.form['interval_step'])

    # Define functions for funcX and funcY based on user input
    def funcX(t: float) -> float:
        return eval(funcX_expr) # if it is an expression it will be executed, enter string

    def funcY(t: float) -> float:
        return eval(funcY_expr)

    # Create the curve object with user-defined functions and interval
    curva = Curva(list_t=np.arange(interval_start, interval_end, interval_step), funcX=funcX, funcY=funcY)
    
    # Run the curve
    curva.run()

    return render_template('result.html', plot_path=plot_path)

def delete_image():
    if os.path.exists(plot_path):
        os.remove(plot_path)

# Register the delete_image function to be called at exit
atexit.register(delete_image)

if __name__ == '__main__':
    app.run(debug=True)
