#!/usr/bin/env python
# coding: utf8
from __future__ import unicode_literals, print_function

import spacy
import sys
import lemminflect
import logging

from subject_replacer import grammar_element, inflection_map


# create logger
logger = logging.getLogger('subject_replacer')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


pos_map_filename = "../config/pos-map-en.json"
pronoun_map_filename = "../config/pronoun-map-en.json"
inflection_map_filename = "../config/inflection-map-en.json"

pronoun_map_builder = grammar_element.GrammarElementCollectionBuilder(pronoun_map_filename)

pronoun_map = pronoun_map_builder.get_element_collection()

pos_map_builder = grammar_element.GrammarElementCollectionBuilder(pos_map_filename)

pos_map = pos_map_builder.get_element_collection()

inflection_map_builder = inflection_map.InflectionMapBuilder(inflection_map_filename)
	
inflectionmap = inflection_map_builder.get_inflection_map()

dependency_tags_to_inflect = (
	"aux", 
	"cop"
	)
	


def parse_sentence(sentenceToParse):
	'''
	Recieves a Document, parses it and retrieves the list of tokens to be
	replaced and the list of tokens to be inflect
	'''

	replaceable_phrase = []
	inflection_list = []

	for sentence in sentenceToParse.sents:

		root_token = sentence.root
		for token in root_token.children:
			logger.debug("token '%s' dependency tag: '%s'", token.orth_, token.dep_)
			# add to disposable list
			if token.dep_ == "nsubj":
				replaceable_phrase.append(token)
				# add children to disposable list
				for child in token.children:
					# print(child)
					replaceable_phrase.append(child)
			if token.dep_ in dependency_tags_to_inflect:
				inflection_list.append(token)

		if len(inflection_list) == 0:
			inflection_list.append(root_token)
			
	return replaceable_phrase, inflection_list


def replace_phrase(sentence, replaceable_phrase, newPhrase):
	'''
	Traverses a Document and returns a list of tokens where the tokens in the
	replaceable_phrase are replaced by those in the newPhrase
	'''

	newSentence = []
	replaced = False

	for token in sentence:
		# print(token)
		if token not in replaceable_phrase:
			# print(token.orth_, token.tag_)
			newSentence.append(token)
		else:
			if not(replaced):
				for replaceToken in newPhrase:
					newSentence.append(replaceToken)
				replaced = True

	return newSentence


def inflect_token(root_token, token):
	'''
	Returns the inflection of a token's lemma, given the provided rules
	'''
	inflection = ""

	lemma = token.lemma_
	person = get_person(root_token)
	number = get_number(root_token)
	logger.debug("Received token '%s' to inflect", inflection)
	logger.debug("lemma is '%s", lemma)
	logger.debug("root token '%s has a tag '%s'", root_token, root_token.tag_)
	logger.debug("Inflect to '%s' person '%s'", person, number)
	

	# verify if inflection rule exists on inflection_map
	inflection = inflectionmap.get_inflection(lemma, person, number)

	if inflection == "":
		inflection_pos_tag = pos_map.filter(person, number)
		inflection = token._.inflect(inflection_pos_tag)

	return inflection


def get_number(token):
	logger.debug("get_number: %s, %s, %s", token.pos_, token.tag_, token.orth_)

	if token.pos_ == "PRON":
		number = pronoun_map.number(token.lower_)
		return number

	number = pos_map.number(token.tag_)

	return number


def get_person(token):

	if token.pos_ == "PRON":
		person = pronoun_map.person(token.lower_)
		return person

	person = pos_map.person(token.tag_)

	return person


def get_noun_chunk_root(noun_chunk_document):
	root_token = ''

	for chunk in noun_chunk_document.noun_chunks:
		root_token = chunk.root
		break

	return root_token


def parse_noun_chunk(noun_chunk_document):
	"""
	Traverses a noun chunk and returns it's root_token and the root_token's person and number
	"""
	root_token = get_noun_chunk_root(noun_chunk_document)
	# print(f"root token is {root_token.orth_}")

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

	logger.debug("inflection list is '%s'", inflection_list)

	new_sentence = replace_phrase(original_doc,
								replaceable_phrase, new_subject_doc)

	# noun_chunk_root, person, number = parse_noun_chunk(new_subject_doc)
	noun_chunk_root = get_noun_chunk_root(new_subject_doc)
	# print(f"root token is {person} person, {number}")

	return_sentence = []
	return_string = ''
	for token in new_sentence:
		if token in inflection_list:
			# result = inflect_token(noun_chunk_root, token, person, number)
			result = inflect_token(noun_chunk_root, token)
			return_string += " " + result
		else:
			return_sentence.append(token)
			return_string += " " + token.orth_

	return return_string.strip()


def main():

	if len(sys.argv) < 3:
		raise Exception(f"Usage: {sys.argv[0]} '<original sentence>' \
			'<nominal clause to replace>'")

	# opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

	replace_text = sys.argv.pop()
	original_text = sys.argv.pop()

	new_text = replace_subject(original_text, replace_text)

	logger.debug(new_text)


if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		logger.error(e)
		SystemExit(e)
