from flask import Flask
app = Flask(__name__)


@app.get("/")
def hello_world():
    return "<b><i>Hello world!</i></b>", 200
