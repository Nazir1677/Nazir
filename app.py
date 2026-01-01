from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["GET", "POST"])
def greet():
    if request.method == "POST":
        name = request.form["name"]
        return render_template("greet.html", username=name )
    if request.method == "post":
        age = request.form["age"]
        return render_template("greet.html", userage=age )
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run()