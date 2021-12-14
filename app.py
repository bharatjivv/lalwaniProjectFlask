from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail
import json


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail_user'],
    MAIL_PASSWORD = params['gmail_password']
)
mail = Mail(app)

if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)


# sno, name, phone_num, msg, date, email
class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(50), nullable=False)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/projects")
def projects():
    return render_template('projects.html')

@app.route("/govt")
def govt():
    return render_template('projects_govt.html')

@app.route("/projects_hospitals")
def projects_hospitals():
    return render_template('projects_hospitals.html')

@app.route("/projects_hotels")
def projects_hotels():
    return render_template('projects_hotels.html')

@app.route("/projects_resorts")
def projects_resorts():
    return render_template('projects_resorts.html')

@app.route("/projects_residence")
def projects_residence():
    return render_template('projects_residence.html')

@app.route("/projects_commercial")
def projects_commercial():
    return render_template('projects_commercial.html')

@app.route("/projects_interior")
def projects_interior():
    return render_template('projects_interior.html')

@app.route("/associates")
def associates():
    return render_template('associates.html')

@app.route("/studio")
def studio():
    return render_template('studio.html')

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = Contacts(name=name, email= email, subject=subject, date = datetime.now(), msg= message)
        db.session.add(entry)
        db.session.commit()
        mail.send_message('Client ' + name + ' Requested To Contact! ',
                          sender=email,
                          recipients = [params['gmail_user']],
                          body = "Subject - " + subject + "\n" + "Message - " + message
                          )

    return render_template('contact.html')

# sno, name, phone_num, msg, date, email
if __name__=="__main__":
    app.run(debug=True)
