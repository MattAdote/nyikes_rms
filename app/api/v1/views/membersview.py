import  datetime, time, \
        jwt, \
        requests, \
        xlsxwriter, io

from werkzeug.security import generate_password_hash, check_password_hash

# project specific imports
from flask import   Blueprint, request, jsonify, make_response, send_file, \
                    current_app as app

# local imports
from app.api.v1.utils import    parse_request, validate_request_data, \
                                check_is_empty, endpoint_error_response, \
                                token_required, generate_authorization_error_response, \
                                endpoint_validate_user_token

from app.api.v1.models import   MembershipClass, \
                                Member, member_schema, members_schema

from . membersview_functions import save_member_record as save, members_validate_request_data, \
                                    generate_members_file, get_uploaded_members_file, \
                                    process_uploaded_members_file

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

@members_view_blueprint.route('/members/file', methods=['GET'])
@token_required
def get_members_file(access_token):
    response = {}
    data = {}
    
    # First, validate the user's token
    user_token_payload = endpoint_validate_user_token(access_token)
    if 'headers' in user_token_payload:
        return generate_authorization_error_response(user_token_payload)

    # Second, parse the request data to check content_type is correct.
    # This is redundant because the content type was already checked
    # when the acess token was being validated.
    data = parse_request(request)
    if type(data) == dict and 'error' in data:
        return make_response(jsonify(data), data['status'])  

    # Third, generate the members file and return
    response = generate_members_file()

    if "output_file" in response and type(response["output_file"]) == io.BytesIO:
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        
        return send_file(
            response["output_file"], 
            mimetype=mimetype, 
            as_attachment=True, 
            attachment_filename=response["filename"],
        )
    elif 'error' in response:
        return make_response(jsonify(response), response['status'])
    else:
        response = {
            "status" : 500,
            "error" : "A system error occurred while generating the file"
        }
        return make_response(jsonify(response), response['status'])

@members_view_blueprint.route('/members/file', methods=['POST'])
@token_required
def post_members_file(access_token):
    response = {}
    uploaded_file = None
    expected_file_parameter = 'addNewMembersFile'
    expected_file_mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

    # First, validate the user's token
    user_token_payload = endpoint_validate_user_token(access_token)
    if 'headers' in user_token_payload:
        return generate_authorization_error_response(user_token_payload)
    # Second, retrieve the file
    uploaded_file = get_uploaded_members_file(request, expected_file_parameter, expected_file_mime_type)
    if 'error' in uploaded_file:
        return make_response(jsonify(uploaded_file), uploaded_file['status'])
    # Third, process the file i.e. import the data
    response.update(process_uploaded_members_file(uploaded_file, 'Member Info'))

    if "error" in response:
        make_response(jsonify(response), response['status'])
    else:
        return send_file(
            response["output_file"], 
            mimetype=expected_file_mime_type, 
            as_attachment=True, 
            attachment_filename=response["filename"],
        )

@members_view_blueprint.route('/members/activate_account/<token>', methods=['GET'])
def activate_account(token):
    return ('<p>Hi, this is where you activate your account.<p>'
            '<p>You will key in your desired username and password in a form to be displayed here')