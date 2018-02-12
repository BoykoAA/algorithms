def fib_digit(n):
    F = list(range(0, n+2))
    F[0] = 0
    F[1] = 1
    if n == 1:
        return (n)
    for i in list(range(2, F[n+1])):
        F[i] = (F[i-1] + F[i-2])%10
    return (F[i])


def main():
    n = int(input())
    print(fib_digit(n))


if __name__ == "__main__":
    main()