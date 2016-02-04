import praw
from lda_gibbs import LDA
import nltk
from collections import deque
from time import sleep


r = praw.Reddit(user_agent='lda analysis by ' + '/u/giraffeApple')
r.login('giraffeApple', 'bambam5')

tokenizer = nltk.tokenize.RegexpTokenizer("[\w']+")
stemmer = nltk.stem.PorterStemmer()
lemmatizer = nltk.stem.WordNetLemmatizer()

ncomments = 500
documents = []
# cache = set()
# while len(cache) < ncomments:
# 	try:
# 		for comment in r.get_comments('all', limit=None):
# 			if comment.id in cache:
# 				continue
# 			doc = tokenizer.tokenize(comment.body.lower())
# 			if len(doc) < 50:
# 				continue
# 			# doc = list(map(lemmatizer.lemmatize, doc))
# 			documents.append(doc)
# 			cache.add(comment.id)
# 	except KeyboardInterrupt:
# 		break
# 	except:
# 		print(len(cache))
# 		sleep(5)
# print('cache len: {}'.format(len(cache)))
sub = r.get_subreddit('all')


# for i, comment in enumerate(r.get_comments('all', limit=ncomments)):
# 	print(i)
# 	doc = tokenizer.tokenize(comment.body.lower())
# 	# if len(doc) < 50:
# 	# 	continue
# 	doc = list(map(lemmatizer.lemmatize, doc))
# 	documents.append(doc)
# print(len(documents))

# print('starting')
# model = LDA(documents)
# theta, beta = model.train(ntopics=200, niter=400)
# tsr = model.topic_significances()
# named_tsr = [(s, model.topic_representatives(i, topn=9, show_scores=False)) \
# 	for i, s in enumerate(tsr)]
# for name, score in sorted(named_tsr, reverse=True)[:20]:
#     print(name, score)