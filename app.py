from api import api
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# register api blueprint
app.register_blueprint(api)


@app.get("/")
def hello_world():
    return "<b><i>Hello world!</i></b>", 200
