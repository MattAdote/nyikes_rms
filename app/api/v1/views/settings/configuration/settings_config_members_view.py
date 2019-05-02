# project specific imports
from flask import   Blueprint, request, jsonify, make_response

# local imports
from app.api.v1.utils import    parse_request, validate_request_data, \
                                check_is_empty, endpoint_error_response, \
                                token_required, generate_authorization_error_response, \
                                endpoint_validate_user_token

from app.api.v1.models import   MembershipClass, membership_class_schema

# Define blueprint for settings view
settings_config_members_view_blueprint = Blueprint('settings_config_members_view', '__name__')


@settings_config_members_view_blueprint.route('/settings/config/members', methods=['POST'])
@token_required
def create_membership_class(access_token):
    """ This creates a new membership class record"""
    response = {}
    data = {}
    
    user_token_payload = endpoint_validate_user_token(access_token)
    if 'headers' in user_token_payload:
        return generate_authorization_error_response(user_token_payload)
        
    # Parse the request data to check content_type is correct
    data = parse_request(request)
    if type(data) == dict and 'error' in data:
        return make_response(jsonify(data), data['status'])

    # check validity of request data
    res_valid_data = settings_config_members_validate_request_data(data)

    # process data if valid, else, return validation findings
    if data == res_valid_data:
        # send to storage
        response = save(res_valid_data)
    else:
        # return error from validation findings
        response = endpoint_error_response(data, res_valid_data)

    return make_response(jsonify(response), response['status'])
def save(membership_class_record):
    """Sends the membership class record to be added to storage."""
    # first check that class_name doesn't already exist
    existing_membershipclass = MembershipClass.query.filter_by(class_name=membership_class_record['class_name']).first()

    if not existing_membershipclass == None:
        return {
            "status":400,
            "error": "Cannot create new membership class. Class: '{}' already exists.".format(membership_class_record['class_name'])
        }

    # Save the new item
    membership_class = MembershipClass(**membership_class_record)
    membership_class.save()
    # Get the newly saved item
    new_membership_class_record = membership_class_schema.dump(membership_class).data
    # Confirm that the new item matches the input that was supplied
    if all(item in new_membership_class_record.items() for item in membership_class_record.items()):
        return {
            "status": 201,
            "data": new_membership_class_record
        }
    else:
        return {
            "status": 503,
            "error": 'An error occurred while saving the record.'
        }

def settings_config_members_validate_request_data(req_data):
    """Validates the membership_class data received"""
    # data = {
    #             "class_name": "test class ABC", required
    #             "monthly_contrib_amount": 1550.00, required
    #         }   
    #
    # parse the recevied data to check for empty or none
    received_data = check_is_empty(req_data)

    # exit if indeed data is empty
    if 'error' in received_data:
        return received_data    
    # Specify the required fields
    req_fields = ['class_name', 'monthly_contrib_amount']
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
