
import bcrypt
from flask import request, make_response
from .middlewares import requires_auth
from .utils import generate_jwt, decode_jwt
from . import app, db
from .models import User

@app.route("/api/user", methods=["GET"])
def get_user():
    try:
        token = request.cookies.get("token")
        user_id = decode_jwt(token)
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return {"error": "No user found"}, 404
        
        user_data = {"first_name": user.first_name, "last_name": user.last_name, "email": user.email}
        
        response = make_response({"user": user_data}, 200)
        
        return response
    
    except Exception as err:
        return {"error": err}, 500

@app.route("/api/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
    
        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        password = data["password"]
        
        if not all ([first_name, last_name, email, password]):
            return {"error": "Missing required fields"}, 400
        
        if User.query.filter_by(email=email).first():
            return {"error": "User with this email already exists"}, 400
        
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        
        user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully"}, 201
    except Exception as err:
        db.session.rollback()
        return {"error": err}, 500
    

@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
    
        email = data["email"]
        password = data["password"]
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return {"error": "User with this email was not found"}, 404
        
        if user and bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            token = generate_jwt(user.id)
            
            user_data = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email
            }
            
            response = make_response({"user": user_data, "token": token}, 200)
            response.set_cookie("token", token, httponly=True, secure=True, max_age=86400)
            return response, 200
        else:
            return {"error": "Invalid credentials"}, 401
    
    except Exception as err:
        return {"error": err}, 500
    
@app.route("/api/logout", methods=["POST"])
@requires_auth
def logout():
    try:
        response = make_response({"message": "Logged out successfully"})
        response.set_cookie('token', '', expires=0, httponly=True, secure=True)
        return response, 200
    except Exception as err:
        return {"error": err}, 500
    
    


