import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_lg")
doc = nlp("The dog.")
# Since this is an interactive Jupyter environment, we can use displacy.render here
html=displacy.render(doc, style='dep')
#displacy.serve(doc, style='dep')
print(html)