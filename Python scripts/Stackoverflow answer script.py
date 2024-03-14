
from ayx import Package
from ayx import Alteryx
! pip install bs4
# ! pip install pycontractions # The package has a depencies that have not been updated, so I couldn't use it.
! pip install contractions
! pip install autocorrect 
# generic librairies
import time as time
import numpy as np
import pandas as pd
import gc

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
!pip install nltk

dtypes_questions = {'Id': 'str', 'Score': 'str', 'Body': 'str', 'OwnerUserId': 'str', 'ParentId': 'str'}

import pandas as pd

# Read the first 1000 records from the CSV file
df_questions = pd.read_csv('C:/Users/Saud Azmi/Downloads/Answers.csv',
                           usecols=['Id', 'OwnerUserId', 'CreationDate', 'ParentId', 'Score', 'Body'], 
                           encoding="ISO-8859-1",
                           dtype=dtypes_questions,
                           nrows=11000
                          )

df_questions.info()

# Removing HTML
df_questions['Body'][1]

# %%time

# Parse question and title then return only the text
df_questions['Body'] = df_questions['Body'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())
# df_questions['Title'] = df_questions['Title'].apply(lambda x: BeautifulSoup(x, 'html.parser').get_text())
df_questions.to_csv('C:/Users/Saud Azmi/Downloads/Answer_output_1.csv', index=False)
df_questions['Score'] = pd.to_numeric(df_questions['Score'], errors='coerce')

# Get the index of the maximum score for each 'ParentId'
idx_max_scores = df_questions.groupby('ParentId')['Score'].idxmax()

# Filter the DataFrame to get the rows with the maximum scores for each 'ParentId'
df_max_scores = df_questions.loc[idx_max_scores]

# Print or do further processing with df_max_scores
# print(df_max_scores)
from ayx import Alteryx
Alteryx.write(df_max_scores,1)