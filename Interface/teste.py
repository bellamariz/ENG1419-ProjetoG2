from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html")


app.run(port=5000, debug= True)