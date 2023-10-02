from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],

    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/users')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if not user:
        flash("¡¡Email NO Es Valido!!","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("La Contraseña NO Valida","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    
    return render_template("dashboard.html",user=User)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route("/users")
def users():
    users = User.get_all()
    return render_template("users.html", all_users=users)

@app.route("/users/new")
def new_user_form():
    return render_template("new_user.html")

@app.route("/users/create", methods=["POST"])
def create_user():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"]
    }
    User.save(data)
    return redirect("/friendships")

@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = User.get_by_id(user_id)
    return render_template("show_user.html", user=user)

@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    User.delete(user_id)
    return redirect("/users")
