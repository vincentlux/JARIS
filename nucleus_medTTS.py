# Created on Thur Dec 20 2018
# author: mso


# the main logic of this program is to create a network representation
# of a document collection and use maximum degree network algorithm to identify
# most important and connected info and then speak the content to a provider.
def main():
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
    maximum_degree = approximate(network)
    # this function will use the text from maximum degree node and convert text to speech using
    # google TTS
    AI(maximum_degree, df)





# this function will read in the file as a dataframe
def file_in():
    import pandas as pd
    # read in the file to create dataframe
    file = pd.read_csv('test.csv')
    df = file
    # return the dataframe so we can do matrix operations on it
    return df





# this function will create a vector space model of the corpus and calculate
# "term frequency - inverse document frequency" weights
def tfidf(df):
    import gensim as gs
    from nltk.tokenize import word_tokenize
    # create a corpus from the keywords
    corpus = []
    for x in df.values:
        corpus.append(x)
    # create a dictionary for downstream network node labels
    node_labels = {}
    for x in range(len(df.index)):
        node_labels[df.index[x]] = df.values[x][0]
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
    import gensim as gs
    import numpy as np
    import pandas as pd
    import networkx as nx
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
    H = nx.relabel_nodes(G, node_labels)
    # return the network "H" so we can use network approximations and algorithms
    return H





# this function will calculate network approximations to find
# maximum degree node
def approximate(network):
    from networkx.algorithms import clique, cluster, centrality
    threshold = 0.10
    low_sim_edges = []
    for x in network.edges.data():
        if (list(x[2].values())) < [threshold]:
                low_sim_edges.append((x[0],x[1]))
    network.remove_edges_from(low_sim_edges)
    # compute the degree centrality of nodes in the network
    central_nodes = centrality.degree_centrality(network)
    # find the highest degree centrality node
    maximum_degree = max(central_nodes.items(), key=lambda k: k[1])   
    # return the max degree node
    return maximum_degree 
    
    
    
    
    
    
def AI(maximum_degree, df):
    import subprocess
    from gtts import gTTS
    # speak on the topical content of this most central node
    content_file = 'centrality.mp3'
    tts_content = gTTS(text=maximum_degree[0], lang='en-us')
    tts_content.save(content_file)
    return_code = subprocess.call(['afplay', content_file])
    # locate and speak on the entire summary
#      file = open('glaucoma.csv','r')
#      for x in file:
#         if maximum_degree[0] in x:
#             summary = x
#             summary_file = 'summary.mp3'
#             tts_summary = gTTS(text=summary, lang='en-us')
#             tts_summary.save(summary_file)
#             return_code = subprocess.call(['afplay', summary_file])    
	




# call the main function so the program executes
main()
