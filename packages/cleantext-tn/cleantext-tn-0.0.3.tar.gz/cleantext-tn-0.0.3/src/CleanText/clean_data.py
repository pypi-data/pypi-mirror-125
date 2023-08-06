import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


def clean_punctuation(text):
    cleaned = re.sub(r'[?|!|\'|"|#]', r'', text)
    cleaned = re.sub(r'[.|,|)|(|\|/]', r' ', cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n", " ")
    return cleaned


def keep_alphabetical(text):
    alpha_sent = ""
    for word in text.split():
        alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent


def remove_stopwords(text):
    sw = stopwords.words("english")
    re_stop_words = re.compile(r"\b(" + "|".join(sw) + ")\\W", re.I)
    return re_stop_words.sub(" ", text)


def lemmatization_text(text):
    lemmatizer = WordNetLemmatizer()
    words = text.split(" ")
    result = []
    for word in words:
        r = lemmatizer.lemmatize(word)
        result.append(r)
    return " ".join(result)


def clean_text(raw, clean_punc=True, clean_non_alphabetical=True, clean_stopwords=True,
               lemmatization=True, return_as_string=False):
    result = raw
    if clean_punc:
        result = clean_punctuation(result)
    if clean_non_alphabetical:
        result = keep_alphabetical(result)
    if clean_stopwords:
        result = remove_stopwords(result)
    if lemmatization:
        result = lemmatization_text(result)
    result = re.sub(' +', ' ', result)
    if not return_as_string:
        result = result.split(" ")
        if "" in result:
            result.remove("")
    return result
