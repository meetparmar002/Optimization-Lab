import pulp as p
import numpy as np
import matplotlib.pyplot as plt
import pandas as ps
from docplex.mp.model import Model

domax = False
choice = input('Enter function you want to perform(min/max): ').lower()
if choice == 'maximize' or choice == 'max':
    domax = True
elif choice == 'minimize' or choice == 'min':
    pass
else:
    print('Enter valid function!')
    exit()


m = Model(name='Lab1')
x = m.continuous_var(name='x')
y = m.continuous_var(name='y')

print('\nInputs must be space separated')
c = input('Enter the cost coefficients: ').split()

n_cons = int(input('Enter the number of constrain you want to have: '))

A = []

for i in range(n_cons):
    constrain = input('Enter constrain'+str(i+1)+' coefficients: ').split()
    if constrain[3] == 'leq':
        m.add_constraint(int(constrain[0])*x +
                         int(constrain[1]) * y <= int(constrain[2]))
    elif constrain[3] == 'geq':
        m.add_constraint(int(constrain[0])*x +
                         int(constrain[1]) * y <= int(constrain[2]))
    A.append(constrain)


if domax:
    m.maximize(int(c[0]) * x + int(c[1]) * y)
else:
    m.minimize(int(c[0]) * x + int(c[1]) * y)
m.print_information()
url = None
key = None
sol = m.solve(url=url, key=key)
print(sol)
m.print_solution()


x, y = np.meshgrid(np.linspace(0, 50, 1000), np.linspace(0, 50, 1000))
X = True
for i in range(len(A)):
    if A[i][3] == 'leq':
        X = X & (int(A[i][0]) * x + int(A[i][1]) * y <= int(A[i][2]))
    elif A[i][3] == 'geq':
        X = X & (int(A[i][0]) * x + int(A[i][1]) * y >= int(A[i][2]))

plt.imshow(X, extent=(
    x.min(), x.max(), y.min(), y.max()), origin='lower', cmap='Reds', alpha=0.3)

x = np.linspace(0, 100, 1000)

y0 = (int(A[0][0]) * x + int(A[0][2])) / int(A[0][1])
plt.plot(x, y0)

plt.show()
