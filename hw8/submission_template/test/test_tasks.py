import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

from src.compile_word_counts import *
from src.compute_pony_lang import *

import json


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        
        

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        
        res = compile_word_counts(self.mock_dialog)


        true_word_counts = open(self.true_word_counts)
        true_res = json.load(true_word_counts)

        # print("res", res)

        for key in true_res:
            if (key in res):
                for word in true_res[key]:
                    if (word in res[key]):
                        self.assertEqual(res[key][word], true_res[key][word])
                    else:
                        self.assertFalse(True)
            else:
                self.assertFalse(True)

        true_word_counts.close()

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        
        res = compute_pony_lang(self.true_word_counts, 100)

        true_tf_idfs = open(self.true_tf_idfs)
        true_res = json.load(true_tf_idfs)

        for key in true_res:
            if (key in res):
                for i in range(len(true_res[key])):
                    self.assertEqual(res[key][i], true_res[key][i])
            else:
                self.assertFalse(True)

        true_tf_idfs.close()
        
    
if __name__ == '__main__':
    unittest.main()