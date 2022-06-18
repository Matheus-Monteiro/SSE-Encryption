# from server.server import app

import pandas as pd
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import os

def check_server():
    return 'sucesso :)'

def build_trapdoor(MK, keyword):
    keyword_index = MD5.new()
    keyword_index.update(str(keyword).encode())
    ECB_cipher = AES.new(MK.encode("utf8"), AES.MODE_ECB)
    return ECB_cipher.encrypt(keyword_index.digest())

def build_codeword(ID, trapdoor):
    ID_index = MD5.new()
    ID_index.update(str(ID).encode())
    ECB_cipher = AES.new(trapdoor, AES.MODE_ECB)
    return ECB_cipher.encrypt(ID_index.digest()).hex()

def search_index(document, trapdoor):
    search_result = []
    data_index = pd.read_csv(document)
    data_index = data_index.values
    # start_time = time.time()
    for row in range(data_index.shape[0]):
        if build_codeword(row, trapdoor) in data_index[row]:
            search_result.append(row)

    # print time.time() - start_time
    return search_result

def get_index_of(keywords):
    keyword = ""
    for w in keywords:
        keyword = keyword + str(w)
    master_key_file_name = "masterkey" #input("Please input the file stored the master key:  ")
    master_key = open(master_key_file_name).read()
    if len(master_key) > 16:
        master_key = bytes(master_key[:16])
    os.chdir('../datasets/')
    trapdoor_file = open(keyword + "_trapdoor", "wb")
    trapdoor_of_keyword = build_trapdoor(master_key, keyword)
    trapdoor_file.write(trapdoor_of_keyword)
    trapdoor_file.close()
    index_file_name = "Database_index.csv" #input("Please input the index file you want to search:  ")
    keyword_trapdoor = keyword + "_trapdoor" #input("Please input the file stored the trapdoor you want to search:  ")
    with open(keyword_trapdoor, "rb") as f:
        keyword_trapdoor = f.read()
    search_result = search_index(index_file_name, keyword_trapdoor)
    os.chdir('../server/')
    response = {'index': search_result}
    return response