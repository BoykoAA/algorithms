n = int(input())
data = [int(i) for i in input().split()]
count = [(" " + str(i)) * data.count(i) for i in range(11) if data.count(i) > 0]
print("".join(count).strip())