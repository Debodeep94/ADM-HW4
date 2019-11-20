from itertools import groupby
from itertools import chain
from collections import defaultdict


n_chars = 64


def counting_sort(A):
    k = max(A)
    n = len(A)
    B = [0 for i in range(n)]
    C = [0 for i in range(k+1)]

    for i in range(n):
        C[A[i]] += 1
        # each element C[i] is equal to the number of i in the array A

    for i in range(1, k+1):
        C[i] += C[i-1]
        # each C[i] is now equal to the number of elements in A equal or less than i

    for i in range(n-1, -1, -1):
        el = A[i]
        index = C[el]-1
        B[index] = el  # insert A[i] in the right position in B, given by C[i]-1
        C[el] += -1  # decrease by one the number of elements equal or less than A[i]

    return B


def char_couting_sort(lst):
    A = [(ord(c)-n_chars) for c in lst]
    B = counting_sort(A)
    return [chr(x+n_chars) for x in B]


def my_groupby(lst, i):
    d = defaultdict(list)

    for x in lst:
        d[x[i]].append(x)

    return list(d.values())


def list_counting_sort(A, j):
    k = ord('z') - ord('A')
    n = len(A)
    B = [0 for i in range(n)]
    C = [0 for i in range(k+1)]

    for i in range(n):
        if A[i] == ' ':
            index = 0
        else:
            index = ord(A[i][j])-n_chars
        C[index] += 1
        # each element C[i] is equal to the number of i in the array A

    for i in range(1, k):
        C[i] += C[i-1]
        # each C[i] is now equal to the number of elements in A equal or less than i

    for i in range(n-1, -1, -1):
        char = ord(A[i][j])-n_chars
        index = C[char]-1
        B[index] = A[i]  # insert A[i] in the right position in B, given by C[i]-1
        C[char] += -1  # decrease by one the number of elements equal or less than A[i]

    # return [list(g) for k, g in groupby(B, key=lambda x: x[j])]
    return my_groupby(B, j)


def rec_alphabetical_sort(lst, j):
    if len(lst)==1 or len(set(lst))<=1:
        return lst

    new_lst = list_counting_sort(lst, j)

    j += 1
    final = []
    for l in new_lst:
        final.append(rec_alphabetical_sort(l, j))
    
    return list(chain.from_iterable(final))  # flatten the list of lists
    



if __name__ == "__main__":
    # array = [4,7,2,4,2,8,5,6,1,2,5]
    # ordered_array = counting_sort(array)
    # print(*array)
    # print(*ordered_array)

    # lst = ['c','z','e','i','d','g','j','q','r','a']
    # ordered_alpha = char_couting_sort(lst)
    # print(*lst)
    # print(*ordered_alpha)

    string_lst2 = ['paolo', 'lorenzo', 'giovanni', 'emanu ele', 'emanu ela', 'paolo']
    ordered_strings = rec_alphabetical_sort(string_lst2, 0)
    print(*string_lst2)
    print(*ordered_strings)
