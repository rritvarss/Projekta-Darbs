from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "parole123"

@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" in session:
        return render_template("index.html")
    else:
        return redirect("/login")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        lietotajvards = request.form.get("lietotajvards")
        parole = request.form.get("parole")
        
        user_id = 1 # TODO nomainit lai iegust no datubazes

        session["user_id"] = user_id
                
        return redirect("/")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        return redirect("/")
        

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
