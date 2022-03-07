from flask import Blueprint, request, jsonify
from decorators import auth_device, use_device
from model import DeviceData, Device, db
from flask_cors import CORS

api = Blueprint('api', __name__, url_prefix='/api')
CORS(api)


@api.post("/<device>/update")
@use_device
@auth_device  # make sure device is authorized
def update(device):
    """ Device updates are posted here """
    required_keys = ["lat", "lon", "battery_voltage", "battery_percentage"]

    # check that all required keys are present
    data = request.get_json()
    for key in required_keys:
        if key not in data:
            return {"message": f"missing '{key}' key"}, 400

    # create a update record
    update_record = DeviceData(device=device)

    for key in required_keys:
        if key != "device_name":
            setattr(update_record, key, data[key])

    db.session.commit()

    # return settings to the device
    return {'message': 'update successful!'}, 200


@api.get("/<device>/latest")
@use_device
def latest(device):
    """ get the latest data from the appropriate device """
    latest_data = device.data[0]
    return jsonify(latest_data)


@api.post("/<device>/settings")
@use_device
def set_settings(device):
    """ update a devices settings """
    data = request.get_json()
    for key in data:
        setattr(device.settings, key, data[key])

    return {"message": "success"}, 200


@api.post("/create-device")
def create_device():
    """ create a new device """
    try:
        data = request.get_json()
        device = Device(name=data["device_name"])
        db.session.add(device)
        db.session.commit()
        return {"message": "device created successfully!", "api_key": device.api_key}, 200
    except KeyError as error:
        return {"message": f"missing key {error}"}, 400
