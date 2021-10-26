from Reddit_Loader import Loader
import datetime
import pandas as pd
import pickle

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

def preprocess_content(submissions):
    pass

if __name__ == "__main__":
    # load_data_from_pushshift(ticker, START, END)
    # I only copied this from the Scraper.ipynb notebook. Need to check if it actually works...
    submissions = pd.read_pickle("./data/submissions.pkl")
    submissions = drop_unneeded_columns(submissions)
    submissions = flag_records_with_no_content(submissions)
    print(submissions)