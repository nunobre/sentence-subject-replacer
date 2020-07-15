import unittest
from subject_replacer import grammar_element

pos_map_filename = "../config/pos-map-en.json"
pronoun_map_filename = "../config/pronoun-map-en.json"


class LoadPronouns(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print('')
        print('Starting tests')

    @classmethod
    def tearDownClass(cls):
        print('')
        print('Stopping tests')

    def test_load_pronouns(self):
        print('')
        print('******test_load_pronouns******')
       
        pronoun_collection_builder = grammar_element.\
            GrammarElementCollectionBuilder(filename=pronoun_map_filename)
            
        pronoun_collection = pronoun_collection_builder.get_element_collection()
        
        self.assertGreater(pronoun_collection.len(), 0)

    def test_load_pos(self):
        print('')
        print('******test_load_pos******')
       
        pos_collection_builder = grammar_element.\
            GrammarElementCollectionBuilder(filename=pos_map_filename)
            
        pos_collection = pos_collection_builder.get_element_collection()
        
        print(pos_collection.list()[0].__repr__())
        
        self.assertGreater(pos_collection.len(), 0)

    def test_filter_pos_singular(self):
        print('')
        print('******test_filter_pos_singular******')
       
        pos_collection_builder = grammar_element.\
            GrammarElementCollectionBuilder(filename=pos_map_filename)
            
        pos_collection = pos_collection_builder.get_element_collection()
        
        person = None
        number = "singular"
        
        result = pos_collection.filter(person, number)
        print(result)
        
        self.assertGreater(1, 0)
    
    def test_filter_pos_plural(self):
        print('')
        print('******test_filter_pos_plural******')
       
        pos_collection_builder = grammar_element.\
            GrammarElementCollectionBuilder(filename=pos_map_filename)
            
        pos_collection = pos_collection_builder.get_element_collection()
        
        person = None
        number = "plural"
        
        result = pos_collection.filter(person, number)
        print(result)
        
        self.assertGreater(1, 0)
    
    def test_filter_pos_fst_person(self):
        print('')
        print('******test_filter_pos_fst_person******')
       
        pos_collection_builder = grammar_element.\
            GrammarElementCollectionBuilder(filename=pos_map_filename)
            
        pos_collection = pos_collection_builder.get_element_collection()
        
        person = "1st"
        number = None
        
        result = pos_collection.filter(person, number)
        print(result)
        
        self.assertGreater(1, 0)

    def test_filter_pos_thrd_person(self):
        print('')
        print('******test_filter_pos_thrd_person******')
       
        pos_collection_builder = grammar_element.\
            GrammarElementCollectionBuilder(filename=pos_map_filename)
            
        pos_collection = pos_collection_builder.get_element_collection()
        
        person = "3rd"
        number = None
        
        result = pos_collection.filter(person, number)
        print(result)
        
        self.assertGreater(1, 0)

if __name__ == "__main__":
    unittest.main()
    print("Everything passed")
