class Cleaner():

    def __init__(self, df):
        self.df = df
    
    def missing_content_flag(self):
        s = self.df
        '''Inserts a column to indicate whether a post contains content or not.'''
        s["missing_content"] = False
        s.loc[(s["selftext"] == "[removed]"), "missing_content"] = True
        s.loc[(s["selftext"] == "[deleted]"), "missing_content"] = True
        s.loc[(s["selftext"].isnull() == True), "missing_content"] = True
        
        empty_content = []
        for i, text in enumerate(s["selftext"]):
            if(len(str(text)) == 0):
                empty_content.append(i)

        s.loc[empty_content, "missing_content"] = True

        return s

    