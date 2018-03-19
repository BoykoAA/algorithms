import sys


def find_pos(xs, query):
    lo, hi = 0, len(xs)
    while lo < hi:
        mid = (lo+hi) // 2
        if query < xs[mid]:
            hi = mid
        elif query > xs[mid]:
            lo = mid + 1
        else:
            return mid + 1
    return -1






    # try:
    #     return xs.index(query) + 1
    # except ValueError:
    #     return -1




def main():
    reader = (map(int, line.split()) for line in sys.stdin)
    n, *xs = next(reader)
    k, *queries = next(reader)
    for query in queries:
        print (find_pos(xs, query), end=" ")



if __name__ == "__main__":
    main()




# def find_pos(xs, query):
#     output = []
#     for q in query:
#         if q in xs:
#             output.append(xs.index(q)+1)
#         else:
#             output.append(-1)
#     return (output)
