import uuid, io, xlsxwriter, pandas as pd, stringcase as sc

from flask import current_app as app, render_template, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash

from app import mail
from app.api.v1.models import   Member, member_schema, members_schema, \
                                MembershipClass, member_classes_schema
from app.api.v1.utils import    check_is_empty, validate_request_data, \
                                async_task, is_valid_email

SALT_ACTIVATE_ACCOUNT = 'new-account-activation-salt'

def get_activate_account_serializer():
    with app.app_context():
        return URLSafeTimedSerializer(app.config['SECRET'])

def save_member_record(member_record):
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
    # dispatch email to the email address in the member record
    # return 
    if 'class_name' in member_record:
        
        if member_record['class_name'] != "":
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
            member_record.update({'membership_class': membership_class})
        else:
            member_record.update({'membership_class': ''})
        # remove the 'class_name' key as it is not an attribute of class Member    
        member_record.pop('class_name')
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
    # restore class_name attribute as it is the friendly name
    # that is exposed to the outside world and is documented
    if 'membership_class' in member_record:
        if member_record['membership_class'] != "":
            member_record.update({'class_name': membership_class.class_name})
        else:
            member_record.update({'class_name': ''})
        member_record.pop('membership_class')

    # Get the newly saved item
    new_member_record = member_schema.dump(member).data
    # Confirm that the new item matches the input that was supplied
    if all(item in new_member_record.items() for item in member_record.items()):
        response = {
            "status": 201,
            "data": new_member_record
        }
    else:
        # I don't expect this code to be ever reached because unless a weird error
        # occurs then the created member record will always have the attributes
        # contained in the original data supplied.
        # Ordinarily, this is expected to be reached when the DB returns string
        # instead of int e.g. phone_number in original data is int but DB returns
        # a string 
        response = {
            "status": 200,
            "data": new_member_record,
            "warning": "Warning: Datatype returned from DB may not match original."
        }
    # Here, we send the activation email to the member in a new thread
    # Primary reason is because this is a side effect of adding a new record
    # Hence, no reason to tie up the response back to the client on the
    # status of the add_new_record operation
    activation_link = url_for(
        'members_view.activate_account',
        token=get_activate_account_serializer().dumps(
                new_member_record['email'], 
                salt=SALT_ACTIVATE_ACCOUNT
            ),
        _external=True
    )
        
    email_text_body = render_template('new_member_activate_account_email.txt', 
        member=new_member_record,
        link=activation_link
    )
    email_html_body = render_template('new_member_activate_account_email.html', 
        member=new_member_record,
        link=activation_link
    )
    send_email(
        "NYIKES RMS: ACCOUNT ACTIVATION", app.config['ADMIN_EMAILS'][0], new_member_record['email'],
        email_text_body,
        html_body=email_html_body
    )
    return response

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

def generate_members_file():
    """
        This generates an MS Excel file to be used to fill in
        records of members to be added to the RMS.

        Returns a dict as follows : {
            "output_file" : the_output_file (type = io.BytesIO),
            "filename" : the_output_filename (type = str),
        }
    """
    num_records = 0
    records_count = 0
    start_table_row = 1
    start_data_row = start_table_row + 1
    
    data_rows = []
    row_data = []

    # First, get the records of the membership classes that have
    # been added to the RMS.
    class_records = get_membership_class_records()
    if 'error' in class_records:
        return class_records
    
    # create workbook
    output_file = io.BytesIO()
    output_filename = 'Nyikes_RMS - Add New Member Records.xlsx'

    workbook = xlsxwriter.Workbook(output_file, {'in_memory': True})
    ws_member_info = workbook.add_worksheet('Member Info')
    ws_membership_class = workbook.add_worksheet('Class info')

    num_records = len(class_records)
    table_membershipclass_cell_range = 'A{}:C{}'.format(start_table_row, start_table_row + num_records)
    table_membershipclass_options = {
        # "data":data_rows,
        "name" : "MembershipClassData",
        "columns" : [
            {"header": "RNo."}, # A
            {"header": "Class"}, # B
            {"header": "Monthly Contribution"} # C
        ],
    }
    ws_membership_class.add_table(table_membershipclass_cell_range, options=table_membershipclass_options)
    # prepare the data to add to the table
    for item in class_records:
        records_count+=1

        row_data.append(records_count)
        row_data.append(item['class_name'])
        row_data.append(item['monthly_contrib_amount'])

        data_rows.append(row_data)

        ws_membership_class.write_row('A{}'.format(start_data_row), data=row_data)
        row_data = []
        start_data_row+=1

    # Create members info table
    member_records_limit = 5
    table_member_cell_range = 'A{}:F{}'.format(start_table_row, start_table_row + member_records_limit)
    table_member_options = {
        "name" : "MemberData",
        "columns" : [
            {"header"   :    "First Name"}, # A
            {"header"   :    "Middle Name"}, # B
            {"header"   :    "Last Name"}, # C
            {"header"   :    "Membership Class"}, # D
            {"header"   :    "Phone Number"}, # E
            {"header"   :    "Email"} # F
        ]
    }
    ws_member_info.add_table(table_member_cell_range, options=table_member_options)

    # add dropdown validation to the rows on the Membershipclass column
    col_to_validate = 'D'
    reference_column = 'B'
    start_at_row = start_data_row - records_count
    stop_at_row = start_data_row - 1
    range_start = start_table_row + 1
    range_stop = range_start + member_records_limit
    for row_num in range(range_start, range_stop):
        ws_member_info.data_validation(
            '{}{}'.format(col_to_validate, row_num), 
            {
                'validate'  :   'list',
                'source'    :   '=\'{}\'!${}${}:${}${}'.format(
                                    ws_membership_class.get_name(), 
                                    reference_column, 
                                    start_at_row,
                                    reference_column,
                                    stop_at_row
                                )
                
            }
        )
    # close the workbook    
    workbook.close()

    # rewind the buffer
    output_file.seek(0)

    return {
        "output_file": output_file,
        "filename": output_filename
    }

def get_membership_class_records():
    """ This returns the membership class records """
    try:
        membership_class = MembershipClass.query.all()
    except:
        return {
            "status":503,
            "error":"Database error encountered when looking up membership class records"
        }
    if not membership_class:
        return {
            "status":404,
            "error":"No membership class records defined"
        }
    
    # load member classes schema
    return member_classes_schema.dump(membership_class).data

def get_uploaded_members_file(req, expected_file_parameter, expected_file_mime_type):
    """ This returns the uploaded members file contained in the request """

    if expected_file_parameter not in req.files:
        response = {
            "status": 400,
            "error": 'File parameter: \'{}\' not found'.format(expected_file_parameter)
        }
        return response
    elif req.files[expected_file_parameter] == None or req.files[expected_file_parameter] == '':
        response = {
            "status": 400,
            "error": 'No data supplied!'
        }
        return response
    else:
        uploaded_file = req.files[expected_file_parameter]
        # confirm that correct file is received!
        if uploaded_file.mimetype != expected_file_mime_type:
            response = {
                "status": 400,
                "error": 'Invalid file uploaded. File not .xlsx file'
            }
            return response
        # So the mimetype checks but this is not a fool proof method
        # This is because the mimetypes are arrived at on the basis
        # of the file extension. So if I take a word document and
        # rename its extension to .xlsx then the document's mimetype
        # would change to the excel mimetype.
        # Therefore, must take care to vet the contents of the file
        
        return uploaded_file

def process_uploaded_members_file(uploaded_members_file, expected_sheet_name):
    """
        Imports data from the uploaded members file into the RMS
    """

    # TARGET_FIELD_NAMES = ['first_name', 'last_name', 'email', 'phone_number', 'middle_name', 'class_name']
    EXPECTED_COLUMN_NAMES = ['First Name', 'Middle Name', 'Last Name', 'Membership Class', 'Phone Number', 'Email']

    response = {}
    
    missing_columns = []
    db_import_result = []
    df = pd.ExcelFile(uploaded_members_file)

    if expected_sheet_name not in df.sheet_names:
        response.update({
            'status':400,
            'error': "Worksheet: {} is missing from uploaded file".format(expected_sheet_name)
        })
        return response
    
    ws_new_member_records = df.parse(expected_sheet_name)

    file_columns = ws_new_member_records.columns
    for expected_column in EXPECTED_COLUMN_NAMES:
        if expected_column not in file_columns.to_list():
            missing_columns.append(expected_column)
    if len(missing_columns) > 0:
        response.update({
            'status':400,
            'error': "Columns: {} missing from Worksheet: {}".format(missing_columns, expected_sheet_name)
        })
        return response
    
    num_new_records_found = len(ws_new_member_records)
    if num_new_records_found == 0:
        response.update({
            'status':400,
            'error': "No records to import from Worksheet: {}".format(expected_sheet_name)
        })
        return response

    # all ok, so now convert the column names to match the model field names
    # rename membership_class column
    ws_new_member_records.rename(
        columns={'Membership Class':'Class Name'},
        inplace=True
    )
    # convert column names to snake case
    for column in ws_new_member_records.columns:
        ws_new_member_records.rename(
            columns={
                column:sc.snakecase(column).replace('__', '_') # replace is due to identified bug. Tested for.
            },
            inplace=True
        )
    # replace any 'NaN' values with empty ''
    ws_new_member_records.fillna('', inplace=True)
    # save each individual record
    for index, row in ws_new_member_records.iterrows():
        # first convert phone_number field to string
        row['phone_number'] = str(row['phone_number'])
        # next, send to storage
        db_response = save_member_record(row.to_dict())
        # record the response against the record
        if 'error' in db_response:
            db_import_result.append(db_response['error'])
        elif 'warning' in db_response:
            db_import_result.append('Success but be advised: {}'.format(db_response['warning']))
        else:
            db_import_result.append('Success')
    
    ws_new_member_records['DB Import Result'] = db_import_result

    # so now we start on preparing the df for output
    # 1. Return the column names to 'Title Case'
    for column in ws_new_member_records.columns:
        if column != 'DB Import Result':
            ws_new_member_records.rename(
                columns={
                    column:sc.titlecase(column) # this converts ok.
                },
                inplace=True
            )
    # 2. Revert the Class Name to Membership Class
    ws_new_member_records.rename(
        columns={'Class Name':'Membership Class'},
        inplace=True
    )
    # 3. append modified dataframe to new sheet in uploaded file
    with pd.ExcelWriter(uploaded_members_file, engine='openpyxl', mode='a') as writer:
        ws_new_member_records.to_excel(writer, sheet_name='DB Import Results')
        
    output_file = io.BytesIO()
    uploaded_members_file.seek(0) # go back to start of uploaded file
    output_file.write(uploaded_members_file.read())
    output_file.seek(0)
    
    response.update({
        "output_file": output_file,
        "filename": uploaded_members_file.filename
    })    

    return response

def send_email(subject, sender, recipient, text_body, html_body=None):
    """
        Sends email to the email address in the new member record
    """
    msg = Message(subject, sender=sender, recipients=[recipient])
    msg.body = text_body
    msg.html = '' if html_body is None else html_body
    _send_async_email(app._get_current_object(), msg)

@async_task
def _send_async_email(fl_app, email_message):
    """
        This dispatches an email in a separate thread
    """
    with fl_app.app_context():
        mail.send(email_message)

def get_member_record(member_email):
    """ 
        Returns member record of specified email if found
        else returns an error
    """
    try:
        member = Member.query.filter_by(email=member_email).first()
    except:
        return {
            "status":500,
            "error": "Ran into a database error looking up member record for email: {}".format(member_email)
        }

    if member is not None:
        return  member_schema.dump(member).data
    else:
        return {
            "status":404,
            "error":"No member record found for email: {}".format(member_email)
        }

def update_member_record(properties_to_update, record_public_id):
    """
        Updates the member record of specified public id with
        the properties supplied if those properties exist in
        member object
    """
    non_existent_properties = []
    # 1. Validate the parameters
    if type(properties_to_update) is not dict:
        return {
            "status": 400,
            "error": "Invalid format supplied: {}".format(type(properties_to_update))
        }
    elif type(record_public_id) is str:
        if record_public_id.count('-') != 4:
            return {
                "status": 400,
                "error": "Public id is not valid UUID"
            }
    else:
        return {
            "status": 400,
            "error": "Invalid public id format supplied: {}".format(type(record_public_id))
        }
    # 2. Get the member record
    member = Member.query.filter_by(public_id=record_public_id).first()
    if member is None:
        return {
            "status": 404,
            "error": "No member found with public id: {}".format(record_public_id)
        }
    # 3. Check that member object has all the properties in the properties to update
    for key in properties_to_update:
        if not hasattr(member, key):
            non_existent_properties.append(key)
    # 4. Return error if non existent properties found
    if len(non_existent_properties) > 0:
        return {
            "status": 400,
            "error": "Bogus attributes supplied: {}".format(non_existent_properties)
        }
    # 5. All ok. Update the member object properties
    for key, value in properties_to_update.items():
        # check that username and email are unique
        if key in ['username', 'email']:
            if key is 'username':
                existing_member = Member.query.filter_by(username=value).first()
            else:
                existing_member = Member.query.filter_by(email=value).first()

            if existing_member is not None:
                if existing_member.public_id != record_public_id:
                    # the public id of existing record is for another record
                    return {
                        "status":400,
                        "error": "Cannot set {}: '{}' already exists.".format(key, value)
                    }
        # store hash of the given password
        if key == 'password':
            value = generate_password_hash(value, method='sha256')
        setattr(member, key, value)
    # 6. Save the member record
    try:
        member.save()
    except:
        return {
            "status": 500,
            "error": "Database error encountered when saving record"
        }
    # 7. Return the serialized member record
    return {
        "status": 200,
        "data": member_schema.dump(member).data
    }

def activate_account_validate_request_data(req_data):
    """Validates the data received for manual account activation"""
    # data = {
    #             "email": "me@domain.com", required
    #         }   
    #
    # parse the recevied data to check for empty or none
    received_data = check_is_empty(req_data)

    # exit if indeed data is empty
    if 'error' in received_data:
        return received_data    
    
    # Specify the required fields
    req_fields = ['email']
    # Initialize list to hold processed fields
    sanitized_data = []

    dict_req_fields = {}
    # get the required fields' data and put in own dictionary
    for field in req_fields:
        if field in received_data:
            dict_req_fields.update({field: received_data[field]})
    # append required fields dictionary to sanitized_data list
    sanitized_data.append(dict_req_fields)

    # send sanitized_data list to actual validation function
    checked_data = validate_request_data(sanitized_data, req_fields)

    # return validation findings if there was an error
    if 'error' in checked_data:
        return checked_data
    
    # check that the email is in email format.
    if not is_valid_email(checked_data['email']):
        return {
            "status":400,
            "error":"Supplied email seems to be in incorrect format: {}".format(checked_data['email'])
        }

    return checked_data

def generate_activation_link(member_email):
    """ 
        Generate an activation link for specified email
    """
    return url_for(
        'members_view.activate_account',
        token=get_activate_account_serializer().dumps(
                member_email, 
                salt=SALT_ACTIVATE_ACCOUNT
            ),
        _external=True
    )

def send_account_activation_email(member_record):
    """
        Send account activation email for member
    """
    activation_link = generate_activation_link(member_record['email'])
    email_text_body = render_template('new_member_activate_account_email.txt', 
        member=member_record,
        link=activation_link
    )
    email_html_body = render_template('new_member_activate_account_email.html', 
        member=member_record,
        link=activation_link
    )
    send_email(
        "NYIKES RMS: ACCOUNT ACTIVATION", app.config['ADMIN_EMAILS'][0], member_record['email'],
        email_text_body,
        html_body=email_html_body
    )