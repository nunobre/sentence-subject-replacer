import unittest
import csv
import logging
from subject_replacer import subject_replacer

# create logger
logger = logging.getLogger('test_subject_replacer')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

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

    logger.info(test_data)

class ReplaceSubjectTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        load_test_data()
        logger.info('')
        logger.info('Starting tests')

    @classmethod
    def tearDownClass(cls):
        logger.info('')
        logger.info('Stopping tests')

    def test_subject_replacer(self):
        logger.info('')
        logger.info('******test_subject_replacer******')
        # get each row text from the csv file.
        for key, value in test_data.items():
            logger.info("running test '%s':", key)
            original_text = value[0]
            new_subject_text = value[1]
            expected_result = value[2]
            logger.info("original_text: '%s'", original_text)
            logger.info("new_subject_text: '%s'", new_subject_text)
            logger.info("expected_result: '%s'", expected_result)
            result = subject_replacer.replace_subject(original_text, new_subject_text)
            logger.info("result: '%s'", result)
            
            self.assertEqual(result, expected_result)
    


if __name__ == "__main__":
    unittest.main()
    logger.info("Everything passed")
