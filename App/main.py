from re import sub
from Dataframe_Cleaner import Cleaner
from Reddit_Loader import Loader
import datetime
import pandas as pd
import pickle
import re
import string
import nltk, ssl

START = "01/01/2020"
END = datetime.datetime.now().strftime("%d/%m/%Y") #today
ticker = "gme"

def load_data_from_pushshift(ticker, start, end):
    ## Loads data from pushshift, drops unneded columns and save it as a pickle file
    l = Loader(ticker, START, END, "wallstreetbets")
    submissions = l.load_submissions()

    submissions.to_pickle("./data/submissions.pkl")

def drop_unneeded_columns(submissions):
    submissions = submissions.drop(columns = ["allow_live_comments", "author_flair_css_class", "author_flair_richtext", 
                        "author_flair_text", "author_flair_type", "author_fullname", "author_patreon_flair",
                        "author_premium", "domain", "awarders", "can_mod_post", "contest_mode",
                        "gildings", "is_crosspostable", "is_meta", "is_original_content", "is_reddit_media_domain",
                        "is_robot_indexable", "is_self", "link_flair_background_color", "link_flair_text_color",
                        "link_flair_type", "link_flair_css_class", "link_flair_richtext", "link_flair_template_id",
                        "locked", "media_only", "no_follow", "over_18", "parent_whitelist_status", "permalink",
                        "pinned", "pwls", "send_replies", "spoiler", "stickied", "subreddit_type", "suggested_sort",
                        "treatment_tags", "whitelist_status", "wls", "preview", "is_gallery", "thumbnail_height",
                        "thumbnail_width", "url_overridden_by_dest", "media_metadata", "secure_media", "secure_media_embed",
                        "author_flair_background_color", "author_flair_text_color", "edited", "gallery_data",
                        "banned_by", "discussion_type", "crosspost_parent", "crosspost_parent_list",
                        "author_flair_template_id", "author_is_blocked", "is_created_from_ads_ui",
                        "steward_reports", "gilded", "distinguished", "collections"])

    return submissions

def flag_records_with_no_content(submissions):
    # Create new column for the flag
    submissions["missing_content"] = False

    # If the content contains [removed] or [deleted] it usually was removed by a moderator
    submissions.loc[(submissions["selftext"] == "[removed]"), "missing_content"] = True
    submissions.loc[(submissions["selftext"] == "[deleted]"), "missing_content"] = True

    # Flag records that have length 0
    empty_content = []
    for i, text in enumerate(submissions["selftext"]):
        if(len(str(text)) == 0):
            empty_content.append(i)
    submissions.loc[empty_content, "missing_content"] = True

    # Containing N/A
    submissions.loc[(submissions["selftext"].isnull() == True), "missing_content"] = True

    return submissions

def read_annotations():
    seed = pd.read_excel("./data/annotation.xlsx", header = None, usecols = range(0, 4))
    # Rename columns
    seed = seed.rename(columns = {0 : "index", 1 : "title", 2 : "content", 3 : "sentiment"})
    return seed

def remove_missing_content(submissions):
        submissions.loc[submissions["missing_content"] == True, "selftext"] = ""
        return submissions

def concatenate_text(submissions):
    submissions["text"] = submissions["title"] + " " + submissions["selftext"]
    return submissions

def drop_columns(submissions):
    submissions = submissions.drop(columns = {"title", "selftext"})
    return submissions

def add_sentiment_column(seed, submissions):
    submissions["sentiment"] = ""
    for i in seed["index"]:
        submissions.loc[i, "sentiment"] = seed.loc[i/10, "sentiment"]
    return submissions

def remove_URL(sample):
    """Remove URLs from a sample string"""
    return re.sub(r"http\S+", "", str(sample))

def remove_escape_newline(sample):
    """Remove URLs from a sample string"""
    return re.sub(r"\n", "", str(sample))

def remove_escape_tab(sample):
    """Remove URLs from a sample string"""
    return re.sub(r"\t", "", str(sample))

def remove_punctuation(text):
    punctuationfree="".join([i for i in str(text) if i not in string.punctuation])
    return punctuationfree

def lowercase_text(submissions):
    submissions["text"] = submissions["text"].str.lower()
    return submissions

def remove_stopwords(l):
    new_list = []
    new_sentence = []
    for sentence in l:
        for word in sentence.split(" "):
            if word not in nltk.corpus.stopwords.words('english') and len(word) > 0:
                new_sentence.append(word)
        new_list.append(new_sentence)
        new_sentence = []
    return new_list

def remove_special_character(l):
    new_l = []
    for word in l:
        if word != "-" and word != "—":
            new_l.append(word.replace("¿", ""))
    return new_l

def remove_some_chars(sample):
    """Remove URLs from a sample string"""
    return re.sub(r"[“”—-]", "", str(sample))


def prepare_data_frame(seed, submissions):
    submissions = remove_missing_content(submissions)
    submissions = concatenate_text(submissions)
    submissions = drop_columns(submissions)
    submissions = add_sentiment_column(seed, submissions)
    return submissions

def clean_text_column(submissions):
    submissions["text"] = submissions["text"].apply(lambda x: remove_URL(x))
    submissions["text"] = submissions["text"].apply(lambda x: remove_escape_newline(x))
    submissions["text"] = submissions["text"].apply(lambda x: remove_escape_tab(x))
    submissions["text"] = submissions["text"].apply(lambda x: remove_punctuation(x))
    submissions = lowercase_text(submissions)
    submissions["text"] = remove_stopwords(list(submissions["text"]))
    submissions["text"] = submissions["text"].apply(lambda x: remove_special_character(x))
    submissions["text"] = submissions["text"].apply(lambda x: remove_some_chars(x))
    return submissions

if __name__ == "__main__":
    # load_data_from_pushshift(ticker, START, END)
    # I only copied this from the Scraper.ipynb notebook. Need to check if it actually works...
    submissions = pd.read_pickle("./data/submissions.pkl")
    submissions = drop_unneeded_columns(submissions)
    submissions = flag_records_with_no_content(submissions)
    seed = read_annotations()
    submissions = prepare_data_frame(seed, submissions)
    submissions = clean_text_column(submissions[:10])
    print(submissions["text"])