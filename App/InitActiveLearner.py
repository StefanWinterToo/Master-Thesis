import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from modAL.models import ActiveLearner
from modAL.uncertainty import uncertainty_sampling
from sklearn.svm import SVC
import os
import pickle
import scipy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder


def check_file_in_dir(path):
    '''
    Checks if the file exists in the given path.
    '''
    return os.path.exists(path)

def load_submissions():
    return pd.read_pickle("./data/cleaned_submissions.pkl")

def tfidf_encoding(data):
    tfidf = TfidfVectorizer(preprocessor=' '.join, lowercase=False, min_df=5) # min_df = Minimum occurance of words
    return tfidf.fit_transform(data)

def initial_training():

    data = load_submissions()

    text = data["text"]
    labels = data["sentiment"]

    # Get labeled instances
    indices = []
    for i in range(0, len(labels), 10):
        indices.append(i)
        
    # Set seed
    X_seed = text[indices]
    y_seed = labels[indices]

    # Get unlabeled instances
    new_indices = []
    for i in range(0, len(data["text"].index)):
        if i not in indices:
            new_indices.append(i)

    # Encode labels
    lenc = LabelEncoder()
    y_train = lenc.fit_transform(y_seed)

    # Vectorize text using tfidf
    
    X_train = tfidf_encoding(data["text"])

    # Set aside test set, to better judge the performance of the AL. This is not done in the literature
    
    X_train_seed, X_test, y_train_seed, y_test = train_test_split(X_train[indices], y_train, test_size=0.2, random_state=10)

    X_train_pool = X_train[new_indices] # Instances that need to be labeled

    if check_file_in_dir('AL/al_init.sav'):
        print("Active Learner Object already exists, loading object now.")
        learner = load_initial_model()
    else:
        # learner = ActiveLearner(
        #     estimator = SVC(probability=True),
        #     query_strategy = uncertainty_sampling,
        #     X_training = X_train_seed,
        #     y_training = y_train_seed
        # )
        pass

    return X_train_seed, X_test, y_train_seed, y_test, X_train_pool, learner, new_indices

def initial_model(learner):
    filename = 'AL/al_init.sav'
    if check_file_in_dir(filename) == False:
        pickle.dump(learner.estimator, open(filename, 'wb')) # Save initial estimator
    else:
        print("Initial model already exists, try load_initial_model")

def save_new_indices(new_indices):
    filename = 'AL/data/annotations/indices/initial_new_indices.pkl'
    if check_file_in_dir(filename) == False:
        pickle.dump(new_indices, open(filename, 'wb'))
    else:
        print("File already exists, try load_new_indices instead")

def load_new_indices(filename = 'AL/data/annotations/indices/initial_new_indices.pkl'):
    if check_file_in_dir(filename) == True:
        f = pickle.load(open(filename, 'rb'))
        return f
    else:
        print("File not in directory, try save_new_indices instead")

def load_initial_model(path = 'AL/al_init.sav'):
    est = pickle.load(open(path, 'rb'))
    return est

def load_accuracy_scores():
    filename = "AL/data/acc_scores/accuracy_scores.pkl"
    if check_file_in_dir(filename) == False:
        accuracy_scores = []
        pickle.dump(accuracy_scores, open(filename, 'wb')) # Save empty accuracy_score list
    else:
        accuracy_scores = pickle.load(open(filename, 'rb')) # Load accuracy_score list
    return accuracy_scores

def save_initial_seed(X_train_seed, y_train_seed):
    path = "AL/data/seed/"
    filename_x_train_seed = path + "X_train_seed.npz"
    filename_y_train_seed = path + "y_train_seed.npy"

    if check_file_in_dir(filename_x_train_seed) == False:
        scipy.sparse.save_npz(filename_x_train_seed, X_train_seed)
        np.save(filename_y_train_seed, y_train_seed)
    else:
        print("Files already exist, use load_initial_seed instead!")

def load_initial_seed(path = "AL/data/seed/"):
    X_train_seed = scipy.sparse.load_npz(path + "X_train_seed.npz")
    y_train_seed = np.load(path + "y_train_seed.npy")
    return X_train_seed, y_train_seed

def save_test_data(X_test, y_test):
    path = "AL/data/test/"
    filename_X_test = path + "X_test.npz"
    filename_y_test = path + "y_test.npy"
    if check_file_in_dir(filename_X_test) == False:
        scipy.sparse.save_npz(filename_X_test, X_test)
        np.save(filename_y_test, y_test)
    else:
        print("Files already exist, use load_test_data instead!")

def load_test_data(path = "AL/data/test/"):
    X_test = scipy.sparse.load_npz(path + "X_test.npz")
    y_test = np.load(path + "y_test.npy")
    return X_test, y_test

def save_pool_data(X_train_pool):
    path = "AL/data/pool/"
    filename_X_train_pool = path + "X_train_pool.npz"
    if check_file_in_dir(filename_X_train_pool) == False:
        scipy.sparse.save_npz(filename_X_train_pool, X_train_pool)
    else:
        print("Files already exist, use load_pool_data instead!")

def load_pool_data(path = "AL/data/pool/"):
    X_train_pool = scipy.sparse.load_npz(path + "X_train_pool.npz")
    return X_train_pool

def get_most_recent_pool():
    '''
    Returns the pool file that was created most recently
    '''
    path = "C:\DEV\Master Thesis\App\AL\data\pool"
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    newest_pool_file = max(paths, key=os.path.getctime)
    return scipy.sparse.load_npz(newest_pool_file)


def run_this():
    X_train_seed, X_test, y_train_seed, y_test, X_train_pool, learner, new_indices = initial_training()
    initial_model(learner)
    save_initial_seed(X_train_seed, y_train_seed)
    save_test_data(X_test, y_test)
    save_pool_data(X_train_pool)
    save_new_indices(new_indices)

run_this()