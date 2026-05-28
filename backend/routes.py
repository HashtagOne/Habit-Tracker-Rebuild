from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Category, Habit, Completion
from datetime import date

routes_blueprint = Blueprint("routes", __name__)

@routes_blueprint.route("/categories", methods=["GET"])
@login_required
def get_categories():

    categories = Category.query.filter_by(user_id=current_user.id).all()
    return jsonify([category.to_dict() for category in categories]), 200

@routes_blueprint.route("/categories", methods=["POST"])
@login_required
def create_category():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("color"):
        return jsonify({"error": "Name and color are required."}), 400
    
    category = Category(
        name=data["name"],
        color=data["color"],
        user_id=current_user.id
    )
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201

@routes_blueprint.route("/categories/<int:id>", methods=["PUT"])
@login_required
def update_category(id):
    category = db.session.get(Category, id)

    if not category or category.user_id != current_user.id:
        return jsonify({"error": "Category not found."}), 404
    
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Name is required."}), 400
    
    category.name = data["name"]
    db.session.commit()
    return jsonify(category.to_dict()), 200

@routes_blueprint.route("/categories/<int:id>", methods=["DELETE"])
@login_required
def delete_category(id):
    category = db.session.get(Category, id)

    if not category or category.user_id != current_user.id:
        return jsonify({"error": "Category not found."}), 404
    
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted."}), 200

@routes_blueprint.route("/habits", methods=["POST"])
@login_required
def create_habit():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("category_id"):
        return jsonify({"error": "Name and category_id are required."}), 400
    
    category = db.session.get(Category, data["category_id"])
    if not category or category.user_id != current_user.id:
        return jsonify({"error": "Category not found."}), 404
    
    habit = Habit(
        name=data["name"],
        category_id=data["category_id"]
    )
    db.session.add(habit)
    db.session.commit()
    return jsonify(habit.to_dict()), 201

@routes_blueprint.route("/habits/<int:id>", methods=["PUT"])
@login_required
def update_habit(id):
    habit = db.session.get(Habit, id)

    if not habit or habit.category.user_id != current_user.id:
        return jsonify({"error": "Habit not found."}), 404
    
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Name is required."}), 400
    
    habit.name= data["name"]
    db.session.commit()
    return jsonify(habit.to_dict()), 200

@routes_blueprint.route("/habits/<int:id>", methods=["DELETE"])
@login_required
def delete_habit(id):
    habit = db.session.get(Habit, id)

    if not habit or habit.category.user_id != current_user.id:
        return jsonify({"error": "Habit not found."}), 404
    
    db.session.delete(habit)
    db.session.commit()
    return jsonify({"message": "Habit deleted."}), 200

@routes_blueprint.route("/completions", methods=["POST"])
@login_required
def create_completion():
    data= request.get_json()

    if not data or not data.get("habit_id"):
        return jsonify({"error": "habit_id is required."}), 400
    
    habit = db.session.get(Habit, data["habit_id"])

    if not habit or habit.category.user_id != current_user.id:
        return jsonify({"error": "Habit not found."}), 404
    
    today = date.today()

    existing = Completion.query.filter_by(
        habit_id=data["habit_id"],
        date=today
    ).first()

    if existing:
        return jsonify({"error": "Already completed today."}), 409
    
    completion = Completion(
        habit_id=data["habit_id"],
        date=today
    )
    db.session.add(completion)
    db.session.commit()
    return jsonify({"id": completion.id, "date": completion.date.isoformat()}), 201

@routes_blueprint.route("/completions/<int:id>", methods=["DELETE"])
@login_required
def delete_completion(id):
    completion = db.session.get(Completion, id)

    if not completion or completion.habit.category.user_id != current_user.id:
        return jsonify({"error": "Completion not found."}), 404
    db.session.delete(completion)
    db.session.commit()
    return jsonify({"message": "Completion deleted."}), 200