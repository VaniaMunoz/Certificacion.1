from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Friendship:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id'] 
        self.friend_id = data['friend_id'] 
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None 
        self.friend = None 

    def get_user(self):
        if not self.user:
            self.user = User.get_by_id(self.user_id)
        return self.user


    def get_friend(self):
        if not self.friend:
            self.friend = User.get_by_id(self.friend_id)
        return self.friend

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM friendships"
        results = connectToMySQL('amistades').query_db(query)
        friendships = []
        for friendship in results:
            friendships.append(cls(friendship))
        return friendships
    @classmethod
    def exists(cls, user_id, friend_id):
        query = "SELECT id FROM friendships WHERE (user_id = %(user_id)s AND friend_id = %(friend_id)s) OR (user_id = %(friend_id)s AND friend_id = %(user_id)s);"
        data = {
            'user_id': user_id,
            'friend_id': friend_id
        }
        result = connectToMySQL('amistades').query_db(query, data)
        return bool(result)
    
    @classmethod
    def create(cls, user_id, friend_id):
        query = "INSERT INTO friendships (user_id, friend_id, created_at, updated_at) VALUES (%(user_id)s, %(friend_id)s, NOW(), NOW());"
        data = {
            'user_id': user_id,
            'friend_id': friend_id
        }
        new_friendship_id = connectToMySQL('amistades').query_db(query, data)
        return new_friendship_id
    
    @classmethod
    def delete(cls, friendship_id):
        query = "DELETE FROM friendships WHERE id = %(id)s;"
        data = {
            'id': friendship_id
        }
        result = connectToMySQL('amistades').query_db(query, data)
        return result