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
    """
    This function takes in input a list of char and returns a new list, based on the first
    one but ordered alphabetically.
    :param lst: list of char
    :return: ordered list of char
    """
    A = [(ord(c)-diff) for c in lst]  # convert each char into an integer and put it into a list
    B = counting_sort(A)  # order the list
    return [chr(x+diff) for x in B]  # convert the integers into chars and return the list


def my_groupby(lst, i):
    """
    This function takes in input a list and an index, groups its items based on the index and
    returns the list grouped.
    :param lst: list to group
    :param i: char position to group the items
    :return: grouped list
    """
    d = {}
    for x in lst:
        d.setdefault(x[i], []).append(x)
    return list(d.values())


def strings_counting_sort(A, j):
    """
    This function takes in input a list and an integer j, 
    which is the index based on which the functions has to order the list of strings.
    It returns a list of lists. Each list has the strings grouped by the j_th item.
    :param A: list of strings to order
    :return: list of lists, ordered by the j_th item
    """
    k = ord('z') - ord('A')  # number of possible chars at position j
    n = len(A)
    C = [0 for i in range(k+1)]  # list to store the number of strings with the same char in position j
    to_return = []  # this list will store the strings whose length is equal or smaller than j

    for i in range(n):  # loop over the list of strings
        if len(A[i]) <= j:  # if the string doesn't have the j_th item, 
            # put the string in the to_return list and go directly to the next string.
            to_return.append(A[i])
            continue

        if A[i][j] == ' ':  # the *space* has index 0 (arbitrary choice)
            index = 0
        else:
            index = ord(A[i][j])-diff
            # the value in position *index* in C will be the number of strings containing
            # the same char in position j. (e.g. if j==3 and A[i][j] = 'a' then index = ord('a') = 1)
        C[index] += 1
        # each element C[i] is equal to the number of i in the array A

    # now remove from the list A the strings already ordered which are contained in to_return
    for word in to_return:
        A.remove(word)

    for i in range(1, k):
        C[i] += C[i-1]
        # each C[i] is now equal to the number of elements in A equal or less than i

    n = len(A)  # re-calculate len(A) since there have been removed some strings
    B = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        char = ord(A[i][j])-diff
        index = C[char]-1
        B[index] = A[i]  # insert A[i] in the right position in B, given by C[i]-1
        C[char] += -1  # decrease by one the number of elements equal or less than A[i]

    # since the list will be returned to the recursive function, it needs to be a list of lists
    # where each list contain the strings with the same char in position j
    grouped_list = my_groupby(B, j)
    if len(to_return) > 0:  # if it is not empty, insert at the head of the grouped_list the list to_return
        grouped_list.insert(0, to_return)
    return grouped_list


def rec_alphabetical_sort(lst, j):
    if len(lst)==1 or len(set(lst))<=1:
        return lst

    new_lst = strings_counting_sort(lst, j)

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
    l = ['a', 'ab', 'a', 'cd', 'cc']
    es1 = ['As', 'Aster', 'Astrolabe', 'Astronomy', 'Astrophysics', 'At', 'Ataman', 'Attack', 'Baa']
    es2 = ['Oak', 'Oak Hill', 'Oak Ridge', 'Oakley Park', 'Oakley River']
    ordered_strings = rec_alphabetical_sort(es2, 0)
    print(*es2)
    print(*ordered_strings)
