from flask import Blueprint, request
from decorators import device_authorized, valid_device
from model import devices, get_device, Device
from flask_cors import CORS

api = Blueprint('api', __name__, url_prefix='/api')
CORS(api)


@api.post("/update")
@device_authorized  # make sure device is authorized
@valid_device  # make sure device is valid (aka registered)
def update():
    """ Device updates are posted here """
    required_keys = ["device_name", "location_fix", "lat", "lon",
                     "location_type", "time", "date", "battery_voltage"]

    # check that all required keys are present
    data = request.get_json()
    for key in required_keys:
        if key not in data:
            return {"message": f"missing '{key}' key"}, 400

    # update device data
    device = get_device(data["device_name"])
    for key in required_keys:
        if key != "device_name":
            setattr(device.data, key, data[key])

    # return settings to the device
    return {'message': 'update successful!'}, 200


@api.route("/latest", methods=['GET', 'POST'])
@valid_device
def latest():
    """ get the latest info from the appropriate device """
    data = request.get_json()
    device = get_device(data["device_name"])

    return {device.name: device.serialize()}


@api.post("/change-settings")
@valid_device
def change_settings():
    """ get the latest info from the appropriate device """
    data = request.get_json()
    device = get_device(data["device_name"])

    for key in data:
        if key != "device_name":
            setattr(device.settings, key, data[key])

    return {"message": "success"}, 200


@api.post("/create-device")
def create_device():
    """ create a new device """
    try:
        data = request.get_json()
        device = Device(data["device_name"])
        devices.append(device)
        return {"message": "device created successfully!", "api_key": device.auth.api_key}, 200
    except KeyError as error:
        return {"message": f"missing key {error}"}, 400
