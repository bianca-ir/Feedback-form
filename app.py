from flask import Flask, render_template, request 
from flask_sqlalchemy import SQLAlchemy 
from send_mail import send_mail


# Initialization 
app = Flask(__name__) 

# We will have 2 databases: development and production. 
ENV = 'prod' 

if ENV == 'dev': 
    app.debug = True 
    # developer database for local deployment 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:katze99@localhost/cafehouse' 
else: 
    app.debug = False 
    # production database for global deployment 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nbtovjoyfcxvnl:f11b0f7b8150432c164ff8209fd53f5a670aeee303972b68523f7f9690db1449@ec2-54-158-247-210.compute-1.amazonaws.com:5432/de8ifsfpekpkqb' 

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