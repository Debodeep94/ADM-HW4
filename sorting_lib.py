# Discussions about time complexity are on the main.ipynb file.

diff = ord('A') - 1


def counting_sort(A):
    """
    This function takes in input a list of integers and return a new ordered list, based on the first one.
    :param A: the list to order
    :type A: list of int
    :return: ordered list
    :rtype: list of int
    """
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
    A = [(ord(c)-diff) for c in lst]
    B = counting_sort(A)
    return [chr(x+diff) for x in B]


def my_groupby(lst, i):
    d = {}
    for x in lst:
        d.setdefault(x[i], []).append(x)
    return list(d.values())


def list_counting_sort(A, j):
    k = ord('z') - ord('A')
    n = len(A)
    C = [0 for i in range(k+1)]
    to_return = []

    for i in range(n):
        if len(A[i]) <= j:
            to_return.append(A[i])
            continue

        if A[i][j] == ' ':
            index = 0
        else:
            index = ord(A[i][j])-diff
        C[index] += 1
        # each element C[i] is equal to the number of i in the array A

    for word in to_return:
        A.remove(word)

    for i in range(1, k):
        C[i] += C[i-1]
        # each C[i] is now equal to the number of elements in A equal or less than i

    n = len(A)
    B = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        char = ord(A[i][j])-diff
        index = C[char]-1
        B[index] = A[i]  # insert A[i] in the right position in B, given by C[i]-1
        C[char] += -1  # decrease by one the number of elements equal or less than A[i]

    # return [list(g) for k, g in groupby(B, key=lambda x: x[j])]
    grouped_list = my_groupby(B, j)
    if len(to_return) > 0:
        grouped_list.insert(0, to_return)
    return grouped_list


def rec_alphabetical_sort(lst, j):
    if len(lst)==1 or len(set(lst))<=1:
        return lst

    new_lst = list_counting_sort(lst, j)

    j += 1
    final = []
    for l in new_lst:
        final.append(rec_alphabetical_sort(l, j))
    
    return [word for sublist in final for word in sublist]  # flatten the list of lists
    



if __name__ == "__main__":
    # array = [4,7,2,4,2,8,5,6,1,2,5]
    # ordered_array = counting_sort(array)
    # print(*array)
    # print(*ordered_array)

    # lst = ['c','z','e','i','d','g','j','q','r','a']
    # ordered_alpha = char_couting_sort(lst)
    # print(*lst)
    # print(*ordered_alpha)

    l1 = ['paolo', 'lorenzo', 'emanu ele', 'emanu ela', 'paolo', 'paol']
    l = ['paolo', 'paol']
    es1 = ['As', 'Aster', 'Astrolabe', 'Astronomy', 'Astrophysics', 'At', 'Ataman', 'Attack', 'Baa']
    ordered_strings = rec_alphabetical_sort(es1, 0)
    print(*es1)
    print(*ordered_strings)
