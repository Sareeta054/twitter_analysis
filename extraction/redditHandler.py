'''
    author: Bipin
'''


'''
Intended features:
1. Ability to get posts from the given subreddit
2. User should be able to provide list of subreddits and topics/keywords
3. Filter the posts according to the given keywords, eg. ("Minneapolis", "politics", "Amy Kru")
    1. Keywords in title should be valued more
    2. Posts with more upvotes should be valued more
'''

import praw
import helpers.oauthConfigReader as ocr


# reddit = praw.Reddit( client_id='zMSzNGC8iBad1Q', 
#                      client_secret='8lb0H2iq8BSlWj2g5u9FoDFsm20', 
#                      user_agent='api tutorial')

class RedditHandler:

    def __init__(self):
        authConfigs = ocr.OauthConfigsReader.getRedditConfigs()
        print("-- Inside Twitter Handler --")
        self.reddit = praw.Reddit( client_id = authConfigs['client_id'],
                                    client_secret = authConfigs['client_secret'],
                                    user_agent = authConfigs['user_agent'])
        
    
    def fetchFromSubreddit(self, subreddit):
        ''' fetch posts from the given subreddit '''
        subreddit = self.reddit.subreddit(subreddit)
        # hottest 10 posts
        posts = []
        for post in subreddit.hot(limit = 50):
            posts.append(post.title)

        print(posts)
        return posts
        

    def fetchPosts(self, subreddits):
        ''' fetch posts from the list of subreddits '''
        pass 

    def filterWithKeyword(self, keyword):
        ''' filter post with the keyword '''
        pass 

    def filterPosts(self, keywords):
        ''' filter posts with the list of keywords '''
        pass

if __name__ == "__main__":
    rh = RedditHandler()
    rh.fetchFromSubreddit("Amy Klobuchar")