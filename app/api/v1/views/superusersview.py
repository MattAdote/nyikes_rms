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
