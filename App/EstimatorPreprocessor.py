import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import gensim

def load_cleaned_submissions():
    data = pd.read_pickle("./data/final_cleaned_submissions.pkl")
    return data

def encode_labels(data, encode = True):
    labels = data["sentiment"]
    if encode:
        lenc = LabelEncoder()
        y = lenc.fit_transform(labels.tolist())
        return y
    else:
        return labels

def vectorize_text(data):
    # Vectorize text using tfidf
    tfidf = TfidfVectorizer(preprocessor=' '.join, lowercase=False, min_df=5) # min_df = Minimum occurance of words
    X = tfidf.fit_transform(data["text"])
    return X

# So far not needed:
def max_sentence_length(sentences, truncate = True, max_len = 90):
    '''
    Truncates sentence to reduce dimensionality.
    '''
    max_sentence_len = 0
    for sentence in sentences:
        if len(sentence) > max_sentence_len:
            max_sentence_len = len(sentence)
    if truncate == True:
        return max_len
    else:
        return max_sentence_len

def embedding_word2vec(sentences, vec_size = 200, min_c = 1, w = 5):
    word_model = gensim.models.Word2Vec(sentences, vector_size = vec_size, min_count = min_c, window = w)
    pretrained_weights = word_model.wv.vectors
    vocab_size, embedding_size = pretrained_weights.shape
    return word_model, pretrained_weights, vocab_size, embedding_size

def word2idx(word_model, word):
    return word_model.wv.key_to_index[word]

def idx2word(word_model, idx):
    return word_model.wv.index_to_key[idx]

def save_param_list_keras(path, p_list):
    textfile = open(path, "w")
    for item in p_list:
        textfile.write(item + "\n")
    textfile.close()