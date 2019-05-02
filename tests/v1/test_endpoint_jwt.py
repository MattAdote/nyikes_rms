import unittest
import os, datetime, jwt
import json, pdb

from .contexts import   create_api_server, db, \
                        endpoint_validate_user_token, endpoint_parse_access_token_payload, \
                        SuperUser, Member

from app.api.v1.utils import DATE_FORMAT

class TestEndpointJwtFunctions(unittest.TestCase):
    """This class represents the endpoint_jwt functions test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
        self.validate_user_token = endpoint_validate_user_token
        self.parse_access_token_payload = endpoint_parse_access_token_payload

        # Generate a dummy user token
        dummy_user_token = jwt.encode(
            {
                "id": "1",
                "username":"dummy_username",
                "type":"admin",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
            },
            self.app.config['SECRET']
        )
        # Generate an access token
        access_token = jwt.encode(
            {
                "username": "dummy_username", # as above
                "user_token":dummy_user_token.decode('UTF-8'),
                "super":"True",
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
            },
            self.app.config['SECRET']
        )
        # decode the access token payload
        self.access_token_payload = jwt.decode(access_token, self.app.config['SECRET'])

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_function_endpoint_validate_user_token_returns_jwt_user_token_payload(self):
        """
            Test that endpoint_validate_user_token() returns jwt user_token's payload
        """
        # Create new superuser first
        input_1 = {
                    "username": "dummy_username",
                    "password": "dummy123"                
        }
        self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        with self.app.app_context():
            access_token_payload = jwt.decode(res.json['data']['access_token'], self.app.config['SECRET'])

            # Get user from db
            if access_token_payload['super'] == "True":
                user = SuperUser.query.filter_by(username=access_token_payload['username']).first()
            else:
                user = Member.query.filter_by(username=access_token_payload['username']).first()
                
            user_secret = DATE_FORMAT.format(user.lastLoggedOut)
        
            # Decode user's token
            user_token_payload = jwt.decode(access_token_payload['user_token'], user_secret)

            # Now the testing bits       
            expected_output = user_token_payload
            
            output = self.validate_user_token(access_token_payload)

        assert type(output) == dict
        self.assertTrue(
            all(item in output.items() for item in expected_output.items()), 
            'Output returned is not equal to expected output: \n \
            output = "{}" INSTEAD OF "{}" \n '.format(output, expected_output)             
        )

    def test_function_endpoint_parse_access_token_payload_returns_error_on_missing_username(self):
        """
            Test that endpoint_parse_access_token_payload() returns error if username missing
        """

        expected_output = {
            'status'    :   400,
            "headers"   :   {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                        'error="invalid_request"; '
                                        'error_description="username missing in access_token payload" '
            }
        }
        
        # pop off the username key
        self.access_token_payload.pop('username')
        
        output = self.parse_access_token_payload(self.access_token_payload)

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
    def test_function_endpoint_parse_access_token_payload_returns_error_on_null_or_empty_username(self):
        """
            Test that endpoint_parse_access_token_payload() returns error if username null or empty
        """

        expected_output = {
            'status'    :   400,
            "headers"   :   {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="username missing a value in access_token payload" '
            }
        }
        
        # pop off the username key
        self.access_token_payload['username'] = ''
        
        output = self.parse_access_token_payload(self.access_token_payload)

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
    def test_function_endpoint_parse_access_token_payload_returns_error_on_missing_user_token(self):
        """
            Test that endpoint_parse_access_token_payload() returns error if user_token missing
        """

        expected_output = {
            'status'    :   400,
            "headers"   :   {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="user_token missing in access_token payload" '
            }
        }
        
        # pop off the username key
        self.access_token_payload.pop('user_token')
        
        output = self.parse_access_token_payload(self.access_token_payload)

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
    def test_function_endpoint_parse_access_token_payload_returns_error_on_null_or_empty_user_token(self):
        """
            Test that endpoint_parse_access_token_payload() returns error if user_token empty or null
        """

        expected_output = {
            'status'    :   400,
            "headers"   :   {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="user_token missing a value in access_token payload" '
            }
        }
        
        # set user_token key to empty value
        self.access_token_payload['user_token'] = ''
        
        output = self.parse_access_token_payload(self.access_token_payload)

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
    def test_function_endpoint_parse_access_token_payload_returns_error_on_missing_super_key(self):
        """
            Test that endpoint_parse_access_token_payload() returns error if super key missing
        """

        expected_output = {
            'status'    :   400,
            "headers"   :   {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="super missing in access_token payload" '
            }
        }
        
        # pop off the super key
        self.access_token_payload.pop('super')
        
        output = self.parse_access_token_payload(self.access_token_payload)

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
    def test_function_endpoint_parse_access_token_payload_returns_error_on_null_or_empty_super_key(self):
        """
            Test that endpoint_parse_access_token_payload() returns error if super key empty or null
        """

        expected_output = {
            'status'    :   400,
            "headers"   :   {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="super missing a value in access_token payload" '
            }
        }
        
        # set the super key to empty
        self.access_token_payload['super'] = ''
        
        output = self.parse_access_token_payload(self.access_token_payload)

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
    def test_function_endpoint_parse_access_token_payload_returns_error_on_super_key_value_not_true_or_false(self):
        """
            Test that endpoint_parse_access_token_payload() returns error if super key value not true or false
        """

        expected_output = {
            'status'    :   400,
            "headers"   :   {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                    'error="invalid_request"; '
                                    'error_description="super has incorrect value" '
            }
        }
        
        # set the super key value to an incorrect one
        self.access_token_payload['super'] = 'Truthy'
        
        output = self.parse_access_token_payload(self.access_token_payload)

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

    

    # def test_function_parse_token_returns_error_if_token_tampered_with(self):
    #     """
    #         Test that an error is returned if the token is tampered with
    #     """
    #     expected_output = {
    #         "status" : 401,
    #         "headers": {
    #             "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
    #                                     'error="invalid_token"; '
    #                                     'error_description="{err_description}" ' 
    #         }
    #     }
    #     # Create new superuser first
    #     input_1 = {
    #                 "username": "test_superuser",
    #                 "password": "super123"                
    #     }

    #     res_1 = self.client.post(
    #         'api/v1/superusers',
    #         data = json.dumps(input_1),
    #         content_type = 'application/json'
    #     )

    #     # Login the superuser
    #     res_2 = self.client.post(
    #         'api/v1/superusers/login',
    #         data = json.dumps(input_1),
    #         content_type = 'application/json'
    #     ) 

    #     # Get the superuser data that we expect to receive
    #     dirty_token = res_2.json['data']['access_token'] + 'b'
    #     input_3 = {
    #         "username": res_2.json['data']['username'],
    #         "user_token":dirty_token
    #     }
        
    #     output = self.parse_token(input_3)

    #     # Assert
    #     self.assertIn('status', output, "status_code key is missing!")
    #     self.assertIn('headers', output, "headers info is missing!")
    #     self.assertIn('WWW-Authenticate', output['headers'], "WWW-Authenticate key missing")
        
    #     self.assertNotEqual(output['status'], "", "No status_code information provided")
    #     self.assertNotEqual(output['headers'], "", "No headers information provided")
    #     self.assertNotEqual(output['headers']['WWW-Authenticate'], "", "No error information provided")

    #     self.assertIsInstance(output['headers']['WWW-Authenticate'], str, "Error info not string data")
    
    # def test_function_parse_token_returns_error_on_usernames_not_matching_but_token_genuine(self):
    #     """
    #         Test that an error is returned if the username supplied with the
    #         request does not match the username that is in the decoded token
    #     """
    #     expected_output = {
    #         "status" : 400,
    #         "headers": {
    #             "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
    #                                     'error="invalid_request"; '
    #                                     'error_description="Identity mismatch" '
    #         }
    #     }

    #     # Create new superuser first
    #     input_1 = {
    #                 "username": "test_superuser",
    #                 "password": "super123"                
    #     }

    #     res_1 = self.client.post(
    #         'api/v1/superusers',
    #         data = json.dumps(input_1),
    #         content_type = 'application/json'
    #     )

    #     # Login the superuser        
    #     res_2 = self.client.post(
    #         'api/v1/superusers/login',
    #         data = json.dumps(input_1),
    #         content_type = 'application/json'
    #     ) 

    #     # Get the superuser data that we expect to receive
    #     spoofed_username = 'user_mjanja'
    #     input_3 = {
    #         "username": spoofed_username,
    #         "user_token":res_2.json['data']['access_token']
    #     }
        
    #     output = self.parse_token(input_3)
        
    #     self.assertIn('status', output, "status_code key is missing!")
    #     self.assertIn('headers', output, "headers info is missing!")
    #     self.assertIn('WWW-Authenticate', output['headers'], "WWW-Authenticate key missing")
        
    #     self.assertNotEqual(output['status'], "", "No status_code information provided")
    #     self.assertNotEqual(output['headers'], "", "No headers information provided")
    #     self.assertNotEqual(output['headers']['WWW-Authenticate'], "", "No error information provided")

    #     self.assertIsInstance(output['headers']['WWW-Authenticate'], str, "Error info not string data")

    #     self.assertTrue(
    #         all(item in output.items() for item in expected_output.items()), 
    #         'Error message returned has an incorrect value: \n \
    #         status = "{}" INSTEAD OF "{}" \n \
    #         headers = "{}" \nINSTEAD OF\n {} '.format(
    #             output['status'], expected_output['status'],
    #             output['headers'], expected_output['headers']
    #         )             
    #     )

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()    
