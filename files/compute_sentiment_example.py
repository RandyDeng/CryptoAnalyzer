import json
import re

TERMS={}

#-------- Load Sentiments Dict ----
sent_file = open('AFINN-111.txt')
sent_lines = sent_file.readlines()
for line in sent_lines:
	s = line.split("\t")
	TERMS[s[0]] = s[1]

sent_file.close()


#-------- Find Sentiment  ----------
def findsentiment(tweet):
    sentiment=0.0

    if tweet.has_key('text'):
        text = tweet['text']		
        text=re.sub('[!@#$)(*<>=+/:;&^%#|\{},.?~`]', '', text)
        splitTweet=text.split()

        for word in splitTweet:
            if TERMS.has_key(word):
                sentiment = sentiment+ float(TERMS[word])

    return sentiment


def main():	

    #This is how a tweet object will look like. The key 'text' within this dictionary has the tweet text.
    raw_tweet_file=open('rawTweet.txt','r')
    tweetobj = raw_tweet_file.read()
    
    tweet = json.loads(tweetobj)
    #Send tweet object to findsentiment function
    sentiment = findsentiment(tweet)
    
    print 'Tweet:',tweet['text']
    print 'Sentiment:',sentiment
                
    
if __name__ == '__main__':
    main()
	
