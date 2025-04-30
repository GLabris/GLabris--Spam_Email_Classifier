import joblib
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# Load the model and vectorizer
model = joblib.load('spam_classifier.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Preprocessing function
def preprocess(text):
    stemmer = PorterStemmer()
    stopwords_set = set(stopwords.words('english'))

    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation)).split()
    text = [stemmer.stem(word) for word in text if word not in stopwords_set]
    return ' '.join(text)

# Loop for repeated classification
while True:
    email = input("\nEnter the email text: ")
    cleaned_email = preprocess(email)
    vectorized_email = vectorizer.transform([cleaned_email])
    prediction = model.predict(vectorized_email)
    print(f"Prediction: {prediction[0].upper()}")

    cont = input("Do you want to classify another email? (Y/N): ").strip().upper()
    if cont != 'Y':
        print("Exiting the classifier. Goodbye!")
        break
