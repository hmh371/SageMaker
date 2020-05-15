import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag, word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import confusion_matrix

import boto3, re, sys, math, json, os, urllib.request #,sagemaker
#from sagemaker import get_execution_role
import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import Image
from IPython.display import display
from time import gmtime, strftime
#from sagemaker.predictor import csv_serializer

try:
  model_data = pd.read_csv('bank_clean.csv', encoding = "latin-1")
  print('Success: Data loaded into dataframe.')
except Exception as e:
    print('Data load error: ',e)

train_data, test_data = np.split(model_data.sample(frac=1, random_state=1729), [int(0.7 * len(model_data))])
print(train_data.shape, test_data.shape)

pd.concat([train_data['y_no'], train_data.drop(['y_no', 'y_yes'], axis=1)], axis=1).to_csv('train.csv', index=False, header=False)
