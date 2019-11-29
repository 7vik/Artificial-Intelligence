ls = []         # list of all possible vals of N
# good = 1 and bad = 0
# cannon fire = 1 and not fire = 0

for N in range(4090,5000):
    kings = [[1 for _ in range(N)] for i in range(4095)]
    jacks = [[1 for _ in range(N)] for i in range(4095)]
    queens = [[0 for _ in range(N)] for i in range(4095)]
    cannon = [[0 for _ in range(N)] for i in range(4095)]
    for d in range(4095):
        cannon[d][0] = 1    # first kingdom always hits
    for day in range(1,4095):     # for each day
        for dom in range(N):    # for each dom
            if cannon[day][dom]:
                if jacks[day][dom] and not queens[day-1][dom]:
                    queens[day][dom] = 1
                else:
                    queens[day][dom] = 0
            else:
                queens[day][dom] = 0 # try 1
            if queens[day-1][dom] and not queens[day][dom]:
                cannon[(day+1) % 4095][(dom+1) % N] = 1

    flag = True
    for do in range(N):
        if queens[4094][do]:
            flag = False
    
    if flag:
        ls.append(N)

print(ls)
            