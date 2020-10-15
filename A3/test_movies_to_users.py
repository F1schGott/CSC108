"""Unit test for recommender_functions.movies_to_users"""
import unittest

from recommender_functions import movies_to_users

class TestMoviesToUsers(unittest.TestCase):

    def test_movies_to_users(self):
        actual = movies_to_users({1: {10: 3.0}, 2: {10: 3.5}})
        expected = {10: [1, 2]}
        self.assertEqual(actual, expected)

    # Add tests below to create a complete set of tests without redundant tests
    # Redundant tests are tests that would only catch bugs that another test
    # would also catch.
    
    def test_movies_to_users_both_empty_0_0(self):
        actual = movies_to_users({1: {}, 2: {}})
        expected = {}
        self.assertEqual(actual, expected)

    def test_movies_to_users_one_empty_1_0(self):
        actual = movies_to_users({1: {10: 3.0}, 2: {}})
        expected = {10: [1]}
        self.assertEqual(actual, expected)    
        
    def test_movies_to_users_one_empty_1_5(self):
        actual = movies_to_users({1: {}, 2: {10: 4.5, 11: 4.5, 12:3.0, 13: 5.0, 14:0}})
        expected = {10: [2], 11:[2], 12:[2], 13:[2], 14:[2]}
        self.assertEqual(actual, expected)
        
    def test_movies_to_users_no_common_3_3(self):
        actual = movies_to_users({1: {12: 3.0, 13:0, 22:0}, 2: {10: 4.5, 11: 4.5, 19:3.5}})
        expected = {10: [2], 11:[2], 12:[1], 13:[1], 22:[1], 19:[2]}
        self.assertEqual(actual, expected)    
        
    def test_movies_to_users_part_common_3_3(self):
        actual = movies_to_users({1: {12: 3.0, 13:0, 10:0}, 2: {10: 4.5, 11: 4.5, 13:4.5}})
        expected = {10: [1, 2], 11:[2], 12:[1], 13:[1,2]}
        self.assertEqual(actual, expected)    
        
    def test_movies_to_users_full_common_3_3(self):
        actual = movies_to_users({1: {12: 3.0, 13:0, 10:0}, 2: {12: 3.5, 13:0.5, 10:5}})
        expected = {10: [1, 2], 12:[1, 2], 13:[1, 2]}
        self.assertEqual(actual, expected)    

if __name__ == '__main__':
    unittest.main(exit=False)
