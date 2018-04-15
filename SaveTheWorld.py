from collections import defaultdict, Counter

def shoot(D,P):
    if 'S' not in P:
        return 0
    if P.count('S') > D:
        return 'IMPOSSIBLE'
    if 'C' not in P:
        return 0
    C=0
    S_arr = []
    for letter in P:
        if letter == "C":
            C+=1
        else:
            if C>0:
                S_arr+=[1<<i for i in range(C)]

    total=sum(S_arr)+P.count('S')
    diff=total-D

    if diff<=0:
        return 0
    # d=Counter(S_arr)
    # res=0
    # for k in sorted(d.keys()):
    #     t=diff//k
    #     res+=min(t,d[k])
    #     diff-=res*k
    #     if diff<=0:
    #         return res
    new_tot=0
    res=0
    for i in sorted(S_arr, reverse=True):
        new_tot+=i
        res+=1
        if new_tot >= diff:
            return res

    return 'IMPOSSIBLE'

assert(shoot(2, 'CC') == 0)
assert(shoot(1, 'SS') == 'IMPOSSIBLE')
assert(shoot(3, 'SS') == 0)
assert(shoot(1, 'CS') == 1)
assert(shoot(2, 'CS') == 0)
assert(shoot(6, 'SCCSSC') == 2)
assert(shoot(3, 'CSCSS') == 5)

t = int(input())
for i in range(1, t + 1):
    D,P = input().split(' ')
    D = int(D)
    print("Case #{}: {}".format(i, shoot(D,P)))