from werkzeug.utils import validate_arguments
from flask_app.models.user import User
from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Login

@app.route("/")
def index():

    return render_template("index.html")


#Register



@app.route("/register", methods=['POST'])
def register():

#Validate user
    if not User.validate_register(request.form):
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    
    user_id = User.register_user(data)


    session['user_id'] = user_id
    return redirect("/dashboard")


#Login route


@app.route("/login", methods=["POST"])
def login():

    data = {
        "email": request.form["email"]
    }
    
    user_in_db = User.get_by_email(data)

    validation_data = {
        "user" : user_in_db,
        "password" : request.form['password']
    }
    
    if not User.validate_login(validation_data):
        return redirect("/")

    
    session['user_id'] = user_in_db.id
    
    return redirect("/dashboard")


#Dashboard


@app.route("/dashboard")
def dashboard():
    user_id = session['user_id']

    data = {
        "user_id" : session['user_id']
    }

    user = User.get_user_info(data)
    
    return render_template("dashboard.html", user = user)



#Logout

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")