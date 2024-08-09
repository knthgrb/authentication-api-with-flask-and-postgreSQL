from flask import request, make_response
from functools import wraps

from ..utils.jwt import decode_jwt

def requires_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return make_response({"error": "Authentication required"}), 401
        
        user_id = decode_jwt(token)
        if user_id is None:
            return make_response({"error": "Invalid or expired token"}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function
