import os
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from dotenv import load_dotenv
from models import db, User

load_dotenv()

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader 
def load_user(user_id):
    return db.session.get(User, int(user_id))

CORS(app, supports_credentials=True, origins=["https://hashtagone.github.io"])
from auth import auth_blueprint
from routes import routes_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(routes_blueprint)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)