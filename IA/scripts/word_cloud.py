from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, SPANISH_STOP_WORDS

texto = """
EL VIOLADOR SERIAL, DETENIDO!
Así llegó a CDMX Jose Dicha
Atacaba a jovenes de la comunidad LGBT 🏳️‍🌈 
Los contactaba y cazaba en 
@Grindr

Los drogaba, violaba y robaba.
Antes de irse, les dejaba cartas.
Agentes d 
@PDI_FGJCDMX
 lo buscaron por meses.
Hoy lo atraparon en Hidalgo.
"""

cloud = WordCloud(stopwords=SPANISH_STOP_WORDS).generate(texto)

# Display

plt.imshow(cloud, interpolation='bilinear')
plt.axis('off')
plt.show()
