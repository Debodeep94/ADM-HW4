def counting_sort(A, k):
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
    

if __name__ == "__main__":
    array = [4,7,2,4,2,8,5,6,1,2,5]
    # array = [2,4,1,0,1]
    k = max(array)
    ordered_array = counting_sort(array, k)
    print(*array)
    print(*ordered_array)
    