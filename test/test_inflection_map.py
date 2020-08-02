import unittest
from subject_replacer import inflection_map


inflection_map_filename = "../config/inflection-map-en.json"

class LoadInflectionMap(unittest.TestCase):

    def load_inflection_map(self):
        inflection_map_builder = inflection_map.\
        InflectionMapBuilder(filename=inflection_map_filename)
        self.inflection_map = inflection_map_builder.get_inflection_map()
    
    
    @classmethod
    def setUpClass(cls):
        print('')
        print('Starting tests')
        cls.load_inflection_map(cls)


    def test(self):
        pass
    @classmethod
    def tearDownClass(cls):
        print('')
        print('Stopping tests')

    def test_load_inflection_map(self):
        print('')
        print('******test_inflection_map******')
        
        self.assertGreater(self.inflection_map.len(), 0)
        
    def test_tobe_first_person_singular(self):
        
        expected_inflection = "am"
        lemma = "be"
        person = "first"
        number = "singular"
        
        inflection = self.inflection_map.get_inflection(lemma, person, number)

        self.assertEqual(expected_inflection, inflection)

    def test_tobe_second_person_singular(self):
        
        expected_inflection = "are"
        lemma = "be"
        person = "second"
        number = "singular"
        
        inflection = self.inflection_map.get_inflection(lemma, person, number)

        self.assertEqual(expected_inflection, inflection)

    def test_tobe_third_person_singular(self):
        
        expected_inflection = "is"
        lemma = "be"
        person = "third"
        number = "singular"
        
        inflection = self.inflection_map.get_inflection(lemma, person, number)

        self.assertEqual(expected_inflection, inflection)


if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
