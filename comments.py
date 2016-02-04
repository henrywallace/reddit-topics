import praw
import pickle
import csv
from pyprind import ProgPercent
from collections import defaultdict, namedtuple

import warnings
warnings.filterwarnings('ignore')

class CommentNode(object):
    def __init__(self, comment):
        self.comment = comment

    def __repr__(self):
        return self.id

    def __hash__(self):
        return hash(self.id)

class CommentGatherer(object):
    def __init__(self):
        with open('login.csv') as f:
            reader = csv.reader(f, delimiter=':')
            login = {k.upper(): v.strip() for k, v in reader}
        self.r = praw.Reddit(user_agent='LDA comment collector by /u/{}'\
            .format(login['USERNAME']))
        self.r.login(login['USERNAME'], login['PASSWORD'])
        self.comments = []
        self.transitions = []

    # def get_replies(self, comment):
    #   is_comment = lambda c: isinstance(c, praw.objects.Comment)
    #   return list(filter(is_comment, comment.replies))

    def gather_replies(self, comment, depth):
        replies = self.filter_comments(comment.replies)
        self.comments.extend(replies)
        self.transitions.extend((comment, r) for r in replies)
        if depth > 1:
            for r in replies:
                self.gather_replies(r, depth - 1)

    def filter_comments(self, comments):
        if len(comments) > 0:
            return comments[:-1]
        else:
            return comments

    # should title be considered top comment?
    # should not transitions be considered a topic?
    def traverse(self, sub_name, nroots=100, max_depth=float('inf')):
        stream = self.r.get_subreddit(sub_name).get_hot(limit=nroots)
        for submission in stream:
            for comment in self.filter_comments(submission.comments):
                # print(comment.body, end='\n\n')
                self.gather_replies(comment, max_depth)




if __name__ == '__main__':
    cg = CommentGatherer()
    cg.traverse('all', nroots=1)






