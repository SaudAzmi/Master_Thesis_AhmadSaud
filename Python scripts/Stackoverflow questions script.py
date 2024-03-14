

import time as time
import numpy as np
import pandas as pd
import gc
import os
# Text librairies
import re
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import ToktokTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tag.util import untag
import contractions
# import pycontractions # Alternative better package for removing contractions
from autocorrect import Speller

# https://numpy.org/devdocs/user/basics.types.html

dtypes_questions = {'Id':'int32', 'Score': 'int16', 'Title': 'str', 'Body': 'str'}

#%%time
df_questions_new = pd.read_csv('C:/Users/Saud Azmi/Downloads/Questions.csv',
                           usecols=['Id', 'Score', 'Title', 'Body'],
                           encoding = "ISO-8859-1",
                           dtype=dtypes_questions,
                           nrows=100
                          )

df_questions_new[['Title', 'Body']] = df_questions_new[['Title', 'Body']].applymap(lambda x: str(x).encode("utf-8", errors='surrogatepass').decode("ISO-8859-1", errors='surrogatepass'))


# Remove all questions that have a negative score
df_questions_new = df_questions_new[df_questions_new["Score"] >= 0]

spell = Speller()
token = ToktokTokenizer()
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
# charac = '!"#$%&\'()*+,-./:;<=>@[\\]^_`{|}~0123456789'
# stop_words = set(stopwords.words("english"))
adjective_tag_list = set(['JJ','JJR', 'JJS', 'RBR', 'RBS']) # List of Adjective's tag from nltk package

df_questions_new['Body'][11]

#%%time

# Parse question and title then return only the text
df_questions_new['Body'] = df_questions_new['Body'].apply(lambda x: BeautifulSoup(open(x), 'html.parser').get_text() if os.path.exists(x) else x)
df_questions_new['Title'] = df_questions_new['Title'].apply(lambda x: BeautifulSoup(open(x), 'html.parser').get_text() if os.path.exists(x) else x)

df_questions_new['Body'][11]

def clean_text(text):
    text = re.sub(r"\'", "'", text) # match all literal apostrophe pattern then replace them by a single whitespace
    text = re.sub(r"\n", " ", text) # match all literal Line Feed (New line) pattern then replace them by a single whitespace
    text = re.sub(r"\xa0", " ", text) # match all literal non-breakable space pattern then replace them by a single whitespace
    text = re.sub('\s+', ' ', text) # match all one or more whitespace then replace them by a single whitespace
    text = text.strip(' ')
    return text

df_questions_new['Title'] = df_questions_new['Title'].apply(lambda x: clean_text(x))
df_questions_new['Body'] = df_questions_new['Body'].apply(lambda x: clean_text(x))

## 2. Remove contractions
def expand_contractions(text):
    """expand shortened words, e.g. 'don't' to 'do not'"""
    text = contractions.fix(text)
    return text


#%%time

df_questions_new['Title'] = df_questions_new['Title'].apply(lambda x: expand_contractions(x))
df_questions_new['Body'] = df_questions_new['Body'].apply(lambda x: expand_contractions(x))


def autocorrect(text):
    words = token.tokenize(text)
    words_correct = [spell(w) for w in words]
    return ' '.join(map(str, words_correct)) # Return the text untokenize


df_questions_new['Title'] = df_questions_new['Title'].str.lower()
df_questions_new['Body'] = df_questions_new['Body'].str.lower()

def remove_punctuation_and_number(text):
    """remove all punctuation and number"""
    return text.translate(str.maketrans(" ", " ", charac))



# def remove_non_alphabetical_character(text):
#     """remove all non-alphabetical character"""
#     text = re.sub("[^a-z]+", " ", text) # remove all non-alphabetical character
#     text = re.sub("\s+", " ", text) # remove whitespaces left after the last operation
#     return text

# df_questions_new['Title'] = df_questions_new['Title'].apply(lambda x: remove_non_alphabetical_character(x))
# df_questions_new['Body'] = df_questions_new['Body'].apply(lambda x: remove_non_alphabetical_character(x))


# pd.set_option('display.max_colwidth', None)

# print(df_questions_new['Body'])
#
from ayx import Alteryx
Alteryx.write(df_questions_new,1)
