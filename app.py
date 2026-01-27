from flask import Flask, render_template, request, redirect, url_for, session
from cs50 import SQL

app = Flask(__name__)
app.config["SECRET_KEY"] = "parole123"

db = SQL("sqlite:///datubaze.db")

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
        
        lietotajs = db.execute("SELECT * FROM lietotaji WHERE lietotajvards=? AND parole=?;", lietotajvards, parole)
        
        if lietotajs:
            print(lietotajs)
            user_id = lietotajs[0]["id"]
        else:
            print("Error")
            return redirect("/register")
            
        session["user_id"] = user_id
                
        return redirect("/")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    elif request.method == "POST":
        lietotajvards = request.form.get("lietotajvards")
        parole = request.form.get("parole")
        apst_parole = request.form.get("apst-parole")
        
        if parole != apst_parole:
            print("paroles nesakrit")
            return redirect("/register")
        
        lietotajs = db.execute("SELECT * FROM lietotaji WHERE lietotajvards=?", lietotajvards)
        
        if lietotajs:
            print("Lietotajvards aiznemts!")
            return redirect("/register")
        else:
            result = db.execute("INSERT INTO lietotaji(lietotajvards, parole) VALUES(?, ?);", lietotajvards, parole)
            
        if result:
            session["user_id"] = result
        
        return redirect("/")
        

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
