from flask import Flask, render_template, url_for, request
from subprocess import Popen, PIPE
import textwrap

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        main_file =  "../models/main.py"
        output_file = "../models/generatedCode.py"

        with open(main_file,"r") as original_code:
            script_to_be_run = original_code.read()

            code_generated_by_blockly = request.get_data(as_text=True)
            command_list = code_generated_by_blockly.splitlines()

            for index in range(len(command_list)):
                command_list[index] = "  "  + command_list[index] + "\n"
            
            code_generated_by_blockly = ''.join(command_list)
        
            script_to_be_run = script_to_be_run.replace("  #REPLACE", code_generated_by_blockly)

            script_to_be_run += "\nexit()"

            with open(output_file, "w") as file:
                file.write(script_to_be_run)
                filho_process = Popen(["python3", output_file, ""])
        
    return render_template("index.html")


app.run(port=5000, debug=False)
