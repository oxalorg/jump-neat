import matplotlib.pyplot as plt
import numpy as np

fh = np.loadtxt('log.txt')

bestf = [row[0] for row in fh]
slen = [row[1] for row in fh]
genes = [row[2] for row in fh]
neurons = [row[3] for row in fh]

num = np.arange(len(bestf))
avgf = np.cumsum(bestf)
avgf = [x/i for i, x in enumerate(bestf)]

# plt.plot(num, genes, 'g', label='no of genes')
# plt.plot(num, neurons, 'y', label='no of neurons')
plt.plot(num, slen, 'b', label='species length')
# plt.plot(num, slen, 'b', label='average fitness')
plt.ylabel('Length')
plt.xlabel('Generations')
# plt.legend(['best fitness', 'avg fitness'], loc='upper left')
plt.legend(['species length'], loc='upper left')
# plt.legend(['no. of genes', 'no. of neurons'], loc='upper left')
plt.show()
