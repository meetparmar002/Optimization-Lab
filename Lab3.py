import numpy as np
import pandas as ps

# INPUT
# 3 4
# 19 30 50 10
# 70 30 40 60
# 40 8 70 20
# 7 9 18
# 5 8 7 14


def VAM(matrix):
    """
    Vogel's Approximation Method(VAM) to find the initial basic feasible solution
    of the Transportation problem(TP).

    matrix=cost matrix including supply column(last column) and demand row(last row)
    """
    m = len(matrix)-1
    n = len(matrix[0])-1
    x = []
    # print(ps.DataFrame(matrix))

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
        # print(penalty)

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
            # x_matrix[mini][maxi] = min(matrix[mini][n], matrix[m][maxi])
            if matrix[mini][n] > matrix[m][maxi]:
                x.append((mini, maxi, matrix[m][maxi], matrix[mini][maxi]))
                matrix[mini][n] = matrix[mini][n] - matrix[m][maxi]
                matrix[m][maxi] = 0
                for i in range(m):
                    matrix[i][maxi] = float('inf')
                # for col in matrix:
                #     del col[maxi]
            else:
                x.append((mini, maxi, matrix[mini][n], matrix[mini][maxi]))
                # x_matrix[mini][maxi] = matrix[mini][n]
                matrix[m][maxi] = matrix[m][maxi] - matrix[mini][n]
                matrix[mini][n] = 0
                for j in range(m):
                    matrix[mini][j] = float('inf')
                # matrix.pop(mini)

            # print(ps.DataFrame(matrix))
            # print(ps.DataFrame(x))

        else:
            for j in range(n):
                item = matrix[maxi][j]
                if minc > item:
                    minc = item
                    mini = j
            if matrix[m][mini] > matrix[maxi][n]:
                x.append((maxi, mini, matrix[maxi][n], matrix[maxi][mini]))
                # x_matrix[maxi][mini] = matrix[maxi][n]
                matrix[m][mini] -= matrix[maxi][n]
                matrix[maxi][n] = 0
                for j in range(n):
                    matrix[maxi][j] = float('inf')
                # matrix.pop(maxi)
            else:
                x.append((maxi, mini, matrix[m][mini], matrix[maxi][mini]))
                # x_matrix[mini][maxi] = matrix[m][mini]
                matrix[maxi][n] -= matrix[m][mini]
                matrix[m][mini] = 0
                for i in range(m):
                    matrix[i][mini] = float('inf')
                # for col in matrix:
                #     del col[mini]
            # print(ps.DataFrame(matrix))
            # print(ps.DataFrame(x))
    return x


if __name__ == '__main__':

    rc = list(map(int, input().strip().split()))
    m = rc[0]
    n = rc[1]
    matrix = []
    for _ in range(m):
        matrix.append(list(map(float, input().strip().split())))

    ais = list(map(float, input().strip().split()))
    bis = list(map(float, input().strip().split()))
    if sum(ais) != sum(bis):
        print('This Transportation Problem is not balanced. \nTry again with other inputs')
    for i in range(m):
        matrix[i].append(ais[i])
    matrix.append(bis)

    matrix2 = []
    for i in range(m):
        matrix2.append(matrix[i])

    # VAM method to find initial basic feasible solution
    x = VAM(matrix)
    x.sort()
    initial_bfs = 0
    print('initial_bfs:')
    for t in x:
        initial_bfs += t[2] * t[3]
        print('x_{a}{b} = {c}'.format(
            a=int(t[0] + 1), b=int(t[1] + 1), c=t[2]), end=', ')
    print('\nCost:', initial_bfs)
