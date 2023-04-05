import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load the data into a pandas DataFrame
data = pd.read_csv("data.csv")

# Split the data into training and test sets
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Create a TfidfVectorizer instance
vectorizer = TfidfVectorizer()

# Fit the vectorizer to the training data and transform it into a TF-IDF matrix
train_tfidf = vectorizer.fit_transform(train_data['text'])

# Transform the test data into a TF-IDF matrix using the same vectorizer and train model
test_tfidf = vectorizer.transform(test_data['text'])
model = LogisticRegression()
model.fit(train_tfidf, train_data['geographic_loc'])

# Evaluate the model's performance on the test data
predictions = model.predict(test_tfidf)
accuracy = accuracy_score(test_data['geographic_loc'], predictions)
precision = precision_score(test_data['geographic_loc'], predictions)
recall = recall_score(test_data['geographic_loc'], predictions)
f1 = f1_score(test_data['geographic_loc'], predictions)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 score:", f1)

# Predict whether a given word is a geographic place or not
word = "Absint"
word_tfidf = vectorizer.transform([word])
geographic_loc = model.predict(word_tfidf)[0]

print(word, "is a geographic place:", geographic_loc)
