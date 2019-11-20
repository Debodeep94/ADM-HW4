from itertools import groupby
from itertools import chain


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


def alphabetical_couting_sort(lst):
    A = [(ord(c)-96) for c in lst]
    B = counting_sort(A)
    return [chr(x+96) for x in B]


def list_counting_sort(A, j):
    k = max([max(l) for l in A])
    n = len(A)
    B = [0 for i in range(n)]
    C = [0 for i in range(k+1)]

    for i in range(n):
        C[A[i][j]] += 1
        # each element C[i] is equal to the number of i in the array A

    for i in range(1, k+1):
        C[i] += C[i-1]
        # each C[i] is now equal to the number of elements in A equal or less than i

    for i in range(n-1, -1, -1):
        char = A[i][j]
        index = C[char]-1
        B[index] = A[i]  # insert A[i] in the right position in B, given by C[i]-1
        C[char] += -1  # decrease by one the number of elements equal or less than A[i]

    return B


def list_counting_sort2(A, j):
    k = ord('z') - ord('A')
    n = len(A)
    B = [0 for i in range(n)]
    C = [0 for i in range(k+1)]

    for i in range(n):
        if A[i] == ' ':
            index = 0
        else:
            index = ord(A[i][j])-64
        print(index)
        C[index] += 1
        # each element C[i] is equal to the number of i in the array A

    for i in range(1, k):
        C[i] += C[i-1]
        # each C[i] is now equal to the number of elements in A equal or less than i

    for i in range(n-1, -1, -1):
        char = ord(A[i][j])-64
        index = C[char]-1
        B[index] = A[i]  # insert A[i] in the right position in B, given by C[i]-1
        C[char] += -1  # decrease by one the number of elements equal or less than A[i]

    return [list(g) for k, g in groupby(B, key=lambda x: x[j])]


def alphabetical_sort(lst):
    # m = len(lst)
    # n = max([len(s) for s in lst])
    int_lst = []
    for word in lst:
        int_lst.append('0'.join([str(ord(c)-96) for c in word]))
        int_lst = list(map(int, int_lst))

    ordered_lst = counting_sort(int_lst)

    final = []
    for sub in ordered_lst:
        tmp = str(sub).split('0')
        final.append([chr(int(x)+96) for x in tmp])

    return [''.join(sub) for sub in final]


def rec_alpha_sort(lst, j):
    if len(lst)==1:
        return lst

    new_lst = list_counting_sort2(lst, j)

    j += 1
    final = []
    for l in new_lst:
        final.append(rec_alpha_sort(l, j))
    
    return list(chain.from_iterable(final))
    



if __name__ == "__main__":
    # array = [4,7,2,4,2,8,5,6,1,2,5]
    # ordered_array = counting_sort(array)
    # print(*array)
    # print(*ordered_array)

    # lst = ['c','z','e','i','d','g','j','q','r','a']
    # ordered_alpha = alphabetical_couting_sort(lst)
    # print(*lst)
    # print(*ordered_alpha)
    string_lst = ['caoc', 'bcev', 'bcar']
    string_lst2 = ['paolo', 'lore nzo', 'giovanni', 'emanu ele', 'emanu ela', 'jorgi nho', 'salvatore']
    ordered_strings = rec_alpha_sort(string_lst2, 0)
    print(*string_lst2)
    print(*ordered_strings)
