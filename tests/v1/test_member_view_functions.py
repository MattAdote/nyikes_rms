import unittest
import os
import json, xlsxwriter, io,  pdb

from .contexts import   create_api_server, db, \
                        BaseModel, \
                        SuperUser, \
                        MembershipClass, member_classes_schema, \
                        save_new_member, get_membership_class_records, generate_members_file, \
                        process_uploaded_members_file 

dirpath = os.getcwd()

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

        self.input_member_record = {
            "first_name": "LaKwanza",
            "middle_name": "ZaKati",
            "last_name": "Mwishowe",
            "email": "mimimember@test123.org",
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
        with self.app.app_context():
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