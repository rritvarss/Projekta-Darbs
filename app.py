from flask import Flask, render_template, request, redirect, url_for, session
from cs50 import SQL
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "parole123"

db = SQL("sqlite:///datubaze.db")

class UserService():
    def __init__(self, db):
        self.db = db

    def autentificet(self, lietotajvards, parole):
        lietotaji = self.db.execute(
            "SELECT * FROM lietotaji WHERE lietotajvards=? AND parole=?",
            lietotajvards, parole
        )
        return lietotaji[0] if lietotaji else None
    
    def lietotajs_eksiste(self, lietotajvards):
        return self.db.execute(
            "SELECT * FROM lietotaji WHERE lietotajvards=?",
            lietotajvards
        )
        
    def izveidot_lietotaju(self, lietotajvards, parole):
        return self.db.execute(
            "INSERT INTO lietotaji(lietotajvards, parole) VALUES(?, ?)",
            lietotajvards, parole
        )   
        
userService = UserService(db)

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "parole123"

        self.db = SQL("sqlite:///datubaze.db")
        self.user_service = UserService(self.db)
        
        self.routes()
        
    def routes(self):
        self.app.add_url_rule("/", view_func=self.index, methods=["GET", "POST"])
        
    def index(self):
        pass
    
    def login(self):
        pass
    
    def register(self):
        pass
    
    def logout(self):
        pass

@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" in session:
        return render_template("index.html")
    else:
        return redirect("/login")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "user_id" in session:
            return redirect("/")
            
        return render_template("login.html")
    

    elif request.method == "POST":
        lietotajvards = request.form.get("lietotajvards")
        parole = request.form.get("parole")
        hashed_parole = hashlib.md5(parole.encode("utf-8")).hexdigest()
        
        lietotajs = userService.autentificet(lietotajvards, hashed_parole)
        
        if lietotajs:
            print(lietotajs)
            user_id = lietotajs["id"]
        else:
            print("Error")
            return redirect("/register")
            
        session["user_id"] = user_id
                
        return redirect("/")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if "user_id" in session:
            return redirect("/")
        return render_template("register.html")
    
    elif request.method == "POST":
        lietotajvards = request.form.get("lietotajvards")
        parole = request.form.get("parole")
        apst_parole = request.form.get("apst-parole")
        hashed_parole = hashlib.md5(parole.encode("utf-8")).hexdigest()
        
        if parole != apst_parole:
            print("paroles nesakrit")
            return redirect("/register")
        
        lietotajs = userService.lietotajs_eksiste(lietotajvards)
        
        if lietotajs:
            print("Lietotajvards aiznemts!")
            return redirect("/register")
        else:
            result = userService.izveidot_lietotaju(lietotajvards, hashed_parole)
            
        if result:
            session["user_id"] = result
        
        return redirect("/")
    
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if request.method == "GET":
        return redirect('/')
    if "user_id" in session:
        session.pop("user_id", default=None)
        return redirect("/login")
        

if __name__ == "__main__":
    # app.add_url_rule("/", view_func=IndexView.as_view("index"))
    # app.add_url_rule("/login", view_func=LoginView.as_view("login"))
    # app.add_url_rule("/register", view_func=RegisterView.as_view("register"))
    # app.add_url_rule("/logout", view_func=LogoutView.as_view("logout"), methods=["GET", "POST"])

    app.run(debug=True, host="127.0.0.1", port=5000)
