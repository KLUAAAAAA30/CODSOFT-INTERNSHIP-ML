# -*- coding: utf-8 -*-
"""Copy of email-spam-detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1feclnPPn5sr8u3KwKSQynDVjKsu__ShY

# Import Lib
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

import warnings
warnings.filterwarnings('ignore')

# importing Stopwords
import nltk
from nltk.corpus import stopwords
import string

# models
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# train test split
from sklearn.model_selection import train_test_split, GridSearchCV

# Pipeline
from sklearn.pipeline import Pipeline

# score
from sklearn.metrics import confusion_matrix,classification_report,ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

"""# Import Data"""

df=pd.read_csv('/kaggle/input/spam-ham-dataset/spam_dataset.csv')

"""# Basic Analysis"""

df.head()

df.describe()

df['label'].value_counts()

df.info()

# adding new column as length of the text
df['length'] = df['text'].apply(len)
df.head()

"""# EDA"""

# plot for count of spam and ham in data
plt.figure(figsize=(14,6))
sns.set_style('darkgrid')
sns.countplot(x='label',data=df)
plt.title('Number of Spam and Ham')

# Plot for distribution lenth of text
plt.figure(figsize=(12,8))
sns.histplot(x='length',data=df,bins=100)
plt.title('Length of Text')

# maximum lenth text
df[df['length']==df['length'].max()]['text']

# distribution of spam and ham by length of text
df.hist(column='length',by='label',figsize=(12,8))

"""# Feature Enginering"""

# function to remove punctuation and stopwords
def text_process(text):
    non_punc = [char for char in text if char not in string.punctuation]
    non_punc=''.join(non_punc)
    return [word for word in non_punc.split() if word not in stopwords.words('english')]

"""# Train Test Split"""

# define X(features),y(target)
X= df['text']
y=df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

"""# Modles"""

# creating a pipline to model the data
# pipeline for MultinomialNB
pipe_mnb = Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tf',TfidfTransformer()),
    ('classifier',MultinomialNB())
])

# pipeline for Random Forest Classifier
pipe_rf =Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tf',TfidfTransformer()),
    ('classifier',RandomForestClassifier())
])

# pipeline for Random Forest Classifier
pipe_svc =Pipeline([
    ('bow',CountVectorizer(analyzer=text_process)),
    ('tf',TfidfTransformer()),
    ('classifier',SVC())
])

# fit the data
pipe_mnb.fit(X_train,y_train)
pipe_rf.fit(X_train,y_train)
pipe_svc.fit(X_train,y_train)

# predict the target feature
pred_mnb = pipe_mnb.predict(X_test)
pred_rf = pipe_rf.predict(X_test)
pred_svc = pipe_svc.predict(X_test)



"""# Prediction Accuracy"""

print('The accuracy for Multinomial Classifer:',accuracy_score(y_test,pred_mnb)*100)
print('The accuracy for Random_forest Classifer:',accuracy_score(y_test,pred_rf)*100)
print('The accuracy for SVC:',accuracy_score(y_test,pred_svc)*100)

"""**The SVC predicts better tham Random Forest Model and Multinomial.**"""

# print confusion matrix and classification report
print ('Classification report on SVC:')
print('\n')
print(classification_report(y_test,pred_svc))

# Display confusioni matrix for SVC

sns.set_style('ticks')
ConfusionMatrixDisplay(confusion_matrix(y_test,pred_svc)).plot()
plt.title("Confusion Matrix for SVC")

from sklearn.model_selection import cross_val_score

# Number of folds
k = 5

# Initialize the SVC model in the pipeline
pipe_svc.set_params(classifier=SVC())

# Perform k-fold cross-validation
cv_scores = cross_val_score(pipe_svc, X, y, cv=k)

# Output the results
print(f'CV Scores for each fold: {cv_scores}')
print(f'Average CV Score: {np.mean(cv_scores)}')

