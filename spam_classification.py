import pandas as pd

import string
import joblib

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report

#Import dataset
df = pd.read_csv('email.csv')


#Initializing stemmer preparing the corpus
stemmer = PorterStemmer()
corpus = []

#Initializing the stopwords set that will be excluded from the 'Message' text
stopwords_set = set(stopwords.words('english'))

#Preprocessing each message
for i in range(len(df)):
    text = df['Message'].iloc[i].lower()
    text = text.translate(str.maketrans('','',string.punctuation)).split()
    text = [stemmer.stem(word) for word in text if word not in stopwords_set]
    text = ' '.join(text)
    corpus.append(text)


#Vectorizing the stemmed messages
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

#Assigning the target
y = df['Category']

#Splitting the dataset into training and test sets
train_X, val_X, train_y, val_y = train_test_split(X, y, test_size=0.2, random_state=5)


#Defining and training the model
svm_model = LinearSVC(max_iter=2000)
svm_model.fit(train_X,train_y)

#Making predictions for validations
pred_y = svm_model.predict(val_X)

joblib.dump(svm_model,'spam_classifier.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')


#Results of the training
print(classification_report(val_y, pred_y))