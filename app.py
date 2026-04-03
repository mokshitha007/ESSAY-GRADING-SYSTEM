from flask import Flask, render_template, request
import pickle
from textblob import TextBlob
import textstat

app = Flask(__name__)

# Load trained model
with open('essay_model.pkl', 'rb') as f:
    model = pickle.load(f)


def find_mistakes(text):
    mistakes = []

    words = text.split()

    for word in words:
        clean_word = word.strip(".,!?;:()[]{}\"'")

        # crude spelling check
        corrected = str(TextBlob(clean_word).correct())

        if clean_word.lower() != corrected.lower() and len(clean_word) > 3:
            mistakes.append({
                "error": clean_word,
                "suggestion": corrected
            })

    # remove duplicate mistakes
    unique = []
    seen = set()

    for m in mistakes:
        key = (m["error"], m["suggestion"])
        if key not in seen:
            seen.add(key)
            unique.append(m)

    return unique[:10]


@app.route('/', methods=['GET', 'POST'])
def home():
    result = None

    if request.method == 'POST':
        essay = request.form['essay']

        # AI predicted score
        predicted_score = int(model.predict([essay])[0])
        predicted_score = max(0, min(predicted_score, 100))

        feedback = []

        word_count = len(essay.split())

        if word_count < 150:
            predicted_score -= 10
            feedback.append("Essay is too short. A strong answer should have at least 150 words.")

        readability = textstat.flesch_reading_ease(essay)

        if readability < 40:
            predicted_score -= 5
            feedback.append("Essay is difficult to read. Use shorter and clearer sentences.")

        paragraphs = [p for p in essay.split('\n') if p.strip()]

        if len(paragraphs) < 3:
            predicted_score -= 10
            feedback.append("Essay should contain introduction, body, and conclusion paragraphs.")

        mistakes = find_mistakes(essay)

        if len(mistakes) > 0:
            feedback.append(f"Detected {len(mistakes)} possible spelling mistakes.")

        predicted_score = max(0, min(predicted_score, 100))

        # Grade mapping
        if predicted_score >= 90:
            grade = "A+"
        elif predicted_score >= 80:
            grade = "A"
        elif predicted_score >= 70:
            grade = "B"
        elif predicted_score >= 60:
            grade = "C"
        elif predicted_score >= 50:
            grade = "D"
        else:
            grade = "F"

        result = {
            "score": predicted_score,
            "grade": grade,
            "feedback": feedback,
            "mistakes": mistakes,
            "word_count": word_count,
            "readability": round(readability, 2)
        }

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)