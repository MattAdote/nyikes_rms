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
                                token_required, generate_authorization_error_response, \
                                endpoint_validate_user_token

from app.api.v1.models import   MembershipClass, \
                                Member, member_schema, members_schema

# Define blueprint for members view
members_view_blueprint = Blueprint('members_view', '__name__')


@members_view_blueprint.route('/members', methods=['POST'])
@token_required
def create_member(access_token):
    """ This creates a new member record"""
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
    res_valid_data = members_validate_request_data(data)
    if 'error' in res_valid_data:
        # get error from validation findings
        response = endpoint_error_response(data, res_valid_data)
    else:
        # send to storage
        response = save(res_valid_data)

    return make_response(jsonify(response), response['status'])

def save(member_record):
    """Sends the member record to be added to storage."""
    
    # first check that member doesn't already exist
    existing_member = Member.query.filter_by(email=member_record['email']).first()

    if existing_member is not None:
        return {
            "status":400,
            "error": "Cannot add new member. Email: '{}' already exists.".format(member_record['email'])
        }

    # flow
    # after confirming member is unique
    # check that class_name is valid
    # if not valid. return error
    # pop off the class_name from the member record
    # add new attribute membership_class = obj MembershipClass of supplied class name
    # save the record
    if 'class_name' in member_record and member_record['class_name'] != "":
        try:
            membership_class = MembershipClass.query.filter_by(class_name=member_record['class_name']).first()
        except:
            return {
                "status":503,
                "error":"Database error encountered when looking up supplied class_name"
            }
        if not membership_class:
            return {
                "status":404,
                "error":"Class name: {} not found".format(member_record['class_name'])
            }
        member_record.pop('class_name')
        member_record.update({'membership_class': membership_class})

    # Save the new item
    try:
        member = Member(**member_record)
    except:
        return {
                    "status":503,
                    "error":"Encountered error initializing new member object from supplied data"
        }
    try:
        member.save()
    except:
        return {
                    "status":503,
                    "error":"Database error encountered when saving new member record"
        }
    # restore class_name attribute if it had been removed
    if 'membership_class' in member_record:
        member_record.pop('membership_class')
        member_record.update({'class_name': membership_class.class_name})

    # Get the newly saved item
    new_member_record = member_schema.dump(member).data
    # Confirm that the new item matches the input that was supplied
    if all(item in new_member_record.items() for item in member_record.items()):
        return {
            "status": 201,
            "data": new_member_record
        }
    else:
        # I don't expect this code to be ever reached because unless a weird error
        # occurs then the created member record will always have the attributes
        # contained in the original data supplied
        return {
            "status": 503,
            "error": 'An error occurred while saving the record.'
        }

def members_validate_request_data(req_data):
    """Validates the member data received"""
    # data = {
    #             "first_name"      : "", required
    #             "last_name"       : "", required  
    #             "email"           : "", required  
    #             "phone_number"    : "", required 
    #             "middle_name"     : "", not required  
    #             "class_name"      : "", not required
    # }   
    #
    # parse the recevied data to check for empty or none
    received_data = check_is_empty(req_data)
    # exit if indeed data is empty
    if 'error' in received_data:
        return received_data    
    # Specify the required and non required fields
    req_fields = ['first_name', 'last_name', 'email', 'phone_number']
    non_req_fields = ['middle_name', 'class_name']
    # Initialize list to hold processed fields
    sanitized_data = []

    # get the required fields' data and put in own dictionary
    dict_req_fields = {}
    for field in req_fields:
        if field in received_data:
            dict_req_fields.update({field: received_data[field]})
    # append required fields dictionary to sanitized_data list
    sanitized_data.append(dict_req_fields)

    # get the non required fields data and put in own dictionary
    dict_non_req_fields = {}
    for field in non_req_fields:
        if field in received_data:
            dict_non_req_fields.update({field: received_data[field]})
    # append non required fields dictionary to sanitized_data list
    sanitized_data.append(dict_non_req_fields)

    # send sanitized_data list to actual validation function and return response
    return validate_request_data(sanitized_data, req_fields)
