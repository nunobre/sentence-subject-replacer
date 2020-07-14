import unittest
import csv
from subject_replacer import subject_replacer

test_data_filename = "test-data.csv"

test_data = {}

def load_test_data(filename=None):
    
    if filename is None:
        filename = test_data_filename

    with open(filename, mode='r') as infile:
            reader = csv.reader(infile)
            for row in reader:
                key = row[0]
                test_data[key] = row[1:]

    print(test_data)

class ReplaceSubjectTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        load_test_data()
        print('')
        print('setUpClass')

    @classmethod
    def tearDownClass(cls):
        print('')
        print('tearDownClass')

    def test_subject_replacer(self):
        print('')
        print('******test_subject_replacer******')
        # get each row text from the csv file.
        for key, value in test_data.items():
            print(f'running test {key}:')
            original_text = value[0]
            new_subject_text = value[1]
            expected_result = value[2]
            print(f'original_text: {original_text}')
            print(f'new_subject_text: {new_subject_text}')
            print(f'expected_result: {expected_result}')
            result = subject_replacer.replace_subject(original_text, new_subject_text)
            
            self.assertEqual(result, expected_result)
    


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
