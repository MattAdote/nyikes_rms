import os, jwt
from functools import wraps
from flask import request, jsonify

from .utility_functions import parse_request, validate_request_data

def token_required(f):
    """
        Validate the user token supplied in the request
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # add code to check the request content type and that data is supplied
        req_data = parse_request(request)
        if 'error' in req_data:
            return jsonify(req_data), req_data['status']

        kwargs = parse_token(req_data)
        if 'error' in kwargs:
            return jsonify(kwargs), kwargs['status']
        else:
            return f(*args, **kwargs)

    return decorated

def parse_token(json_data):
    valid_req_data = validate_request_data([json_data], ['username', 'user_token'])
    if 'error' in valid_req_data:
        return valid_req_data
    
    token = valid_req_data['user_token']
            
    # Decode the user token
    try:
        decoded_token = jwt.decode(token, os.getenv('SECRET'))
    except Exception as e:
        response = {
            "status":403,
            "error": "Token error: {} ".format( e)
        }
        return response
    
    # Verify that the username in decoded token matches
    # the username supplied with the token
    if valid_req_data['username'] != decoded_token['username']:
        response = {
            "status" : 404,
            "error" : "Token error: Identity mismatch"
        }
        return response

    # we pass the user token back to the view function
    user_token_info = {
        "username":decoded_token['username'],
        "user_token":decoded_token['user_token']
    }
    kwargs = {
        "access_token" : user_token_info
    }

    return kwargs
