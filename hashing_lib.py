import numpy as np
import math
import pandas as np


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

    def hash_mul(self, s, seed):
        m = self.array_len
        pwr = 1
        key = 0
        for _, character in enumerate(s):
            # Using Horner's method to convert the string to an integer
            key = (key+ (ord(character)*pwr)%m ) %m
            pwr = (pwr*128)%m
        A = 0.618 / seed
        h = math.floor(m*((key*A)%1))
        return int(h)

    def add(self, item):
        for i in range(1, self.hash_count + 1):
            index = self.hash_mul(item, i)
            self.array[index] = 1

    def exists(self, item):
        exists = True
        for i in range(1, self.hash_count + 1):
            index = self.hash_mul(item, i)
            exists = (self.array[index] == 1)
            if not exists:
                break
        return exists

    def describe(self):
        print("False-positive probability: ", self.fp_prob)
        print("Number of items: ", self.n_items)
        print("Array length: ", self.array_len)
        print("Number of hash functions needed: ", self.hash_count)

