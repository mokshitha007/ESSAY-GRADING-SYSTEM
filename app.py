from flask import Flask, render_template, request
import textstat
import language_tool_python
import os

app = Flask(__name__)
tool = language_tool_python.LanguageTool('en-US')

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    feedback = []
    if request.method == "POST":
        essay = request.form.get("essay", "")
        if essay.strip():
            flesch_score = textstat.flesch_reading_ease(essay)
            grade_level = textstat.text_standard(essay, float_output=False)
            matches = tool.check(essay)
            feedback = [f"{m.ruleId}: {m.message}" for m in matches]
            result = {"flesch_score": flesch_score, "grade_level": grade_level}
    return render_template("index.html", result=result, feedback=feedback)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
