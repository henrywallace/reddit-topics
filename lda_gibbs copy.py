import lda
from scipy.stats.mstats import gmean
from scipy.stats import entropy as divergence
import numpy as np

class LDA(object):
    def __init__(self, documents=None):
        self.documents = documents
        self.doc_term = self.get_doc_term(self.documents)

    def get_doc_term(self, documents):
        self.term2id = {}     # keys, values = unique tags, indices
        k = 0
        id_name = lambda term: str(term).lower()      # use lower case str as id name
        for doc in documents:
            for t in map(id_name, doc):
                if t not in self.term2id:
                    self.term2id[t] = k
                    k += 1
        self.ndocs, self.nterms = len(documents), len(self.term2id)
        A = np.zeros((self.ndocs, self.nterms), dtype='int64')    # document term matrix
        for i, doc in enumerate(self.documents):
            for t in map(id_name, doc):
                A[i, self.term2id[t]] = 1   # use identity weight
        self.id2term = {v: k for k, v in self.term2id.items()}
        return A

    def train(self, ntopics, niter, seed=None):
        model = lda.LDA(n_topics=ntopics, n_iter=niter)
        model.fit(self.doc_term)
        self.theta, self.beta = model.doc_topic_, model.topic_word_
        self.ntopics = ntopics
        return self.theta, self.beta

    def term_score(self, topic_ind, term_ind):
        term_prob = self.beta[topic_ind, term_ind]
        idf = np.log(term_prob / gmean(self.beta[:, term_ind]))
        return term_prob * idf

    def topic_representatives(self, topic_ind, topn=10, show_scores=True):
        labels = [self.id2term[i] for i in range(self.nterms)]
        scores = [(self.term_score(topic_ind, i), labels[i]) for i in range(self.nterms)]
        top = tuple(sorted(scores, reverse=True)[:topn])
        if show_scores:
            return top
        else:
            return tuple(name for score, name in top)
    
    def topic_significances(self):
        # GET EXTREME DISTRIBUTIONS
        u_dist = [1/self.nterms] * self.nterms
        topic_dist = self.theta.sum(axis=0)
        topic_dist /= topic_dist.sum()
        v_dist = np.dot(self.beta.T, topic_dist)
        b_dist = [1/self.ndocs] * self.ndocs
        # CALCULATE KL TOPIC DISTANCES
        u_kl = [divergence(self.beta[i], u_dist) for i in range(self.ntopics)]
        v_kl = [divergence(self.beta[i], v_dist) for i in range(self.ntopics)]
        b_kl = [divergence(self.theta[:, i], b_dist) for i in range(self.ntopics)]
        u_sum, v_sum, b_sum = sum(u_kl), sum(v_kl), sum(b_kl)
        u_min, v_min, b_min = min(u_kl), min(v_kl), min(b_kl)
        u_max, v_max, b_max = max(u_kl), max(v_kl), max(b_kl)
        n_u, n_v, n_b = ([c[i]*(1 - c[i]/u_sum) for i in range(self.ntopics)] \
            for c in [u_kl, v_kl, b_kl])
        m_u, m_v, m_b = ([(c[i] - c_min)/(c_max - c_min) for i in range(self.ntopics)] \
            for c, c_min, c_max in [(u_kl, u_min, u_max), (v_kl, v_min, v_max), (b_kl, b_min, b_max)])
        (upsi_u, upsi_v), (psi_b, psi_u, psi_v) = [(0.5, 0.5), (1/3, 1/3, 1/3)]
        x = [n_b[i]*(upsi_u*n_u[i] + upsi_v*n_v[i]) for i in range(self.ntopics)]
        omega = [psi_b*m_b[i] + psi_u*m_u[i] + psi_v*m_v[i] for i in range(self.ntopics)]
        return [x[k]*omega[k] for k in range(self.ntopics)]

if __name__ == '__main__':
    model = LDA([[1, 2, 3, 4], [5, 6, 7, 8]])
    theta, beta = model.train(ntopics=30, niter=100, seed=42)
#     tsr = lda.topic_significances()
#     named_tsr = [(s, lda.topic_representatives(i, topn=3, show_scores=False)) for i, s in enumerate(tsr)]
#     for name, score in sorted(named_tsr, reverse=True):
#         print(name, score)
