import unittest

import stringcase

class Test3rdPartyLibraryFunctions(unittest.TestCase):
    """This class represents the third party library functions test case"""

    def test_stringcase_method_to_convert_string_to_snakecase_returns_two_underscores(self):
        """
            This is actually a test to confirm buggy behaviour of the stringcase conversion
            utility's methods.
        """
        title_case_string = 'Title Case String'
        
        converted_string = stringcase.snakecase(title_case_string)

        assert('__' in converted_string)

