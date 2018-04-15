from random import randrange
from collections import defaultdict

def index_dict(lis):
    d=defaultdict(list)
    for ind,val in enumerate(lis):
        d[val].append(ind)
    return d

def trouble_sort(orig_list):
    d=index_dict(orig_list)
    sorted_list = sorted(orig_list)
    flag=False
    for i in range(len(sorted_list)):
        flag=False
        for j in d[sorted_list[i]]:
            if abs(i-j)%2==0:
                flag=True
                d[sorted_list[i]].remove(j)
                break
        if flag==False:
            return i
    return 'OK'

assert(trouble_sort([0, 5, 2, 8]) == 1)
assert(trouble_sort([0, 7, 6, 3]) == 'OK')
assert(trouble_sort([4, 1, 2, 3]) == 0)
assert(trouble_sort([7, 8, 8, 7]) == 'OK')
assert(trouble_sort([1, 2, 5, 4]) == 2)
assert(trouble_sort([5, 4, 8, 1]) == 0)
assert(trouble_sort([9, 9, 7, 6]) == 0)
assert(trouble_sort([9, 5, 3, 3]) == 2)
assert(trouble_sort([6, 4, 2, 2]) == 2)
assert(trouble_sort([8, 0, 9, 6]) == 0)
assert(trouble_sort([29, 32, 37, 24, 65, 44, 99, 30, 5, 53]) == 4)
assert(trouble_sort([22, 58, 31, 60, 9, 36, 35, 17, 94, 78]) == 3)
assert(trouble_sort([5, 61, 13, 54, 70, 96, 37, 36, 54, 12]) == 'OK')
assert(trouble_sort([37, 48, 71, 59, 43]) == 1)
# print(trouble_sort([randrange(10) for i in range(10000)]))

t = int(input())
for i in range(1, t + 1):
    n = int(input())
    a = list(map(int, input().split(' ')))
    print("Case #{}: {}".format(i, trouble_sort(a)))

