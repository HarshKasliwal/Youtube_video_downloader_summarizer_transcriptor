from nltk.corpus import stopwords
import networkx as nx
from nltk.tokenize import word_tokenize,sent_tokenize
import numpy as np
def get_score(sim_mat):
    nx_graph = nx.from_numpy_array(sim_mat)
    score = nx.pagerank(nx_graph, max_iter=500)
    return score

def summarize(text):
    sentences = sent_tokenize(text) 
    t_clean_sentences = []
    for i in range(len(sentences)):
        obj = text_preprocessing(sentences[i])
        j = obj.text_cleaner()
        t_clean_sentences.append(j)
      
    clean_sentences = []
    for i in range(len(t_clean_sentences)):
        a = gb.predict(vectorizer.transform([t_clean_sentences[i]]))
        if a[0] != 'whQuestion' and a[0] != 'ynQuestion':
            clean_sentences.append(t_clean_sentences[i])



    stop_words = set(stopwords.words('english'))

    filtered_sentences = []

    for i in range(len(clean_sentences)):
        word_tokens = word_tokenize(clean_sentences[i])
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_sentences.append(" ".join(filtered_sentence))
    filtered_sentences
    #sentence vectors
    sentence_vectors = []
    for i in filtered_sentences:
        if len(i) != 0:
            v = sum([word_embeddings.get(w, np.zeros((100,))) for w in i.split()])/(len(i.split())+0.001)
        else:
            v = np.zeros((100,))
        sentence_vectors.append(v)

    from sklearn.metrics.pairwise import cosine_similarity
    sim_mat = np.zeros([len(clean_sentences), len(clean_sentences)])

    for i in range(len(clean_sentences)):
          for j in range(len(clean_sentences)):
                if i != j:
                      sim_mat[i][j] = cosine_similarity(sentence_vectors[i].reshape(1,100), sentence_vectors[j].reshape(1,100))[0,0]
    
    #pagerank scores
    scores = get_score(sim_mat)
    ranked_sentences = sorted(((scores[i],s) for i,s in enumerate(clean_sentences)), reverse=True)
    # Specify number of sentences to form the summary
  

    # Generate summary
    summary = []
    for i in range(len(ranked_sentences)):
        summary.append(ranked_sentences[i][1].capitalize())
    return summary

summarize("gari.txt")