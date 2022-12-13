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

def search_index(table_name, trapdoor, cursor, columns_list):
    search_result = []

    query = "SELECT * from " + table_name
    result_proxy = cursor.execute(query)

    size = 1000
    results = result_proxy.fetchmany(size)
    #results = cursor.fetchall()

    from_db = []
    while results:
        for result in results:
            result = list(result)
            from_db.append(result)
        
        results = result_proxy.fetchmany(size)

    # data_index = pd.read_csv(document)
    data_index = pd.DataFrame(from_db, columns=columns_list)
    data_index = data_index.values

    for row in range(data_index.shape[0]):
        if build_codeword(row, trapdoor) in data_index[row]:
            search_result.append(row+1)

    return search_result

# @profile
def get_index_of(keywords, table_name):
    keyword = ""
    for w in keywords:
        keyword = keyword + str(w)
    master_key_file_name = "masterkey" #input("Please input the file stored the master key:  ")

    # print('CURRENT DIR:', os.getcwd())
    # print ("FILE EXISTS:"+str(os.path.exists(master_key_file_name)))
    
    master_key = open(master_key_file_name).read()
    if len(master_key) > 16:
        master_key = bytes(master_key[:16])
    
    os.chdir('../datasets/')

    document_name = "Database.db" #name of the database to be encrypted
    connection = sqlite3.connect(document_name)
    cursor = connection.cursor()
    
    data = cursor.execute("SELECT * FROM " + table_name)
    columns_list = list(map(lambda x: x[0], data.description))

    trapdoor_file = open(keyword + "_trapdoor", "wb")
    trapdoor_of_keyword = build_trapdoor(master_key, keyword)
    trapdoor_file.write(trapdoor_of_keyword)
    trapdoor_file.close()

    keyword_trapdoor = keyword + "_trapdoor" #input("Please input the file stored the trapdoor you want to search:  ")
    with open(keyword_trapdoor, "rb") as f:
        keyword_trapdoor = f.read()
    search_result = search_index(table_name, keyword_trapdoor, cursor, columns_list)
    cursor.close()

    os.chdir('../server/')
    response = {'index': search_result}
    return response