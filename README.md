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
-->             if (is_twitter_cf_modal(word)):
-->                 tag = 'MD'
            output.append((word, tag))
            prev2 = prev
            prev = tag

        return output



def is_twitter_cf_modal(word):
    if word == 'should' or \
        word == 'shoulda' or \
        word == 'shulda' or \
        word == 'shuda' or \
        word == 'shudda' or \
        word == 'shudve' or \
        word == 'would' or \
        word == 'woulda' or \
        word == 'wuda' or \
        word == 'wulda' or \
        word == 'wudda' or \
        word == 'wudve' or \
        word == 'wlda' or \
        word == 'could' or \
        word == 'coulda' or \
        word == 'cudda' or \
        word == 'culda' or \
        word == 'cudve' or \
        word == 'must' or \
        word == 'mustve' or \
        word == 'might' or \
        word == 'mightve' or \
        word == 'outght' or \
        word == 'may' or \
        word == 'i\'d' or \
        word == 'id' or \
        word == 'we\'d' or \
        word == 'youd' or \
        word == 'you\'d':
            return True
    return False

---------------------------------------------