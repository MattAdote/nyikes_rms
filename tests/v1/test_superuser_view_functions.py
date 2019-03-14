import unittest
import os, datetime, jwt
import json, pdb

from .contexts import   create_api_server, db, \
                        BaseModel, \
                        SuperUser, superuser_schema, \
                        verify_credentials, start_session, end_session, generate_token, validate_token

class TestSuperuserViewFunctions(unittest.TestCase):
    """This class represents the superuser view functions test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        
        self.app = create_api_server("testing")
        self.client = self.app.test_client()
        self.superuser = SuperUser
        self.verify_credentials = verify_credentials
        self.start_session = start_session
        self.end_session = end_session
        self.generate_token = generate_token
        self.validate_token = validate_token

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
        with self.app.app_context():
            output = self.verify_credentials(input_1)
        
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

    # def test_function_start_session_A_sets_lastLoggedIn_attr(self):
    #     """ Tests that the function to start a session sets the lastLoggedIn attr"""
    
    #     # the flow:
    #     # create a superuser record
    #     # get a superuser object from the returned record
    #     # set the old lastLoggedIn attr to one of my own
    #     # start a new session
    #     # confirm that the lastLoggedIn attr has changed by comparing it with the current value

    #     # First, create a new superuser record
    #     input_1 = {
    #                 "username": "test_superuser",
    #                 "password": "super123"                
    #     }
    #     res_1 = self.client.post(
    #         'api/v1/superusers',
    #         data = json.dumps(input_1),
    #         content_type = 'application/json'
    #     )

    #     lastLoggedIn_to_set = "2019-Jan-01 01:29:59"
    #     with self.app.app_context():
    #         obj_superuser = SuperUser.query.filter_by(
    #             username=res_1.json['data']['username'],
    #             password=res_1.json['data']['password']
    #         ).first()
    #         obj_superuser.lastLoggedIn = datetime.datetime.strptime(lastLoggedIn_to_set)
    #         old_lastLoggedIn = obj_superuser.lastLoggedIn

    #         self.start_session(obj_superuser)
        
    #     self.assertTrue(obj_superuser.lastLoggedIn > old_lastLoggedIn, 'Session Time not Greater than old time')

    def test_function_start_session_B_persists_superuser_obj_with_new_lastLoggedIn_attr_to_db(self):
        """ 
            Tests that the function to start a session persists the superuser obj to db with
            the new lastLoggedIn attribute    
        """
        # the flow:
        # create a superuser record
        # get a superuser object from the returned record
        # set the old lastLoggedIn attr to one of my own
        # start a new session
        # confirm that the objet is saved by retrieving it from db
        # compare the db value with the earlier object to check that they match

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

        with self.app.app_context():
            obj_superuser = SuperUser.query.get(res_1.json['data']['id'])
            self.start_session(obj_superuser)
            db_obj_superuser = SuperUser.query.filter_by(
                username=res_1.json['data']['username'],
                password=res_1.json['data']['password']
            ).first()

        self.assertEqual(db_obj_superuser.lastLoggedIn, obj_superuser.lastLoggedIn, "DB and Object Not Equal")
    
    def test_function_start_session_C_returns_lastLoggedOut_attr_as_string(self):
        """ Tests that the function to start a session returns the lastLoggedOut attr"""
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
        with self.app.app_context():
            obj_superuser = SuperUser.query.get(res_1.json['data']['id'])
            output = self.start_session(obj_superuser)

        assert(type(output) == str)
    
    def test_function_end_session_returns_bool_True_on_success(self):
        """ Tests that the function to end a session returns the boolean True"""
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
        with self.app.app_context():
            # No need to start a session first because:
            # 1. start_session() begins with ending all other sessions
            # 2. end_session() just updates the log out time to now and returns true
            # We're testing that the log out update is working
            obj_superuser = SuperUser.query.get(res_1.json['data']['id'])
            output = self.end_session(obj_superuser)


        assert(type(output) == bool)
        self.assertTrue(output)
    
    def test_function_generate_token_returns_jwt_token(self):
        """ Tests that the function to generate a token returns a jwt token """

        # the flow:
        # supply secret as last logged out time of object
        # call generate_token
        # evaluate response to check that jwt.decode returns a dict

        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        with self.app.app_context():
            obj_superuser = SuperUser.query.get(res_1.json['data']['id'])
            superuser_secret = self.start_session(obj_superuser)
            token = self.generate_token(obj_superuser, superuser_secret)
        decoded_token = jwt.decode(token, superuser_secret)
        
        assert(type(decoded_token) == dict)

    
    def test_function_validate_token_returns_token_payload_on_successful_decode(self):
        """ Test that function validate_token returns the user's token payload """
        
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        with self.app.app_context():
            obj_superuser = SuperUser.query.get(res_1.json['data']['id'])
            superuser_secret = self.start_session(obj_superuser)
            token = self.generate_token(obj_superuser, superuser_secret)
            server_access_token_payload = {
                "username"      :   obj_superuser.username,
                "user_token"    :   token.decode('UTF-8'), 
                "super"         :   "True",
                "exp"           :   5
            }
            validated_token_payload = self.validate_token(server_access_token_payload)

        self.assertIn('username', validated_token_payload, "user_token payload is missing 'username' key")
        self.assertEqual(obj_superuser.username, validated_token_payload['username'], "Payload username invalid")


    def test_function_validate_token_returns_error_on_payload_input_missing_username(self):
        """ 
            Test that function validate_token returns an error if
            the input access_token_payload is missing key 'username'
        """

        expected_output =  {
            "status" : 400,
            "headers": {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                        'error="invalid_request"; '
                                        'error_description="username missing in access_token payload" '
            }   
        }

        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        with self.app.app_context():
            obj_superuser = SuperUser.query.get(res_1.json['data']['id'])
            superuser_secret = self.start_session(obj_superuser)
            token = self.generate_token(obj_superuser, superuser_secret)
            server_access_token_payload = {
                # "username"      :   obj_superuser.username,
                "user_token"    :   token.decode('UTF-8'), 
                "super"         :   "True",
                "exp"           :   5
            }
            output = self.validate_token(server_access_token_payload)

        self.assertIn('status', output)
        self.assertEqual(output['status'], expected_output['status'], "\nOutput status code does not match Expected")

        self.assertIn('headers', output)
        self.assertEqual(output['headers'], expected_output['headers'], "\nOutput Headers do not match Expected")

    def test_function_validate_token_returns_error_on_payload_input_empty_username(self):
        """ 
            Test that function validate_token returns an error if
            the input access_token_payload key 'username' is empty
        """
        expected_output =  {
            "status" : 400,
            "headers": {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                        'error="invalid_request"; '
                                        'error_description="username missing a value in access_token payload" '
            }   
        }
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        with self.app.app_context():
            obj_superuser = SuperUser.query.get(res_1.json['data']['id'])
            superuser_secret = self.start_session(obj_superuser)
            token = self.generate_token(obj_superuser, superuser_secret)
            server_access_token_payload = {
                "username"      :   "",
                "user_token"    :   token.decode('UTF-8'), 
                "super"         :   "True",
                "exp"           :   5
            }
            output = self.validate_token(server_access_token_payload)

        self.assertIn('status', output)
        self.assertEqual(output['status'], expected_output['status'], "\nOutput status code does not match Expected")

        self.assertIn('headers', output)
        self.assertEqual(output['headers'], expected_output['headers'], "\nOutput Headers do not match Expected")
    
    def test_function_validate_token_returns_error_on_payload_input_missing_token(self):
        """ 
            Test that function validate_token returns an error if
            the input access_token_payload is missing key 'user_token'
        """

        expected_output =  {
            "status" : 400,
            "headers": {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                        'error="invalid_request"; '
                                        'error_description="user_token missing in access_token payload" '
            }   
        }

        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        with self.app.app_context():
            obj_superuser = SuperUser.query.get(res_1.json['data']['id'])
            superuser_secret = self.start_session(obj_superuser)
            token = self.generate_token(obj_superuser, superuser_secret)
            server_access_token_payload = {
                "username"      :   obj_superuser.username,
                # "user_token"    :   token.decode('UTF-8'), 
                "super"         :   "True",
                "exp"           :   5
            }
            output = self.validate_token(server_access_token_payload)

        self.assertIn('status', output)
        self.assertEqual(output['status'], expected_output['status'], "\nOutput status code does not match Expected")

        self.assertIn('headers', output)
        self.assertEqual(output['headers'], expected_output['headers'], "\nOutput Headers do not match Expected")

    def test_function_validate_token_returns_error_on_payload_input_empty_token(self):
        """ 
            Test that function validate_token returns an error if
            the input access_token_payload key 'user_token' is empty
        """
        expected_output =  {
            "status" : 400,
            "headers": {
                "WWW-Authenticate" :    'Bearer realm="NYIKES RMS"; '
                                        'error="invalid_request"; '
                                        'error_description="user_token missing a value in access_token payload" '
            }   
        }
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        res_1 = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        with self.app.app_context():
            obj_superuser = SuperUser.query.get(res_1.json['data']['id'])
            superuser_secret = self.start_session(obj_superuser)
            token = self.generate_token(obj_superuser, superuser_secret)
            server_access_token_payload = {
                "username"      :   obj_superuser.username,
                "user_token"    :   "", 
                "super"         :   "True",
                "exp"           :   5
            }
            output = self.validate_token(server_access_token_payload)

        self.assertIn('status', output)
        self.assertEqual(output['status'], expected_output['status'], "\nOutput status code does not match Expected")

        self.assertIn('headers', output)
        self.assertEqual(output['headers'], expected_output['headers'], "\nOutput Headers do not match Expected")
    


    def test_function_validate_token_returns_error_on_failed_decode(self):
        """ 
            Test that function validate_token returns an error if
            the token decode operation fails on the user's token
        """
    
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()    
