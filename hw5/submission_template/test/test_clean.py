import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

import json


from src.clean import *


class CleanTest(unittest.TestCase):
    def setUp(self):
        # You might want to load the fixture files as variables, and test your code against them. Check the fixtures folder.
        # print("setting up...")

        self.test_dir_path = "test/fixtures/"

        

    def test_title(self):
        with open(self.test_dir_path + "test_1.json") as file:
            print("Test 1: ")
            # No title or title_text and thus the output should be None
            for line in file:
                json_data = load_json(line.rstrip())
                t_json = validate_and_transform(json_data)
                # print(t_json)
                message = """Posts that don’t have either "title" or "title_text" should be removed."""
                self.assertEqual(t_json, None, message)
            
            print("OK")

    def test2(self):
        with open(self.test_dir_path + "test_2.json") as file:
            print("test 2:")
            # datetime in createdAt doesn't match the format and thus output should be None
            for line in file:
                json_data = load_json(line.rstrip())
                message = "createdAt dates that don’t pass the ISO datetime standard should be removed."
                self.assertEqual(validate_datetime_exists(json_data), True, message)
                t_json = validate_and_transform(json_data)

                # print(t_json)
                self.assertEqual(t_json, None, message)

            print("OK")

    def test3(self):
        with open(self.test_dir_path + "test_3.json") as file:

            print("test 3:")
            # Invalid JSON dictionary so output should be None
            for line in file:
                json_data = load_json(line.rstrip())
                message = "Any lines that contain invalid JSON dictionaries should be ignored."
                self.assertEqual(json_data, None, message)
            
            print("OK")

    def test4(self):
        with open(self.test_dir_path + "test_4.json") as file:
            print("test 4:")
            # author is null, N/A, or empty string and thus output should be None
            for line in file:
                json_data = load_json(line.rstrip())

                self.assertEqual(validate_author_not_null_or_na(json_data), False, "author is not null or NA")
                t_json = validate_and_transform(json_data)
                message = """Any lines for which "author" is null, N/A or empty."""
                self.assertEqual(t_json, None, message)
            
            print("OK")
    
    def test5(self):
        with open(self.test_dir_path + "test_5.json") as file:
            print("test 5:")
            # total_count is not cast-able to an int and thus output should be None
            for line in file:
                json_data = load_json(line.rstrip())
                t_json = validate_and_transform(json_data)
                message = """total_count is a string containing a cast-able number, total_count is cast to an int properly."""
                # print(t_json)
                self.assertEqual(t_json, None, message)
            
            print("OK")

    def test6(self):
        with open(self.test_dir_path + "test_6.json") as file:
            print("test 6:")
            # tags should be a list of words with each containing no spaces
            for line in file:
                json_data = load_json(line.rstrip())
                # len_tags_before = len(json_data["tags"])
                t_json = validate_and_transform(json_data)

                # len_tags_after = len(t_json["tags"])
                message = """The tags field gets split on spaces when given a tag containing THREE words (e.g., “nba basketball game”)."""
                # print(t_json["tags"])
                
                for tag in t_json["tags"]:
                    splitted = tag.split()
                    # print(tag, len(tag), splitted, len(splitted))
                    self.assertEqual(len(splitted), 1, message)
                
                print("OK")
                    

    
        
    
if __name__ == '__main__':
    unittest.main()