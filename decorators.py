from functools import wraps
from flask import request
from model import get_device, get_device_names


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

        """
        # make sure api_key and device_name is valid
        print(get_device_names())
        if data["device_name"] not in get_device_names():
            return {"message": "invalid device_name or api_key"}, 400

        
        device = get_device(data["device_name"])
        print(data["api_key"], device.auth.api_key)
        if data["api_key"] != device.auth.api_key:
            return {"message": "invalid device_name or api_key"}, 400
        """

        return function(*args, **kwargs)

    return decorated_function


def valid_device(function):
    """ Check if the device in the request is valid """
    @wraps(function)
    def decorated_function(*args, **kwargs):
        data = request.get_json()

        if not data:
            return {"message": "no json data"}, 400

        if data["device_name"] not in get_device_names():
            return {"message": "invalid device name"}, 400

        return function(*args, **kwargs)

    return decorated_function
