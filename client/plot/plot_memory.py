import numpy as np
import matplotlib.pyplot as plt

with open('memory.txt') as f:
    lines = f.readlines()

x = list(map(int, lines[0][0:-1].split()))

y_time_sse1 = np.array(list(map(float, lines[1][0:-1].split())))
y_time_sse2 = np.array(list(map(float, lines[3][0:-1].split())))
y_time_sse3 = np.array(list(map(float, lines[5][0:-1].split())))
y_time_sse4 = np.array(list(map(float, lines[7][0:-1].split())))

d = 1
for i in range(9, len(lines), 8):
    y_time_sse1 += np.array(list(map(float, lines[i][0:-1].split())))
    d += 1
y_time_sse1 /= d

d = 1
for i in range(11, len(lines), 8):
    y_time_sse2 += np.array(list(map(float, lines[i][0:-1].split())))
    d += 1
y_time_sse2 /= d

d = 1
for i in range(13, len(lines), 8):
    y_time_sse3 += np.array(list(map(float, lines[i][0:-1].split())))
    d += 1
y_time_sse3 /= d

d = 1
for i in range(15, len(lines), 8):
    y_time_sse4 += np.array(list(map(float, lines[i][0:-1].split())))
    d += 1
y_time_sse4 /= d

color = ['chartreuse', 'orange', 'firebrick', 'blue']
marker = ['^', '*', '.', 'o']
label = ['sse-search-1', 'sse-search-2', 'sse-search-3', 'sse-search-4']

plt.plot(x, y_time_sse1, color=color[0], marker=marker[0], label=label[0])
plt.plot(x, y_time_sse2, color=color[1], marker=marker[1], label=label[1])
plt.plot(x, y_time_sse3, color=color[2], marker=marker[2], label=label[2])
plt.plot(x, y_time_sse4, color=color[3], marker=marker[3], label=label[3])

plt.ylabel('Memory Usage (%)')
plt.xlabel('Number of Queries')
plt.title('SSE Search Results')
plt.legend()
# plt.show()
plt.savefig('frida_memory' + '.pdf')