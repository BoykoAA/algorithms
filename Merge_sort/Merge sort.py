def merge(a, b):
    tmp = []
    global k
    while a and b:
        if a[0] <= b[0]:
            tmp.append(a.pop(0))
        else:
            tmp.append(b.pop(0))
            k += len(a)
    tmp.extend(a or b)
    return tmp


def mergesort(lst):
    if len(lst) == 1:
        return lst
    m = len(lst) // 2
    return merge(mergesort(lst[: m]), mergesort(lst[m:]))


def main():
    n = int(input())
    queue = [int(i) for i in input().split()]
    mergesort(queue)
    print(k)


if __name__ == '__main__':
    k = 0
    main()

# Второй вариант
    # def merg_sort(A):
    #
    #     if len(A) <= 1:
    #         return A
    #
    #     middle = int(len(A) / 2)
    #     left = merg_sort(A[:middle])
    #     right = merg_sort(A[middle:])
    #
    #     return merg(left, right)
    #
    #
    # def merg(left, right):
    #     result = []
    #
    #     while len(left) > 0 and len(right) > 0:
    #         if left[0] <= right[0]:
    #             result.append(left[0])
    #             left = left[1:]
    #         else:
    #             result.append(right[0])
    #             right = right[1:]
    #     if len(left) > 0:
    #         result += left
    #     if len(right) > 0:
    #         result += right
    #     return result