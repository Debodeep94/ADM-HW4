import math
import numpy as np
import time


class BloomFilter(object):
    """
    This class contains the variable and the methods needed for the implementation and use
    of a Bloom Filter
    """
     
    def __init__(self, n_items, fp_prob, hash_count = 0):
        self.fp_prob = fp_prob  # false positive probability
        self.n_items = n_items  # number of items to add to the filter
        self.array_len = self.get_array_len(self.n_items, self.fp_prob)  # length of the array
        self.hash_count = hash_count  # number of hash functions needed
        if hash_count == 0:
            self.hash_count = self.get_hash_count(self.n_items, self.array_len)
        self.array = np.zeros(self.array_len)  # array initialized to all zeros

    def get_array_len(self, n, p):
        """
        Calculate the length of the array needed with n items and a required false positive prob p.
        """
        m = -(n*math.log(p))/(math.log(2)**2)
        return int(m)

    def get_hash_count(self, n, m):
        """
        Calculate the number of hash functions needed with n items to achieve p false positive prob.
        """
        k = (m/n)*math.log(2)
        return int(k)

    def hash(self, s, seed):
        """
        Given a string s and an int seed, calculate the hash code of the string using the DJB2-H method.
        """
        g = 31
        res = 1

        for c in s:
            res = g*res + ord(c)*seed

        return (res % self.array_len)

    def add(self, s):
        """
        Add a string s to the Bloom filter.
        """
        for i in range(1, self.hash_count + 1):
            index = self.hash(s, i)  # get hash value
            self.array[index] = 1  # set the corresponding index of the array to 1

    def exists(self, s):
        """
        Check if the filter contains a string s.
        """
        for i in range(1, self.hash_count + 1):
            index = self.hash(s, i)
            if self.array[index] == 0:
                return False
        return True

    def describe(self):
        """
        Print the main info about the filter.
        """
        print("False-positive probability (%): ", self.fp_prob*100)
        print("Number of items: ", self.n_items)
        print("Array length: ", self.array_len)
        print("Number of hash functions: ", self.hash_count)


def exec_bloom_filter(BF, passwords1_path, passwords2_path):
    """
    ADD the passwords in passwords1 to the filter and check how many passwords
    from passwords2 are duplicates.
    """
    start = time.time()

    # add the passwords from passwords1
    with open(passwords1_path, 'r') as passwords1:
        i = 0
        for pwd in passwords1:
            BF.add(pwd)
            if i%1000000 == 0:
                print(i)
            i += 1

    duplicates = 0
    # check the passwords in passwords2
    with open(passwords2_path, 'r') as passwords2:
        i = 0
        for pwd in passwords2:
            if i%1000000 == 0:
                print(i)
            if BF.exists(pwd):
                duplicates += 1
            i += 1
        
    end = time.time()
    
    # return the list of duplicates for eventually saving them in a file
    return (duplicates, int(end-start))


if __name__ == "__main__":

    passwords1_path = r"data/passwords/passwords1.txt"
    passwords2_path = r"data/passwords/passwords2.txt"

    # calculate the number of passwords to add
    print("Calculating the number of passwords to add to the filter")
    n = 0
    with open(passwords1_path, 'r') as passwords1:
        for pwd in passwords1:
            n += 1
    n

    # Initializing the Bloom filter
    print("Initializing Bloom filter\n")
    BF = BloomFilter(n, 0.0001, 11)
    BF.describe()
    print('\n')

    (duplicates, seconds) = exec_bloom_filter(BF, passwords1_path, passwords2_path)

    print('\nNumber of hash function used: ', BF.hash_count) 
    print('Number of duplicates detected: ', duplicates) 
    print('Probability of false positives: (%)', BF.fp_prob*100) 
    print('Execution time: ', seconds, ' seconds')