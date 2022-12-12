from sys import flags
from server import app
from flask import Flask, request, jsonify
import json

from server.service.service import search_index
from server.service.service import build_codeword
from server.service.service import build_trapdoor
from server.service.service import check_server
from server.service.service import get_index_of

import os

@app.route("/check", methods=['GET', 'POST'])
def check():
    return check_server()

@app.route("/search", methods=['GET', 'POST'])
def search():
    keywords = request.json['keyword']
    table_name = request.json['table_name']

    # print(10 * "#")
    # print(keywords)
    # print(10 * "#")
    # print(10 * "#", flush=True)
    # search_result = dict()
    # response = {'index': search_result}
    
    print(os.getcwd())
    
    # return response
    
    return get_index_of(keywords, table_name)