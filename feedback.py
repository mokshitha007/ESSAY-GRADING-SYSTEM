import language_tool_python
import textstat
import spacy

tool = language_tool_python.LanguageTool('en-US')
nlp = spacy.load("en_core_web_sm")

def grammar_score(text):

    errors = len(tool.check(text))

    if errors < 3:
        return 9
    elif errors < 6:
        return 8
    elif errors < 10:
        return 6
    else:
        return 4


def vocabulary_score(text):

    doc = nlp(text)

    words = [token.text.lower() for token in doc if token.is_alpha]

    if len(words) == 0:
        return 0

    richness = len(set(words)) / len(words)

    return round(richness * 10, 2)


def readability_score(text):

    score = textstat.flesch_reading_ease(text)

    if score > 60:
        return 9
    elif score > 50:
        return 8
    elif score > 40:
        return 7
    else:
        return 6