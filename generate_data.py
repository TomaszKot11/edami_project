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
from copy import deepcopy

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

        #prev_candidates = candidates
        candidates = create_new_candidates(candidates)

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


def create_1len_table(text):
    table = []
    sid = 1
    sentences = text.split(". ")
    sentences[-1] = sentences[-1].replace('.','')
    for sent in sentences:
        eid = 1
        words = sent.split(" ")
        for word in words:
            table.append([sid, eid, word])
            eid += 1
        sid += 1
    return table


def create_1_len_seq(table, min_support):
    seq_1len = []
    items = []
    for elem in table:
        item = elem[-1]
        if item not in items:
            items.append(item)
            cur_seq = []
            for e in table:
                if item == e[-1]:
                    cur_seq.append(e[:-1])
            seq_1len.append(cur_seq)

    final_seq_1len = []
    final_items = []
    i = 0
    for seq in seq_1len:
        if len(seq) >= min_support:
            final_seq_1len.append(seq)
            final_items.append(items[i])
        i += 1
    return final_seq_1len, final_items





def create_2_len_seq(seq_1len, items, min_support):
    fst_idx = 0
    seq_2len = []
    items_2len = []
    for fst_item in items:

        snd_idx = 0
        for snd_item in items:
            items_2len.append([fst_item, snd_item])
            cur_sequences = []
            for fst_seq in seq_1len[fst_idx]:

                for snd_seq in seq_1len[snd_idx]:

                    cur_seq = deepcopy(fst_seq)
                    if fst_seq[0] == snd_seq[0] and fst_seq[-1] < snd_seq[-1]:

                        cur_seq.append(snd_seq[-1])
                        cur_sequences.append(cur_seq)
            seq_2len.append(cur_sequences)
            snd_idx += 1
        fst_idx +=1

    final_seq = []
    final_items = []
    i = 0
    for seq in seq_2len:
        if len(seq) >= min_support:
            final_seq.append(seq)
            final_items.append(items_2len[i])
        i += 1
    return final_seq, final_items




def create_x_len_seq(seq_x_len, seq_2len, items_x, items_2, min_support):
    fst_idx = 0
    seq_xlen = []
    items_xlen = []
    for fst_item in items_x:

        snd_idx = 0
        items_2_subset = [it for it in items_2 if it[0] == fst_item[-1]]
        for snd_item in items_2_subset:

            snd_idx = items_2.index(snd_item)
            cur_fst_item = deepcopy(fst_item)
            cur_fst_item.append(snd_item[1])
            items_xlen.append(cur_fst_item)


            cur_sequences = []
            for fst_seq in seq_x_len[fst_idx]:
                #print(fst_seq)
                for snd_seq in seq_2len[snd_idx]:
                    #print(snd_seq)
                    cur_seq = deepcopy(fst_seq)
                    if fst_seq[0] == snd_seq[0] and fst_seq[-1] == snd_seq[1]:
                        cur_seq.append(snd_seq[-1])
                        cur_sequences.append(cur_seq)
                #print("-------------------------------")
            seq_xlen.append(cur_sequences)

        fst_idx +=1

    final_seq = []
    final_items = []
    i = 0
    for seq in seq_xlen:
        if len(seq) >= min_support:
            final_seq.append(seq)
            final_items.append(items_xlen[i])
        i += 1
    return final_seq, final_items




def SPADE(text, min_support, max_seq_len):
    table_1len = create_1len_table(text)
    seq_1len, items = create_1_len_seq(table_1len, min_support)
    seq_2_len, items_2 = create_2_len_seq(seq_1len, items, min_support)
    new_seq_len = seq_2_len
    new_items = items_2

    seq_len = 2
    while max_seq_len > seq_len and len(new_items) != 0:
        prev_seq_len = new_seq_len
        prev_items = new_items
        new_seq_len, new_items = create_x_len_seq(prev_seq_len, seq_2_len, prev_items, items_2, min_support)
        #print(new_items)
        seq_len += 1
    
    return new_items








# Example of use
#minimum_support = 4
#max_seq_len = 4
#url = 'https://en.wikipedia.org/wiki/United_States'
#text = get_text_wiki(url)
#page_code, word_list, number_list = text_to_code(text)

#candidates = GSP(page_code, number_list, minimum_support=9, max_seq_len=3)


#candidates_translated = translate_to_words(candidates, word_list)
#candidates_translated


#cand_spade = SPADE(text, min_support=9, max_seq_len=3)
#cand_spade


#text = 'jest krowa tam drzewo dole. nie ma krowa tam dole. drzewo nie. jest tam pies drzewo. drzewo krowa nie. co byla krowa tam dole. co tam jest drzewo. nie tam krowa. tam krowa jest.'
#table_1len = create_1len_table(text)
#seq_1len, items = create_1_len_seq(table_1len, min_support=9)
#seq_2len, items_2len = create_2_len_seq(seq_1len, items, min_support=9)
#seq_3len, items_3len = create_x_len_seq(seq_2len, seq_2len, items_2len, items_2len, min_support=9)



