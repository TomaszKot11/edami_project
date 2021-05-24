import requests
import wikipedia
import re
import pandas as pd
import numpy as np
from collections import Counter
import itertools
from urllib import request
import urllib
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt

from wikipedia.wikipedia import page




def get_text_wiki(url):
    res = requests.get(url)
    wiki = BeautifulSoup(res.text, "html.parser")
    text = str('')
    for i in wiki.select('p'):
        text += i.getText()
    # Delete headers
    text = re.sub(r'==.*?==+', '', text)
    text = text.replace('\n', '')
    # Delete punctuation but not dots
    text = re.sub(r'[^\w\s&^.]','',text)
    text = text.lower()
    # Delete words shorter than 3
    text = re.sub(r'\b\w{1,3}\b', '', text)
    text = re.sub('\s+',' ', text)
    text = text.replace("..", ".")
    text = text.replace("..", ".")
    text = text.replace(". .", ".")
    text = text.replace(" .", ".")
    #text = re.sub(r'\s([?.!"](?:\s|$))', r'\1', text)
    #text = re.sub(r'..', r'.', text)
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
    sentences[-1] = sentences[-1].replace('.','')
    #print(sentences)
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





def create_seq_list(page_code):
    page_code = [value for value in page_code if value != '-1']

    seq_list = []
    new_seq = []
    for i in range(len(page_code)):
        if page_code[i] != '-2':
            new_seq.append(page_code[i])
        else:
            seq_list.append(new_seq)
            new_seq = []
    return seq_list







def create_new_candidates(prev_candidates):
    new_candidates_list = []
    for cand in prev_candidates:
        first_elem = [cand[0]]
        rest = cand[1:]
        #print(first_elem)
        #print(rest)
        for cand2 in prev_candidates:
            without_last_elem = cand2[:-1]
            #print(without_last_elem)
            if rest == without_last_elem:
                #print("jest git")
                #print(first_elem+cand2)
                #cand2.insert(0,first_elem)
                #print(cand2)
                new_candidates_list.append(first_elem+cand2)
                #print(new_candidates_list)
    new_candidates_list.sort()
    new_candidates_list = list(new_candidates_list for new_candidates_list,_ in itertools.groupby(new_candidates_list))
    return new_candidates_list



def calculate_support(candidates_list, seq_list):
    total_support = []
    for candidates in candidates_list:
        #print(candidates)
        cand_support = 0   
        for seq in seq_list:
            #print(seq)
            current_support = 1
            seq_sublist = seq
            for elem in candidates:
                if elem in seq_sublist:
                    #print(elem)
                    idx = seq_sublist.index(elem)
                    seq_sublist = seq_sublist[idx+1:]
                    #print(seq_sublist)
                else:
                    #print(elem)
                    current_support = 0
                    break   
            cand_support += current_support
        total_support.append(cand_support)
    return total_support



def GSP(page_code, number_list, minimum_support, max_seq_len):
    seq_list = create_seq_list(page_code)
    candidates = [[number_list] for number_list in number_list]  
    prev_candidates = candidates
    i = 1
    while len(candidates) != 0 and i <= max_seq_len:
        prev_candidates = candidates
        support_all = calculate_support(candidates, seq_list)
        candidates_idx = [i for i,v in enumerate(support_all) if v >= minimum_support]
        candidates = [candidates[i] for i in candidates_idx]
        
        #print(candidates)
        candidates = create_new_candidates(candidates)
        #print(candidates)
        i += 1
    if len(candidates) == 0 :
        candidates = prev_candidates
    return prev_candidates



def translate_to_words(candidates, word_list):
    for i in range(len(candidates)):
        for j in range(len(candidates[i])):
            candidates[i][j] = word_list[int(candidates[i][j])]
    return candidates


def create_graph(candidates):

    G = nx.DiGraph()
    for cand in candidates:
        for i in range(len(cand)-1):
            if G.has_edge(cand[i], cand[i+1]):
                w = G[cand[i]][cand[i+1]]['weight'] + 1
            else:
                w = 1
            #if w > 4:
            #    w = 4
            G.add_edge(cand[i], cand[i+1], weight = w)    
    weights = [G[u][v]['weight'] for u,v in G.edges()]
    #weights = weights - min(weights)
    weights = [round((float(i)-min(weights))/(max(weights)-min(weights))*3+1) for i in weights]
    #pos = nx.spring_layout(G, scale=10)
    #nx.draw_kamada_kawai(G, with_labels = True, width = weights)
    nx.draw_circular(G, with_labels = True, width = weights, node_color='forestgreen', edge_color='skyblue')
    plt.show()






# Example of use
#minimum_support = 4
#max_seq_len = 4
#url = 'https://en.wikipedia.org/wiki/United_States'
#text = get_text_wiki(url)
#page_code, word_list, number_list = text_to_code(text)

#candidates = GSP(page_code, number_list, minimum_support, max_seq_len)


#candidates_translated = translate_to_words(candidates, word_list)


