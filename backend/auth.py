import bcrypt
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from models import db, User

auth_blueprint = Blueprint("auth", __name__)

@auth_blueprint.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"error": "Username already taken."}), 409
    

    hashed = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

    user = User(
        username=data["username"],
        password=hashed.decode("utf-8")
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Account created successfully."}), 201

@auth_blueprint.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password are required."}), 400
    
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not bcrypt.checkpw(
        data["password"].encode("utf-8"),
        user.password.encode("utf-8")
    ):
        return jsonify({"error": "Invalid username or password."}), 401
    
    login_user(user)
    return jsonify({"message": "Logged in.", "username": user.username}), 200

@auth_blueprint.route("/auth/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out."}), 200