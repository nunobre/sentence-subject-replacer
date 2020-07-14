#!/usr/bin/env python
# coding: utf8
from __future__ import unicode_literals, print_function

import spacy
import sys
import lemminflect

from spacy import displacy

def main():

	if len(sys.argv) < 2:
		raise Exception(f"Usage: {sys.argv[0]} '<sentence to parse>'")

	opts = []
	inputSentence = ''
	for arg in sys.argv[1:]:
		if arg.startswith("-"):
			opts.append(arg)
		else:
			inputSentence = arg

	nlp = spacy.load("en_core_web_sm")
	doc = nlp(inputSentence)

	print("Noun chunks:  [start]")
	for chunk in doc.noun_chunks:
		print(" ",chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text)
	print("Noun chunks:  [end]")

	for token in doc:
		
		print(token.orth_, 
			token.tag_,
			token.pos_,
			token.dep_
			#spacy.explain(token.tag_),
			#nlp.vocab.morphology.tag_map[token.tag_]
			)

	html=displacy.render(doc, style='dep')

	if "-f" in opts:
		filenameTemp =  inputSentence.replace(".", "")
		filename =  filenameTemp.replace(" ", "_") + '.html'
		filename = "../bin/" + filename
		print(filename)
		f = open(filename, "w")
		f.write(html)
		f.close()

if __name__ == "__main__":
    try:
    	main()
    except Exception as e:
    	print(e)
    	SystemExit(e)
    

