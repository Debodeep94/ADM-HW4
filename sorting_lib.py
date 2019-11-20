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


def alphabetical_sort(lst):
    m = len(lst)
    n = max([len(s) for s in lst])
    int_lst = []
    for word in lst:
        int_lst.append([(ord(c)-96) for c in word])

    ordered_lst = list_counting_sort(int_lst, 0)

    final = []
    for sub in ordered_lst:
        final.append([chr(x+96) for x in sub])

    return [''.join(sub) for sub in final]


if __name__ == "__main__":
    # array = [4,7,2,4,2,8,5,6,1,2,5]
    # ordered_array = counting_sort(array)
    # print(*array)
    # print(*ordered_array)

    # lst = ['c','z','e','i','d','g','j','q','r','a']
    # ordered_alpha = alphabetical_couting_sort(lst)
    # print(*lst)
    # print(*ordered_alpha)
    
    string_lst = ['paolo', 'lorenzo', 'giovanni', 'emanuele', 'emanuela', 'jorginho', 'salvatore']
    ordered_strings = alphabetical_sort(string_lst)
    print(*string_lst)
    print(*ordered_strings)
