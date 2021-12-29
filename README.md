# Master-Thesis
This is the repository for Stefan Winter's Master thesis at Tilburg University.

## App
The app folder contains all the code.
Note: Due to time pressure technical debt was incurred. As a result, the project structure is quite messy and will be fixed in due time.
Most data is not pushed to the repository, because of Github's size constraints.
All packages and modules that were used can be found in the Requirements.txt file.

Additional information on some important packages:
To label the initial train set, I created a graphical user interface using tkinter: https://docs.python.org/3/library/tkinter.html

To create the t-sne visualization, I relied on the documentation provided by Yellowbrick: https://www.scikit-yb.org/en/latest/api/text/tsne.html

To implement the Active Learner, I used modAL: https://github.com/modAL-python/modAL

To implement BERT the following tutorial was used: https://www.kaggle.com/xhlulu/disaster-nlp-keras-bert-using-tfhub/notebook

The LSTM for sentiment classification was implemented by using material provided during the Deep Learning course at Tilburg University, taught by Dr. Vanmassenhove and Dr. Saygili. The LSTM implementation for time-series forecasting mostly relied on the tutorial at machinelearningmastery: https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/

All scikit-learn packages and classes, such as train_test_split, TfidfVecotriser, LabelEncoder, GridSearchCV, Pipeline, SVM and NB were implemented by utilizing material provided during the Machine Learning course at Tilburg University, taught by Dr. Güven and Dr. Önal.

To query the data from pushshift, the explanation of pmaw API wrapper from Github was used: https://github.com/mattpodolak/pmaw
The data was manually verified, by comparing specific, randomly-sampled, instances with the actual posts on reddit.