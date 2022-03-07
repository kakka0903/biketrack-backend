from flask import request, current_app
from functools import wraps
from model import get_device


def device_authorized(function):
    """ wrapper to reject requests that are not authenticated """
    @wraps(function)
    def decorated_function(*args, **kwargs):
        data = request.get_json()

        if not data:
            return {"message": "no json data present"}, 400

        # make sure device name is present
        if "device_name" not in data:
            return {"message": "device_name not in json"}, 400

        # make auth data is present
        if not data or "api_key" not in data:
            return {"message": "api_key not in json"}, 400

        # make sure device exists
        device = get_device(data["device_name"])
        if not device:
            return {"message": "invalid device_name or api_key"}, 400

        # check if api_key matches device registered api_key
        device = get_device(data["device_name"])
        validated = data["api_key"] == device.api_key

        # check if api_key matches universal apikey
        if not validated and current_app.config["UNIVERSAL_API_KEY"]:
            validated = data["api_key"] == current_app.config["UNIVERSAL_API_KEY"]

        if not validated:
            return {"message": "invalid device_name or api_key"}, 400

        return function(*args, **kwargs)

    return decorated_function


def use_device(function):
    """ get the device used in the request from the db and pass it to the function """
    @wraps(function)
    def decorated_function(*args, **kwargs):
        kwargs["device"] = get_device(kwargs["device"])
        if not kwargs["device"]:
            return {"message": "invalid device name"}, 400
        return function(*args, **kwargs)

    return decorated_function
