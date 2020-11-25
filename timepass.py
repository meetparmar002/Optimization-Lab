import numpy as np
import matplotlib.pyplot as plt

a = [[1, 2], [3, 4]]
print(a)
b = []
for i in a:
    b.append(i.copy())
a[0][0] = 5
print(a)
print(b)
