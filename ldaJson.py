# pip install -r requirements.txt

# Latent Dirichlet Allocation = LDA
# generative statistical model that allows sets of observations

# its working now but i dont know if i still need this .. keep it for now
import codecs
import sys

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

# importing nltk for stopwords
import nltk; nltk.download('stopwords')

# download spacy (english) for text pre-processing
# in terminal or command prompt: python3 -m spacy download en (or de for german)
# or see nlp= [...] under the spacy import
# the spacy module is necessary for lemmatization later on

# importing the core packages, whereas pandas, matplotlib and numpy are
# for visualization
import re
import numpy as np # not used rn.. maybe later i dont know yet
import pandas as pd
from pprint import pprint

# gensim : lib for topic modelling, doc indexing + similarity retrieval with large corpora
# gensim import
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel

# spacy is generally for Natural Language Processing
# import spacy for lemmatization
# (spacy.load)en_core_web_sm or de_core_news_sm
import spacy
# init spacy 'en' model, keep tagger component
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# now the plotting tools
import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt # (not needed - delete later)
#%matplotlib inline

# warnings
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# for removing the stopwords de_core_news_sm
from nltk.corpus import stopwords

# importing the dataset
# the json will be stored in the dir : data
# can also reference the link

df = pd.read_json('export_hardware.json')
# print(df.target_names.unique())
# df.head()

# we can remove unwanted characters from email addresses
# as well as formatting that won't really work well with gensim
text_corpus = df.text_plain.values.tolist()
# remove the email address
text_corpus = [re.sub('\S*@\S*\s?', '', doc) for doc in text_corpus]
# remove newline characters
text_corpus = [re.sub('\s+', ' ', doc) for doc in text_corpus]
# remove single quote characters
text_corpus = [re.sub("\'", "", doc) for doc in text_corpus]

# print(text_corpus[1])

# next up : Tokenizing words
# -> breaking up a sequence of strings into pieces (tokens)
# removing punctuation
# provided by gensim


def doc_to_words(sentences):
    for sentence in sentences:
        yield gensim.utils.simple_preprocess(str(sentence.encode('utf-8')), deacc=True)


words = list(doc_to_words(text_corpus))

# print(' ------------------- doc to words example ------------------- ')

# removing stopwords
stop_words = stopwords.words('english')
# extending the stopwords individually
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'would', 'do'])


def removing_stopwords(text):
    return [[word for word in gensim.utils.simple_preprocess(str(doc.encode('utf-8'))) if word not in stop_words] for doc in text_corpus]


words = removing_stopwords(words)

# print(' ------------------- removed stopwords example ------------------- ')
# print(words[1])

# lemmatization :
# words that appear in various forms, so we want the base form of that word
# that way they can be analysed as a single item
# apply before topic clustering


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    texts_out = []
    for idx, sent in enumerate(texts):
        if idx % 500 == 0:
            print(str(idx) + ' docs lemmatized')
            #sys.stdout.write(str(idx))
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


#we want to keep nouns, adjectices etc.
data_lemmatized = lemmatization(words, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

# view the lemmatized data
# print(' ------------------- lemmatized example (ind 1) ------------------- ')

# print(data_lemmatized[:1])

# create the dictionary and a corpus (machine-readable collection of texts for analysis)
# first creating the dictionary
id2word = corpora.Dictionary(data_lemmatized)

# creating the corpus / term document frequency
texts = data_lemmatized
corpus = [id2word.doc2bow(text) for text in texts]

# view the corpus
# print(' ------------------- corpus example (ind 1) ------------------- ')
# print(corpus[:1])

# what does the output mean ?
# f.e. [0,1] implies, that the word with id 0 occurs once in the first document
#
# build the LDA model
# Properties explained : https://radimrehurek.com/gensim/models/ldamulticore.html
#
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=20, random_state=100, update_every=1, chunksize=100, passes=10, alpha='auto', per_word_topics=True)

# with that done, we can now see the keywords that
# apply to each topic and the relative weight within
print(' ------------------- LDA_model ------------------- ')
pprint(lda_model.print_topics())
doc_lda = lda_model[corpus]

# how to interpret the model
# representing the top 10 keywords, and the weight of each one
# the weight reflecting, how important the keyword is to that topic
#
# now we can visualize
#
#
# this :
# pyLDAvis.enable_notebook()
# vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
# vis
# when using notebook
#
# this when running as a script
# not yet working ( taking way too long )
visualization = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
pyLDAvis.save_html(visualization, 'LDA_Visual.html')

