from functools import wraps
from flask import request
from model import get_device_names


def validated(function):
    """ wrapper for API requests """
    @wraps(function)
    def decorated_function(*args, **kwargs):

        data = request.get_json()

        # check that json is present
        if not data:
            return {"message": "missing json data"}, 400

        # check that device key is present
        if "device_name" not in data:
            return {"message": "missing 'device_name' key from json data"}, 400

        # check that device is valid name
        if data["device_name"] not in get_device_names():
            return {"message": "invalid device_name"}, 400

        return function(*args, **kwargs)

    return decorated_function
