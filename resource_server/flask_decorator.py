from flask import request, jsonify
from jwt import decode, PyJWKClient
from jwt.exceptions import ExpiredSignatureError, InvalidAudienceError, DecodeError
from jwt_validator import JwtValidator

def bearer_jwt_required(jwt_validator: JwtValidator):
    
    def decorator(function):
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                return jsonify({"error": "Authorization header missing"}), 401

            parts = auth_header.split()
            if len(parts) != 2 or parts[0] != 'Bearer':
                return jsonify({"error": "Invalid token type"}), 401

            access_token = parts[1]
            try:
                jwt_validator.is_token_valid(access_token)
            except ExpiredSignatureError:
                return jsonify({"error": "Token has expired"}), 401
            except InvalidAudienceError:
                return jsonify({"error": "Invalid audience"}), 401
            except DecodeError:
                return jsonify({"error": "Token is invalid"}), 401
            return function(*args, **kwargs)
        wrapper.__name__ = function.__name__
        return wrapper
    return decorator
