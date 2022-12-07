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
import sqlite3

def create_dataset(num_of_rows, number_of_columns, faker):
    dataset, words = [], []
    for row in range(num_of_rows):
        line = []
        for col in range(number_of_columns):
            name = faker.name()
            line.append(name)
            words.append(name)
        dataset.append(line)
    return pd.DataFrame(dataset), pd.unique(words).tolist()

def get_search_set(k, words):
    words_search = []
    for i in range(k):
        idx = randint(0, len(words) - 1)
        words_search.append( words[idx] )
    return words_search

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

    dataset_size = [125, 250, 500, 1000, 2000, 4000]
    number_of_columns = 10
    # number_of_queries_per_dataset = [x for x in range(100, 1001, 100)]
    number_of_queries_per_dataset = [100, 250, 500, 750, 1000]

    number_of_rounds = 10
    for round in range(number_of_rounds):
        for number_of_queries in number_of_queries_per_dataset:
            y_cpu, y_mem, y_time, x = [], [], [], []
            # table_number = 1
            for size in tqdm(dataset_size):
                
                dataset, words = create_dataset(size, number_of_columns, fake)
                queries = get_search_set(number_of_queries, words)

                # write dataset and columns in the datasets directory
                os.chdir('../datasets/')
                
                table_name = 'SSE_sql_test' 
                connection = sqlite3.connect('Database.db')
                cursor = connection.cursor()
                dataset.to_sql(table_name, connection, if_exists='replace', index=False)

                # dataset.to_csv('Database.csv', na_rep='Unkown')
                # with open(r'keywordlist', 'w') as fp:
                #    column_names = list(dataset.columns.values.tolist())
                #    flag = False
                #    for item in column_names:
                #        if flag == True:
                #           fp.write(",%s" % item)
                #        else:
                #            fp.write("%s" % item)
                #        flag = True

                connection.commit()
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
                # dir = '../datasets/'
                # for f in os.listdir(dir):
                #     os.remove(os.path.join(dir, f))

                # table_number = table_number + 1

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

    cursor.close()