from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.item_model import Item
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/handleRegistration', methods=['POST'])
def handleRegistration():
    is_valid=True
    if not User.validate_registration_form(request.form):
        is_valid = False
    if is_valid == False:
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        'fname':request.form['fname'],
        'lname':request.form['lname'],
        'email':request.form['email'],
        'password':pw_hash  #request.form['password']
    }
    user_id = User.insert(data)
    session['user_id'] = user_id
    session["fname"] = request.form["fname"]
    return redirect('/dashboard')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': session['user_id']
    }
    result = User.get_user_by_id(data)
    all_items = Item.get_all_items_and_users()
    return render_template('dashboard.html', user=result, all_items=all_items)

@app.route('/handleLogin', methods=['POST'])
def handleLogin():
    is_valid=True
    # grab the user info in the db by the email addy
    print(request.form['email'])
    data = {
        'email':request.form['email'] 
    }
    user_info = User.get_user_by_email(data)
    if not user_info:
        flash('invalid user', 'log')
        return redirect('/')
    
    # verify the passwords hashes match
    if not bcrypt.check_password_hash(user_info[0]['password'], request.form['password']):
        flash('invalid password', 'log')
        return redirect('/')
    # if they match, save user in session
    session['user_id'] = user_info[0]['id']
    session["fname"] = user_info[0]['fname']
    session["lname"] = user_info[0]['lname']
    #else print an error 
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/my_items')
def get_user_items():
    if "user_id" not in session:
        return redirect("/")

    data = {
        "id": session['user_id'] 
    }
    result = User.get_items_by_user(data)
    if len(result) == 0:
        return []

    print(f"items: {result[0]}")
    name = session["fname"]
    return render_template("my_items.html", items=result, name=name)