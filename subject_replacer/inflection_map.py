import json

class InflectionMap(object):
    """The inflection map contains a list of rules having each:
        - lemma, ex: be
        - person, ex: first
        - number, ex: singular
        - inflection, ex: am
        
    """

    def __init__(self):
        self._inflection_map = dict()

    def append(self, lemma, person, number, inflection):
        self._inflection_map[(lemma, person, number)] = inflection
    
    def len(self):
        return len(self._inflection_map)

    def list(self):
        return list(self._inflection_map.values())

    def get_inflection(self, lemma, person, number):
        
        inflection = "" 

        try:
            inflection = self._inflection_map[(lemma, person, number)]
        
        except Exception:
            pass
        
        return inflection

class InflectionMapBuilder(object):
    """Element collection factory"""
    _filename = "../config/inflection-map-en.json"

    def __init__(self, filename=None):
        self._inflection_map = InflectionMap()

        if filename is not None:
            self._filename = filename

        with open(self._filename, "r") as read_file:
            element_json = json.load(read_file)

        for record in element_json:
            current_lemma = record["lemma"]
            current_person = record["person"]
            current_number = record["number"]
            current_inflection = record["inflection"]
                
            self._inflection_map.append(current_lemma, 
                                        current_person, 
                                        current_number, 
                                        current_inflection)


    def get_inflection_map(self):
        return self._inflection_map
