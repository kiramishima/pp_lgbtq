import spacy
import numpy as np
import string
from spacy.lang.es.stop_words import STOP_WORDS

spacy_nlp = spacy.load('es_core_news_sm')
punct = string.punctuation
stopwords = list(STOP_WORDS) # listado de stopwords

doc = """
Acabo de conocer a http://poppers.com.mx y están buenísimos! menciona el código CDMXLGBT y obtén un 15% de descuento en tu compra @PoppersComMx
"""

# Procesamos el texto
nlp = spacy_nlp(doc)
for token in nlp:
    if token.text not in stopwords and token.text not in punct:
        print(token.text)

