from flask import Flask, render_template, url_for, request
from subprocess import Popen, PIPE
import textwrap

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        code_generated_by_blockly = request.get_data(as_text=True)
        codigo_base(code_generated_by_blockly)
        
    return render_template("index.html")

@app.route("/turn/<int:x>")
def girar(x):
    comando = "car.setAngle(" + str(abs(x)) + ")\n"
    comando += "execute(car.turn)\n"
    codigo_base(comando)
    return comando

@app.route("/speed/<int:y>")
def velocidade(y):
    comando = "car.setSpeed(" + str(y/100) + ")\n"
    codigo_base(comando)
    return comando

@app.route("/f/<int:z>")
def mover_frente(z):
    comando = "car.setDirection(" + "F" + ")\n"
    comando += "car.setDistance("+ str(abs(z)) +")\n"
    comando += "execute(car.move)\n"
    codigo_base(comando)
    return comando

@app.route("/t/<int:w>")
def mover_tras(w):
    comando = "car.setDirection("+"T"+")\n"
    comando += "car.setDistance("+ str(abs(w)) +")\n"
    comando += "execute(car.move)\n"
    codigo_base(comando)
    return comando

def codigo_base(code_generated_by_blockly)
    main_file =  "../models/main.py"
    output_file = "../models/generatedCode.py"

    with open(main_file,"r") as original_code:
        script_to_be_run = original_code.read()


        command_list = code_generated_by_blockly.splitlines()

        for index in range(len(command_list)):
            command_list[index] = "  "  + command_list[index] + "\n"
        
        code_generated_by_blockly = ''.join(command_list)
    
        script_to_be_run = script_to_be_run.replace("  #REPLACE", code_generated_by_blockly)

        script_to_be_run += "\nexit()"

        with open(output_file, "w") as file:
            file.write(script_to_be_run)
            filho_process = Popen(["python3", output_file, ""])
            
app.run(port=5005, debug=False)

