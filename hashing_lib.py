import numpy as np


class BloomFilter(object):
     
    def __init__(self, n_items, fp_prob):
        self.fp_prob = fp_prob
        self.n_items = n_items
        self.array_len = self.get_array_len(self.n_items, self.fp_prob)
        self.hash_count = self.get_hash_count(self.n_items, self.array_len)
        self.array = np.zeros(self.array_len)

    def get_array_len(self, n, p):
        m = -(n*np.log(p))/((np.log(2)**2))
        return int(m)

    def get_hash_count(self, n, m):
        k = (m/n)*np.log(2)
        return int(k)

    def add(self, item):
        return None

    def exists(self, item):
        return None