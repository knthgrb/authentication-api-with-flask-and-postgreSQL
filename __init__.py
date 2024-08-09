from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
db = SQLAlchemy()

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)


# Import models after initializing db
from .models import User
from .models import Fund

# Create database tables if it does not exist
with app.app_context():
    db.create_all()



