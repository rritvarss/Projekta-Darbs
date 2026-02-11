from flask import Flask, render_template, request, redirect, url_for, session
from cs50 import SQL
import hashlib
import serial

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
        
class ServoService():
    def __init__(self):
        self.curr_angle = 0 
    
    def write_angle(self, angle):
        if not ser:
            print("Nav savienots!")
            return
        
        angle = max(0, min(180, angle))
        ser.write(f"{angle},{self.curr_angle}\n".encode())
        self.curr_angle = angle
    

class App:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = "parole123"
        self.db = SQL("sqlite:///datubaze.db")
        self.user_service = UserService(self.db)
        
        self.routes()
        
    def routes(self):
        self.app.add_url_rule("/", view_func=self.index, methods=["GET", "POST"])
        self.app.add_url_rule("/login", view_func=self.login, methods=["GET", "POST"])
        self.app.add_url_rule("/register", view_func=self.register, methods=["GET", "POST"])
        self.app.add_url_rule("/logout", view_func=self.logout, methods=["GET", "POST"])
        
        
    def index(self):
        if "user_id" not in session:
            return redirect("/login")
            
        if request.method == "GET":
            return render_template("index.html")
        
        if request.method == "POST":
            try:
                angle = int(request.form.get("angle"))
            except:
                angle = 0
            
            servoService.write_angle(angle)
            return redirect("/")
        
        
    def login(self):
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
                user_id = lietotajs["id"]
            else:
                print("Error")
                return redirect("/register")
                
            session["user_id"] = user_id
                    
            return redirect("/")


    def register(self):
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

    
    def logout(self):
        if request.method == "GET":
            return redirect('/')
        
        if request.method == "POST":
            if "user_id" in session:
                session.pop("user_id", default=None)
                return redirect("/login")


if __name__ == "__main__":
    try:
        ser = serial.Serial("/dev/ttyACM0", 9600)
    except serial.SerialException:
        ser = None
    
    db = SQL("sqlite:///datubaze.db")
    
    userService = UserService(db)
    servoService = ServoService()
    app_instance = App()
    app_instance.app.run(debug=True, host="127.0.0.1", port=5000)