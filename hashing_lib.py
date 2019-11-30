import math
import numpy as np
import time
import multiprocessing as mp
import os


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


def exec_bloom_filter(BF, passwords1, passwords2):
    """
    ADD the passwords in passwords1 to the filter and check how many passwords
    from passwords2 are duplicates.
    """
    start = time.time()

    # add the passwords from passwords1
    i = 0
    for pwd in passwords1:
        BF.add(pwd)
        print(i)
        i += 1

    duplicates = []
    # check the passwords in passwords2
    i = 0
    for pwd in passwords2:
        print(i)
        if BF.exists(pwd):
            duplicates.append(pwd)
        i += 1
        
    end = time.time()
    print('Number of hash function used: ', BF.hash_count) 
    print('Number of duplicates detected: ', len(duplicates)) 
    print('Probability of false positives: (%)', BF.fp_prob*100) 
    print('Execution time: ', int(end-start), ' seconds')
    
    # return the list of duplicates for eventually saving them in a file
    return duplicates


################ Multiprocessing section ####################

def add_wrapper(BF, fpath, chunkStart, chunkSize):
    """
    ADD to the filter the passwords contained in the portion of file
    between chunkStart and (chunkStart + chunkSize).
    Returns the array that will be added to the final one in the BloomFilter,
    given the fact the this function gets executed in multiprocess.
    """
    with open(fpath) as f:
        f.seek(chunkStart)  # start reading the file from chunkStart
        passwords = f.read(chunkSize).splitlines()  # read until chunkSize
        for pwd in passwords:
            # add the passwords to the filter
            BF.add(pwd)
    return BF.array


def check_wrapper(BF, fpath, chunkStart, chunkSize):
    """
    CHECK the presence in the Bloom Filter of the passwords contained in the portion of file
    between chunkStart and (chunkStart + chunkSize).
    Returns the number of duplicates found that will be added to the final number of duplicates,
    given the fact the this function gets executed in multiprocess.
    """
    with open(fpath) as f:
        duplicates = 0
        f.seek(chunkStart)  # start reading the file from chunkStart
        passwords = f.read(chunkSize).splitlines()  # read until chunkSize
        for pwd in passwords:
            # check how many passwords are duplicates
            if BF.exists(pwd):
                duplicates += 1
        return duplicates


def chunkify(fpath,size=1024*1024):
    """
    This function subdivides the total length of the input file into
    chucks, where chunkStart is the position of the first byte of the chunk
    and (chunkEnd - chunkStart) is the number of bytes to include in the chunk.
    Each time returns a tuple with the yield expression so that the function
    can continue it's course.
    """
    fileEnd = os.path.getsize(fpath)
    with open(fpath,'rb') as f:
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size,1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break


def multiprocess_add(BF, filepath):
    """
    Execute the ADDITION of the passwords from the file to the filter by subdividing the task
    in multiple processes.
    """
    # init objects
    pool = mp.Pool(mp.cpu_count())
    jobs = []

    # create jobs
    for chunkStart,chunkSize in chunkify(filepath):
        jobs.append( pool.apply_async(add_wrapper,(BF, filepath, chunkStart,chunkSize)) )

    # wait for all jobs to finish
    for job in jobs:
        BF.array += job.get()  # add the result to the final array

    BF.array = (BF.array > 0).astype(int)  # convert the values of the array in 0 and 1 's

    # clean up the pool
    pool.close()


def multiprocess_check(BF, filepath):
    """
    CHECK the number of duplicates in the file passwords2 respect to the filter 
    by subdividing the task in multiple processes.
    """
    # init objects
    pool = mp.Pool(mp.cpu_count())
    jobs = []
    duplicates = 0
    # create jobs
    for chunkStart,chunkSize in chunkify(filepath):
        jobs.append( pool.apply_async(check_wrapper,(BF, filepath, chunkStart, chunkSize)) )

    # wait for all jobs to finish
    for job in jobs:
        duplicates += job.get()


    # clean up the pool
    pool.close()

    return duplicates


if __name__ == "__main__":

    passwords1_path = r"data/passwords/passwords1.txt"
    passwords2_path = r"data/passwords/passwords2.txt"

    # print("Reading passwords1")
    # with open(p1_test, 'r') as f:
    #     passwords1 = f.read().splitlines()

    # print("Reading passwords2")
    # with open(p2_test, 'r') as f:
    #     passwords2 = f.read().splitlines()

    # Initializing the Bloom filter
    print("Initializing Bloom filter\n")
    n = 100000000
    BF = BloomFilter(n, 0.00001, 11)
    BF.describe()
    print('\n')

    # duplicates = exec_bloom_filter(BF, passwords1, passwords2)

    start = time.time()
    print("ADD process started")
    multiprocess_add(BF, passwords1_path)
    print("\nCHECK process started")
    duplicates = multiprocess_check(BF, passwords2_path)
    end = time.time()
    seconds = int(end-start)

    print('\nNumber of hash function used: ', BF.hash_count) 
    print('Number of duplicates detected: ', duplicates) 
    print('Probability of false positives: (%)', BF.fp_prob*100) 
    print('Execution time: ', seconds, ' seconds')

    # with open('duplicates1.txt', 'w') as f:
    #     for pwd in duplicates:
    #         f.write("%s\n" % pwd)