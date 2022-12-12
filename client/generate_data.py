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

    dataset = pd.DataFrame(dataset)
    words = pd.DataFrame(words)

    cnd, ncold = dataset.columns.values, []
    for i in range(len(cnd)):
        ncold.append('column' + str(i))
    dataset.set_axis(ncold, axis='columns', inplace=True)

    cnw, ncolw = words.columns.values, []
    for i in range(len(cnw)):
        ncolw.append('column' + str(i))
    words.set_axis(ncolw, axis='columns', inplace=True)
    
    return dataset, words

def get_search_set(k, words):
    words_search = []
    for i in range(k):
        idx = randint(0, len(words) - 1)
        words_search.append( words[idx] )
    return words_search

def generated_databases(dataset_size):
    os.chdir('../datasets/')
    seed(123)
    Faker.seed(123)
    fake = Faker()
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()
    for size in dataset_size:
        table_name_db = 'SSE_sql_test_' + str(size)
        table_name_word_list = 'SSE_sql_test_word_' + str(size)
        dataset, words = create_dataset(size, number_of_columns, fake)
        dataset.to_sql(table_name_db, connection, if_exists='replace', index=False)
        words.to_sql(table_name_word_list, connection, if_exists='replace', index=False)
    connection.commit()
    cursor.close()
    os.chdir('../client/')

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
    dataset_size = [125, 250, 500, 1000, 2000, 4000]
    number_of_columns = 10
    number_of_queries_per_dataset = [100, 250, 500, 750, 1000]

    # Use the following method to generated an entire dataset and wordlits
    # generated_databases(dataset_size)

    connection = sqlite3.connect('../datasets/Database.db')
    cursor = connection.cursor()

    number_of_rounds = 1
    for round in range(number_of_rounds):
        for number_of_queries in number_of_queries_per_dataset:
            y_cpu, y_mem, y_time, x = [], [], [], []
            for size in tqdm(dataset_size):
                table_name_word_list = 'SSE_sql_test_word_' + str(size)
                cursor.execute('select column0 from ' + table_name_word_list)
                words =  [item[0] for item in cursor.fetchall()]
                queries = get_search_set(number_of_queries, words)

                table_name = 'SSE_sql_test_' + str(size) 
                os.system("python3 build_index.py " + table_name)
                
                start_time = time.time()
                for i in range(len(queries)):
                    query = {'keyword': queries[i]}
                    response = requests.get('http://127.0.0.1:5003/search', json=query)
                total_time = time.time() - start_time

                y_mem.append(psutil.virtual_memory()[2])
                y_cpu.append(psutil.cpu_percent(0.5))
                y_time.append(total_time)
                x.append(size)
                
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