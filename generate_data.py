import wikipedia
import re
import pandas as pd
import numpy as np



def get_text_wiki(url):
    # function gets url to a wikipedia webpage and
    # returns clean text from it
    url = url.split("/")
    print(url[-1])
    wiki = wikipedia.page(url[-1])
    text = wiki.content
    # Delete headers
    text = re.sub(r'==.*?==+', '', text)
    text = text.replace('\n', '')
    # Delete punctuation but not dots
    text = re.sub(r'[^\w\s&^.]','',text)
    text = text.lower()
    return text

def text_to_code(text):
    # function gets text and
    # returns:
    # - page_code - coded text where each word has a different number
    # - word_list - list of words in text
    # - number_list - list of numbers corresponding to the given words
    word_list = []
    number_list = []
    page_code = []
    word_delimiter = "-1"
    sent_delimiter = "-2"
    
    sentences = text.split(". ")
    i = 0
    for sent in sentences:
        words = sent.split(" ")
        for word in words:
            if (word in word_list):
                idx = word_list.index(word)
                num = number_list[idx]
                page_code.append(num)
            else:
                word_list.append(word)
                number_list.append(str(i))
                page_code.append(str(i))
                i = i + 1
    
            page_code.append(word_delimiter)

        page_code.pop()
        page_code.append(sent_delimiter)
    return page_code, word_list, number_list


#url = 'https://en.wikipedia.org/wiki/United_States'
#text = get_text_wiki(url)
#page_code, word_list, number_list = text_to_code(text)

