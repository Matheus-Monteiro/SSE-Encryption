import sqlite3
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Random import random
import numpy as np
import time
import os
import hashlib

def build_trapdoor(MK, keyword):
    # keyword_index = MD5.new()
    # keyword_index.update(str(keyword).encode())
    keyword_index = hashlib.sha256(str(keyword).encode())
    ECB_cipher = AES.new(MK.encode("utf8"), AES.MODE_ECB)
    return ECB_cipher.encrypt(keyword_index.digest())


def build_codeword(ID, trapdoor):
    # ID_index = MD5.new()
    # ID_index.update(str(ID).encode())
    ID_index = hashlib.sha256(str(ID).encode())
    ECB_cipher = AES.new(trapdoor, AES.MODE_ECB)
    return ECB_cipher.encrypt(ID_index.digest()).hex()


def build_index(MK, ID, keyword_list):
    secure_index = [0] * len(keyword_list)
    for i in range(len(keyword_list)):
        codeword = build_codeword(ID, build_trapdoor(MK, keyword_list[i]))
        secure_index[i] = codeword
    random.shuffle(secure_index)
    return secure_index

def searchable_encryption(table_name, master_key, keyword_type_list, cursor):
    index_header = []
    for i in range(1, len(keyword_type_list) + 1):
        index_header.append("index_" + str(i))

    from_db = []
    document_index = []
    # start_time = time.time()

    query = "SELECT * from " + table_name
    cursor.execute(query)

    size = 1000
    results = cursor.fetchmany(size)

    while results:
        for result in results:
            result = list(result)
            from_db.append(result)

        results = cursor.fetchmany(size)

    raw_data = pd.DataFrame(from_db, columns=columns_list)
    features = list(raw_data)
    raw_data = raw_data.values

    column_number = [i for i in range(0, len(features)) if features[i] in columns_list]

    for row in range(raw_data.shape[0]):
        record = raw_data[row]
        record_keyword_list = [record[i] for i in column_number]
        record_index = build_index(master_key, row, record_keyword_list)
        document_index.append(record_index)

    # time_cost = time.time() - start_time
    # print(time_cost)

    document_index_dataframe = pd.DataFrame(np.array(document_index), columns=index_header)
    new_file_name = table_name + "_index"
    document_index_dataframe.to_sql(new_file_name, connection, if_exists='replace', index=False)


if __name__ == "__main__":

    master_key_file_name = "masterkey" #input("Please input the file stored the master key:  ")
    master_key = open(master_key_file_name).read()
    # master_key = open("masterkey", 'r')
    if len(master_key) > 16:
        print("the length of master key is larger than 16 bytes, only the first 16 bytes are used")
        master_key = bytes(master_key[:16])

    os.chdir('../datasets/')

    document_name = "Database.db" #input("Please input the file to be encrypted:  ")
    connection = sqlite3.connect(document_name)
    cursor = connection.cursor()

    # table_names = []
    # for i in range (1, 7):
    #     tn = "SSE_sql_test" + str(i)
    #     table_names.append(tn)

    table_name = 'SSE_sql_test'
    columns_list = []
    data = cursor.execute("SELECT * from " + table_name + " limit 1")

    for column in data.description:
        columns_list.append(column[0])

    #keyword_list_file_name = "keywordlist" #input("please input the file stores keyword type:  ")
    #keyword_type_list = open(keyword_list_file_name).read().split(",")
    
    searchable_encryption(table_name, master_key, columns_list, cursor)

    # print("Finished")

    # for tn in table_names:
    #     columns_list = []
    #     data = cursor.execute("SELECT * from " + tn + " limit 1")

    #     for column in data.description:
    #         columns_list.append(column[0])

    #     searchable_encryption(tn, master_key, columns_list, cursor)

    cursor.close()
    connection.commit()

    os.chdir('../client/')