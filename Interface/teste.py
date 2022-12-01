from flask import Flask, render_template, url_for, request
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        language = """
        from models.car import Car
        car = Car()

        """
        language += request.get_data(as_text=True)
        print(language)
    return render_template("index.html")


app.run(port=5000, debug= True)
