import math
import numpy as np
import time


class BloomFilter(object):
     
    def __init__(self, n_items, fp_prob):
        self.fp_prob = fp_prob
        self.n_items = n_items
        self.array_len = self.get_array_len(self.n_items, self.fp_prob)
        self.hash_count = self.get_hash_count(self.n_items, self.array_len)
        self.array = np.zeros(self.array_len)

    def get_array_len(self, n, p):
        m = -(n*math.log(p))/(math.log(2)**2)
        return int(m)

    def get_hash_count(self, n, m):
        k = (m/n)*math.log(2)
        return int(k)+1

    # def hash_mul(self, s, seed):
    #     m = self.array_len
    #     idx = seed%len(s)
    #     s = list(s)
    #     s[idx] = chr(ord(s[idx]) + seed)
    #     s = ''.join(s)
    #     pwr = 1
    #     key = 0
    #     for _, character in enumerate(s):
    #         # Using Horner's method to convert the string to an integer
    #         key = (key + (ord(character)*pwr)%m ) %m
    #         pwr = (pwr*128)%m
    #     A = (math.sqrt(5)-1) / 2
    #     h = math.floor(m*((key*A)%1))
    #     return h

    def hash_base(self, s, seed):
        g = 31
        res = 0

        for c in s:
            res = g*res + ord(c)*seed

        return res % self.array_len

    def add(self, item):
        for i in range(self.hash_count):
            index = self.hash_base(item, i)
            self.array[index] = 1

    def exists(self, item):
        for i in range(1, self.hash_count + 1):
            index = self.hash_base(item, i)
            if self.array[index] == 0:
                return False
        return True

    def describe(self):
        print("False-positive probability (%): ", self.fp_prob*100)
        print("Number of items: ", self.n_items)
        print("Array length: ", self.array_len)
        print("Number of hash functions needed: ", self.hash_count)


def exec_bloom_filter(BF, passwords1, passwords2):
    start = time.time()
    l1 = len(passwords1)
    i = 0
    for pwd in passwords1:
        print('% .2f' %(i*100/l1))
        BF.add(pwd)
        i += 1

    duplicates = []
    i = 0
    l2 = len(passwords2)
    for pwd in passwords2:
        print('% .2f' %(i*100/l2))
        if BF.exists(pwd):
            duplicates.append(pwd)
        i += 1
        
    end = time.time()
    print('Number of hash function used: ', BF.hash_count) 
    print('Number of duplicates detected: ', len(duplicates)) 
    print('Probability of false positives: (%)', BF.fp_prob*100) 
    print('Execution time: ', int(end-start), ' seconds')
    np.savetxt('array.txt', BF.array, delimiter=',')
    return duplicates


if __name__ == "__main__":

    filepath1 = r"data\passwords\passwords1.txt"
    with open(filepath1, 'r') as f:
        passwords1 = f.read().splitlines()

    filepath2 = r"data\passwords\passwords2.txt"
    with open(filepath2, 'r') as f:
        passwords2 = f.read().splitlines()

    # n = len(passwords1)
    n = 30000
    BF = BloomFilter(n, 0.001)
    BF.describe()
    print('\n')

    duplicates = exec_bloom_filter(BF, passwords1[:30000], passwords2[:3000])

    with open('duplicates1.txt', 'w') as f:
        for pwd in duplicates:
            f.write("%s\n" % pwd)