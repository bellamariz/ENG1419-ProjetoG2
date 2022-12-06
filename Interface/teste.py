from flask import Flask, render_template, url_for, request
from subprocess import Popen, PIPE
import textwrap

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        script_to_be_run = """
        # from models.car import Car
        # car = Car()

        """
        script_to_be_run = textwrap.dedent(script_to_be_run)
        script_to_be_run = "\t\t\t" + request.get_data(as_text=True)
        

        #teste simulador
        filho_process = Popen(["python", ".\motor-simulation\\filho-simulador.py", script_to_be_run])
        
    return render_template("index.html")


app.run(port=5000, debug= True)
