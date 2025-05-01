# GLabris-Spam_Email_Classifier
A simple project that uses a SVM model to detect spam emails based on their content

## Project Overview

This Machine Learning project is a simple **Spam Email Classifier** that uses a **Support Vector Machine (SVM)** model to classify emails as either "spam" or "ham". The model is trained on a dataset of labeled emails. Before the model is trained, the emails go through 
a preproccesing stage where the data is stemmed and the stopwords are removed. Then the clean data is vectorized by a **TfidfVectorizer** to process the textual data. 

## The Dataset

The dataset that was used for the training of the model is a Kaggle dataset made by Ashfak Yeafi under the Apache 2.0 licesne.

- Dataset source: [Spam email classification](https://www.kaggle.com/datasets/ashfakyeafi/spam-email-classification)


## Requirements and usability

In order to use this tool you need:
- Python 3.7+ is recommended
- The following libraries: scikit-learn, pandas, numpy, nltk
- Train the model by running the 'spam_classification.py' file in your system

## Future of this project

This project will be updated and here are some features i have in mind:

- Expand the dataset for better results
- Add proper clear history functionality in the GUI
- Work on the spam, recal and f1-score

