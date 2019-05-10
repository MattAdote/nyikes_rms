import  datetime, time, \
        jwt, \
        requests, \
        xlsxwriter, io

from werkzeug.security import generate_password_hash, check_password_hash

# project specific imports
from flask import   Blueprint, request, jsonify, make_response, send_file, \
                    render_template, current_app as app
from itsdangerous import SignatureExpired

# local imports
from app.api.v1.utils import    DATETIME_FORMATER, \
                                parse_request, validate_request_data, \
                                check_is_empty, endpoint_error_response, \
                                token_required, generate_authorization_error_response, \
                                endpoint_validate_user_token

from app.api.v1.models import   MembershipClass, Member, \
                                member_schema, members_schema, \
                                AcitvateAccountForm

from . membersview_functions import activate_account_validate_request_data, \
                                    save_member_record as save, members_validate_request_data, \
                                    generate_members_file, get_uploaded_members_file, \
                                    process_uploaded_members_file, get_member_record, \
                                    get_activate_account_serializer, SALT_ACTIVATE_ACCOUNT, \
                                    update_member_record, send_email, send_account_activation_email, \
                                    generate_reset_password_link

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
        return make_response(jsonify(response), response['status'])
    else:
        return send_file(
            response["output_file"], 
            mimetype=expected_file_mime_type, 
            as_attachment=True, 
            attachment_filename=response["filename"],
        )

@members_view_blueprint.route('/members/activate_account/<token>', methods=['GET', 'POST'])
def activate_account(token):
    with app.app_context():
        T_EXPIRE = app.config['ACTIVATION_TOKEN_EXPIRY_SECONDS']

    INVALID_TOKEN_VALUES = ['', "", '""', "''"]
    if token is None or token in INVALID_TOKEN_VALUES:
        return render_template('activate_account_error_no_token.html'), 400
    try:
        member_email = get_activate_account_serializer().loads(token, salt=SALT_ACTIVATE_ACCOUNT, max_age=T_EXPIRE)
    except SignatureExpired:
        return "<h1>The token has expired. Please use the Nyikes RMS Application to activate your account</h1>"
    except:
        return "<h1>There is a problem with the token. Please use the Nyikes RMS Application to activate your account</h1>"
    # get the member record of specified email
    # if success, display the activation form
    # else, return an error
    member_record = get_member_record(member_email)
    if 'error' not in member_record:
        account_activation_form = AcitvateAccountForm()
        
        if account_activation_form.validate_on_submit():
            # form is submitted
            # update the member's record with the username and password
            # dispatch an email notifying the user of successful update
            member_properties = request.form.to_dict()
            member_properties.pop('confirm_password')
            # add the activation timestamp and set the boolean
            member_properties.update({"DateAccountActivated": DATETIME_FORMATER.format(datetime.datetime.now())})
            member_properties.update({"accountActivated": True})

            updated_record = update_member_record(member_properties, member_record['public_id'])
            
            if 'error' in updated_record:
                return '<h1>Error:</h1><p>{}</p>'.format(updated_record['error'])
            # Dispatch email notification of successfull activation
            email_text_body = render_template(
                'new_member_activate_account_success_email.txt', 
                member=updated_record['data']
            )
            email_html_body = render_template(
                'activate_account_success.html',
                member=updated_record['data']
            )
            send_email(
                "NYIKES RMS: ACCOUNT ACTIVATION SUCCESS", app.config['ADMIN_EMAILS'][0],
                updated_record['data']['email'],
                email_text_body,
                html_body=email_html_body
            )
            
            return render_template('activate_account_success.html', member=updated_record['data']), 200
        
        fa = request.path
        return render_template('activate_account.html', form=account_activation_form, form_action=fa)
    else:
        return '<p>Hi, there was an error processing the activation: {}<p>'.format(member_record['error'])

@members_view_blueprint.route('/members/activate_account', methods=['POST'])
def process_activate_account_request():
    """ This processes a request to manually activate an account """
    
    response ={
        "status":200,
        "data":"Manual account activation done here"
    }
    
    # Parse the request data to check content_type is correct
    data = parse_request(request)
    if type(data) == dict and 'error' in data:
        return make_response(jsonify(data), data['status'])

    # check validity of request data
    res_valid_data = activate_account_validate_request_data(data)

    # process data if valid, else, return validation findings
    if data == res_valid_data:
        # 1. get the member record
        member_record = get_member_record(res_valid_data['email'])
        if 'error' in member_record:
            return make_response(jsonify(member_record), member_record['status'])
        # 2. take action based on activation status
        if member_record['accountActivated'] is False:
            send_account_activation_email(member_record)
            response = {
                "status":200,
                "data":"Please check your mailbox for the account activation link"
            }
        else:
            email_text_body = render_template('advice_reset_password_email.txt', member=member_record)
            email_html_body = render_template('advice_reset_password_email.html',member=member_record)
            send_email(
                "NYIKES RMS: ACCOUNT ACTIVATION NOTICE", app.config['ADMIN_EMAILS'][0], member_record['email'],
                email_text_body,
                html_body=email_html_body
            )
            response = {
                "status":200,
                "data":"Please check your mailbox. Instructions have been sent to your email address at {}".format(member_record['email'])
            }
    else:
        # return error from validation findings
        response = endpoint_error_response(data, res_valid_data)

    return make_response(jsonify(response), response['status'])

@members_view_blueprint.route('/members/reset_password', methods=['POST'])
def process_reset_password_request():
    """ This processes a request to reset the password for a member's account"""
    
    # Parse the request data to check content_type is correct
    data = parse_request(request)
    if type(data) == dict and 'error' in data:
        return make_response(jsonify(data), data['status'])

    # check validity of request data
    res_valid_data = activate_account_validate_request_data(data)

    # process data if valid, else, return validation findings
    if data == res_valid_data:
        # 1. get the member record
        member_record = get_member_record(res_valid_data['email'])
        if 'error' in member_record:
            return make_response(jsonify(member_record), member_record['status'])
        # 2. dispatch the reset password email
        reset_link = generate_reset_password_link(member_record['email'])
        email_text_body = render_template('reset_password_email.txt', member=member_record, link=reset_link)
        email_html_body = render_template('reset_password_email.html',member=member_record, link=reset_link)
        send_email(
            "NYIKES RMS: RESET PASSWORD", app.config['ADMIN_EMAILS'][0], member_record['email'],
            email_text_body,
            html_body=email_html_body
        )
        response = {
            "status":200,
            "data":"Please check your mailbox at {} for the reset password link".format(member_record['email'])
        }
    else:
        # return error from validation findings
        response = endpoint_error_response(data, res_valid_data)

    return make_response(jsonify(response), response['status'])