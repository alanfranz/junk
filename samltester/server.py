#!/usr/bin/env python

from flask import Flask
import requests

app = Flask(__name__)

@app.route('/submit_saml_response'):
def post_saml_response():
    pass

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/js/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))

if __name__ == '__main__':
    app.run()

