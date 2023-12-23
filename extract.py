import pandas
import gensim
from nltk.tokenize import word_tokenize
import string

def tokenization (text):
    tokens = word_tokenize(text)
    return [w for w in tokens if w.isalpha()]

text_df = pandas.read_csv('/Users/xuenie_0527/Desktop/UTHM/Year3/PSM1/word2vec/spamoutput.csv')
text = text_df.iloc[:,0]
text_list = []
for row in text:
    text_list.append(tokenization(row))

# model = gensim.models.Word2Vec(sentences=text_list, min_count=1, vector_size=5, sg=1)
# print(model.wv.most_similar(positive=['quick'],topn=3))

punctuation = string.punctuation.replace('!', '')
print(punctuation)
