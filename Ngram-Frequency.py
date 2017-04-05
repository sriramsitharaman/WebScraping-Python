import nltk
from nltk import bigrams
from nltk import trigrams
import operator
folder="C:\\Users\\Sriram\\Desktop\\"
text=""
for i in range(1,7):
    f = open(folder+"indeed-"+str(i)+".csv")
    for row in f:
        text+=row.replace("\n"," ")
		
# split the texts into tokens
tokens = nltk.word_tokenize(text)
tokens = [token.lower() for token in tokens if len(token) > 1] #same as unigrams
bi_tokens = bigrams(tokens)
tri_tokens = trigrams(tokens)

unigramsDict = {}
for token in tokens:
  if token not in unigramsDict:
    unigramsDict[token] = 1
  else:
    unigramsDict[token] += 1
bigramsDict = {}
for token in bi_tokens:
  if token not in bigramsDict:
    bigramsDict[token] = 1
  else:
    bigramsDict[token] += 1
trigramsDict = {}
for token in tri_tokens:
  if token not in trigramsDict:
    trigramsDict[token] = 1
  else:
    trigramsDict[token] += 1
sorted_unigrams = sorted(unigramsDict.items(), key=operator.itemgetter(1),reverse=True)
sorted_bigrams = sorted(bigramsDict.items(), key=operator.itemgetter(1),reverse=True)
sorted_trigrams = sorted(trigramsDict.items(), key=operator.itemgetter(1),reverse=True)