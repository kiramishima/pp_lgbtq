import stanza
import string
from spacy.lang.es.stop_words import STOP_WORDS

stanza.download('es')
punct = string.punctuation
nlp = stanza.Pipeline('es', processor='tokenize,sentiment')
stopwords = list(STOP_WORDS) 

doc = """
Acabo de conocer a http://poppers.com.mx y están buenísimos! menciona el código CDMXLGBT y obtén un 15% de descuento en tu compra @PoppersComMx
"""
res = nlp(doc)

# print(res)
# print(res.entities)

for i, sentence in enumerate(res.sentences):
    for word in sentence.words:
        if word.text not in stopwords and word.text not in punct:
            print(f'word: {word.text} \tlemma: {word.lemma}')
