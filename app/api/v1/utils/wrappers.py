import os, jwt
from functools import wraps
from flask import request, jsonify, make_response

from .utility_functions import parse_request, validate_request_data

def token_required(f):
    """
        Validate the user token supplied in the request
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # add code to check the request content type and that data is supplied
        if 'Authorization' not in request.headers or request.headers['Authorization'] == "":
            # Client seems unaware that Authorization is required.
            response_header = ["WWW-Authenticate", 'Bearer realm="NYIKES_RMS"']

            response = make_response() 
            response.status_code = 401
            response.headers.set(response_header[0], response_header[1])
            
            return response
        
        # check for correct content-type
        req_data = parse_request(request)
        if 'error' in req_data:
            response = make_response()
            response.status_code = req_data['status']
            response.headers.set('WWW-Authentication', req_data['error'])
            return response

        # extract token from Auth header
        token = parse_auth_header(request.headers['Authorization'])
        if 'headers' in token:
            return generate_error_response(token)
        
        # Add token to the request data
        req_data.update({"user_token":token})
        
        # Parse the token
        kwargs = parse_token(req_data)
        if 'headers' in kwargs:
            return generate_error_response(kwargs)
        else:
            return f(*args, **kwargs)

    return decorated

def parse_token(json_data):
    valid_req_data = validate_request_data([json_data], ['username', 'user_token'])
    if 'error' in valid_req_data:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="{}" '.format(valid_req_data['error'])
        }
        response = {'status' : 400}
        response.update({"headers": www_authenticate_info })
        return response
    
    token = valid_req_data['user_token']
            
    # Decode the user token
    try:
        decoded_token = jwt.decode(token, os.getenv('SECRET'))
    except Exception as e:
        # There's a problem with the token
        www_authenticate_info = {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_token"; '
                                    'error_description="{}" '.format(e)        
        }
        response = {'status':401}
        response.update({"headers":www_authenticate_info})
        return response
    
    # Verify that the username in decoded token matches
    # the username supplied with the token
    if valid_req_data['username'] != decoded_token['username']:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="Identity mismatch" '
        }
        response = {'status' : 400}
        response.update({"headers": www_authenticate_info })
        return response

    # pass the user token back to the view function
    user_token_info = {
        "username":decoded_token['username'],
        "user_token":decoded_token['user_token']
    }
    kwargs = {
        "access_token" : user_token_info
    }

    return kwargs

def parse_auth_header(auth_header):
    """
        Parses the auth header to check for token
        
        :param the request object

        :returns the jwt token
    """

    response = {}
    
    auth_data = auth_header.split()
    if len(auth_data) == 2 and auth_data[0] == 'Bearer':
        token = auth_data[1]
        return token
    else:
        www_authenticate_info = {
                "WWW-Authenticate" :'Bearer realm="NYIKES_RMS" '
        }
        response = {
            'status'    :   400,
            "headers"   :   www_authenticate_info
        }
        return  response

def generate_error_response(dict_response):
    """
        Generates an error reponse to be returned
        via the WWW-Authenticate header
    """
    err_response = make_response()
    err_response.status_code = dict_response['status']
    for k, v in dict_response['headers'].items():
        err_response.headers.set(k, v)

    return err_response
