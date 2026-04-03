from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import pickle

# Sample training data
X_train = [
    "This essay is very well written with strong grammar and vocabulary.",
    "The essay has some grammar mistakes and weak structure.",
    "Excellent argument, detailed explanation, and perfect flow.",
    "Poor grammar poor spelling and very short essay."
]

y_train = [95, 60, 98, 40]

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('model', LinearRegression())
])

pipeline.fit(X_train, y_train)

with open('essay_model.pkl', 'wb') as f:
    pickle.dump(pipeline, f)

print("Model trained and saved successfully.")