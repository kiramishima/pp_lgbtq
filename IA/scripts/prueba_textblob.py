from textblob import TextBlob

texto = "Hoy fue un buen día"

valencia = TextBlob(texto)
print(valencia.sentiment)