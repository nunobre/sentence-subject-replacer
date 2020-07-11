# Subject Replacer

´´´
original sentence = "Poly wants a cracker"
np = "My dog"
output = "My dog wants a cracker"

´´´ 

## Strategy

1.  Receive original sentence and nominal phrase to replace
2.  Parse original sentence and compute:
    *  'replaceable_phrase', nominal phrase to be replaced (ex: "Poly")
    *  'inflection_list', list of verbs to be inflected
3.  Parse the replacing nominal phrase to get its person and number (ex: "3rd person singular")
4.  Create a new list of tokens where 
    *  tokens in 'replaceable_phrase' are replaced by the ones in the provided nominal phrase
    *  tokens in 'inflection_list' are inflected to person and number from 3

## Sources
*  spacy: https://spacy.io/
*  grammar annotation: https://universaldependencies.org/
*  peen tree bank: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
*  list of english pronouns: https://www.english-grammar-revolution.com/list-of-pronouns.html