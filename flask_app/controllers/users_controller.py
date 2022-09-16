from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from datetime import datetime
realdate = '%d-%m-%Y'

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/shows')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("invalid Password", "login")
        return redirect ('/')
    session['user_id'] = user.id
    return redirect('/shows')


@app.route('/shows')
def shows():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template("shows.html", user=User.get_by_id(data),  all_shows = Show.get_all(), dtformat=realdate) 


@app.route('/shows/new')
def new_show():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    return render_template("add_show.html", user=User.get_by_id(data))


@app.route('/create_show', methods = ['POST'])
def create_show():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect('/shows/new')
    data = {
        "user_id": session['user_id'],
        "title":request.form['title'],
        "network":request.form['network'], 
        "release_date":request.form['release_date'], 
        "description":request.form['description']
    }
    Show.save(data)
    return redirect("/shows")


@app.route('/shows/<int:id>')
def show_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session['user_id']
    }
    show_data = {
        "id": id,
    }
    this_show = Show.get_by_id(show_data)
    print(this_show.creator)
    return render_template("display_show.html", user=User.get_by_id(data), one_show = this_show)


@app.route('/update_show/<int:id>', methods=['POST'])
def update_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Show.validate_show(request.form):
        return redirect(f'/shows/edit/{id}')
    data = {
        "id": session['user_id']
    }
    show_data = {
        "id": id,
        "user_id": session['user_id'],
        "title":request.form['title'],
        "network":request.form['network'], 
        "release_date":request.form['release_date'], 
        "description":request.form['description'],
    }
    Show.update(show_data)
    return redirect('/shows')


@app.route('/shows/edit/<int:id>')
def edit_show(id):
    if 'user_id' not in session:
        return redirect('/logout') #i need to fix these validations and edit my stuff and dsubmit the assignemnt 
    data = {
        "id": session['user_id']
    }
    show_data = {
        "id": id
    }
    return render_template("edit_show.html", user=User.get_by_id(data), one_show= Show.get_by_id(show_data))


@app.route ('/delete_show/<int:id>')
def delete_show(id):
    data = {
        'id': id
    }
    Show.delete_show(data)
    return redirect('/shows')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')