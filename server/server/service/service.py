import sqlite3
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import os
import hashlib
# from memory_profiler import profile

def check_server():
    return 'sucesso :)'

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

def search_index(table_name, keywords, cursor, columns_list):
    search_result = []

    query = "SELECT * from " + table_name
    result_proxy = cursor.execute(query)

    size = 1000
    results = result_proxy.fetchmany(size)

    from_db = []
    while results:
        for result in results:
            result = list(result)
            from_db.append(result)
        
        results = result_proxy.fetchmany(size)

    data_index = pd.DataFrame(from_db, columns=columns_list)
    data_index = data_index.values

    for row in range(data_index.shape[0]):
        flag = False
        for kw in keywords:
            if kw in data_index[row]:
                flag = True
                break
        if flag:
            search_result.append(row+1)

    return search_result

def get_index_of(keywords, table_name):
    os.chdir('../datasets/')

    document_name = "Database.db" #name of the database to be encrypted
    connection = sqlite3.connect(document_name)
    cursor = connection.cursor()
    
    data = cursor.execute("SELECT * FROM " + table_name)
    columns_list = list(map(lambda x: x[0], data.description))

    search_result = search_index(table_name, keywords, cursor, columns_list)
    cursor.close()

    os.chdir('../server/')
    response = {'index': search_result}
    return response