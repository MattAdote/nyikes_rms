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
        auth_data = {}

        # check that Authorization header is present and has a value
        if 'Authorization' not in request.headers or request.headers['Authorization'] == "":
            # Client seems unaware that Authorization is required.
            response_header = ["WWW-Authenticate", 'Bearer realm="NYIKES_RMS"']

            response = make_response() 
            response.status_code = 401
            response.headers.set(response_header[0], response_header[1])
            
            return response
        
        # check that the rms custom header is present and has a value
        if 'X-NYIKES-RMS-User' not in request.headers or request.headers['X-NYIKES-RMS-User'] == "":
            # Client seems unaware that they should supply the username of the authenticated user
            response_header = ["WWW-Authenticate",  'Bearer realm="NYIKES_RMS"'
                                                    'error="invalid_request"; '
                                                    'error_description="Header: \"X-NYIKES-RMS-User\" missing or null" '
            ]
            
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
            return generate_authorization_error_response(token)
        auth_data.update({"access_token":token})
        
        # extract username from Nyikes-RMS_User header
        hdr_username = request.headers['X-NYIKES-RMS-User']
        auth_data.update({"hdr_username":hdr_username})
        
        # Parse the token
        token_payload = parse_token(auth_data)
        if 'headers' in token_payload:
            return generate_authorization_error_response(token_payload)
        else:
            kwargs.update(token_payload)
            return f(*args, **kwargs)

    return decorated

def parse_token(json_data):
    # Decode the supplied access token
    try:
        decoded_access_token = jwt.decode(json_data['access_token'], os.getenv('SECRET'))
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
    # the username supplied in the header
    if json_data['hdr_username'] != decoded_access_token['username']:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="Identity mismatch" '
        }
        response = {'status' : 400}
        response.update({"headers": www_authenticate_info })
        return response

    # pass the decoded token back to the view function
    kwargs = {
        "access_token" : decoded_access_token
    }

    return kwargs

def parse_auth_header(auth_header):
    """
        Parses the auth header to check for token
        
        :param the Authorization header

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

def generate_authorization_error_response(dict_response):
    """
        Generates an error reponse to be returned
        via the WWW-Authenticate header
    """
    err_response = make_response()
    err_response.status_code = dict_response['status']
    for k, v in dict_response['headers'].items():
        err_response.headers.set(k, v)

    return err_response
