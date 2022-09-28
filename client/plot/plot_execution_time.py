import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
from matplotlib.pyplot import figure

# figure(figsize=(9, 8), dpi=100)

with open('execution_time.txt') as f:
    lines = f.readlines()

def get_y__measurements(id):
    y = []
    for i in range(id, len(lines), 20):
        y.append(np.array(list(map(float, lines[i][0:-1].split()))))
    return np.array(y)

def plot_line_with_confidence_interval(x, y_measurements, color, marker, label):
    y_mean = y_measurements.mean(axis=0)
    confidende_interval = []
    for i in range(0, y_measurements.shape[1]):
        data = np.array(y_measurements[:,i:i+1]).T[0] # 1D vector tranposed
        confidende_interval.append(st.norm.interval(alpha=0.99, loc=np.mean(data), scale=st.sem(data)))

    y_lower = [confidende_interval[i][0] for i in range(len(confidende_interval))]
    y_upper = [confidende_interval[i][1] for i in range(len(confidende_interval))]

    # asymmetric_error = np.array(list(zip(lolimit, uplimit))).T
    plt.plot(x, y_mean, color=color, marker=marker, label=label)
    plt.fill_between(x, y_lower, y_upper, alpha=0.2, color='tab:orange')

    # plt.errorbar(x, y_mean, yerr=lolimit, color=color, fmt=marker)
    # plt.errorbar(x, y_mean, yerr=asymmetric_error, fmt=marker, ecolor=color)

x = np.array(list(map(int, lines[0][0:-1].split())))
y_time_sse1 = get_y__measurements(1)
y_time_sse2 = get_y__measurements(3)
y_time_sse3 = get_y__measurements(5)
y_time_sse4 = get_y__measurements(7)
y_time_sse5 = get_y__measurements(9)
y_time_sse6 = get_y__measurements(11)
y_time_sse7 = get_y__measurements(13)
y_time_sse8 = get_y__measurements(15)
y_time_sse9 = get_y__measurements(17)
y_time_sse10 = get_y__measurements(19)

color = ['chartreuse', 'orange', 'firebrick', 'blue', 'pink', 'green', 'darkslategray', 'purple', 'gray', 'brown']
marker = ['^', '*', '.', 'o', '^', '*', '.', 'o', '*', '.']
# label = ['sse-search-1', 'sse-search-2', 'sse-search-3', 'sse-search-4']
label = ["Search-" + str(i) for i in range(100, 1001, 100) ]

plot_line_with_confidence_interval(x, y_time_sse1, color[0], marker[0], label[0])
plot_line_with_confidence_interval(x, y_time_sse2, color[1], marker[1], label[1])
plot_line_with_confidence_interval(x, y_time_sse3, color[2], marker[2], label[2])
plot_line_with_confidence_interval(x, y_time_sse4, color[3], marker[3], label[3])
plot_line_with_confidence_interval(x, y_time_sse5, color[4], marker[4], label[4])
plot_line_with_confidence_interval(x, y_time_sse6, color[5], marker[5], label[5])
plot_line_with_confidence_interval(x, y_time_sse7, color[6], marker[6], label[6])
plot_line_with_confidence_interval(x, y_time_sse8, color[7], marker[7], label[7])
plot_line_with_confidence_interval(x, y_time_sse9, color[8], marker[8], label[8])
plot_line_with_confidence_interval(x, y_time_sse10, color[9], marker[9], label[9])

plt.ylabel('Time (s)')
plt.xlabel('DB Size')
plt.title('SSE Search Results')
# plt.legend(bbox_to_anchor=(0.87, 1.12), loc='upper left', borderaxespad=0)

ax = plt.gca()
# ax.set_xlim([xmin, xmax])
ax.set_ylim([0, 6.5])


legend = plt.legend(fontsize='medium', ncol=2,handleheight=2.4, labelspacing=-0.5, columnspacing=2.05, loc='upper center', edgecolor='black')
legend.get_frame().set_alpha(None)
legend.get_frame().set_facecolor((0, 0, 1, 0.1))

# plt.show()
plt.savefig('frida_time' + '.pdf')