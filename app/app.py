import socket
from flask import Flask

app = Flask(__name__)

@app.route('/')
def show_hostname():
    hostname = socket.gethostname()
    return f"Hello! This request was served by server: {hostname}\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)