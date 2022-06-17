from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import *
from send_mail import send_mail
import os
import re


# Initialization 
app = Flask(__name__) 

# We will have 2 databases: development and production. 
ENV = 'prod' 



if ENV == 'dev': 
    app.debug = True 
    # developer database for local deployment 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:katze99@localhost/cafehouse' 
else: 
    app.debug = False 
    # production database for global deployment 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gpayohujzputac:daba9fabb17ad3fe2bdc1eab3f465a2045e401a80bc106aaa5e85fbe287ad818@ec2-52-200-215-149.compute-1.amazonaws.com:5432/deg5150ef4hao9' 
    DATABASE_URL = os.environ.get("DATABASE_URL").replace("postgres", "postgresql")


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app) # database object 

class FeedbackForm(db.Model): 
    __tablename__ = 'feedback' 
    id = db.Column(db.Integer, primary_key=True) 
    customer = db.Column(db.String(200), unique=True) 
    location = db.Column(db.String(200))
    rating = db.Column(db.Integer) 
    comments = db.Column(db.Text())

    def __init__(self, customer, location, rating, comments): 
        self.customer = customer 
        self.location = location 
        self.rating = rating 
        self.comments = comments



@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit(): 
    if request.method == 'POST': 
        customer = request.form['customer']
        location = request.form['location']
        rating = request.form['rating']
        comments = request.form['comments']
     #   print(customer, location, rating, comments) 
        if customer == '' or location == '': 
            return render_template('index.html', message='Please enter required information')
        
        if db.session.query(FeedbackForm).filter(FeedbackForm.customer == customer).count() == 0: 
            data = FeedbackForm(customer, location, rating, comments) 
            db.session.add(data) 
            db.session.commit() 
            send_mail(customer, location, rating, comments) 
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback!')

if __name__ == '__main__': 
 #    app.debug = True 
    app.run() 