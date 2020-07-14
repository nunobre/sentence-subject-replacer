#!/usr/bin/env python
# coding: utf8
from __future__ import unicode_literals, print_function

import spacy
import sys
import lemminflect
from subject_replacer import pronouns


# from spacy import displacy

pronoun_map_builder = pronouns.PronounCollectionBuilder("../config/pronoun-map-en.json")

pronoun_map = pronoun_map_builder.get_pronoun_collection()

pos_person_map = {
	'subject': 'verb',
	'NN': '3rd',
	'NNP': '3rd',
	'NNS': '3rd',
	'NNPS': '3rd',
	'PRP': 'VBP'
}

pos_number_map = {
	'POS': 'number',
	'NN': 'singular', # noun singular : verb 
	'NNP': 'singular', # noun singular : verb 
	'NNS': 'plural',
	'NNPS': 'plural'
}


def parse_sentence(sentenceToParse):
	''' 
	Recieves a Document, parses it and retrieves the list of tokens to be 
	replaced and the list of tokens to be inflected
	'''

	replaceable_phrase = []
	inflection_list = []

	for sentence in sentenceToParse.sents:
		#print("sentence")
		#print(sentence)
		root_token = sentence.root
		inflection_list.append(root_token)
		#print(f"sentence.root: {root_token}")
		for token in root_token.children:
			print(token.dep_)
			#add to disposable list		
			if token.dep_ == "nsubj":
				replaceable_phrase.append(token)
				#add children to disposable list
				for child in token.children:
					#print(child)
					replaceable_phrase.append(child)
			if token.dep_ in ("aux", "cop"):
				inflection_list.append(token)

	return replaceable_phrase, inflection_list

def replace_phrase(sentence, replaceable_phrase, newPhrase):
	'''
	Traverses a Document and returns a list of tokens where the tokens in the 
	replaceable_phrase are replaced by those in the newPhrase
	'''

	newSentence = []
	replaced = False
	
	for token in sentence:
		#print(token)
		if token not in replaceable_phrase:
			print(token.orth_, token.tag_)
			newSentence.append(token)
		else:
			if not(replaced):
				for replaceToken in newPhrase:
					newSentence.append(replaceToken)
				replaced = True

	return newSentence

def inflect_token(root_token, token, person, number):
	'''
	Returns the inflection of a token's lemma, given the provided rules
	'''
	inflection = token.orth_

	print(f"Received token '{inflection}' to inflect")
	print(f"lemma is '{token.lemma_}'")
	print(f"Inflect to '{person}' person  '{number}'")

	# if token.orth_ in pronoun_map.values()

	return inflection

def get_number(token):
	print("number",token.pos_, token.tag_, token.orth_)

	if token.pos_ == "PRON":
		number = pronoun_map.person(token.lower_)
		return number

	number = pos_number_map[token.tag_]

	return number

def get_person(token):

	if token.pos_ == "PRON":
		person = pronoun_map.number(token.lower_)
		return person

	person = pos_person_map[token.tag_]

	return person


def get_noun_chunk_root(noun_chunk_document):
	root_token = ''

	for chunk in noun_chunk_document.noun_chunks:
		root_token = chunk.root
		break

	return root_token


def parse_noun_chunk(noun_chunk_document):
	root_token = get_noun_chunk_root(noun_chunk_document)
	print(f"root token is {root_token.orth_}")

	return root_token, get_person(root_token), get_number(root_token)


def replace_subject(original_text, new_subject_text):
	"""
	receives two strings and returns a new string where the subject on 
	the orignial_text the new_subject_text 
	"""

	nlp = spacy.load("en_core_web_lg")

	original_doc = nlp(original_text)
	new_subject_doc = nlp(new_subject_text)

	replaceable_phrase, inflection_list = parse_sentence(original_doc)

	print(f"inflection list is {inflection_list}")

	new_sentence = replace_phrase(original_doc,
								replaceable_phrase,new_subject_doc)

	noun_chunk_root, person, number = parse_noun_chunk(new_subject_doc)
	print(f"root token is {person} person, {number}")

	return_sentence = []
	return_string = ''
	for token in new_sentence:
		if token in inflection_list:
			result = inflect_token(noun_chunk_root, token, person, number)
			return_string += " " + result
		else:
			return_sentence.append(token)
			return_string += " " + token.orth_

	return return_string


def main():

	if len(sys.argv) < 3:
		raise Exception(f"Usage: {sys.argv[0]} '<original sentence>' \
			'<nominal clause to replace>'")

	# opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

	replace_text = sys.argv.pop()
	original_text = sys.argv.pop()

	new_text = replace_subject(original_text, replace_text)

	print(new_text)


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(e)
		SystemExit(e)
