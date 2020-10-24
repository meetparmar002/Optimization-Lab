import pulp as p
from pulp import PULP_CBC_CMD
import numpy as np
import matplotlib.pyplot as plt
from sys import maxsize


def max_A(A):
    m = -1*maxsize
    for i in range(len(A)):
        m = max(m, float(A[i][2]))
    return m


# bool variable for whether to do max or min
domax = False
choice = input('Enter function you want to perform(min/max): ').lower()
if choice == 'maximize' or choice == 'max':
    # defining maximization problem
    problem = p.LpProblem('lp_problem', p.LpMaximize)
    domax = True
elif choice == 'minimize' or choice == 'min':
    # defining minimization problem
    problem = p.LpProblem('lp_problem', p.LpMinimize)
else:
    print('Enter valid function!')
    exit()

# defining decision variable
x = p.LpVariable('x', lowBound=0, cat='Continuous')
y = p.LpVariable('y', lowBound=0, cat='Continuous')

print('Inputs must be space separated')
c = input('Enter the cost coefficients: ').split()
if len(c) != 2:
    print('Please enter valid coefficient!')
    exit()

# objective function
problem += float(c[0])*x+float(c[1])*y

n_cons = int(input('Enter the number of constrain you want to have: '))
# n_cons = 3
A = []
for i in range(n_cons):
    # constrains
    constrain = input('Enter constrain ' + str(i + 1) +
                      ' coefficients: ').split()
    if len(constrain) != 4:
        print('Please enter valid constrain!')
        exit()
    if constrain[3] == 'leq':
        problem += float(constrain[0])*x + \
            float(constrain[1]) * y <= float(constrain[2])
    elif constrain[3] == 'geq':
        problem += float(constrain[0])*x + \
            float(constrain[1]) * y >= float(constrain[2])
    A.append(constrain)

# solving problem using PULP's CBC compiler
status = problem.solve(PULP_CBC_CMD(msg=False))

# if solution is found then print
if p.LpStatus[status].lower() == 'optimal':
    print('\nBounded feasible region')
    if domax:
        print('Unique Maximum sulution')
    else:
        print('Unique Minimum sulution')
    if domax:
        print('Miximum Solution: ')
    else:
        print('Minimum Solution: ')
    for var in problem.variables():
        print('%s = %.4f ' % (var.name, var.varValue))
    print('value = %.4f' % p.value(problem.objective))
# if solution could not be found then exit
elif p.LpStatus[status].lower() == 'infeasible':
    print('\nNo feasible region')
    print('Infeasible solution')
    exit()

maxa = max_A(A)

# creating X-Y plane using NumPy's meshgrid function
x, y = np.meshgrid(np.linspace(0, maxa + 5, 1000),
                   np.linspace(0, maxa + 5, 1000))

# This is to plot the feasible region if exists
X = True
for i in range(len(A)):
    if A[i][3] == 'leq':
        X = X & (float(A[i][0]) * x + float(A[i][1]) * y <= float(A[i][2]))
    elif A[i][3] == 'geq':
        X = X & (float(A[i][0]) * x + float(A[i][1]) * y >= float(A[i][2]))

# plot
plt.imshow(X, extent=(
    x.min(), x.max(), y.min(), y.max()), origin='lower', cmap='Reds', alpha=0.3)

# this is to plot the lines of feasible region
x = np.linspace(0, maxa+5, 1000)
for i in range(len(A)):
    if float(A[i][0]) == 0:
        plt.axhline(y=float(A[i][2]) / float(A[i][1]), xmin=0, xmax=0.6,
                    label=A[i][1] + 'y = ' + A[i][2])
        continue
    elif float(A[i][1]) == 0:
        plt.axvline(x=float(A[i][2]) / float(A[i][0]), ymin=0, ymax=0.6,
                    label=A[i][0] + 'x = ' + A[i][2])
        continue
    elif float(A[i][0]) != 0 and float(A[i][1]) != 0:
        y = (-1 * float(A[i][0]) * x + float(A[i][2])) / float(A[i][1])

    plt.plot(x, y, label=A[i][0] +
             'x + ' + A[i][1] + 'y = ' + A[i][2])

plt.xlim(0, 50)
plt.ylim(0, 50)
plt.xlabel('x')
plt.ylabel('y')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
