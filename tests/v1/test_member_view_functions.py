import unittest
import os
import json, xlsxwriter, io,  pdb

from flask import render_template

from .contexts import   create_api_server, db, \
                        BaseModel, \
                        SuperUser, \
                        Member, MembershipClass, member_classes_schema, \
                        save_new_member, get_membership_class_records, get_member_record, \
                        generate_members_file, process_uploaded_members_file, send_email, \
                        update_member_record                        

scriptpath = os.path.realpath(__file__)
dirpath, filen = os.path.split(scriptpath)

class TestMemberViewFunctions(unittest.TestCase):
    """This class represents the member view functions test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
        self.superuser = SuperUser
        self.save_new_member = save_new_member
        self.get_membership_class_records = get_membership_class_records
        self.generate_members_file = generate_members_file
        self.process_uploaded_members_file = process_uploaded_members_file
        self.send_email = send_email
        self.get_member_record = get_member_record
        self.update_member_record = update_member_record

        self.input_member_record = {
            "first_name": "LaKwanza",
            "middle_name": "ZaKati",
            "last_name": "Mwishowe",
            "email": "ianadote@gmail.com",
            "phone_number": "0700987654",
            "class_name": "Test Class A B C"
        }
        
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_function_save_returns_error_on_membership_class_class_name_not_found(self):
        """ 
            Tests that the function to save a new member record returns
            an error if the class_name supplied in member record is not
            found.
        """
        # First, set a class_name that does not exist
        self.input_member_record['class_name'] = 'MeNoExist'
        # Next, define the expected output
        expected_output = {
            "status": 404,
            "error" : "Class name: {} not found".format(self.input_member_record['class_name'])
        }
        # test the function
        with self.app.app_context():
            output = self.save_new_member(self.input_member_record)
        # make the assertions
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('error', output, 'error key is missing in output')

        self.assertTrue(
            all(item in output.items() for item in expected_output.items()), 
            'Output returned is not equal to expected output: \n \
            output = "{}" \n INSTEAD OF \n "{}" \n '.format(output, expected_output)             
        )

    def test_function_send_email_sends_email_successfully(self):
        """ 
            Tests that the function to send an email is able to
            successfully send an email 
        """
        with self.app.app_context():
            email_text_body = render_template('new_member_activate_account_email.txt', 
                member=self.input_member_record,
                link='activation_link'
            )
            test_data = {
                "subject" : "Test Email from Nyikes RMS",
                "sender" : self.app.config['ADMIN_EMAILS'][0],
                "recipient" : self.input_member_record['email'],
                "text_body" : "{}".format(email_text_body)
            }
            
            try:
                self.send_email(
                    test_data['subject'], 
                    test_data['sender'], 
                    test_data['recipient'], 
                    test_data['text_body']            
                )
                assert True
            except:
                assert False

    def test_function_save_returns_new_member_record_with_id(self):
        """ 
            Tests that the function to save a new member record returns
            a new menber record with id
        """

        expected_output = {
            "status": 201,
            "data" : {
                "id":1,
                # plus input member record attributes
            }
        }
        expected_output['data'].update(self.input_member_record)
        with self.app.test_request_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class.save()
            # 2. test the save function
            output = self.save_new_member(self.input_member_record)
        # make the assertions
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('data', output, 'data key is missing in output')
        self.assertIn('id', output['data'], 'id key missing in output.data')

        self.assertEqual(output['status'], expected_output['status'], 'status returned Not status expected ')
        self.assertEqual(output['data']['first_name'], expected_output['data']['first_name'], 'first_name returned Not first_name supplied ')
        self.assertEqual(output['data']['middle_name'], expected_output['data']['middle_name'], 'middle_name supplied Not middle_name returned')
        self.assertEqual(output['data']['last_name'], expected_output['data']['last_name'], 'last_name returned Not last_name supplied')
        self.assertEqual(output['data']['email'], expected_output['data']['email'], 'email returned Not email supplied')
        self.assertEqual(output['data']['phone_number'], expected_output['data']['phone_number'], 'monthly_contrib_amount returned Not monthly_contrib_amount supplied')
        self.assertEqual(output['data']['class_name'], expected_output['data']['class_name'], 'class_name returned Not class_name supplied')
    
    def test_function_update_member_record_returns_error_on_invalid_property_to_update_param_type(self):
        """ 
            Tests that the function to update a member record returns an error if the
            type of the property_to_update parameter is invalid
        """
        properties_to_update = 'I am an invalid parameter'
        expected_output = {
            "status": 400,
            "error" : "Invalid format supplied: {}".format(type(properties_to_update))
        }
        with self.app.test_request_context():
            output = self.update_member_record(properties_to_update, 'random public id')

        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, "status_code key is missing!")
        self.assertIn('error', output, "error key is missing!")
        
        self.assertNotEqual(output['status'], "", "No status_code information provided")
        self.assertNotEqual(output['error'], "", "No error information provided")

        self.assertIsInstance(output['error'], str, "Error info not string data")
        
        self.assertEqual(output['status'], expected_output['status'], "Output received does not match expected")
        self.assertEqual(output['error'], expected_output['error'], "Output received does not match expected")

    def test_function_update_member_record_returns_error_on_invalid_record_public_id_param_type(self):
        """ 
            Tests that the function to update a member record returns an error if the
            type of the record_public_id parameter is invalid
        """
        properties_to_update = {"valid": 'I am an quasi valid parameter'}
        record_public_id = ['random-public-id-3-4']
        expected_output = {
            "status": 400,
            "error": "Invalid public id format supplied: {}".format(type(record_public_id))
        }
        with self.app.test_request_context():
            output = self.update_member_record(properties_to_update, record_public_id)

        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, "status_code key is missing!")
        self.assertIn('error', output, "error key is missing!")
        
        self.assertNotEqual(output['status'], "", "No status_code information provided")
        self.assertNotEqual(output['error'], "", "No error information provided")

        self.assertIsInstance(output['error'], str, "Error info not string data")
        
        self.assertEqual(output['status'], expected_output['status'], "Output received does not match expected")
        self.assertEqual(output['error'], expected_output['error'], "Output received does not match expected")

    def test_function_update_member_record_returns_error_on_empty_record_public_id(self):
        """ 
            Tests that the function to update a member record returns an error if the
            record_public_id parameter is empty or has no value
        """
        properties_to_update = {"valid": 'I am an quasi valid parameter'}
        record_public_id = ""
        expected_output = {
            "status": 400,
            "error": "Public id is not valid UUID"
        }
        with self.app.test_request_context():
            output = self.update_member_record(properties_to_update, record_public_id)

        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, "status_code key is missing!")
        self.assertIn('error', output, "error key is missing!")
        
        self.assertNotEqual(output['status'], "", "No status_code information provided")
        self.assertNotEqual(output['error'], "", "No error information provided")

        self.assertIsInstance(output['error'], str, "Error info not string data")
        
        self.assertEqual(output['status'], expected_output['status'], "Output received does not match expected")
        self.assertEqual(output['error'], expected_output['error'], "Output received does not match expected")

    def test_function_update_member_record_returns_error_if_record_public_id_not_UUID_string_format(self):
        """ 
            Tests that the function to update a member record returns an error if the
            record_public_id parameter does not have exactly four '-' characters
        """
        properties_to_update = {"valid": 'I am an quasi valid parameter'}
        record_public_id = "i-have-more-than-four-hyphen-characters"
        expected_output = {
            "status": 400,
            "error": "Public id is not valid UUID"
        }
        with self.app.test_request_context():
            output = self.update_member_record(properties_to_update, record_public_id)

        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, "status_code key is missing!")
        self.assertIn('error', output, "error key is missing!")
        
        self.assertNotEqual(output['status'], "", "No status_code information provided")
        self.assertNotEqual(output['error'], "", "No error information provided")

        self.assertIsInstance(output['error'], str, "Error info not string data")
        
        self.assertEqual(output['status'], expected_output['status'], "Output received does not match expected")
        self.assertEqual(output['error'], expected_output['error'], "Output received does not match expected")
    
    def test_function_update_member_record_returns_error_if_username_not_unique(self):
        """ 
            Tests that the function to update a member record returns an error if the
            username property supplied is not unique
        """
        
        new_member = {
            "first_name": "LaKwanza",
            "middle_name": "ZaKati",
            "last_name": "Mwishowe",
            "email": "newmember@domain.com",
            "phone_number": "0700987654",
            "class_name": "Test Class A B C"
        }
        existing_username = {"username":"Niko"}
        expected_output = {
            "status": 400,
            "error": "Cannot set username: '{}' already exists.".format(existing_username['username'])
        }
        with self.app.test_request_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class.save()
            # 2. create new member 1
            existing_member = self.save_new_member(self.input_member_record)
            # 3. set username for new member
            output = self.update_member_record(existing_username, existing_member['data']['public_id'])
            # 4. create second new member
            new_member = self.save_new_member(new_member)
            # 5. test the update function - set username of new member 2 = new member 1's username
            output = self.update_member_record(existing_username, new_member['data']['public_id'])

        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, "status_code key is missing!")
        self.assertIn('error', output, "error key is missing!")
        
        self.assertNotEqual(output['status'], "", "No status_code information provided")
        self.assertNotEqual(output['error'], "", "No error information provided")

        self.assertIsInstance(output['error'], str, "Error info not string data")
        
        self.assertEqual(output['status'], expected_output['status'], "Output received does not match expected")
        self.assertEqual(output['error'], expected_output['error'], "Output received does not match expected")
    
    def test_function_update_member_record_returns_error_if_email_not_unique(self):
        """ 
            Tests that the function to update a member record returns an error if the
            email property supplied is not unique
        """
        
        new_member_info = {
            "first_name": "LaKwanza",
            "middle_name": "ZaKati",
            "last_name": "Mwishowe",
            "email": "newmember@domain.com",
            "phone_number": "0700987654",
            "class_name": "Test Class A B C"
        }
        existing_email = {"email":self.input_member_record['email']}
        expected_output = {
            "status": 400,
            "error": "Cannot set email: '{}' already exists.".format(existing_email['email'])
        }
        with self.app.test_request_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class.save()
            # 2. create new member 1
            existing_member = self.save_new_member(self.input_member_record)
            # 3. create second new member
            new_member = self.save_new_member(new_member_info)
            # 4. test the update function - set email of new member = existing member's email
            output = self.update_member_record({"email":existing_member['data']['email']}, new_member['data']['public_id'])

        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, "status_code key is missing!")
        self.assertIn('error', output, "error key is missing!")
        
        self.assertNotEqual(output['status'], "", "No status_code information provided")
        self.assertNotEqual(output['error'], "", "No error information provided")

        self.assertIsInstance(output['error'], str, "Error info not string data")
        
        self.assertEqual(output['status'], expected_output['status'], "Output received does not match expected")
        self.assertEqual(output['error'], expected_output['error'], "Output received does not match expected")
    
    def test_function_update_member_record_returns_error_if_email_format_incorrect(self):
        """ 
            Tests that the function to update a member record returns an error if the
            email format is incorrect
        """
        
        properties_to_update = {"email":"invalid@domain,com"}
        expected_output = {
            "status": 400,
            "error": "Email address seems to be in incorrect format: {}".format(properties_to_update['email'])
        }
        with self.app.test_request_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class.save()
            # 2. create new member record
            new_member = self.save_new_member(self.input_member_record)
            # 3. test the update function - set email of new member = invalid email
            output = self.update_member_record(properties_to_update, new_member['data']['public_id'])

        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, "status_code key is missing!")
        self.assertIn('error', output, "error key is missing!")
        
        self.assertNotEqual(output['status'], "", "No status_code information provided")
        self.assertNotEqual(output['error'], "", "No error information provided")

        self.assertIsInstance(output['error'], str, "Error info not string data")
        
        self.assertEqual(output['status'], expected_output['status'], "Output received does not match expected")
        self.assertEqual(output['error'], expected_output['error'], "Output received does not match expected")
    
    def test_function_update_member_record_returns_record_if_username_for_existing_record(self):
        """ 
            Tests that the function to update a member record runs normally and doesn't
            break if a new username was supplied which is equal to the existing username
        """
        
        existing_username = {"username":"Niko"}
        expected_output = {
            "status": 200,
            "data" : {
                # plus input member record attributes
                # and plus the username
            }
        }
        expected_output['data'].update(self.input_member_record)
        expected_output['data'].update(existing_username)
        with self.app.test_request_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class.save()
            # 2. create new member
            existing_member = self.save_new_member(self.input_member_record)
            # 3. update username for new member
            output_0 = self.update_member_record(existing_username, existing_member['data']['public_id'])
            # 4. update username for new member with same username
            output = self.update_member_record(existing_username, existing_member['data']['public_id'])
            
        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('data', output, 'data key is missing in output')
        self.assertIn('public_id', output['data'], 'public_id key missing in output.data')
        self.assertIn('username', output['data'], 'username key missing in output.data')

        self.assertEqual(output['status'], expected_output['status'], 'status returned Not status expected ')
        self.assertEqual(output['data']['first_name'], expected_output['data']['first_name'], 'first_name returned Not first_name supplied ')
        self.assertEqual(output['data']['middle_name'], expected_output['data']['middle_name'], 'middle_name supplied Not middle_name returned')
        self.assertEqual(output['data']['last_name'], expected_output['data']['last_name'], 'last_name returned Not last_name supplied')
        self.assertEqual(output['data']['email'], expected_output['data']['email'], 'email returned Not email supplied')
        self.assertEqual(output['data']['phone_number'], expected_output['data']['phone_number'], 'monthly_contrib_amount returned Not monthly_contrib_amount supplied')
        self.assertEqual(output['data']['class_name'], expected_output['data']['class_name'], 'class_name returned Not class_name supplied')
    
    def test_function_update_member_record_returns_record_if_new_username_for_existing_record_set(self):
        """ 
            Tests that the function to update a member record runs normally and doesn't
            break if a new username was supplied which is equal to the existing username
        """
        
        existing_username = {"username":"Niko"}
        new_username = {"username":"NikoNewMsee"}
        expected_output = {
            "status": 200,
            "data" : {
                # plus input member record attributes
                # and plus the username
            }
        }
        expected_output['data'].update(self.input_member_record)
        expected_output['data'].update(new_username)
        with self.app.test_request_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class.save()
            # 2. create new member
            existing_member = self.save_new_member(self.input_member_record)
            # 3. update username for new member
            output_0 = self.update_member_record(existing_username, existing_member['data']['public_id'])
            # 4. update username for new member with new username
            output = self.update_member_record(new_username, existing_member['data']['public_id'])
            
        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('data', output, 'data key is missing in output')
        self.assertIn('public_id', output['data'], 'public_id key missing in output.data')
        self.assertIn('username', output['data'], 'username key missing in output.data')

        self.assertEqual(output['status'], expected_output['status'], 'status returned Not status expected ')
        self.assertEqual(output['data']['first_name'], expected_output['data']['first_name'], 'first_name returned Not first_name supplied ')
        self.assertEqual(output['data']['middle_name'], expected_output['data']['middle_name'], 'middle_name supplied Not middle_name returned')
        self.assertEqual(output['data']['last_name'], expected_output['data']['last_name'], 'last_name returned Not last_name supplied')
        self.assertEqual(output['data']['email'], expected_output['data']['email'], 'email returned Not email supplied')
        self.assertEqual(output['data']['phone_number'], expected_output['data']['phone_number'], 'monthly_contrib_amount returned Not monthly_contrib_amount supplied')
        self.assertEqual(output['data']['class_name'], expected_output['data']['class_name'], 'class_name returned Not class_name supplied')
        self.assertEqual(output['data']['username'], expected_output['data']['username'], 'username returned Not username supplied')
        
    def test_function_update_member_record_returns_record_if_email_for_existing_record(self):
        """ 
            Tests that the function to update a member record runs normally and doesn't
            break if a new email was supplied which is equal to the existing email
        """
        
        existing_email = {"email":self.input_member_record['email']}
        expected_output = {
            "status": 200,
            "data" : {
                # plus input member record attributes
            }
        }
        expected_output['data'].update(self.input_member_record)
        with self.app.test_request_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class.save()
            # 2. create new member
            existing_member = self.save_new_member(self.input_member_record)
            # 3. update email for new member with member's own existing email
            output = self.update_member_record(existing_email, existing_member['data']['public_id'])
            
        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('data', output, 'data key is missing in output')
        self.assertIn('public_id', output['data'], 'public_id key missing in output.data')
        self.assertIn('username', output['data'], 'username key missing in output.data')

        self.assertEqual(output['status'], expected_output['status'], 'status returned Not status expected ')
        self.assertEqual(output['data']['first_name'], expected_output['data']['first_name'], 'first_name returned Not first_name supplied ')
        self.assertEqual(output['data']['middle_name'], expected_output['data']['middle_name'], 'middle_name supplied Not middle_name returned')
        self.assertEqual(output['data']['last_name'], expected_output['data']['last_name'], 'last_name returned Not last_name supplied')
        self.assertEqual(output['data']['email'], expected_output['data']['email'], 'email returned Not email supplied')
        self.assertEqual(output['data']['phone_number'], expected_output['data']['phone_number'], 'monthly_contrib_amount returned Not monthly_contrib_amount supplied')
        self.assertEqual(output['data']['class_name'], expected_output['data']['class_name'], 'class_name returned Not class_name supplied')
        
    def test_function_update_member_record_returns_updated_record_with_username(self):
        """ 
            Tests that the function to update a member record returns the
            updated record
        """
        properties_to_update = {
            "username": "Yule Msee",
            "password": "ati-what?"
        }
        expected_output = {
            "status": 200,
            "data" : {
                "id":1,
                # plus input member record attributes
                # and plus properties to update w/o password
            }
        }
        expected_output['data'].update(self.input_member_record)
        expected_output['data'].update({"username" : properties_to_update["username"]})
        with self.app.test_request_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class.save()
            # 2. create new member record
            member_record = self.save_new_member(self.input_member_record)
            # 3. test the function
            output = self.update_member_record(properties_to_update, member_record['data']['public_id'])
        
        # make the assertions
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('data', output, 'data key is missing in output')
        self.assertIn('public_id', output['data'], 'public_id key missing in output.data')
        self.assertIn('username', output['data'], 'username key missing in output.data')

        self.assertEqual(output['status'], expected_output['status'], 'status returned Not status expected ')
        self.assertEqual(output['data']['first_name'], expected_output['data']['first_name'], 'first_name returned Not first_name supplied ')
        self.assertEqual(output['data']['middle_name'], expected_output['data']['middle_name'], 'middle_name supplied Not middle_name returned')
        self.assertEqual(output['data']['last_name'], expected_output['data']['last_name'], 'last_name returned Not last_name supplied')
        self.assertEqual(output['data']['email'], expected_output['data']['email'], 'email returned Not email supplied')
        self.assertEqual(output['data']['phone_number'], expected_output['data']['phone_number'], 'monthly_contrib_amount returned Not monthly_contrib_amount supplied')
        self.assertEqual(output['data']['class_name'], expected_output['data']['class_name'], 'class_name returned Not class_name supplied')
        self.assertEqual(output['data']['username'], expected_output['data']['username'], 'username returned Not username supplied')

    def test_function_get_member_record_returns_error_on_db_error_member_table_not_exist(self):
        """
            Test that get_member_record() returns error if the database raises an error
            when looking up the Member and the member table doesn't exist or there's an
            error when retrieving the member record
        """
        member_email="random@email.dom"
        
        expected_output = {
            "status" : 500,
            "error": "Ran into a database error looking up member record for email: {}".format(member_email)
        }

        with self.app.app_context():
            Member.__table__.drop(db.get_engine())
            output = self.get_member_record(member_email)

        # Make the assertions
        assert type(output) == dict
        self.assertIn('status', output, "status_code key is missing!")
        self.assertIn('error', output, "error key is missing!")
        
        self.assertNotEqual(output['status'], "", "No status_code information provided")
        self.assertNotEqual(output['error'], "", "No error information provided")

        self.assertIsInstance(output['error'], str, "Error info not string data")
        
        self.assertEqual(output['status'], expected_output['status'], "Output received does not match expected")
        self.assertEqual(output['error'], expected_output['error'], "Output received does not match expected")
    
    def test_function_get_member_record_returns_error_if_no_record_found(self):
        """ 
            Tests that the function to get a member record returns
            an error if none is found
        """
        member_email = "notexist@domain.com"

        expected_output = {
            "status": 404,
            "error" : "No member record found for email: {}".format(member_email)
        }

        with self.app.app_context():
            # test the function
            output = self.get_member_record(member_email)

        # make the assertions
        assert type(output) == dict

        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('error', output, 'error key is missing in output')

        self.assertEqual(output['status'], expected_output['status'], 'Output not equal to expected output')
        self.assertEqual(output['error'], expected_output['error'], 'Output not equal to expected output')
    
    def test_function_get_member_record_returns_member_record_of_specified_email(self):
        """ 
            Tests that the function to get a member record returns
            the member record of specified email address
        """

        expected_output = {}
        expected_output.update(self.input_member_record)

        with self.app.test_request_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class.save()
            # 2. create a new member record
            new_record = self.save_new_member(self.input_member_record)
            # test the function
            output = self.get_member_record(new_record['data']['email'])

        # make the assertions
        assert type(output) == dict
        self.assertIn('public_id', output, 'public_id key missing in output')
        self.assertEqual(output['email'], expected_output['email'], 'Output not equal to expected output')
    
    def test_function_get_membership_class_records_returns_error_if_no_records_found(self):
        """ 
            Tests that the function to get membership class records returns
            an error if no membership class records are found
        """

        expected_output = {
            "status": 404,
            "error" : "No membership class records defined"
        }

        with self.app.app_context():
            # test the function
            output = self.get_membership_class_records()

        # make the assertions
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('error', output, 'error key is missing in output')

        self.assertTrue(
            all(item in output.items() for item in expected_output.items()), 
            'Output returned is not equal to expected output: \n \
            output = "{}" \n INSTEAD OF \n "{}" \n '.format(output, expected_output)             
        )
    
    def test_function_get_membership_class_records_returns_list_of_dictionary_records(self):
        """ 
            Tests that the function to get membership class records returns
            a list of dictionary records containing the membershipclass records
        """

        with self.app.app_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class2 = MembershipClass(class_name='Test Class 2', monthly_contrib_amount=1050.00)
            
            obj_membership_class.save()
            obj_membership_class2.save()

            obj_membership_classes = MembershipClass.query.all()
            membership_class_records = member_classes_schema.dump(obj_membership_classes).data

            # 2. Define the expected output
            expected_output = membership_class_records

            # 3. test the function
            output = self.get_membership_class_records()

        # pdb.set_trace()
        # make the assertions
        assert type(output) == list
        assert type(output[0]) == dict        

        self.assertEqual(output, expected_output, "Output received NOT Equal to Expected Output")

    def test_function_generate_member_file_creates_xlsx_file(self):
        """ 
            Tests that the function to get membership class records returns
            an error if no membership class records are found
        """

        with self.app.app_context():
            # 1. create new membership_class record
            obj_membership_class = MembershipClass(class_name=self.input_member_record['class_name'], monthly_contrib_amount=1450.00)
            obj_membership_class2 = MembershipClass(class_name='Test Class 2', monthly_contrib_amount=1050.00)
            
            obj_membership_class.save()
            obj_membership_class2.save()
            
            # pdb.set_trace()
            # 2. test the function
            output = self.generate_members_file()

        # pdb.set_trace()
        # make the assertions
        self.assertIn('output_file', output)
        self.assertIn('filename', output)

        assert type(output['output_file']) == io.BytesIO
        assert type(output['filename']) == str
    
    def test_function_process_uploaded_members_file_returns_error_on_members_sheet_missing(self):
        """
            Test that function returns error if the members informationn sheet is missing
            from the Excel workbook.
        """
        expected_ws_name = "Member Info"
        expected_output = {
            "status": 400,
            "error": "Worksheet: {} is missing from uploaded file".format(expected_ws_name)
        }
    
        test_file_path = '{}/_resources/ex_member_records_wrong_data.xlsx'.format(dirpath)

        with self.app.app_context():
            # test the function
            output = self.process_uploaded_members_file(test_file_path, expected_ws_name)

        # make the assertions
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('error', output, 'error key is missing in output')

        self.assertEqual(output['status'], expected_output['status'], 'Output not equal to expected output')
        self.assertEqual(output['error'], expected_output['error'], 'Output not equal to expected output')
    
    def test_function_process_uploaded_members_file_returns_error_on_column_names_missing(self):
        """
            Test that function returns error if the expected column names are missing
            from the Members Info worksheet
        """
        expected_ws_name = 'Member Info'
        expected_column_names = ['First Name', 'Middle Name', 'Last Name', 'Membership Class', 'Phone Number', 'Email']
        removed_column_names = ['Middle Name', 'Email']

        expected_output = {
            "status": 400,
            "error": "Columns: {} missing from Worksheet: {}".format(removed_column_names, expected_ws_name)
        }
    
        test_file_path = '{}/_resources/ex_uploaded_member_records_missing_column_names.xlsx'.format(dirpath)

        with self.app.app_context():
            # test the function
            output = self.process_uploaded_members_file(test_file_path, expected_ws_name)

        # make the assertions
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('error', output, 'error key is missing in output')

        self.assertEqual(output['status'], expected_output['status'], 'Output not equal to expected output')
        self.assertEqual(output['error'], expected_output['error'], 'Output recieved not equal to expected output')
    
    def test_function_process_uploaded_members_file_returns_error_on_zero_new_member_records(self):
        """
            Test that function returns error if there are no new member records in the worksheet
        """
        expected_ws_name = 'Member Info'
        expected_column_names = ['First Name', 'Middle Name', 'Last Name', 'Membership Class', 'Phone Number', 'Email']

        expected_output = {
            "status": 400,
            "error": "No records to import from Worksheet: {}".format(expected_ws_name)
        }
    
        test_file_path = '{}/_resources/ex_member_records_no_new_records.xlsx'.format(dirpath)
        
        with self.app.app_context():
            # test the function
            output = self.process_uploaded_members_file(test_file_path, expected_ws_name)

        # make the assertions
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('error', output, 'error key is missing in output')

        self.assertEqual(output['status'], expected_output['status'], 'Output not equal to expected output')
        self.assertEqual(output['error'], expected_output['error'], 'Output not equal to expected output')

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main() 