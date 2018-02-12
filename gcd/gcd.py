def gcd(a, b):
    if a == 0 or b == 0:
        return max(a, b)
    else:
        if a > b:
            return gcd(a % b, b)
        else:
            return gcd(a, b % a)

def main():
    a, b = map(int, input().split())
    print(gcd(a, b))


if __name__ == "__main__":
    main()