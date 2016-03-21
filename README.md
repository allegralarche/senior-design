-------------------------------------------------------------------
Make sure you do this:
mysql -u root
GRANT SELECT ON randomTwitter_by_month.* TO 'username'@'localhost';
GRANT SELECT ON randomTwitter_by_month.* TO 'username'@'%';
-------------------------------------------------------------------
Scripts

getTweetsFromSQL.py is used to parse the results of an SQL query to a text file. To run, use do the following two steps.

1. Run in command prompt: 
ssh username@ssh.wwbp.org -i "path_to_private_key" -L 3306:127.0.0.1:3306 -N

2. Run in different command prompt:
python getTweetsFromSQL.py <username> <sql query file> <path to output file>

getTaggedFile.py is used to tag the Tweets that were output from getTweetsFromSQL.py
Usage: python getTaggedFile.py <input file> <output file>
-------------------------------------------------------------------

Code added to nltk/tag/perceptron.py

    def tag(self, tokens):
        '''
        Tag tokenized sentences.
        :params tokens: list of word
        :type tokens: list(str)
        '''
        prev, prev2 = self.START
        output = []
        
        context = self.START + [self.normalize(w) for w in tokens] + self.END
        for i, word in enumerate(tokens):
            tag = self.tagdict.get(word)
            if not tag:
                features = self._get_features(i, word, context, prev, prev2)
                tag = self.model.predict(features)
            ### ADD THESE LINES
            if (is_twitter_cf_modal(word)):
                tag = 'MD'
            ###
            output.append((word, tag))
            prev2 = prev
            prev = tag

        return output


### ADD THIS FUNCTION ###
def is_twitter_cf_modal(word):
    w = word.lower()
    if (w == 'should' or 
        w == 'shoulda' or 
        w == 'shulda' or 
        w == 'shuda' or 
        w == 'shudda' or 
        w == 'shudve' or 
        w == 'would' or 
        w == 'woulda' or 
        w == 'wuda' or 
        w == 'wulda' or 
        w == 'wudda' or 
        w == 'wudve' or 
        w == 'wlda' or 
        w == 'could' or 
        w == 'coulda' or 
        w == 'cudda' or 
        w == 'culda' or 
        w == 'cudve' or 
        w == 'must' or 
        w == 'mustve' or 
        w == 'might' or 
        w == 'mightve' or 
        w == 'outght' or 
        w == 'may' or 
        w == 'i\'d' or 
        w == 'id' or 
        w == 'we\'d' or 
        w == 'youd' or 
        w == 'you\'d'):
            return True
    return False

---------------------------------------------