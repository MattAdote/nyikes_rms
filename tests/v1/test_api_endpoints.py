import unittest, pytest
import os
import json, pdb

from .contexts import create_api_server, db

scriptpath = os.path.realpath(__file__)
dirpath, filen = os.path.split(scriptpath)

class TestApiEndpoints(unittest.TestCase):
    """This class represents the meetup test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_api_server("testing")
        self.client = self.app.test_client()

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    @pytest.fixture
    def getLoggedInSuperuser(self, request):
        """
            This sets the loggedInSuperuser attribute to the
            TestApiEndpoints class so that the test functions
            can have access to the access_token and username
            of a logged in Superuser
        """
        
        self.setUp()
        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_1 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Assign the logged in superuser to the class
        request.cls.loggedInSuperuser = res_1.json['data']

    def test_endpoint_default_returns_json(self):
        """Test API endpoint is reachable and returns json"""
        res = self.client.get('api/v1/')       
        
        self.assertTrue(res.is_json, "Json not returned.")

        self.assertEqual(res.status_code, 200)
        
    def test_endpoint_post_superuser_returns_json(self):
        """Test API endpoint is reachable and returns json"""
        
        res = self.client.post('api/v1/superusers')       
        
        self.assertTrue(res.is_json, "Json not returned.")
    
    def test_endpoint_post_superuser_returns_error_on_incorrect_content_tyoe(self):
        """Test API endpoint returns error if incorrect or no content type given """
        res = self.client.post('api/v1/superusers')
        
        self.assertIn('error', res.json, 'Error not Returned')

        self.assertEqual(400, res.status_code)
        
    def test_endpoint_post_superuser_returns_error_if_required_field_empty(self):
        """Test API endpoint returns error if request fields are empty """

        res = self.client.post(
            'api/v1/superusers',
            data = json.dumps({
                    "username": "",
                    "password": ""                
            }),
            content_type = 'application/json'
        )

        self.assertIn('error', res.json)
        self.assertEqual(400, res.status_code)
    
    def test_endpoint_post_superuser_returns_new_user_with_id(self):
        """Test API endpoint returns newly created user with id """

        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }

        res = self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        self.assertIn('id', res.json['data'])
        self.assertEqual(res.json['data']['username'], input_1['username'], 'Username Supplied Not Username Returned')
        self.assertNotEqual(res.json['data']['username'], "", "Hashed password not returned. Empty string received")
    # def test_endpoint_patch_superuser_returns_json(self)
    #     assert False

    def test_endpoint_get_specific_superuser_returns_superuser_of_specified_id(self):
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
        expected_output = {
            "id": res_1.json['data']['id'],
            "username": res_1.json['data']['username']
        }
        # Login the superuser
        res_2 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        
        # make a call to GET /superusers/<superuser_id>
        superuser_id = res_1.json['data']['id']
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_2.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_2.json['data']['username']
        }
        res_3 = self.client.get(
            'api/v1/superusers/{}'.format(superuser_id),
            data = json.dumps({}),
            headers = headers   
        )       

        self.assertEqual( res_3.json['data']['id'], expected_output['id'], "\nReturned id does not match Expected id")
        self.assertEqual( res_3.json['data']['username'], expected_output['username'], "\nReturned username does not match Expected username") 
    
    def test_endpoint_get_specific_superuser_returns_error_if_user_not_found(self):
        expected_output = {
            "status": 404,
            "error": "User not found. Likely does not exist"
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
        
        # make a call to GET /superusers/<superuser_id>
        superuser_id = 10201
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_2.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_2.json['data']['username']
        }
        res_3 = self.client.get(
            'api/v1/superusers/{}'.format(superuser_id),
            data = json.dumps({}),
            headers = headers   
        )       

        self.assertIn('status', res_3.json)
        self.assertIn('error', res_3.json)

        self.assertEqual( res_3.json['status'], expected_output['status'], "\nReturned error does not match Expected id")
        self.assertEqual( res_3.json['error'], expected_output['error'], "\nReturned error does not match Expected username") 
    
    def test_endpoint_get_specific_superuser_returns_error_if_db_operation_fail(self):
        expected_output = {
            "status": 500,
            "error": "Database error. Check your input"
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
        
        # make a call to GET /superusers/<superuser_id>
        superuser_id = 'malicious input'
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_2.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_2.json['data']['username']
        }
        res_3 = self.client.get(
            'api/v1/superusers/{}'.format(superuser_id),
            data = json.dumps({}),
            headers = headers   
        )       

        self.assertIn('status', res_3.json)
        self.assertIn('error', res_3.json)

        self.assertEqual( res_3.json['status'], expected_output['status'], "\nReturned error does not match Expected id")
        self.assertEqual( res_3.json['error'], expected_output['error'], "\nReturned error does not match Expected username") 

    def test_endpoint_get_all_superusers_returns_json(self):
        """Test API endpoint is reachable and returns json"""
        
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
                'Authorization':  "Bearer {}".format(res_2.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_2.json['data']['username']
        }
        res_3 = self.client.get(
            'api/v1/superusers',
            data = json.dumps({}),
            headers = headers   
        )       
        self.assertTrue(res_3.is_json, "Json not returned.")
    
    def test_endpoint_login_superusers_returns_json(self):
        """Test API endpoint is reachable and returns json"""
        
        res = self.client.post('api/v1/superusers/login')       

        self.assertTrue(res.is_json, "Json not returned.")
        if not 'error' in res.json:
            self.assertEqual(res.status_code, 200)
        else:
            self.assertIn('error', res.json)

    def test_endpoint_login_superusers_returns_superuser_record(self):
        """Test API endpoint is reachable and returns json"""
        # Expected json output data fields
        expected_output_data_fields = ['id', 'username']

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

        # Assert that all is well
        self.assertTrue(res_2.is_json, "Json not returned.")
        self.assertEqual(res_2.status_code, 200)
        
        self.assertIn('id', res_2.json['data'], "id attribute is missing")
        self.assertIn('username', res_2.json['data'], "username attribute is missing")
        self.assertTrue(all(key in res_2.json['data'].keys() for key in expected_output_data_fields),
            "Received output data keys does not match Expected Output keys 100%"
        )

    def test_endpoint_post_settings_config_members_returns_json(self):
        """Test API endpoint is reachable and returns json"""
        
        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_1 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        
        # make a call to POST /settings/config/members
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_1.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_1.json['data']['username']
        }
        res_2 = self.client.post(
            'api/v1/settings/config/members',
            data = json.dumps({}),
            headers = headers   
        )
        
        # will need to find a better way to address this issue of checking that json returned
        # this is because this test breaks when I secure an endpoint with jwt
        self.assertTrue(res_2.is_json, "Json not returned.")
        
    def test_endpoint_post_settings_config_members_returns_error_on_incorrect_content_tyoe(self):
        """Test API endpoint returns error if incorrect or no content type given """
        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_1 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        
        # make a call to POST /settings/config/members
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_1.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_1.json['data']['username']
        }
        res_2 = self.client.post(
            'api/v1/settings/config/members',
            data = json.dumps({}),
            headers = headers   
        )

        self.assertIn('error', res_2.json, 'Error not Returned')

        self.assertEqual(400, res_2.status_code)

    def test_endpoint_post_settings_config_members_returns_error_if_required_field_empty(self):
        """Test API endpoint returns error if request fields are empty """

        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_1 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        
        # make a call to POST /settings/config/members
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_1.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_1.json['data']['username']
        }
        res_2 = self.client.post(
            'api/v1/settings/config/members',
            data = json.dumps({
                "class_name": "",
                "monthly_contrib_amount": ""                
            }),
            headers = headers,
            content_type = 'application/json'
        )

        self.assertIn('error', res_2.json)
        self.assertEqual(400, res_2.status_code)

    def test_endpoint_post_settings_config_members_returns_new_membership_class_record_with_id(self):
        """Test API endpoint returns newly created membership class record with id """
        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_1 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        
        # make a call to POST /settings/config/members
        input_data = {
            "class_name": "Test Class ABC",
            "monthly_contrib_amount": 1550.00
        }
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_1.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_1.json['data']['username']
        }
        res_2 = self.client.post(
            'api/v1/settings/config/members',
            data = json.dumps({
                "class_name": "Test Class ABC",
                "monthly_contrib_amount": 1550.00                
            }),
            headers = headers,
            content_type = 'application/json'
        )

        self.assertIn('id', res_2.json['data'])
        self.assertEqual(res_2.json['data']['class_name'], input_data['class_name'], 'class_name supplied Not class_name returned')
        self.assertEqual(res_2.json['data']['monthly_contrib_amount'], input_data['monthly_contrib_amount'], 'monthly_contrib_amount supplied Not monthly_contrib_amount returned')

    def test_endpoint_post_members_returns_json(self):
        """Test API endpoint is reachable and returns json"""
        
        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_1 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        # create membership class
        input_2 = {
            "class_name": "Test Class ABC",
            "monthly_contrib_amount": 1550.00
        }
        
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_1.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_1.json['data']['username']
        }
        # make a call to POST /settings/config/members
        res_2 = self.client.post(
            'api/v1/settings/config/members',
            data = json.dumps(input_2),
            headers = headers,
            content_type = 'application/json'
        )

        # make a call to POST /members
        input_3 = {
            "class_name" : res_2.json['data']['class_name'],
            "first_name" : "Test First Name",
            "middle_name" : "Jaribu la kati", 
            "last_name" : "Test last name", 
            "email" : "testmember@testdomain.com", 
            "phone_number" : "0700123456"
        }
        res_3 = self.client.post(
            'api/v1/members',
            headers = headers,
            content_type = 'application/json',
            data = json.dumps({}),
        )

        # confirm that json received
        self.assertTrue(res_3.is_json, "Json not returned.")
    
    def test_endpoint_post_members_returns_error_on_incorrect_content_tyoe(self):
        """Test API endpoint returns error if incorrect or no content type given """
        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_1 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        
        # make a call to POST /members
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_1.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_1.json['data']['username']
        }
        res_2 = self.client.post(
            'api/v1/members',
            data = json.dumps({}),
            headers = headers   
        )

        self.assertIn('error', res_2.json, 'Error not Returned')

        self.assertEqual(400, res_2.status_code)

    def test_endpoint_post_members_returns_error_if_required_field_empty(self):
        """Test API endpoint returns error if request fields are empty """

        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_1 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        
        # create membership class
        input_2 = {
            "class_name": "Test Class ABC",
            "monthly_contrib_amount": 1550.00
        }
        
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_1.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_1.json['data']['username']
        }
        # make a call to POST /settings/config/members
        res_2 = self.client.post(
            'api/v1/settings/config/members',
            data = json.dumps(input_2),
            headers = headers,
            content_type = 'application/json'
        )

        # make a call to POST /members
        input_3 = {
            "class_name" : res_2.json['data']['class_name'],
            "first_name" : "Test First Name",
            "middle_name" : "Jaribu la kati", 
            "last_name" : "", 
            "email" : "testmember@testdomain.com", 
            "phone_number" : "0700123456"
        }

        res_3 = self.client.post(
            'api/v1/members',
            data = json.dumps(input_3),
            headers = headers,
            content_type = 'application/json'
        )

        self.assertIn('error', res_3.json)
        self.assertEqual(400, res_3.status_code)

    def test_endpoint_post_members_returns_new_member_record_with_id(self):
        """Test API endpoint returns newly created member record with id """
        # Create new superuser first
        input_1 = {
                    "username": "test_superuser",
                    "password": "super123"                
        }
        self.client.post(
            'api/v1/superusers',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )

        # Login the superuser
        res_1 = self.client.post(
            'api/v1/superusers/login',
            data = json.dumps(input_1),
            content_type = 'application/json'
        )
        
        # create membership class
        input_2 = {
            "class_name": "Test Class ABC",
            "monthly_contrib_amount": 1550.00
        }
        
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(res_1.json['data']['access_token']),
                'X-NYIKES-RMS-User' : res_1.json['data']['username']
        }
        # make a call to POST /settings/config/members
        res_2 = self.client.post(
            'api/v1/settings/config/members',
            data = json.dumps(input_2),
            headers = headers,
            content_type = 'application/json'
        )

        # make a call to POST /members
        input_3 = {
            "class_name" : res_2.json['data']['class_name'],
            "first_name" : "Test First Name",
            "middle_name" : "Jaribu la kati", 
            "last_name" : "Test last name", 
            "email" : "testmember@testdomain.com", 
            "phone_number" : "0700123456"
        }

        res_3 = self.client.post(
            'api/v1/members',
            data = json.dumps(input_3),
            headers = headers,
            content_type = 'application/json'
        )
        # make the assertions
        self.assertIn('id', res_3.json['data'])
        self.assertEqual(res_3.json['data']['first_name'], input_3['first_name'], 'first_name returned Not first_name supplied ')
        self.assertEqual(res_3.json['data']['middle_name'], input_3['middle_name'], 'middle_name supplied Not middle_name returned')
        self.assertEqual(res_3.json['data']['last_name'], input_3['last_name'], 'last_name returned Not last_name supplied')
        self.assertEqual(res_3.json['data']['email'], input_3['email'], 'email returned Not email supplied')
        self.assertEqual(res_3.json['data']['phone_number'], input_3['phone_number'], 'monthly_contrib_amount returned Not monthly_contrib_amount supplied')
        self.assertEqual(res_3.json['data']['class_name'], input_3['class_name'], 'class_name returned Not class_name supplied')

    @pytest.mark.usefixtures("getLoggedInSuperuser")
    def test_endpoint_get_members_file_returns_error_on_no_membershipclass_records(self):
        """
            Test API endpoint returns error if no membership class records have been 
            defined yet.
        """
        expected_output = {
            "status": 404,
            "error" : "No membership class records defined"
        }
        # make a call to GET /members/file
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(self.loggedInSuperuser['access_token']),
                'X-NYIKES-RMS-User' : self.loggedInSuperuser['username']
        }
        res_3 = self.client.get(
            'api/v1/members/file',
            data = json.dumps({}),
            headers = headers   
        )
        # Make the assertions
        self.assertTrue(res_3.is_json, "Json not returned.")
        self.assertIn('status', res_3.json, 'status key missing in output')
        self.assertIn('error', res_3.json, 'error key is missing in output')

        self.assertTrue(
            all(item in res_3.json.items() for item in expected_output.items()), 
            'Output returned is not equal to expected output: \n \
            output = "{}" \n INSTEAD OF \n "{}" \n '.format(res_3.json, expected_output)             
        )

    @pytest.mark.usefixtures("getLoggedInSuperuser")
    def test_endpoint_get_members_file_returns__400_status_code_on_incorrect_content_tyoe(self):
        """Test API endpoint returns 401 status code if incorrect or no content type given """
        headers = {
                # 'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(self.loggedInSuperuser['access_token']),
                'X-NYIKES-RMS-User' : self.loggedInSuperuser['username']
        }
        res = self.client.get(
            'api/v1/members/file',
            data = json.dumps({}),
            headers = headers 
        )

        self.assertEqual(400, res.status_code)
    
    @pytest.mark.usefixtures("getLoggedInSuperuser")
    def test_endpoint_get_members_file_returns__xlsx_file_with_correct_content_type(self):
        """Test API endpoint returns .xlsx file with the ms-excel content-type """
        headers = {
                'Content-Type' : 'application/json',
                'Authorization':  "Bearer {}".format(self.loggedInSuperuser['access_token']),
                'X-NYIKES-RMS-User' : self.loggedInSuperuser['username']
        }

        # create membership class
        input_1 = {
            "class_name": "Test Class ABC",
            "monthly_contrib_amount": 1550.00
        }        
        # make a call to POST /settings/config/members
        res_1 = self.client.post(
            'api/v1/settings/config/members',
            data = json.dumps(input_1),
            headers = headers,
            content_type = 'application/json'
        )

        # make a call to GET /members/file
        res_2 = self.client.get(
            'api/v1/members/file',
            data = json.dumps({}),
            headers = headers 
        )

        # make the assertions
        self.assertEqual(res_2.content_type, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('content-disposition', res_2.headers)
        self.assertIn('attachment', res_2.headers['content-disposition'])

        assert type(res_2.data) == bytes

    @pytest.mark.usefixtures("getLoggedInSuperuser")
    def test_endpoint_post_members_file_returns__400_status_code_on_incorrect_content_tyoe(self):
        """Test API endpoint returns 401 status code if incorrect or no content type given """
        headers = {
                'Content-Type' : 'application/x-www-form-urlencoded-',
                'Authorization':  "Bearer {}".format(self.loggedInSuperuser['access_token']),
                'X-NYIKES-RMS-User' : self.loggedInSuperuser['username']
        }
        res = self.client.post(
            'api/v1/members/file',
            data = None,
            headers = headers 
        )

        self.assertEqual(400, res.status_code)
    
    @pytest.mark.usefixtures("getLoggedInSuperuser")
    def test_endpoint_post_members_file_returns_error_if_expected_file_parameter_name_incorrect(self):
        """ 
            Tests that the function returns an error if expected file field name parameter is
            incorrect
        """
        expected_file_parameter = 'addNewMembersFile'
        file_path = '{}/_resources/ex_member_records.xlsx'.format(dirpath)
        
        expected_output = {
            "status": 400,
            "error": 'File parameter: \'{}\' not found'.format(expected_file_parameter)
        }
        headers = {
                # 'Content-Type' : 'application/x-www-form-urlencoded',
                'Content-Type' : 'multipart/form-data',
                'Authorization':  "Bearer {}".format(self.loggedInSuperuser['access_token']),
                'X-NYIKES-RMS-User' : self.loggedInSuperuser['username']
        }        
        # make the call
        fh = open(file_path, 'rb')
        res = self.client.post(
            'api/v1/members/file',
            data = {
                expected_file_parameter + 's':fh
            },
            headers = headers,
        )
        fh.close()
        
        # make the assertions
        self.assertTrue(res.is_json, "Error not returned as JSON")
        
        # test the output
        output = res.json
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('error', output, 'error key is missing in output')

        self.assertEqual(output['status'], expected_output['status'])
        self.assertEqual(output['error'], expected_output['error'])
    
    @pytest.mark.usefixtures("getLoggedInSuperuser")
    def test_endpoint_post_members_file_returns_error_if_expected_file_parameter_name_missing(self):
        """ 
            Tests that the function returns an error if expected file field name parameter is
            missing
        """
        expected_file_parameter = 'addNewMembersFile'
        file_path = '{}/_resources/ex_member_records.xlsx'.format(dirpath)
        expected_output = {
            "status": 400,
            "error": 'File parameter: \'{}\' not found'.format(expected_file_parameter)
        }
        
        headers = {
                'Content-Type' : 'multipart/form-data',
                'Authorization':  "Bearer {}".format(self.loggedInSuperuser['access_token']),
                'X-NYIKES-RMS-User' : self.loggedInSuperuser['username']
        }
                
        # make the call
        fh = open(file_path, 'rb')
        res = self.client.post(
            'api/v1/members/file',
            data = {
                'random parameter name':fh
            },
            headers = headers,
        )
        fh.close()
        
        # make the assertions
        self.assertTrue(res.is_json, "Error not returned as JSON")
        
        # test the output
        output = res.json
        
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('error', output, 'error key is missing in output')

        self.assertEqual(output['status'], expected_output['status'])
        self.assertEqual(output['error'], expected_output['error'])

    @pytest.mark.usefixtures("getLoggedInSuperuser")
    def test_endpoint_post_members_file_returns_error_if_uploaded_file_not_excel_mimetype(self):
        """ 
            Tests that the function returns an error if mimetype of uploaded file is
            not the excel xlsx one.
        """
        file_path = '{}/_resources/ex_non_excel_file.docx'.format(dirpath)
        expected_file_parameter = 'addNewMembersFile'
        expected_file_mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        expected_output = {
            "status": 400,
            "error": 'Invalid file uploaded. File not .xlsx file'
        }
        
        headers = {
                'Content-Type' : 'multipart/form-data',
                'Authorization':  "Bearer {}".format(self.loggedInSuperuser['access_token']),
                'X-NYIKES-RMS-User' : self.loggedInSuperuser['username']
        }
                
        # make the call
        fh = open(file_path, 'rb')
        res = self.client.post(
            'api/v1/members/file',
            data = {
                expected_file_parameter:fh
            },
            headers = headers,
        )
        fh.close()
        
        # make the assertions
        self.assertTrue(res.is_json, "Error not returned as JSON")
        
        # test the output
        output = res.json
        
        self.assertIn('status', output, 'status key missing in output')
        self.assertIn('error', output, 'error key is missing in output')

        self.assertEqual(output['status'], expected_output['status'])
        self.assertEqual(output['error'], expected_output['error'])
    
    @pytest.mark.usefixtures("getLoggedInSuperuser")
    def test_endpoint_post_members_file_returns__xlsx_file_with_correct_content_type(self):
        """Test API endpoint returns updated xlsx file with the ms-excel content-type """
        
        file_to_upload = '{}/_resources/ex_member_records.xlsx'.format(dirpath)
        expected_file_parameter = 'addNewMembersFile'
        
        headers = {
                'Content-Type' : 'multipart/form-data',
                'Authorization':  "Bearer {}".format(self.loggedInSuperuser['access_token']),
                'X-NYIKES-RMS-User' : self.loggedInSuperuser['username']
        }

        fh = open(file_to_upload, 'rb')
        # make a call to GET /members/file
        res_2 = self.client.post(
            'api/v1/members/file',
            data = {expected_file_parameter:fh},
            headers = headers 
        )
        fh.close()

        # make the assertions
        self.assertEqual(res_2.content_type, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('content-disposition', res_2.headers)
        self.assertIn('attachment', res_2.headers['content-disposition'])

        assert type(res_2.data) == bytes

    def tearDown(self):
        """teardown all initialized variables."""
        
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
