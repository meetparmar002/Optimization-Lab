import numpy as np

def simplex_method(c, A):
    c.extend([0.0] * len(A))
    # array of cost coefficient
    Cj = np.array(c)
    A = np.array(A)
    ab = []
    ab.append(list(A[:, len(A[0])-1]))
    for i in range(3):
        ab.append(list(A[:, i]))
    ab = [list(map(float, i)) for i in ab]
    eye = np.eye(len(A))
    # print(eye)
    for i in range(len(A)):
        ab.append(list(eye[i]))
    # print(ab)
    ab = np.transpose(ab)

    # NOTE- here first column is 'b' and others are 'aj'
    a = np.array(ab)

    # Cb vector
    CB = np.transpose([0.0] * len(A))

    # basic vector
    XB = []
    for i in range(len(A)):
        XB.append(i+4)

    while True:  # for iterations
        # Zj-Cj
        Zj_Cj = []
        for i in range(5):
            Zj = sum(CB * a[:, i+1])
            Zj_Cj.append(Zj - Cj[i])

        # to find entering variable
        min = float('inf')
        idx = 0
        for i in range(len(Zj_Cj)):
            if min > Zj_Cj[i]:
                min, idx = Zj_Cj[i], i

        # if all the Zj-Cj values are >= 0 than we have reached the optimality
        # no need to go further
        if min >= 0:
            break

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

        # to find the leaving variable
        m_ratio = float('inf')
        idx = 0
        for i in range(len(min_ratio)):
            if m_ratio > min_ratio[i]:
                m_ratio, idx = min_ratio[i], i

        leaving_variable = XB[idx]

        # insert the entering variable to the basic vector
        XB[idx] = entering_variable
        CB[idx] = Cj[entering_variable - 1]

        # key value
        key_value = a[idx][entering_variable]

        # evaluates the rows
        a[idx] = a[idx] / key_value
        for i in range(len(A)):
            if i != idx:
                a[i] = a[i]-(a[i][entering_variable])*a[idx]

    # to display the output
    x = [0] * 5
    for i in range(len(XB)):
        x[XB[i]-1] = a[i][0]

    print('\nOUTPUT: (x_1, x_2, x_3) = (%.2f, %.2f, %.2f)' %
          (x[0], x[1], x[2]))
    print('Optimal(Maximum) Value Z = %.2f' % (sum(CB * a[:, 0])))

    # print(XB)
    # print(CB)
    # print(a)


if __name__ == '__main__':
    print('Simplex Method to solve LPP of at most 3 variable\n')
    c = list(map(float, input('Enter cost coeffecients: ').strip().split()))[
        :3]
    if len(c) != 3:
        print('Enter cost coeffecients properly!')
        exit(1)
    A = []
    dum = 0
    con = int(input('\nHow many constrain are there? '))
    print('\nFormat: ai1 ai2 ai3 leq bi; e.g. 1 2 3 leq 4')
    while dum < con:
        a = input('Enter the constrain %d: ' % (dum + 1)).split()
        if len(a) != 5 or a[3] != 'leq':
            print('Enter valid constrain!')
            if a[2] == 'leq':
                print('You might have forgotten the third varible')
        else:
            A.append(a)
            dum += 1

    simplex_method(c, A)

    # simplex_method([1.0, 1.0, 3.0], [
    #                ['3', '2', '1', 'leq', '3'], ['2', '1', '2', 'leq', '2']])
