import praw
from nltk.corpus.reader import wordnet
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import stopwords
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain, repeat
from wordcloud import WordCloud

def sub_documents(sub, nposts=200):
    r = praw.Reddit('comment LDA')
    sub = r.get_subreddit(sub)
    tokenizer = RegexpTokenizer("[\w']+")
    docs = [tokenizer.tokenize(p.title.lower().replace("'s", '')) for p in sub.get_top_from_all(limit=nposts)]
    lemmatizer = WordNetLemmatizer()
    docs = [[lemmatizer.lemmatize(w, pos=wordnet_pos(pos)) for w, pos in pos_tag(d)] for d in docs]
    return docs

def wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def plot_cloud(docs, nwords=100):
    word_counts = Counter(chain.from_iterable(docs))
    doc_word_counts = [dict(Counter(d)) for d in docs]
    word_doc_counts = {w: sum(w in d for d in docs) for w in word_counts.keys()}
    doc_tfidf = [{w: (1 + np.log(dwc[w]))*np.log(1 + len(docs)/word_doc_counts[w]) \
              for w in dwc.keys()} for dwc in doc_word_counts]
    stop = set(stopwords.words('english'))
    term_avg_tfidf = {w: np.sum([dt.get(w, 0) for dt in doc_tfidf]) \
        for w in word_counts.keys() if w not in stop}
    terms = sorted(term_avg_tfidf.items(), key=lambda x: x[1], reverse=True)[:nwords]
    big_string = ' '.join(' '.join(repeat(w, int(c))) for w, c in terms)
    cloud = WordCloud(background_color='white', width=2000, height=2000,
        font_path='/System/Library/Fonts/HelveticaNeue.dfont').generate(big_string)
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    docs = sub_documents('science', nposts=200)
    plot_cloud(docs)






