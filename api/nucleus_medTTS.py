# Created on Thur Dec 20 2018
# author: mso

import time
import pandas as pd
import collections
from nltk.tokenize import word_tokenize
import gensim as gs
import numpy as np
import networkx as nx
from networkx.algorithms import clique

# the main logic of this program is to create a network representation
# of a document collection and use maximum degree network algorithm to identify
# most important and connected info and then speak the content to a provider.
def main():
    # start the timer
    start = time.time()
    # a file containing a list of documents is
    # converted into a dataframe and inserted into  variable "df"
    # the first column of a csv, tsv, txt, etc., is used as
    # the downstream network nodes
    df = file_in()
    # insert dataframe as parameter variable into our text mining model
    # returned vector space model with parameters is inserted into
    # these three variables - tf_idf weighting scheme, document collection, network labels, respectively
    tf_idf, corpus, dictionary, node_labels = tfidf(df)
    # returned similarity matrix and network "H" is inserted into variable "network"
    network = cosine_similarity(tf_idf, corpus, node_labels)
    # "network" is inserted into the approximate function to calculate
    # relationships within the document network
    cliques = approximate(network)
    # this function will use the text from maximum degree node and convert text to speech using
    # google TTS
    AI(cliques, df)
    stop = time.time()
    complexity = stop - start
    print('---------------------------\n','solved in ',format(complexity,'.2f'),'seconds')
    

# this function will read in the file as a dataframe
def file_in():
    # read in the file to create dataframe
    file = pd.read_csv('test.csv')
    df = file
    df = df['title'] + df['abstract']
    # return the dataframe so we can do matrix operations on it
    return df

# this function will create a vector space model of the corpus and calculate
# "term frequency - inverse document frequency" weights
def tfidf(df):
    # create a corpus from the keywords
    df = df[0]
    corpus = []
    for x in df:
        corpus.append(x)
    # create a dictionary for downstream network node labels
    node_labels = {}
    for x in range(len(df.index)):
        node_labels[df.index[x]] = df.values[x]
    tokenized = [[w.lower() for w in word_tokenize(str(text))] for text in corpus]
    # create a dictionary from the corpus
    dictionary = gs.corpora.Dictionary(tokenized)
    # create a bag of words rep with parameter tuning for D
    D = 1
    old_corpus = [dictionary.doc2bow(token) for token in tokenized]
    corpus = []
    for doc in old_corpus:
        threshold = [i for i in doc if i[1] >= D]
        corpus.append(threshold)
    # create a tf-idf model
    tf_idf = gs.models.TfidfModel(corpus)
    # return matrix with tf-idf weights, corpus, so we can later calculate similarity
    return tf_idf, corpus, dictionary, node_labels

# this function will calculate similarity between documents
# and create a network representation of the corpus
# so we can use network algorithms to analyze relationships
def cosine_similarity(tf_idf, corpus, node_labels):
    # similarity matrix with doc x doc
    sim = gs.similarities.MatrixSimilarity(tf_idf[corpus])
    # initialize an empty list
    similarity_matrix = []
    for s in sim:
        similarity_matrix.append(s)
    # use numpy and make an array that we can use for pandas
    similarity_array = np.array(similarity_matrix)
    df = pd.DataFrame(similarity_array)
    # import the network library and read in the dataframe
    G = nx.from_pandas_adjacency(df)
    network = nx.relabel_nodes(G, node_labels)
    # return the network "H" so we can use network approximations and algorithms
    return network

# this function will calculate network approximations to find
# maximum degree node
def approximate(network):
    threshold = 0.25
    low_sim_edges = []
    for x in network.edges.data():
        if (list(x[2].values())) < [threshold]:
                low_sim_edges.append((x[0],x[1]))
    network.remove_edges_from(low_sim_edges)
    # compute the degree centrality of nodes in the network
    cliques = clique.enumerate_all_cliques(network)
    # find the maximal clique   
    # return the clique

    return cliques 

def AI(cliques, df):
    for c in cliques:
        if len(c) > 1:
            print(c)



def network_search(input_list):
    '''
    input:
        [{'doc_id': '46', 'content': ['Percutaneous cryoab...'], ...]
    output:
        {0: {'doc_id': '46', 'content': ['Percutaneous cryoablation...']},1: {...}}

    '''
    temp_list = []
    for i in range(len(input_list)):
        temp_list.append(input_list[i]["content"][0])
    
    df = pd.DataFrame(temp_list)
    tf_idf, corpus, dictionary, node_labels = tfidf(df)
    network = cosine_similarity(tf_idf, corpus, node_labels)
    cliques = approximate(network)
    res_list = []
    for c in cliques:
        if len(c) > 1:
            res_list.append(c)
            # print(c)
    
    res_dict = collections.defaultdict(dict)
    for i in range(len(res_list)):
        res_dict[i]['doc_id'] = str(i)
        res_dict[i]['content'] = res_list[i]
    
    print(dict(res_dict))
    return dict(res_dict)


    # print(temp_list, len(temp_list), '\n', temp_list[0])






# call the main function so the program executes
# main()
