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
    return get_index_of(keywords)