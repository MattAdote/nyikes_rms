import unittest
import os
import json, pdb

from .contexts import create_api_server

class TestMeetupsEndpoint(unittest.TestCase):
    """This class represents the meetup test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_api_server("testing")
        self.client = self.app.test_client()


    def test_endpoint_default_returns_json(self):
        """Test API endpoint is reachable and returns json"""
        res = self.client.get('api/v1/')       
        # pdb.set_trace()
        self.assertTrue(res.is_json, "Json not returned.")

        self.assertEqual(res.status_code, 200)
    
    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()