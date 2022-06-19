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
    # erase files
    try:
        os.remove("plot/execution_time.txt")
    except:
        pass
    try:
        os.remove("plot/cpu.txt")
    except:
        pass
    try:
        os.remove("plot/memory.txt")
    except:
        pass

    # init variables
    seed(123)
    Faker.seed(123)
    fake = Faker()

    number_of_columns, size, offset, number_of_queries_per_dataset, dataset_size = 10, 100, 500, [10, 20, 30, 40], []
    for i in range(7):
        dataset_size.append(size)
        size += offset

    number_of_rounds = 30
    for round in range(number_of_rounds):
        for number_of_queries in number_of_queries_per_dataset:
            y_cpu, y_mem, y_time, x = [], [], [], []
            for size in tqdm(dataset_size):
                
                dataset = create_dataset(size, number_of_columns, fake)
                queries = get_search_set(dataset, number_of_queries)

                # write dataset and columns in the datasets directory
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

                # build index with encrypted data
                os.system("python3 build_index.py")
                
                # run the generated queries
                start_time = time.time()
                for i in range(len(queries)):
                    query = {'keyword': queries[i]}
                    response = requests.get('http://127.0.0.1:5003/search', json=query)
                total_time = time.time() - start_time

                y_mem.append(psutil.virtual_memory()[2])
                y_cpu.append(psutil.cpu_percent(0.5))
                y_time.append(total_time)
                x.append(size)
                
                # erase all generated files in the dataset directory
                dir = '../datasets/'
                for f in os.listdir(dir):
                    os.remove(os.path.join(dir, f))

            # write data in files
            with open('plot/execution_time.txt', 'a') as f:
                for i in range(len(x)):
                    f.write("%s " % x[i])
                f.write("%s" % '\n')
                for i in range(len(y_time)):
                    f.write("%s " % y_time[i])
                f.write("%s" % '\n')

            with open('plot/cpu.txt', 'a') as f:
                for i in range(len(x)):
                    f.write("%s " % x[i])
                f.write("%s" % '\n')
                for i in range(len(y_cpu)):
                    f.write("%s " % y_cpu[i])
                f.write("%s" % '\n')

            with open('plot/memory.txt', 'a') as f:
                for i in range(len(x)):
                    f.write("%s " % x[i])
                f.write("%s" % '\n')
                for i in range(len(y_mem)):
                    f.write("%s " % y_mem[i])
                f.write("%s" % '\n')