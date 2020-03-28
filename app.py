from flask import Flask
from flask import request
import base64

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/upload', methods=['POST'])
def handle_form():
    data = request.data

    decoded = base64.b64decode(request.json['base'])
    media_write = open('test.m4a', 'w')
    media_write.write(decoded)

    return 'response'
