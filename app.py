import os
from api import api
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(api)
CORS(app)

try:
    if os.environ["UNIVERSAL_API_KEY"]:
        app.logger.warning("Don't use UNIVERSAL_API_KET in prod")
        app.logger.warning("Anyone with access to the key can post fake data")
except KeyError:
    pass


@app.get("/")
def hello_world():
    return "<b><i>Hello world!</i></b>", 200
