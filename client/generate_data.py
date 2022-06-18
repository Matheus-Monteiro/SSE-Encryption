from faker import Faker
import pandas as pd
import os
import requests
import json
from random import seed
from random import randint
import time
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import psutil

def create_dataset(num_of_rows, number_of_columns, faker):
    dataset = []
    for row in range(num_of_rows):
        line = []
        for col in range(number_of_columns):
            line.append(faker.name())
        dataset.append(line)
    return pd.DataFrame(dataset)

def get_search_set(dataset, k):
    words = []
    for i in range(k):
        row = randint(1, dataset.shape[0] - 1)
        col = randint(1, dataset.shape[1]) - 1
        words.append( dataset.iloc[row, col] )
    return words

if __name__ == '__main__':
    seed(123)
    Faker.seed(123)
    fake = Faker()

    size, last, offset, search_size = [], 100, 500, [10, 20, 30, 40]
    for i in range(1):
        size.append(last)
        last += offset

    time_info_x, time_info_y = [], []
    memo_info_x, memo_info_y = [], []
    cpu_info_x, cpu_info_y = [], []
    label = []

    APGAR = False

    for string_size in search_size:
        x, y = [], []
        y_cpu, y_mem = [], []

        for sz in size:
            
            dataset = create_dataset(sz, 10, fake)
            words = get_search_set(dataset, string_size)

            os.chdir('../datasets/')
            dataset.to_csv('Database.csv', na_rep='Unkown')
            with open(r'keywordlist', 'w') as fp:
                column_names = list(dataset.columns.values.tolist())
                flag = False
                for item in column_names:
                    if flag == True:
                        fp.write(",%s" % item)
                    else:
                        fp.write("%s" % item)
                    flag = True

            os.chdir('../client/')
            os.system("python3 build_index.py")
            start_time = time.time()

            for i in tqdm(range(len(words))):
                if APGAR == True:
                    continue
                query = {'keyword': words[i]}
                response = requests.get('http://127.0.0.1:5003/search', json=query)
                APGAR = True
            total_time = time.time() - start_time
            y_mem.append(psutil.virtual_memory()[2])
            y_cpu.append(psutil.cpu_percent(0.5))
            x.append(sz)
            y.append(total_time)
            
            dir = '../datasets/'
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f))

        memo_info_x.append(x.copy())
        cpu_info_x.append(x.copy())
        memo_info_y.append(y_mem.copy())
        cpu_info_y.append(y_cpu.copy())
        time_info_x.append(x.copy())
        time_info_y.append(y.copy())
        label.append('sse-search-' + str(string_size))

    #plot

    color = ['chartreuse', 'orange', 'firebrick', 'blue', 'violet']
    marker = ['^', '*', '.', 'o']

    for i in range(len(memo_info_x)):
        plt.plot(time_info_x[i], time_info_y[i], color=color[i], marker=marker[i], label=label[i])

    plt.ylabel('Time (s)')
    plt.xlabel('Number of Queries')
    plt.title('SSE Search Results')
    plt.legend()
    plt.savefig('frida_time' + '.pdf')

    fig = plt.figure()
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    for i in range(len(memo_info_x)):
        plt.plot(memo_info_x[i], memo_info_y[i], color=color[i], marker=marker[i], label=label[i])

    plt.ylabel('Memory (%)')
    plt.xlabel('Number of Queries')
    plt.title('Memory Consumption')
    plt.legend()
    plt.savefig('frida_memory' + '.pdf')

    fig = plt.figure()
    plt.figure().clear()
    plt.close()
    plt.cla()
    plt.clf()

    for i in range(len(cpu_info_x)):
        plt.plot(cpu_info_x[i], cpu_info_y[i], color=color[i], marker=marker[i], label=label[i])

    plt.ylabel('CPU (%)')
    plt.xlabel('Number of Queries')
    plt.title('CPU Consumption')
    plt.legend()
    plt.savefig('frida_cpu' + '.pdf')