
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)

# Configurarea Mail Serverului (contul de Gmail al tău pentru trimiterea mesajelor)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('DEL_EMAIL')  # contul tău de Gmail
app.config['MAIL_PASSWORD'] = os.getenv('PASSWORD')   # App Password-ul pentru Gmail
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/despre")
def despre():
    return render_template("despre.html")

@app.route("/servicii")
def servicii():
    return render_template("servicii.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")



@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        nume = request.form["nume"]
        email = request.form["email"]
        telefon = request.form["phone"]
        mesaj = request.form["mesaj"]

        # ----------------------
        # 1. Trimite mesaj către CONSULTANT
        # ----------------------
        msg_to_consultant = Message(
            subject="Mesaj nou de pe site",
            sender=os.getenv('DEL_EMAIL'),                    # expeditorul real 
            recipients=[os.getenv('REC_EMAIL')]                # destinatar = consultantul
        )
        msg_to_consultant.body = f"""Ai primit un mesaj nou de la {nume}!

Date de contact:
- Email: {email}
- Telefon: {telefon}

Mesaj:
{mesaj}
"""
        msg_to_consultant.reply_to = email  # Răspunsul se va trimite utilizatorului 
        mail.send(msg_to_consultant)

        # ----------------------
        # 2. Trimite confirmare către utilizator
        # ----------------------
        msg_to_user = Message(
            subject="Mesajul tău a fost înregistrat!",
            sender=os.getenv('REC_EMAIL'),  # Expeditor = consultantul
            recipients=[email]              # Către utilizator
        )
        msg_to_user.body = f"""Salut {nume},

Îți mulțumim că ne-ai contactat! Am primit mesajul tău și consultantul nostru te va contacta în cel mai scurt timp.

O zi frumoasă în continuare!"""

        mail.send(msg_to_user)

        return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)


            

