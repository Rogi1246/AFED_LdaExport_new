import codecs
import sys
# import nltk
from nltk.corpus import stopwords
# nltk.download()
import re
import pandas as pd
from pprint import pprint
# gensim : lib for topic modelling, doc indexing + similarity retrieval with large corpora
import gensim
import gensim.corpora as corpora
from gensim.models import CoherenceModel
from gensim.utils import simple_preprocess
# spacy is generally for Natural Language Processing
# import spacy for lemmatization
# (spacy.load)en_core_web_sm or de_core_news_sm (python3 -m spacy download en (or de for german))
import spacy
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
# plotting
import pyLDAvis
import pyLDAvis.gensim
# warnings
import warnings

# Latent Dirichlet Allocation = LDA
# generative statistical model that allows sets of observations
#
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
warnings.filterwarnings("ignore", category=DeprecationWarning)


stop_words = stopwords.words('english')
print(len(stop_words))
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'would', 'do', 'com', 'may', 'talk', 'http', 'say'])
print(len(stop_words))

# importing the dataset
# the json will be stored in the dir : data
# can also reference the link
df = pd.read_json('exports/export_testSMALL.json')

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


def removing_stopwords(text):
    return [[word for word in gensim.utils.simple_preprocess(str(doc.encode('utf-8'))) if word not in stop_words] for
            doc in text_corpus]

words = removing_stopwords(words)


# lemmatization :
# words that appear in various forms, so we want the base form of that word
# that way they can be analysed as a single item
# apply before topic clustering


def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    texts_out = []
    for idx, sent in enumerate(texts):
        if idx % 500 == 0:
            print(str(idx) + ' docs lemmatized')
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


# we want to keep nouns, adjectives etc.
data_lemmatized = lemmatization(words, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

# create the dictionary and a corpus (machine-readable collection of texts for analysis)
# first creating the dictionary
id2word = corpora.Dictionary(data_lemmatized)

# creating the corpus / term document frequency
texts = data_lemmatized
corpus = [id2word.doc2bow(text) for text in texts]

# build the LDA model
# Properties explained : https://radimrehurek.com/gensim/models/ldamulticore.html
#
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=20, random_state=100,
                                            update_every=1, chunksize=100, passes=10, alpha='auto',
                                            per_word_topics=True)

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
