from flask import Flask
from flask_mail import Mail, Message
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'yourgmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
mail = Mail(app)
from flask import Flask, render_template, request, redirect, session
import sqlite3
import random   
tips = [
    "Always verify website URLs — fake links can steal your money.",
    "Avoid clicking unknown WhatsApp or SMS links — scammers target mobile users.",
    "Never share OTP, PIN, or passwords with anyone.",
    "Check URL spelling — fraud sites change one character only.",
    "Use strong passwords with symbols, numbers, and mixed case.",
    "Enable 2-factor authentication for all accounts.",
    "Avoid entering credentials on public WiFi networks.",
    "Backup important files — ransomware can lock your system."
]
app.secret_key = "CyberShield123"

# database connection helper
def db():
    return sqlite3.connect("cybersafe.db")

# create tables if not exist
def init_db():
    con = db()
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        issue TEXT,
        message TEXT,
        status TEXT
    )""")

    con.commit()
    con.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        con = db()
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
                        (name,email,password,"user"))
            con.commit()
            return redirect("/login")
        except:
            return "User already exists!"
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        con = db()
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password))
        user = cur.fetchone()

        if user:
            session["user_id"] = user[0]
            session["name"] = user[1]
            session["role"] = user[4]
            return redirect("/dashboard")
        else:
            return "Invalid credentials!"

    return render_template("login.html")

from flask import session, redirect, url_for

@app.route("/dashboard")
def dashboard():
    if "name" not in session:      
        return redirect(url_for("home"))

    selected_tip = random.choice(tips)
    return render_template("dashboard.html", name=session.get("name"), tip=selected_tip)

@app.route("/modules")
def modules():
    return render_template("modules.html")

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/certificate")
def certificate():
    return render_template("certificate.html")

@app.route("/report", methods=["GET","POST"])
def report():
    if request.method == "POST":
        issue = request.form["issue"]
        priority = request.form["priority"]
        message = request.form["message"]

        con = db()
        cur = con.cursor()
        cur.execute("INSERT INTO reports(user_id,issue,priority,message,status)                  VALUES(?,?,?,?,?)",(session["user_id"],issue,priority,message,"Pending"))

        con.commit()

        return "Report submitted successfully!"

    return render_template("report.html")

@app.route("/admin")
def admin():
    if session.get("role") == "admin":
        con = db()
        cur = con.cursor()
        cur.execute("SELECT reports.id, users.name, reports.issue, reports.status FROM reports JOIN users ON users.id=reports.user_id")
        data = cur.fetchall()
        return render_template("admin.html", reports=data)
    return "Access Denied!"
@app.route("/password_checker")
def password_checker():
    return render_template("password_checker.html")
@app.route("/phishing_detector")
def phishing_detector():
    return render_template("phishing_detector.html")
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")
@app.route("/posters")
def posters():
    return render_template("posters.html")
@app.route("/module/social_privacy")
def social_privacy():
    return render_template("module_social_privacy.html")
@app.route("/module/email_scams")
def email_scams():
    return render_template("module_email_scams.html")
@app.route("/module/gaming_safety")
def gaming_safety():
    return render_template("module_gaming_safety.html")
@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    message = None
    
    if request.method == "POST":
        email = request.form["email"]

        # Create reset link (can be real token later)
        reset_link = "http://127.0.0.1:5000/reset/" + email  

        msg = Message(
            "Password Reset Request - CyberShield",
            sender="yourgmail@gmail.com",
            recipients=[email]
        )
        msg.body = f"""Hello,

We received your password reset request.
Click below link to reset your password:

{reset_link}

If you didn’t request this, ignore the email.

Stay safe,
CyberShield Team
"""

        try:
            mail.send(msg)
            message = "Reset link sent to your email!"
        except:
            message = "Failed to send email — check SMTP settings."

    return render_template("forgot_password.html", message=message)
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
app.run(debug=True)


