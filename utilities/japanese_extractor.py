import spacy
import ginza
nlp = spacy.load("ja_ginza")


# Load Ginza model directly
nlp = spacy.load("ja_ginza")


def extract_nouns_verbs_ginza(text):
    doc = nlp(text)

    keywords = []

    for token in doc:
        if token.pos_ == "NOUN" or token.pos_ == "VERB" or token.pos_ == "ADJ":
            keywords.append(token.text)
    return keywords
