# Input:
# 1 1 3
# 3 2 1 leq 3
# 2 1 2 leq 2

# OUTPUT:
# (x_1, x_2, x_3) = (0.00, 0.00, 1.00)
# Optimal(Maximum) Value Z = 3.00

import numpy as np
import pandas as pd
from tabulate import tabulate


def simplex_method(c, A):
    # number of original veriables
    n = len(c)

    # number of slack variables
    sn = len(A)

    total_var = n + sn

    c.extend([0.0] * sn)

    # array of cost coefficient including the slack variables'
    Cj = np.array(c)

    A = np.array(A)
    ab = []
    ab.append(list(A[:, len(A[0])-1]))
    for i in range(n):
        ab.append(list(A[:, i]))
    ab = [list(map(float, i)) for i in ab]
    eye = np.eye(sn)
    # print(eye)
    for i in range(len(A)):
        ab.append(list(eye[i]))
    ab2 = np.transpose(ab)

    # NOTE- here first column is 'b' and remaining are 'a1,a2,a3,...'
    a = np.array(ab2)
    # print(ab)

    # first iteration/initialization
    # Cb vector
    CB = np.transpose([0.0] * sn)

    # basic vector, initially consists of only slack variables
    XB = []
    for i in range(sn):
        XB.append(i + n + 1)

    # print(l)
    # headings of the table
    headings = ['CB', 'XB', 'b']
    for i in range(total_var):
        headings.append('a{}'.format(i + 1))
    headings.append('min ratio')
    itr = 1

    while True:  # for iterations
        doBreak = False

        # content of the table
        l = []
        l.append(list(CB))
        l.append(XB)

        for i in range(total_var + 1):
            l.append(list(a[:, i]))

        print('\n\nIteration #%d' % itr)

        # Zj-Cj
        Zj_Cj = []
        j = 1
        while j < total_var+1:
            Zj = sum(CB * a[:, j])
            Zj_Cj.append(Zj - Cj[j - 1])
            j += 1

        # to find entering-variable
        min = float('inf')
        idx = 0
        for i in range(len(Zj_Cj)):
            if min > Zj_Cj[i]:
                min, idx = Zj_Cj[i], i

        # if all the Zj-Cj values are >= 0 than we have reached the optimality(for maximization)
        # no need to go further
        if min >= 0:
            doBreak = True

        entering_variable = idx + 1

        # to find min ratio
        min_ratio = []
        for i in range(len(A)):
            # don't calculate the min ration if aj<=0,
            # instead of that put the infinity
            if a[i][entering_variable] > 0:
                min_ratio.append(a[i][0] / a[i][entering_variable])
            else:
                min_ratio.append(float('inf'))

        l.append(min_ratio)
        # create table
        print('                 Cj     ', end='')
        for i in range(len(Cj)):
            print('%.1f' % Cj[i], end='    ')
        print('\n-----------------------------------------------------------------------------')

        table = tabulate(np.transpose(l), headers=headings, tablefmt='orgtbl')
        print(table)
        print(
            '------------------------------------------------------------------------------')
        print('          Zj-Cj       ', end='')

        for i in range(len(Zj_Cj)):
            print('%.1f' % Zj_Cj[i], end='    ')

        # to find the leaving-variable
        m_ratio = float('inf')
        idx = 0
        for i in range(len(min_ratio)):
            if m_ratio > min_ratio[i]:
                m_ratio, idx = min_ratio[i], i

        leaving_variable = XB[idx]

        # insert the entering-variable to the basic vector
        XB[idx] = entering_variable
        CB[idx] = Cj[entering_variable - 1]

        # key value
        key_value = a[idx][entering_variable]

        # evaluates the rows
        a[idx] = a[idx] / key_value
        for i in range(len(A)):
            if i != idx:
                a[i] = a[i] - (a[i][entering_variable]) * a[idx]

        if doBreak:
            break

        itr += 1

    # to display the output
    x = [0] * (total_var)
    for i in range(len(XB)):
        x[XB[i]-1] = a[i][0]

    # print('\nOUTPUT: (x_1, x_2, x_3) = (%.2f, %.2f, %.2f)' % (x[0], x[1], x[2]))

    print('\n\nOUTPUT: (', end='')
    for i in range(n-1):
        print('x_%d' % (i + 1), end=', ')
    print('x_%d' % (n), end=') = (')
    for i in range(n-1):
        print('%.2f' % x[i], end=', ')
    print('%.2f)' % x[n-1])

    print('Optimal(Maximum) Value Z = %.2f' % (sum(CB * a[:, 0])))

    # print(XB)
    # print(CB)
    # print(a)


if __name__ == '__main__':
    print('Simplex Method to solve LPP\n')

    # inputs
    n = int(input('How many variables are there? : '))
    c = list(map(float, input('Enter the cost coeffecients: ').strip().split()))
    if len(c) != n:
        print('Error: Enter proper number of cost coeffecients!')
        exit(1)
    A = []
    dum = 0
    con = int(input('\nHow many constrain are there? '))
    print('\nFormat: ai1 ai2 ai3 leq bi; e.g. 1 2 3 leq 4')
    while dum < con:
        a = input('Enter the constrain %d: ' % (dum + 1)).split()
        if len(a) != (n+2) or a[len(a)-2] != 'leq':
            print('Error: Enter valid constrain!')
        else:
            A.append(a)
            dum += 1

    simplex_method(c, A)

    # simplex_method([1.0, 1.0, 3.0], [
    #                ['3', '2', '1', 'leq', '3'], ['2', '1', '2', 'leq', '2']])
