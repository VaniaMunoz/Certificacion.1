from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.friendship import Friendship
from flask_app.models.user import User

@app.route("/friendships")
def friendships():
    friendships = Friendship.get_all()
    return render_template("friendships.html", all_friendships=friendships)

@app.route("/friendships/add")
def new_friendship_form():
    users = User.get_all()
    return render_template("new_friendship.html", all_users=users)

@app.route("/friendships/create", methods=["POST"])
def create_friendship():
    user_id = request.form["user_id"]
    friend_id = request.form["friend_id"]

    if Friendship.exists(user_id, friend_id):
        flash("Ya existe una amistad entre estos usuarios.", "error")
    else:
        Friendship.create(user_id, friend_id)

    return redirect("/friendships")

@app.route("/friendships/<int:friendship_id>/delete")
def delete_friendship(friendship_id):
    Friendship.delete(friendship_id)
    return redirect("/friendships")