from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt


# Decorator to check user have a valid JWT token
def auth_required(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        verify_jwt_in_request()
        return func(*args, **kwargs)
    return wrapper_func

# Decorator to check user have a valid JWT token and is an admin
def admin_auth_required(func):
    @wraps(func)
    def wrapper_func(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return {"status": "error",'message': 'Admin access required'}, 403
        return func(*args, **kwargs)
    return wrapper_func
