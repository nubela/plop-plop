#!/usr/bin/python
from flup.server.fcgi import WSGIServer
from web.plop import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='./fcgi.sock').run()