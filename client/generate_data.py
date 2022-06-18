from faker import Faker
import pandas as pd
import os
import requests
import json

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
    for i in range(1, min(len(dataset), k + 1)):
        words.append( dataset[i][0] )
    return words

if __name__ == '__main__':

    Faker.seed(123)

    fake = Faker()

    size = [10 * x for x in range(1, 4)]

    for sz in size:
        dataset = create_dataset(sz, 10, fake)
        words = get_search_set(dataset, 4)

        print(words)
        print()

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

    # query = {'keyword': ['Aaron Graham']}
    # response = requests.get('http://127.0.0.1:5003/search', json=query)
    # print(response.text)