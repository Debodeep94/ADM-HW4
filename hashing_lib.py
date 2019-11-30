import math
import numpy as np
import time
from threading import Thread
from multiprocessing import Process, cpu_count


class BloomFilter(object):
     
    def __init__(self, n_items, fp_prob, hash_count = 0):
        self.fp_prob = fp_prob
        self.n_items = n_items
        self.array_len = self.get_array_len(self.n_items, self.fp_prob)
        self.hash_count = hash_count
        if hash_count == 0:
            self.hash_count = self.get_hash_count(self.n_items, self.array_len)
        self.array = np.zeros(self.array_len)

    def get_array_len(self, n, p):
        m = -(n*math.log(p))/(math.log(2)**2)
        return int(m)

    def get_hash_count(self, n, m):
        k = (m/n)*math.log(2)
        return int(k)

    def hash(self, s, seed):
        g = 31
        res = 1

        for c in s:
            res = g*res + ord(c)*seed

        return (res % self.array_len)

    def add(self, item):
        for i in range(1, self.hash_count + 1):
            index = self.hash(item, i)
            self.array[index] = 1

    def exists(self, item):
        for i in range(1, self.hash_count + 1):
            index = self.hash(item, i)
            if self.array[index] == 0:
                return False
        return True

    def describe(self):
        print("False-positive probability (%): ", self.fp_prob*100)
        print("Number of items: ", self.n_items)
        print("Array length: ", self.array_len)
        print("Number of hash functions: ", self.hash_count)


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


def add(BF, passwords):
    i = 0
    for pwd in passwords:
        BF.add(pwd)
        print(i)
        i += 1


def check(BF, passwords, duplicates):
    i = 0
    for pwd in passwords:
        if BF.exists(pwd):
            duplicates += 1
        print(i)
        i += 1


def multithread_add(BF, passwords, n_threads):
    N = len(passwords)
    l_chunks = N // n_threads
    chunks = [passwords[i:i + l_chunks] for i in range(0, N, l_chunks)]

    if len(chunks) > n_threads:
        chunks[-2] += chunks[-1]
        del chunks[-1]

    threads = []

    for i in range(n_threads):
        threads.append(
            Process(name='Thread-' + str(i),
            target=add, args=(BF, chunks[i]))
        )

    # start each thread
    for t in threads:
        t.start()

    # wait for each thread to finish its execution
    for t in threads:
        t.join()


def multithread_check(BF, passwords, n_threads):
    N = len(passwords)
    l_chunks = N // n_threads
    chunks = [passwords[i:i + l_chunks] for i in range(0, N, l_chunks)]

    if len(chunks) > n_threads:
        chunks[-2] += chunks[-1]
        del chunks[-1]

    threads = []
    partial_duplicates = [0 for i in range(n_threads)]

    for i in range(n_threads):
        threads.append(
            Process(name='Thread-' + str(i),
            target=check, args=(BF, chunks[i], partial_duplicates[i]))
        )

    # start each thread
    for t in threads:
        t.start()

    # wait for each thread to finish its execution
    for t in threads:
        t.join()

    duplicates = 0
    for d in partial_duplicates:
        duplicates += d

    return duplicates


def multithread_exec_filter(BF, passwords1, passwords2_path, n_threads):
    start = time.time()

    print("Adding passwords from Passwords1 to the filter")
    multithread_add(BF, passwords1[:30000], n_threads)
    passwords1 = None
    print("Password1 added")
    
    print("Reading passwords from passwords2.txt")
    with open(passwords2_path, 'r') as f:
        passwords2 = f.read().splitlines()
    print("Checking existing passwords from Password2")
    duplicates = multithread_check(BF, passwords2[:10000], n_threads)

    end = time.time()
    print("FINISHED")
    
    return (duplicates, int(end-start))


if __name__ == "__main__":

    passwords1_path = r"data\passwords\passwords1.txt"
    passwords2_path = r"data\passwords\passwords2.txt"

    print("Reading passwords1")
    with open(passwords1_path, 'r') as f:
        passwords1 = f.read().splitlines()

    print("Initializing Bloom filter\n")
    n = len(passwords1)
    BF = BloomFilter(n, 0.00001, 11)
    BF.describe()
    print('\n')

    # duplicates = exec_bloom_filter(BF, passwords1, passwords2)
    n_threads = 1
    (duplicates, seconds) = multithread_exec_filter(BF, passwords1, passwords2_path, n_threads)

    print('\nNumber of hash function used: ', BF.hash_count) 
    print('Number of duplicates detected: ', duplicates) 
    print('Probability of false positives: (%)', BF.fp_prob*100) 
    print('Execution time: ', seconds, ' seconds')

    # with open('duplicates1.txt', 'w') as f:
    #     for pwd in duplicates:
    #         f.write("%s\n" % pwd)