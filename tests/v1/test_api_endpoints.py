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
        self.assertTrue(all(item in res.json['data'].items() for item in input_1.items()))
    
    # def test_endpoint_patch_superuser_returns_json(self):
    #     assert False

    # def test_endpoint_get_specific_superuser_returns_json(self):
    #     assert False

    def test_endpoint_get_all_superusers_returns_json(self):
        """Test API endpoint is reachable and returns json"""
        
        res = self.client.get('api/v1/superusers')       

        self.assertTrue(res.is_json, "Json not returned.")
        self.assertEqual(res.status_code, 200)
    
    def tearDown(self):
        """teardown all initialized variables."""
        
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
