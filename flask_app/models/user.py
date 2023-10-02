from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

DB = "certificaciones"

class User:
    db = "certificaciones"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        return connectToMySQL('certificaciones').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('certificaciones').query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('certificaciones').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('certificaciones').query_db(query,data)
        return cls(results[0])

    @classmethod
    def authenticated_user_by_input(cls, user_input):
        
        valid = True
        existing_user = cls.get_by_email(user_input["email"])

        password_valid = True

        if not existing_user:
            valid = False
            
        else:
            data = {
                "email": user_input["email"]
            }
            query = "SELECT password FROM users WHERE email = %(email)s;"
            hashed_pw = connectToMySQL(DB).query_db(query,data)[0]["password"]

            password_valid = bcrypt.check_password_hash(
            hashed_pw, user_input['password'])
        
            if not password_valid:
                valid = False

        if not valid:
            flash("La combinación de Email y contraseña no coincide con nuestros registros..", "login")
            return False

        return existing_user

    
    @classmethod
    def create_valid_user(cls, user):

        if not cls.is_valid(user):
            return False

        pw_hash = bcrypt.generate_password_hash(user['password'])
        user = user.copy()
        user["password"] = pw_hash
        print("User after adding pw: ", user)

        query = """
                INSERT into users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""

        new_user_id = connectToMySQL(DB).query_db(query, user)
        new_user = cls.get_by_id(new_user_id)

        return new_user


    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash("Email ya ocupado.","regístrate")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("¡¡Email NO Es Valido!!","regístrate")
            is_valid=False
        if len(user['first_name']) < 3:
            flash("El apellido debe tener al menos 3 caracteres", "regístrese")
            is_valid= False
        if len(user['last_name']) < 3:
            flash("El apellido debe tener al menos 3 caracteres", "regístrese")
            is_valid= False
        if len(user['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres", "register")
            is_valid= False
        if user['password'] != user['confirm']:
            flash("Las contraseñas no coinciden", "regístrate")
        return is_valid