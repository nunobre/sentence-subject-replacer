import json

class Pronoun(object):
	"""Pronoun representation"""
	def __init__(self, pronoun_type, value, person, number):
		super(Pronoun, self).__init__()
		self.pronoun_type = pronoun_type
		self.value = value
		self.person = person
		self.number = number


class PronounCollection(object):
	"""Collection of Pronouns"""

	def __init__(self):
		super(PronounCollection, self).__init__()
		self._pronoun_collection = dict()

	def append(self, pronoun):
		self._pronoun_collection[pronoun.value] = pronoun

	def __iter__(self):
		return PronounCollectionIterator(self)

	def __len__(self):
		return len(self._pronoun_collection)

	def list(self):
		return self._pronoun_collection.values()

	def person(self, value):
		pronoun = self._pronoun_collection[value]
		return pronoun.person

	def number(self, value):
		pronoun = self._pronoun_collection[value]
		return pronoun.number

class PronounCollectionIterator(object):
	"""docstring for PronounCollectionIterator"""
	
	def __init__(self, pronoun_collection):
		super(PronounCollectionIterator, self).__init__()
		self._pronoun_collection = list(pronoun_collection.list())
		

	def __next__(self):
		if len(self._pronoun_collection) > 0:
			return self._pronoun_collection.pop()

		raise StopIteration

class PronounCollectionBuilder(object):
	"""Pronoun collection factory"""
	_filename = "pronoun_map.json"

	def __init__(self, filename=None):
		super(PronounCollectionBuilder, self).__init__()
		self._pronoun_collection = PronounCollection()

		if filename is not None:
			self._filename = filename

		with open(self._filename, "r") as read_file:
			pronoun_json = json.load(read_file)


		for record in pronoun_json:
			current_pronoun = Pronoun(
				record["type"],
				record["value"],
				record["person"],
				record["number"])
			self._pronoun_collection.append(current_pronoun)

	def get_pronoun_collection(self):
		return self._pronoun_collection

def main():
	
	pronoun_collection_builder = PronounCollectionBuilder()
	pronoun_collection = pronoun_collection_builder.\
								get_pronoun_collection()


	for pronoun in pronoun_collection:
		print(pronoun.type,
			pronoun.value,
			pronoun.person,
			pronoun.number)
		
	print(pronoun_collection.person("i"))
	print(pronoun_collection.number("i"))

if __name__ == "__main__":
	#try:
	main()

		


