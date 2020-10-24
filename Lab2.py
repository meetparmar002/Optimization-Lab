# import numpy as np

from tabulate import tabulate

l = [["Hassan", 21, "LUMS"], ["Ali", 22, "FAST"], ["Ahmed", 23, "UET"]]
table = tabulate(l, headers=['Name', 'Age', 'University'], tablefmt='orgtbl')

print(table)
# def simplex_method(c, A):
#     c.extend([0.0, 0.0])
#     Cj = np.array(c)
#     A = np.array(A)
#     ab = []
#     ab.append(list(A[:, len(A[0])-1]))
#     for i in range(3):
#         ab.append(list(A[:, i]))
#     ab = [list(map(float, i)) for i in ab]
#     ab.append([1.0, 0.0])
#     ab.append([0.0, 1.0])
#     ab = np.transpose(ab)
#     a = np.array(ab)

#     CB = np.transpose([0, 0])
#     XB = [4, 5]

#     while True:
#         Zj_Cj = []
#         for i in range(5):
#             Zj = sum(CB * a[:, i+1])
#             Zj_Cj.append(Zj - Cj[i])

#         min = float('inf')
#         idx = 0
#         for i in range(len(Zj_Cj)):
#             if min > Zj_Cj[i]:
#                 min, idx = Zj_Cj[i], i
#         if min >= 0:
#             break
#         entering_variable = idx + 1

#         min_ratio = []
#         for i in range(2):
#             if a[i][entering_variable] > 0:
#                 min_ratio.append(a[i][0] / a[i][entering_variable])
#             else:
#                 min_ratio.append(float('inf'))
#         m_ratio = float('inf')
#         idx = 0
#         for i in range(len(min_ratio)):
#             if m_ratio > min_ratio[i]:
#                 m_ratio, idx = min_ratio[i], i

#         leaving_variable = XB[idx]
#         XB[idx] = entering_variable
#         CB[idx] = Cj[entering_variable - 1]

#         key_value = a[idx][entering_variable]
#         if idx == 0:
#             a[idx] = a[idx] / key_value
#             a[idx + 1] = a[idx + 1] - (a[idx + 1][entering_variable]) * a[idx]
#         else:
#             a[idx] = a[idx] / key_value
#             a[idx - 1] = a[idx - 1] - (a[idx - 1][entering_variable]) * a[idx]

#     x = [0] * 5

#     for i in range(len(XB)):
#         x[XB[i]-1] = a[i][0]

#     print('OUTPUT: (x_1, x_2, x_3) = ({x1}, {x2}, {x3})'.format(
#         x1=x[0], x2=x[1], x3=x[2]))
#     print('Optimal Value Z = %.2f' % (sum(CB * a[:, 0])))
    
#     # print(XB)
#     # print(CB)
#     # print(a)


# if __name__ == '__main__':
#     c = list(map(float, input('Enter cost coeffecients: ').strip().split()))[
#         :3]
#     if len(c) != 3:
#         print('Enter cost coeffecients properly!')
#         exit(1)
#     A = []
#     dum = 0
#     while dum < 2:
#         a = input('Enter the constrain %d: ' % (dum+1)).split()
#         if len(a) != 5 or a[3] != 'leq':
#             print('Enter valid constrain!')
#         else:
#             A.append(a)
#             dum += 1

#     simplex_method(c, A)

#     # simplex_method([1.0, 1.0, 3.0], [
#     #                ['3', '2', '1', 'leq', '3'], ['2', '1', '2', 'leq', '2']])
