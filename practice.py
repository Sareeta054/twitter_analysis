import praw
from praw.models import MoreComments
reddit = praw.Reddit( client_id='zMSzNGC8iBad1Q', 
                     client_secret='8lb0H2iq8BSlWj2g5u9FoDFsm20', 
                     user_agent='api tutorial')
hot_posts = reddit.subreddit('Minneapolis').hot(limit=1)
count=0
for post in hot_posts:
    for top_level_comment in post.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        count+=1
        print(top_level_comment.body)
print(count)

#


#for top_level_comment in submission.comments:
#    if isinstance(top_level_comment, MoreComments):
#        continue
#    print(top_level_comment.body)
    
#submission = reddit.submission(id='driacq')
#for top_level_comment in submission.comments:
#    print(top_level_comment.body)
#print(submission.comments)
#
#subreddit = reddit.subreddit('AskReddit')
#for submission in subreddit.stream.submissions():
#    print(submission)
#
#
# class complex_number:
#     def __init__(self, r=0,i=0):
#         self.real = r;
#         self.imag = i;
#         
#    def getData(self):
#        print("".format(self))