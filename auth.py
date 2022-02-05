import json
import uuid
from flask import current_app, request
from functools import wraps


SECRETS_PATH = ".secrets.json"


def init_auth():
    """
        Makes sure the app has a API_KEY in config.
        API_KEY is stored in the secrets file.
        A new one is generated if there is no key.
    """

    try:
        key = load_api_key()
    except FileNotFoundError or ValueError:
        current_app.logger.info("Could not load API_KEY from .secrets")
        key = create_api_key()
        store_api_key(key)

    current_app.config["API_KEY"] = key
    current_app.logger.info(f"Key set to {key}")


def load_api_key():
    """ load api_key from secrets file """
    with open(SECRETS_PATH, "r") as file:
        data = json.load(file)
        return data["api_key"]


def store_api_key(key):
    """ store api_key in secrets file """
    with open(SECRETS_PATH, "w") as file:
        json.dump({"api_key": key}, file)


def create_api_key():
    """ generate a uuid as the api key """
    return str(uuid.uuid4())


def authenticated(function):
    """ wrapper to reject requests that are not authenticated """
    @wraps(function)
    def decorated_function(*args, **kwargs):
        data = request.get_json()

        if not data or "api_key" not in data:
            return {"message": "api_key not present"}, 400

        if data["api_key"] != current_app.config["API_KEY"]:
            return {"message": "api_key not recognised"}, 400

        return function(*args, **kwargs)

    return decorated_function
