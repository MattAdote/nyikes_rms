import requests

# project specific imports
from flask import Blueprint, request, jsonify, make_response

# local imports
from app.api.v1.utils import validate_request_data, parse_request, check_is_empty, endpoint_error_response
from app.api.v1.models import SuperUser, superuser_schema

# Define blueprint for meetup view
superusers_view_blueprint = Blueprint('superusers_view', '__name__')

@superusers_view_blueprint.route('/superusers', methods=['POST'])
def create_superuser():
    """ This creates a new superuser record"""
    response = {}
    data = {}

    # Parse the request data to check content_type is correct
    data = parse_request(request)
    if type(data) == dict and 'error' in data:
        return make_response(jsonify(data), data['status'])

    # check validity of request data
    res_valid_data = superuser_validate_request_data(data)

    # process data if valid, else, return validation findings
    if data == res_valid_data:
        # send to storage
        response = save(res_valid_data)
    else:
        # return error from validation findings
        response = endpoint_error_response(data, res_valid_data)

    return make_response(jsonify(response), response['status'])

def save(superuser_record):
    """Sends the superuser to be added to storage."""

    # Save the new item
    superuser = SuperUser(superuser_record['username'], superuser_record['password'])
    superuser.save()
    # Get the newly saved item
    new_superuser_record = superuser_schema.dump(superuser).data
    # Confirm that the new item matches the input that was supplied
    if all(item in new_superuser_record.items() for item in superuser_record.items()):
        return {
            "status": 201,
            "data": new_superuser_record
        }
    else:
        return {
            "status": 503,
            "error": 'An error occurred while saving the record.'
        }

def superuser_validate_request_data(req_data):
    """Validates the superuser data received"""
    # data = {
    #             "username": "test_user", required
    #             "password": "123", required
    #         }   
    #
    # parse the recevied data to check for empty or none
    received_data = check_is_empty(req_data)

    # exit if indeed data is empty
    if 'error' in received_data:
        return received_data    
    # Specify the required fields
    req_fields = ['username', 'password']
    # Initialize list to hold processed fields
    sanitized_data = []

    dict_req_fields = {}
    # get the required fields' data and put in own dictionary
    for field in req_fields:
        if field in received_data:
            dict_req_fields.update({field: received_data[field]})
    # append required fields dictionary to sanitized_data list
    sanitized_data.append(dict_req_fields)

    # send sanitized_data list to actual validation function and return response
    return validate_request_data(sanitized_data, req_fields)


@superusers_view_blueprint.route('/superusers', methods=['GET'])
def superuser():
    """ The superuser view for the API Server"""
    
    response = {
        'status': 200,
        'data': []
    }

    return make_response(jsonify(response), response['status'])

# Commented out the below. This is to be the redirect url called by facebook
# @superusers_view_blueprint.route('/superusers/login/account_kit', methods=['POST'])
# def login_superuser_account_kit():
#     """ Logs in a superuser via Facebook Account Kit """
#     data = parse_request(request)
#     if type(data) == dict and 'error' in data:
#         return make_response(jsonify(data), data['status']) 

#     if request:
#         print('Called my guys')

#         # required fields
#         app_id = '602045066941772'
#         redirect = 'https://nyikes-rms-stage.herokuapp.com/api/v1/superusers/login/account_kit'
#         state = 'this-is-meant-to-be-some-long-random-csrf-token-that-i-need-to-randomify'
#         # optional fields    
#         debug = True
#         locale = 'en_GB'
        
#         fb_data = {
#                 "app_id" : app_id,
#                 "redirect" : redirect,
#                 "state" : state,
#                 "debug":debug,
#                 "locale" : locale
#         }
#         if 'phone_number' in data:
#             facebook_api_url = "https://www.accountkit.com/v1.1/basic/dialog/sms_login/"
#             country_code = '254'
#             phone_number = data['phone_number']

#             fb_data.update({
#                 "country_code" : country_code,
#                 "phone_number": phone_number
#             })
#             requests.post(facebook_api_url, data=fb_data)
#         elif 'email' in data:
#             facebook_api_url = "https://www.accountkit.com/v1.0/basic/dialog/email_login/"
#             fb_data.update({
#                 "email" : data['email']
#             })
#             requests.post(facebook_api_url, data=fb_data)

@superusers_view_blueprint.route('/superusers/login', methods=['POST'])
def login_superuser():
    """ Logs in a superuser """
    
    # the flow:
    # 1. validate the received data
    # if not valid return error message
    # 2. verify supplied credentials
    # if verification fails, return error message
    # 3. start a new session
    # - first check if there's existing session and end it
    # - start new session
    # - produce the signing key for the new session
    # 4. Generate a token and sign it with the new session's
    # signing key (output of step 3 above)
    # 5. Return:
    # - id and username in json body
    # - token in header with the following payload:
    #    - id : superuser_id
    #    - type : super
    #    - iat : datetime
    #    - exp : datetime within 6 hours

    # 1. Validate received data
    # check request content type
    data = parse_request(request)
    if type(data) == dict and 'error' in data:
        return make_response(jsonify(data), data['status'])    
    # check validity of request data
    request_data = []
    req_fields = ['username', 'password']
    request_data.append(data)
    res_valid_data = validate_request_data(request_data, req_fields)
    
    # process data if valid, else, return validation findings
    if data == res_valid_data:
        # 2. Verify supplied credentials
        su = verify_credentials(data)
        if type(su) == dict and 'error' in su:
            return make_response(jsonify(su), su['status'])
        # su = SuperUser.query.filter_by(username=data['username'], password=data['password']).first()
        # if su:
        #     su_record = superuser_schema.dump(su).data
        #     # remove password attr as not expected in endpoint output
        #     su_record.pop('password')
        #     response = {
        #         'status': 200,
        #         'data': su_record
        #     }
        # else:
        #     response = {
        #         'status': 403,
        #         'error': 'Invalid credentials supplied'
        #     }
    else:
        # return error from validation findings
        response = endpoint_error_response(data, res_valid_data)

    return make_response(jsonify(response), response['status'])
    

def verify_credentials(dict_credentials):
    """
        Takes a dict of username and password for verification

        Returns Superuser object if verification successful
        else, returns an error message
    """
    response = {}
    su_username = SuperUser.query.filter_by(username=dict_credentials['username']).first()
    if su_username:
        su = SuperUser.query.filter_by(
                username=dict_credentials['username'],
                password=dict_credentials['password'],
            ).first()
        if su:
            return su
        else:
            response = {
                'status': 403,
                'error': 'Incorrect Password!'
            }
    else:
        response = {
            'status': 403,
            'error': 'Username: {} not found'.format(dict_credentials['username'])
        }
    return response
