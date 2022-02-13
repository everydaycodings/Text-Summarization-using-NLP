from spacy.lang.en.stop_words import STOP_WORDS
import en_core_web_sm
from string import punctuation
from heapq import nlargest
import spacy_streamlit
import requests
import json
from bs4 import BeautifulSoup
import configparser


nlp= en_core_web_sm.load()
stopwords = list(STOP_WORDS)
punctuation = punctuation + "\n"

config = configparser.ConfigParser()
config.read("config.ini")
news_api_key = config["API"]["news_api"]



def spacy_rander(summary):

    summ = nlp(summary)
    rend = spacy_streamlit.visualize_ner(summ, labels=nlp.get_pipe("ner").labels, title="Summary Visualization", show_table=False)
    
    return rend


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


def fetch_news_links():
    link_list = []

    reqUrl = "https://newsapi.org/v2/everything?sources=bbc-news&q=india&language=en&apiKey={}".format(news_api_key)

    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }

    payload = ""

    response = requests.request("GET", reqUrl, data=payload,  headers=headersList).text
    response = json.loads(response)

    tw = 0
    for i in range(len(response["articles"])):
        if tw ==10:
            pass
        else:
            if "/news/" in response["articles"][i]["url"]:
                link_list.append(response["articles"][i]["url"])
            else:
                pass
            tw += 1

    return link_list



def get_summary(text):
    doc = nlp(text)
    tokens = [token.text for token in doc]

    word_frequencies = word_frequency(doc)
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max(word_frequencies.values())
    
    sentence_tokens = [sent for sent in doc.sents]
    sentence_scores = sentence_score(sentence_tokens, word_frequencies)

    
    select_length = int(len(sentence_tokens)*0.10)
    summary  = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    summary = [word.text  for word in summary]
    summary = " ".join(summary)

    return summary





    
