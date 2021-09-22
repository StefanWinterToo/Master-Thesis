from pmaw import PushshiftAPI
from Date_Converter import Convert
import pandas as pd

# Loads data from Pushshift
class Loader():
    def __init__(self, ticker, after, before, sub):
        self.ticker = ticker
        self.after = after
        self.before = before
        self.sub = sub
        self.convert_date()
    
    def convert_date(self):
        c = Convert(self.after, self.before)
        self.after, self.before = c.convert_time_to_unix()

    def load_submissions(self):
        api = PushshiftAPI()

        submissions = api.search_submissions(subreddit=self.sub, q = self.ticker, before=self.before, after=self.after, mem_safe=True, safe_exit=True)
        print(f'Retrieved {len(submissions)} submissions from Pushshift.')

        submissions_df = pd.DataFrame(submissions)

        return submissions_df