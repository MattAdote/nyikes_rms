import unittest
# import os, datetime, jwt
import json, pdb

from .contexts import   create_api_server, db, \
                        BaseModel, \
                        SuperUser, \
                        MembershipClass, \
                        save_new_member

class TestMemberViewFunctions(unittest.TestCase):
    """This class represents the member view functions test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
        self.superuser = SuperUser
        self.save_new_member = save_new_member

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

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main() 