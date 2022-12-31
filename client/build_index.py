import sqlite3
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Random import random
import numpy as np
import time
import os
import hashlib
import sys
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import csv

def rsa_encrypt(data: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    encrypted_data = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data

def rsa_decrypt(encrypted_data: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data

def rsa_create_keys(number_of_bits):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=number_of_bits
    )
    
    # Serialize the private key and write it to a file
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("private_key.pem", "wb") as f:
        f.write(private_key_bytes)

def get_keys():
    # Read the PEM-formatted private key from the file
    with open("private_key.pem", "rb") as f:
        private_key_bytes = f.read()

    # Deserialize the private key and load it into an RSAPrivateKey object
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None
    )

    public_key = private_key.public_key()

    return public_key, private_key

def encrypt_table_row(row, public_key):
    new_row = []
    for word in row:
        new_row.append(rsa_encrypt(bytes(word, 'utf-8'), public_key))
    return new_row

def decrypt_table_row(row, private_key):
    new_row = []
    for word in row:
        new_row.append(rsa_decrypt(word, private_key).decode("utf-8"))
    return new_row

def data_base_encryption(table_name, cursor):
    public_key, private_key = get_keys()

    table_name = 'SSE_sql_test_1000'

    from_db_ecnp = []

    query = "SELECT * from " + table_name
    cursor.execute(query)

    size = 1000
    results = cursor.fetchmany(size)

    while results:
        for result in results:
            result = list(result)
            from_db_ecnp.append(encrypt_table_row(result, public_key))
        results = cursor.fetchmany(size)

    # for row in from_db_ecnp:
    #     print(decrypt_table_row(row, private_key))

    # print(len(from_db_ecnp), len(from_db_ecnp[0]))
    # print(len(columns_list))

    raw_data = pd.DataFrame(from_db_ecnp, columns=columns_list)
    features = list(raw_data)
    raw_data = raw_data.values

    # column_number = [i for i in range(0, len(features)) if features[i] in columns_list]
    document_index_dataframe = pd.DataFrame(np.array(from_db_ecnp), columns=columns_list)
    
    new_file_name = table_name + "_index"
    document_index_dataframe.to_sql(new_file_name, connection, if_exists='replace', index=False)


if __name__ == "__main__":
    os.chdir('../datasets/')

    # DB connection
    document_name = "Database.db" #input("Please input the file to be encrypted:  ")
    connection = sqlite3.connect(document_name)
    cursor = connection.cursor()

    # Create keys
    rsa_create_keys(4096)

    # Load RSA key pair
    public_key, private_key = get_keys()

    # # Test
    # msg = "abc"
    # enc_msg = rsa_encrypt(bytes("abc", 'utf-8'), public_key)
    # print(enc_msg)
    # dcp_msg = rsa_decrypt(enc_msg, private_key)
    # print(dcp_msg.decode("utf-8"))

    table_names = []
    for i in range (1, 7):
        tn = "SSE_sql_test" + str(i)
        table_names.append(tn)

    table_name = sys.argv[1]
    columns_list = []
    data = cursor.execute("SELECT * from " + table_name + " limit 1")

    for column in data.description:
        columns_list.append(column[0])

    data_base_encryption(table_name, cursor)

    cursor.close()
    connection.commit()

    os.chdir('../client/')