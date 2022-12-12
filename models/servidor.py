from flask import Flask

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    print("oi")        
    return "i"


app.run(port=5000, host="0.0.0.0")