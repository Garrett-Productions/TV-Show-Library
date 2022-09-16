from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash
import re 
db = "python_exam"

class Show:
    def __init__( self, db_data ):
        self.id = db_data['id']
        self.user_id = db_data['user_id']
        self.creator = None
        self.title = db_data['title']
        self.network = db_data['network']
        self.release_date = db_data['release_date']
        self.description = db_data['description']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']


    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title']) < 3:
            flash ("Title be 3 characters or longer", "show")
            is_valid=False
        if len(show['network']) < 3:
            flash ("Must include a network", "show")
            is_valid=False
        if len(show['description']) < 3:
            flash ("Please Describe the show.", "show")
            is_valid=False
        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO shows (user_id, title, network, release_date, description) VALUES (%(user_id)s, %(title)s, %(network)s, %(release_date)s, %(description)s);"
        return connectToMySQL(db).query_db(query,data)


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM shows JOIN users on shows.user_id WHERE user_id = users.id;"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows JOIN users on shows.user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        show_list =[]
        for one_show in results:
            each_show = cls(one_show)
            user_data = {
                "id": one_show['users.id'],
                "first_name" : one_show['first_name'],
                "last_name" : one_show['last_name'],
                "email" : one_show['email'],
                "password" : one_show['password'],
                "created_at" : one_show['users.created_at'],
                "updated_at" : one_show['users.updated_at']
            }
            each_show.creator = user.User(user_data)
            show_list.append(each_show)
        return show_list

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM shows JOIN users on shows.user_id = users.id WHERE shows.id = %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        user_data = {
                "id": results[0]['users.id'],
                "first_name" : results[0]['first_name'],
                "last_name" : results[0]['last_name'],
                "email" : results[0]['email'],
                "password" : results[0]['password'],
                "created_at" : results[0]['users.created_at'],
                "updated_at" : results[0]['users.updated_at']
            }
        one_show = cls(results[0])
        one_show.creator = user.User(user_data)
        return one_show


    @classmethod
    def update(cls,data):
        query = "UPDATE shows SET user_id=%(user_id)s, title=%(title)s, network=%(network)s, release_date=%(release_date)s, description=%(description)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)


    @classmethod
    def delete_show(cls,data):
        query = "DELETE FROM shows WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)