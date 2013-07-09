import os
from flask import Flask
from werkzeug.wsgi import SharedDataMiddleware


app = Flask(__name__)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app,
                                    {'/media/': os.path.join(os.path.dirname(__file__), 'media')})