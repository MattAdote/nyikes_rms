import  datetime, time, \
        jwt, \
        requests

from werkzeug.security import generate_password_hash, check_password_hash

# project specific imports
from flask import   Blueprint, request, jsonify, make_response, \
                    current_app as app

# local imports
from app.api.v1.utils import    parse_request, validate_request_data, \
                                check_is_empty, endpoint_error_response, \
                                token_required, generate_authorization_error_response
from app.api.v1.models import SuperUser, superuser_schema, superusers_schema


DATE_FORMAT = "{:%Y-%b-%d %H:%M:%S}"
TOKEN_EXPIRATION_MINUTES = 180

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

    # Hash the superuser's password
    superuser_record['password'] = generate_password_hash(superuser_record['password'], method='sha256')
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
@token_required
def superuser(**kwargs):
    """ The superuser view for the API Server"""
    
    if len(kwargs) != 1:
        response = { 
            "status":400,
            "error" : "args greater than 1. Supplied: {} ".format(kwargs.items())
        }
        return make_response(jsonify(response), response['status'])
    
    user_token_payload = validate_token(kwargs['access_token'])
    if 'headers' in user_token_payload:
        return generate_authorization_error_response(user_token_payload)

    # get the superusers from db
    superusers = SuperUser.query.all()
    su_records = superusers_schema.dump(superusers).data

    # remove the password attr as not expected in output
    for record in su_records:
        record.pop('password')

    response = {
        'status': 200,
        'data': su_records
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
    # data = {
    #             "username": "test_user", required
    #             "password": "123", required
    #         }   
    
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
        # 3. Start a new session and get session_key
        session_secret_key = start_session(su)
        if type(session_secret_key) == dict and 'error' in session_secret_key:
            return make_response(jsonify(session_secret_key), session_secret_key['status'])
        # 4.1 Generate user token
        user_token = generate_token(su, session_secret_key)
        #4.2 Generate server token
        token = jwt.encode(
            {
                "username":su.username,
                "user_token":user_token.decode('UTF-8'), # this is signed by user's dynamic secret key
                "super":"True",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
            },
            app.config['SECRET']
        )

        # 5. Return 
        su_record = superuser_schema.dump(su).data
        su_record.pop('password') # remove password attr as not expected in endpoint output
        su_record.update({
            "access_token": token.decode('UTF-8'), # append user's access token
            "token_type":"Bearer",
            "expires_in":TOKEN_EXPIRATION_MINUTES
        }) 
        response = {
            'status': 200,
            'data': su_record,
        }
        
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
    su = SuperUser.query.filter_by(username=dict_credentials['username']).first()
    if su:
        if check_password_hash(su.password, dict_credentials['password']):
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

def start_session(obj_superuser):
    """
        Starts a new session for the given superuser
        
        Returns string output which is the secret key to sign
        the token to be generated
    """
    # First check if there're pre-existing sessions and log them out
    if obj_superuser.lastLoggedIn > obj_superuser.lastLoggedOut:
        response = end_session(obj_superuser)
        time.sleep(0.6) # put some delay after last log out
        if type(response) == dict and 'error' in response:
            return response

    # Next, update the user's log in time and return lastLoggedOut time as string.
    # The lastLoggedOut is the user's secret key used to sign their token
    try:
        obj_superuser.lastLoggedIn = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")
        obj_superuser.save()
    except:
        response = {
            "status":503,
            "error": "Unable to save to db."
        }
        return response
    return "{:%Y-%b-%d %H:%M:%S}".format(obj_superuser.lastLoggedOut)

def end_session(obj_superuser):
    """
        Ends a session for the given superuser
    """
    try:
        obj_superuser.lastLoggedOut = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")
        obj_superuser.save()
    except:
        response = {
            "status":503,
            "error": "Unable to save to db."
        }
        return response
    return True

def generate_token(obj_superuser, secret_key):
    """
        Generates a jwt token specific to a user

        :param obj_superuser, \n
        :param secret_key \n
        
        :returns jwt encoded token
    """

    token = jwt.encode(
        {
            "id": obj_superuser.id,
            "username":obj_superuser.username,
            "type":"super",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_MINUTES)
        },
        secret_key
    )

    return token

def validate_token(access_token_payload):
    """
        Validates the user's token contained in the access token

        :returns the decoded token's payload
    """
    err_response = {}
    
    # Check that supplied input is ok
    err_response = parse_access_token_payload(access_token_payload)
    if 'headers' in err_response:
        return err_response

    # Get user from db
    obj_superuser = SuperUser.query.filter_by(username=access_token_payload['username']).first()
    user_secret = DATE_FORMAT.format(obj_superuser.lastLoggedOut)
    
    # Decode user's token
    try:
        token_payload = jwt.decode(access_token_payload['user_token'], user_secret)
    except Exception as e:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_token"; '
                                    'error_description="{}" '.format(e)
        }
        err_response = {
            "status" : 401,
            "headers": www_authenticate_info
        }
        
        return err_response
    return token_payload

def parse_access_token_payload(access_token_payload):
    """
        Checks the access token for missing or empty values

        :param access_token_payload

        :returns Error on missing or empty values othereise
        returns the access_token_payload
    """
    err_response = {}
    if 'username' not in access_token_payload:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="username missing in access_token payload" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response
    elif access_token_payload['username'] == "" or access_token_payload['username'] == None:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="username missing a value in access_token payload" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response
    elif 'user_token' not in access_token_payload:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="user_token missing in access_token payload" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response
    elif access_token_payload['user_token'] == "" or access_token_payload['user_token'] == None:
        www_authenticate_info =  {
            "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="user_token missing a value in access_token payload" '
        }
        err_response = {
            "status" : 400,
            "headers": www_authenticate_info
        }
        return err_response
    else:
        return access_token_payload
