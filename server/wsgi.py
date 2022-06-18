from wsgiref.simple_server import make_server
from server import app

if __name__ == '__main__':
    app.run(port="5003")