# NEW CODE
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime


with open('config.json', 'r') as c:
    params = json.load(c)["params"]
local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/hotel_mdn'

if (local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)


class Contact(db.Model):
    '''
    sno, name, email,phone_num, mes, date,
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    mes = db.Column(db.String(120), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12), nullable=True)


class Booking(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    mes = db.Column(db.String(120), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    transport=db.Column(db.String(120), nullable=False)
    rooms=db.Column(db.String(50), nullable=False)



class Post(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    tagline = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    img_file = db.Column(db.String(12), nullable=False)
    date = db.Column(db.String(12), nullable=True)


@app.route("/")
def home():
    posts = Post.query.filter_by().all()[0:params['number_of_post']]
    return render_template('index.html', params=params, posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', params=params)


@app.route("/dashboard")
def dashboard():
    if ('user' in session and session['user'] == params['admin_user']):
        post = Post.querry.all()
        return render_template('dashboard.html')

    if request.method == "POST":
        # REDIRECT TO ADMIN PANEL
        username = request.form.get('uname')
        userpass = request.form.get('pass')

        if (username == params['admin_user'] and userpass == params['admin_password']):
            session['user'] = username
            return render_template('dashboard.html', param=params)

    return render_template("login.html", params=params)


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contact(name=name, email=email, phone_num=phone,
                        mes=message, date=datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html', params=params)

@app.route("/booking", methods=['GET', 'POST'])
def booking():
    if (request.method == 'POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        rooms=request.form.get('rooms')
        transport=request.form.get('transport')
        entry = Booking(name=name, email=email, phone_num=phone,
                        mes=message, date=datetime.now() ,rooms=rooms,transport=transport)
        db.session.add(entry)
        db.session.commit()

    return render_template('booking.html', params=params)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Post.query.filter_by(slug=post_slug).first()

    return render_template('post.html', params=params, post=post)


app.run(debug=True)
