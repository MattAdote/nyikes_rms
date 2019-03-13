import unittest
import os, datetime, jwt
import json, pdb

from .contexts import   create_api_server, db, parse_token, parse_auth_header

class TestWrapperFunctions(unittest.TestCase):
    """This class represents the wrapper functions test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
        self.parse_token = parse_token
        self.parse_auth_header = parse_auth_header

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()
    
    def test_function_parse_auth_header_returns_jwt_token(self):
        """
            Test that parse_auth_header() returns jwt token
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
        # make a call to GET /superusers
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_2.json['data']['user_token'])
        }
        res_3 = self.client.get(
            'api/v1/superusers',
            data = json.dumps({'username': res_1.json['data']['username']}),
            headers = headers   
        )
        output = self.parse_auth_header(headers['Authorization'])
        token_data = output.split('.')
        
        assert type(output) == str
        self.assertEqual(len(token_data), 3, "JWT Token not returned. Incorrect num parts on split ")

    def test_function_parse_auth_header_returns_error_on_missing_or_bad_header_info(self):
        """
            Test that parse_auth_header() returns jwt token
        """

        expected_output = {
            'status'    :   400,
            "headers"   :   {
                "WWW-Authenticate" :'Bearer realm="NYIKES_RMS" '
            }
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
        for test_scenario in [1,2]:
            # scenario 1, Authorization header missing a value totally.
            if test_scenario == 1:
                headers = {
                        'Content-Type' : 'application/json',
                        'Authorization':  " "
                }
            else: # scenario 2, Authorization header is missing token
                headers = {
                        'Content-Type' : 'application/json',
                        'Authorization':  "Bearer "
                }

            # make a call to GET /superusers
            res_3 = self.client.get(
                'api/v1/superusers',
                data = json.dumps({'username': res_1.json['data']['username']}),
                headers = headers   
            )
            output = self.parse_auth_header(headers['Authorization'])
            
            assert type(output) == dict
            self.assertIn('status', output, "status_code key is missing!")
            self.assertIn('headers', output, "headers info is missing!")
            self.assertIn('WWW-Authenticate', output['headers'], "WWW-Authenticate key missing")
            
            self.assertNotEqual(output['status'], "", "No status_code information provided")
            self.assertNotEqual(output['headers'], "", "No headers information provided")
            self.assertNotEqual(output['headers']['WWW-Authenticate'], "", "No error information provided")

            self.assertIsInstance(output['headers']['WWW-Authenticate'], str, "Error info not string data")

            self.assertTrue(
                all(item in output.items() for item in expected_output.items()), 
                'Error message returned has an incorrect value: \n \
                status = "{}" INSTEAD OF "{}" \n \
                headers = "{}" \nINSTEAD OF\n {} '.format(
                    output['status'], expected_output['status'],
                    output['headers'], expected_output['headers']
                )             
            )

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
        expected_output = {
            "status" : 401,
            "headers": {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                        'error="invalid_token"; '
                                        'error_description="{err_description}" ' 
            }
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
        dirty_token = res_2.json['data']['user_token'] + 'b'
        input_3 = {
            "username": res_2.json['data']['username'],
            "user_token":dirty_token
        }
        
        output = self.parse_token(input_3)

        # Assert
        self.assertIn('status', output, "status_code key is missing!")
        self.assertIn('headers', output, "headers info is missing!")
        self.assertIn('WWW-Authenticate', output['headers'], "WWW-Authenticate key missing")
        
        self.assertNotEqual(output['status'], "", "No status_code information provided")
        self.assertNotEqual(output['headers'], "", "No headers information provided")
        self.assertNotEqual(output['headers']['WWW-Authenticate'], "", "No error information provided")

        self.assertIsInstance(output['headers']['WWW-Authenticate'], str, "Error info not string data")
    
    def test_function_parse_token_returns_error_on_usernames_not_matching_but_token_genuine(self):
        """
            Test that an error is returned if the username supplied with the
            request does not match the username that is in the decoded token
        """
        expected_output = {
            "status" : 400,
            "headers": {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                        'error="invalid_request"; '
                                        'error_description="Identity mismatch" '
            }
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
        
        self.assertIn('status', output, "status_code key is missing!")
        self.assertIn('headers', output, "headers info is missing!")
        self.assertIn('WWW-Authenticate', output['headers'], "WWW-Authenticate key missing")
        
        self.assertNotEqual(output['status'], "", "No status_code information provided")
        self.assertNotEqual(output['headers'], "", "No headers information provided")
        self.assertNotEqual(output['headers']['WWW-Authenticate'], "", "No error information provided")

        self.assertIsInstance(output['headers']['WWW-Authenticate'], str, "Error info not string data")

        self.assertTrue(
            all(item in output.items() for item in expected_output.items()), 
            'Error message returned has an incorrect value: \n \
            status = "{}" INSTEAD OF "{}" \n \
            headers = "{}" \nINSTEAD OF\n {} '.format(
                output['status'], expected_output['status'],
                output['headers'], expected_output['headers']
            )             
        )

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()    
