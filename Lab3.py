import numpy as np
import pandas as ps

# INPUT
# 3 4
# 19 30 50 10
# 70 30 40 60
# 40 8 70 20
# 7 9 18
# 5 8 7 14

# 3 4
# 3 1 7 4
# 2 6 5 9
# 8 3 3 2
# 250 350 400
# 200 300 350 150


def __VAM__(matrix):
    """
    Vogel's Approximation Method(VAM) to find the initial basic feasible solution
    of the Transportation problem(TP).

    matrix=cost matrix including supply column(last column) and demand row(last row)
    """
    m = len(matrix)-1
    n = len(matrix[0])-1
    x = []

    while True:
        penalty = []
        for i in range(m):
            if matrix[i][n] == 0:
                penalty.append(-1*float('inf'))
            else:
                min1, min2 = matrix[i][0], None
                for item in matrix[i][1:n]:
                    if min1 > item:
                        min2 = min1
                        min1 = item
                    elif min2 == None or min2 > item:
                        min2 = item
                penalty.append(min2 - min1)

        for j in range(n):
            if matrix[m][j] == 0:
                penalty.append(-1*float('inf'))
            else:
                min1, min2 = matrix[0][j], None
                for i in range(1, m):
                    item = matrix[i][j]
                    if min1 > item:
                        min2 = min1
                        min1 = item
                    elif min2 == None or min2 > item:
                        min2 = item
                penalty.append(min2 - min1)

        maxp = penalty[0]
        maxi = 0
        for t in range(1, len(penalty)):
            if maxp < penalty[t]:
                maxp = penalty[t]
                maxi = t
        if maxp == -1*float('inf'):
            break
        isItRow = True
        if maxi >= m:
            maxi -= m
            isItRow = False
        minc = float('inf')
        mini = 0
        if not isItRow:
            for i in range(m):
                item = matrix[i][maxi]
                if minc > item:
                    minc = item
                    mini = i
            if matrix[mini][n] > matrix[m][maxi]:
                x.append((mini, maxi, matrix[m][maxi], matrix[mini][maxi]))
                matrix[mini][n] = matrix[mini][n] - matrix[m][maxi]
                matrix[m][maxi] = 0
                for i in range(m):
                    matrix[i][maxi] = float('inf')
            else:
                x.append((mini, maxi, matrix[mini][n], matrix[mini][maxi]))
                matrix[m][maxi] = matrix[m][maxi] - matrix[mini][n]
                matrix[mini][n] = 0
                for j in range(m):
                    matrix[mini][j] = float('inf')
        else:
            for j in range(n):
                item = matrix[maxi][j]
                if minc > item:
                    minc = item
                    mini = j
            if matrix[m][mini] > matrix[maxi][n]:
                x.append((maxi, mini, matrix[maxi][n], matrix[maxi][mini]))
                matrix[m][mini] -= matrix[maxi][n]
                matrix[maxi][n] = 0
                for j in range(n):
                    matrix[maxi][j] = float('inf')
            else:
                x.append((maxi, mini, matrix[m][mini], matrix[maxi][mini]))
                matrix[maxi][n] -= matrix[m][mini]
                matrix[m][mini] = 0
                for i in range(m):
                    matrix[i][mini] = float('inf')
    return x


def __MODI__(matrix, ibfs):
    '''
    Modified Distribution method to find optimal solution of Transportation Problem
    given cost matrix and initial basic feasible solution founded by VAM method 
    '''
    m = len(matrix)
    n = len(matrix[0])

    new_mat = []
    for i in range(m):
        temp = []
        for j in range(n):
            temp.append([matrix[i][j], -1, False])
        new_mat.append(temp)
    for t in ibfs:
        new_mat[t[0]][t[1]][1], new_mat[t[0]][t[1]][2] = t[2], True
    print(ps.DataFrame(new_mat))

    u = [-999999] * m
    v = [-999999] * n

    allocations = []
    for i in range(m):
        count = 0
        for j in range(n):
            item = new_mat[i][j]
            if item[2]:
                count += 1
        allocations.append(count)
    for j in range(n):
        count = 0
        for i in range(m):
            item = new_mat[i][j]
            if item[2]:
                count += 1
        allocations.append(count)
    # print(allocations)
    maxa = 0
    idx = 0
    for i in range(len(allocations)):
        if maxa < allocations[i]:
            maxa = allocations[i]
            idx = i
    isItRow = True
    if idx >= m:
        idx -= m
        isItRow = False
        v[idx] = 0
    else:
        u[idx] = 0

    if isItRow:
        for j in range(n):
            if new_mat[idx][j][2]:
                v[j] = new_mat[idx][j][0] - u[idx]
    else:
        for i in range(m):
            if new_mat[i][idx][2]:
                u[i] = new_mat[i][idx][0]-v[idx]
    while -1 * 999999 in u or -1 * 999999 in v:
        for i in range(m):
            for j in range(n):
                item = new_mat[i][j]
                if item[2]:
                    if v[j] == -999999 and u[i] != -999999:
                        v[j] = item[0] - u[i]
                    elif v[j] != -999999 and u[i] == -999999:
                        u[i] = item[0] - v[j]
    # print(u)
    # print(v)

    delta = []
    for i in range(m):
        for j in range(n):
            item = new_mat[i][j]
            if not item[2]:
                delta.append((item[0] - u[i] - v[j], i, j))

    # print(delta)
    mind, r, c = delta[0][0], 0, 0
    for t in delta:
        if mind > t[0]:
            mind = t[0]
            r = t[1]
            c = t[2]

    if mind >= 0:
        # break
        print('Whoo! We have found the optimal solution')
    if mind < 0:
        print('Shit! This was not the Optimal solution')


if __name__ == '__main__':

    rc = list(map(int, input().strip().split()))
    m = rc[0]
    n = rc[1]
    matrix_for_vam = []
    for i in range(m):
        row = list(map(float, input().strip().split()))
        matrix_for_vam.append(row)

    matrix_for_modi = []
    for row in matrix_for_vam:
        matrix_for_modi.append(row.copy())

    ais = list(map(float, input().strip().split()))
    bis = list(map(float, input().strip().split()))
    if sum(ais) != sum(bis):
        print('This Transportation Problem is not balanced. \nTry again with other inputs')
        exit(code=1)
    for i in range(m):
        matrix_for_vam[i].append(ais[i])
    matrix_for_vam.append(bis)

    # VAM method to find initial basic feasible solution
    ibfs = __VAM__(matrix_for_vam)
    # ibfs[i][0]-->row index of allocated cell
    # ibfs[i][1]--> col index of allocated cell
    # ibfs[i][2]-->allocated units(Xij)
    # ibfs[i][3]-->corresponding cost

    ibfs.sort()
    initial_bfs = 0
    print('initial_bfs:')
    for t in ibfs:
        initial_bfs += t[2] * t[3]
        print('x_{a}{b} = {c}'.format(
            a=int(t[0] + 1), b=int(t[1] + 1), c=t[2]), end=', ')
    print('\nCost:', initial_bfs)

    __MODI__(matrix_for_modi, ibfs)
