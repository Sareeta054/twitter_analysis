# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 15:21:57 2019

@author: -
"""

import praw

     def (self, client_id, client_secret, user_agent):
        self.reddit = praw.Reddit(client_id, client_secret, user_agent)
        

# TODO: Add logic to switch between handle in a user friendly way. Read keys from config.      
if __name__ == '__main__':
    print('inside main')
    runner = Runner()
    runner.initReddit('zMSzNGC8iBad1Q', '8lb0H2iq8BSlWj2g5u9FoDFsm20', 'api tutorial')
    subreddit = runner.reddit.subreddit('Minneapolis').hot(limit=None)
    print(subreddit)
