# import pdb

import unittest
import os
import json

from .contexts import validate_request_data, validate_route_param, invalid_param, check_is_empty

class TestUtilitiesFunctions(unittest.TestCase):
    """This class represents the utilities test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.validate_request_data = validate_request_data
        self.validate_route_param = validate_route_param
        self.invalid_param = invalid_param
        self.check_is_empty = check_is_empty

    def test_validate_required_fields_present(self):
        """Test that required fields are present"""
        input_data =  [     {   "req_field_1": "Required is present",
                                "req_field_2": "Required is present"
                            },
                            {
                                "not_required_1": [],
                                "not_required_2" : []
                            }
                        ]
        input_required_fields = ['req_field_1', 'req_field_2']

        output = self.validate_request_data(input_data, input_required_fields)

        if 'error' not in output:
            self.assertIn("req_field_1", output)
            self.assertIn("req_field_2", output)

    def test_validate_required_fields_not_empty(self):
        """Test that required fields are not empty"""
        input_data =  [     {   "req_field_1": "Required is present",
                                "req_field_2": ""
                            },
                            {
                                "not_required_1": [],
                                "not_required_2" : []
                            }
                        ]
        input_required_fields = ['req_field_1', 'req_field_2']

        output = self.validate_request_data(input_data, input_required_fields)

        self.assertIn('error', output)
        self.assertIn('Required field(s) empty', output['error'], 'A required field is empty')
        
    def test_validate_remove_empty_non_required(self):
        """Test that empty non required fields are removed from request data"""
        
        input_data =  [     {   "req_field_1": "Required is present",
                                "req_field_2": "Required is present"
                            },
                            {
                                "not_required_1": [],
                                "not_required_2" : ""
                            }
                        ]
        input_required_fields = ['req_field_1', 'req_field_2']

        expected_output = { "req_field_1": "Required is present",
                            "req_field_2": "Required is present",
                            "not_required_1": []
                        }

        output = self.validate_request_data(input_data, input_required_fields)

        self.assertTrue(all(item in output.items() for item in expected_output.items()))       
    
    def test_method_check_is_empty_returns_error_with_status_400(self):
        """Test that the check_is_empty method returns an error with status code 400"""
        
        input_data =  ''
        expected_output = {
            "status": 400,
            "error": "No data provided"
        }

        output = self.check_is_empty(input_data)

        # assert that the expected keys and values as above are present in output
        self.assertTrue(all(item in output.items() for item in expected_output.items()))

    def test_method_validate_route_param_returns_int(self):
        """Test that the route param can be converted to int"""
        input_1 = '1'

        output = self.validate_route_param(input_1)

        assert type(output) == int
    
    def test_method_validate_route_param_returns_error_if_not_int(self):
        """Test that the route param can be converted to int"""
        input_1 = ''

        output = self.validate_route_param(input_1)

        self.assertIn('error', output)

    def test_method_invalid_param_returns_a_dict_with_error_key(self):
        """Test that the invalid_param method returns a dict that contains an 'error' key and status is 400"""

        input_1_invalid_param = {
            'topic': '',
            'location': '',
            'happening_on': ''
        }
        input_2_expected_param = {
            'topic': '',
            'location': '',
            'happeningOn': ''
        }

        expected_status_code = 400
        expected_error_msg = 'Invalid parameter(s):'

        output = self.invalid_param(input_1_invalid_param, input_2_expected_param)


        assert type(output) == dict
        self.assertIn('status', output)
        self.assertIn('error', output)
        self.assertEqual(expected_status_code, output['status'])
        self.assertIn(expected_error_msg, output['error'])


    def tearDown(self):
        """teardown all initialized variables."""

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
