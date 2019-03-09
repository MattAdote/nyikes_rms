import unittest
import os
import json, pdb

from .contexts import   create_api_server, db, \
                        BaseModel, \
                        SuperUser, superuser_schema, \
                        verify_credentials

class TestSuperuserViewFunctions(unittest.TestCase):
    """This class represents the superuser view functions test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
        self.superuser = SuperUser
        self.verify_credentials = verify_credentials

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_function_verify_credentials_returns_superuser_object_on_success(self):
        """ Tests that the function to verify credentials returns a superuser object on successful verification """

        # First, create a new superuser record
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        # Next, use the returned data to make call to the function
        res_1.json['data'].pop('id') # function expects dict of username and password only
        with self.app.app_context():
            output = self.verify_credentials(res_1.json['data'])
        
        # Finally, assert all is well
        self.assertTrue(isinstance(output, SuperUser), 'Output not instance of class Superuser')        
    
    def test_function_verify_credentials_returns_error_on_invalid_username(self):
        """ Tests that the function to verify credentials returns an error on failed username verification """

        # First, create a new superuser record
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        # Next, use the returned data to make call to the function
        res_1.json['data'].pop('id') # function expects dict of username and password only
        res_1.json['data']['username'] = 'Incorrect username' # set an incorrect username
        with self.app.app_context():
            output = self.verify_credentials(res_1.json['data'])
        
        expected_status_code = 403
        expected_error_msg = 'Username: {} not found'.format(res_1.json['data']['username'])

        # Finally, assert
        assert type(output) == dict
        self.assertIn('status', output)
        self.assertIn('error', output)
        self.assertEqual(expected_status_code, output['status'], "Expected status code not returned")
        self.assertIn(expected_error_msg, output['error'], "Expected error message not returned")  

    def test_function_verify_credentials_returns_error_on_invalid_password(self):
        """ Tests that the function to verify credentials returns an error on failed password verification """

        # First, create a new superuser record
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        # Next, use the returned data to make call to the function
        res_1.json['data'].pop('id') # function expects dict of username and password only
        res_1.json['data']['password'] = 'Incorrect password' # set an incorrect username
        with self.app.app_context():
            output = self.verify_credentials(res_1.json['data'])
        
        expected_status_code = 403
        expected_error_msg = 'Incorrect Password!'

        # Finally, assert
        assert type(output) == dict
        self.assertIn('status', output)
        self.assertIn('error', output)
        self.assertEqual(expected_status_code, output['status'], "Expected status code not returned")
        self.assertIn(expected_error_msg, output['error'], "Expected error message not returned")      

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()    
