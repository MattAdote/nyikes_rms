import unittest
import os
import json, pdb

from .contexts import create_api_server, db

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
                'Authorization':  "Bearer {}".format(res_2.json['data']['access_token'])
        }
        res_3 = self.client.get(
            'api/v1/superusers/{}'.format(superuser_id),
            data = json.dumps({'username': res_2.json['data']['username']}),
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
                'Authorization':  "Bearer {}".format(res_2.json['data']['access_token'])
        }
        res_3 = self.client.get(
            'api/v1/superusers/{}'.format(superuser_id),
            data = json.dumps({'username': res_2.json['data']['username']}),
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
                'Authorization':  "Bearer {}".format(res_2.json['data']['access_token'])
        }
        res_3 = self.client.get(
            'api/v1/superusers/{}'.format(superuser_id),
            data = json.dumps({'username': res_2.json['data']['username']}),
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
                'Authorization':  "Bearer {}".format(res_2.json['data']['access_token'])
        }
        res_3 = self.client.get(
            'api/v1/superusers',
            data = json.dumps({'username': res_2.json['data']['username']}),
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

    
    def tearDown(self):
        """teardown all initialized variables."""
        
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
