import unittest
import os, datetime, jwt
import json, pdb

from .contexts import   create_api_server, db, parse_token

class TestWrapperFunctions(unittest.TestCase):
    """This class represents the wrapper functions test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
        self.parse_token = parse_token

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_function_parse_token_returns_expected_kwargs(self):
        """
            Test that the expected kwargs are returned
        """
        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }

        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_2 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        ) 

        # Get the superuser data that we expect to receive
        input_3 = {
            "username": res_2.json['data']['username'],
            "user_token":res_2.json['data']['user_token']
        }

        output = self.parse_token(input_3)

        # Assert that all is well
        self.assertIn('access_token', output, 'Key, access_token missing')
        self.assertIn('username', output['access_token'], 'Key, username, missing in access_token')
        self.assertIn('user_token', output['access_token'], 'Key, user_token, missing in access_token')

        self.assertNotEqual(output['access_token']['username'], "", 'username has no value')
        self.assertNotEqual(output['access_token']['user_token'], "", 'user_token has no value')

    def test_function_parse_token_returns_error_if_token_tampered_with(self):
        """
            Test that an error is returned if the token is tampered with
        """

        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }

        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_2 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        ) 

        # Get the superuser data that we expect to receive
        dirty_token = res_2.json['data']['user_token'] + 'b'
        input_3 = {
            "username": res_2.json['data']['username'],
            "user_token":dirty_token
        }
        
        output = self.parse_token(input_3)

        # Assert
        self.assertIn('error', output, 'Error not thrown on dirty token')
        self.assertNotEqual(output['error'], "", 'No error message provided')
    
    def test_function_parse_token_returns_error_on_usernames_not_matching_but_token_genuine(self):
        """
            Test that an error is returned if the username supplied with the
            request does not match the username that is in the decoded token
        """
        expected_error = {
            "status" : 404,
            "error" : "Token error: Identity mismatch"
        }

        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }

        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser        
        res_2 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        ) 

        # Get the superuser data that we expect to receive
        spoofed_username = 'user_mjanja'
        input_3 = {
            "username": spoofed_username,
            "user_token":res_2.json['data']['user_token']
        }
        
        output = self.parse_token(input_3)

        # Assert
        self.assertIn('error', output, 'Error not thrown on username mismatch')
        self.assertTrue(
            all(item in output.items() for item in expected_error.items()), 
            'Error message returned has at least one incorrect value: \n \
            status = "{}" INSTEAD OF "{}"\n \
            error = "{}" INSTEAD OF "{}" '.format(
                output['status'], expected_error['status'],
                output['error'], expected_error['error']
            )
        )
        self.assertNotEqual(output['error'], "", 'No error message provided')

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()    
