from flask import Flask, request
from bitcoinrpc.authproxy import AuthServiceProxy
import logging

global access 

access = AuthServiceProxy("http://admin1:123@bitcoin:19001", timeout=120)

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)

app = Flask(__name__)

def reconnect():
    global access 
    access = AuthServiceProxy("http://admin1:123@bitcoin:19001", timeout=120)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/generate", methods= ['POST'])
def generate():
    body = request.get_json()

    try:
        address = body['address']
        blocks = body['blocks']
    except KeyError as e:
        return 500

    try:
        res = access.generatetoaddress(blocks, address)
    except Exception as e:
        reconnect()
        return {'error': str(e)}
    return {'res': res}

@app.route("/balance")
def get_address():
    try:
        res = access.getbalance()
    except Exception as e:
        reconnect()
        return {'error': str(e)}
    return {'res': res}

@app.route("/send", methods= ['POST'])
def send_transaction():
    body = request.get_json()
    try:
        to = body['to']
        amount = body['amount']
    except KeyError as e:
        return 500

    try:
        res = access.sendtoaddress(to, amount)
    except Exception as e:
        reconnect()
        return {'error': str(e)}
    return {'res': res}