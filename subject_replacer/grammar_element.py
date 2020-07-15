import json


class GrammarElement(object):
	"""Grammar Element representation"""
	def __init__(self, element_type, value, person, number):
		super(GrammarElement, self).__init__()
		self.element_type = element_type
		self.value = value
		self.person = person
		self.number = number
	
	def __repr__(self):
		return str(self.__dict__)


class GrammarElementCollection(object):
	"""Collection of Elements"""

	def __init__(self):
		super(GrammarElementCollection, self).__init__()
		self._element_collection = dict()

	def append(self, element):
		self._element_collection[element.value] = element

	def __iter__(self):
		return ElementCollectionIterator(self)

	def __len__(self):
		return len(self._element_collection)
	
	def len(self):
		return len(self._element_collection)

	def list(self):
		return list(self._element_collection.values())

	def person(self, value):
		element = self._element_collection[value]
		return element.person

	def number(self, value):
		element = self._element_collection[value]
		return element.number
	
	def filter(self, person=None, number=None):
		
		result_temp = self.list()
		
		if person is not None: 
			result_temp = {element for element in self.list()\
		 		if element.person == person}
		
		result = result_temp
		
		if number is not None: 
			result_temp = {element for element in result\
				if element.number == number}
		
		result = result_temp
		
		return result
		

class ElementCollectionIterator(object):
	"""docstring for ElementCollectionIterator"""

	def __init__(self, element_collection):
		super(ElementCollectionIterator, self).__init__()
		self._element_collection = list(element_collection.list())

	def __next__(self):
		if len(self._element_collection) > 0:
			return self._element_collection.pop()

		raise StopIteration


class GrammarElementCollectionBuilder(object):
	"""Element collection factory"""
	_filename = "../config/element-map-en.json"

	def __init__(self, filename=None):
		super(GrammarElementCollectionBuilder, self).__init__()
		self._element_collection = GrammarElementCollection()

		if filename is not None:
			self._filename = filename

		with open(self._filename, "r") as read_file:
			element_json = json.load(read_file)

		for record in element_json:
			current_element = GrammarElement(
				record["type"],
				record["value"],
				record["person"],
				record["number"])
			self._element_collection.append(current_element)

	def get_element_collection(self):
		return self._element_collection
