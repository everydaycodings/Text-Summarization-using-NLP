import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy import load
import en_core_web_sm
from string import punctuation
from heapq import nlargest


nlp= en_core_web_sm.load()
stopwords = list(STOP_WORDS)
punctuation = punctuation + "\n"


def word_frequency(doc):
    word_frequencies = {}

    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    
    return word_frequencies


def sentence_score(sentence_tokens, word_frequencies):
    sentence_score = {}

    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_score.keys():
                    sentence_score[sent] = word_frequencies[word.text.lower()] 
                else:
                    sentence_score[sent] += word_frequencies[word.text.lower()]
    
    return sentence_score


def get_summary(text):
    doc = nlp(text)
    tokens = [token.text for token in doc]

    word_frequencies = word_frequency(doc)
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max(word_frequencies.values())
    
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = sentence_score(sentence_tokens, word_frequencies)

    if len(text) >= 3000:
        select_length = int(len(sentence_tokens)*0.3)
    else:
        select_length = int(len(sentence_tokens)*0.3)
    summary  = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    summary = [word.text  for word in summary]
    summary = " ".join(summary)

    return summary





    
