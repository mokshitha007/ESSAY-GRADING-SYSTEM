import pickle

with open("essay_model.pkl", "rb") as f:
    model = pickle.load(f)

def grade_essay(text):

    prediction = model.predict([text])[0]

    score = max(0, min(10, round(prediction, 2)))

    return score