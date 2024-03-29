from flask import Blueprint, current_app, request, jsonify, json
from decorators import auth_device, use_device
from model import DeviceData, Device, DeviceSettings, db, secs_since_update
from flask_cors import CORS
from sqlalchemy import exc

api = Blueprint('api', __name__, url_prefix='/api')
CORS(api)


@api.get("/<device>")
@use_device
def get_device(device):
    return jsonify(device)


@api.post("/<device>")
def new_device(device):
    """ create a new device """
    try:
        device = Device(name=device)
        DeviceSettings(device=device)
        db.session.add(device)
        db.session.commit()
        return {"message": "device created successfully!", "api_key": device.api_key}, 200
    except KeyError as error:
        return {"message": f"missing key {error}"}, 400
    except exc.IntegrityError:
        return {"message": "device name is already taken"}, 409


@api.delete("/<device>")
@use_device
def delete_device(device):
    """ delete device, device settings and device data """
    db.session.delete(device.settings)
    for data in device.data:
        db.session.delete(data)
    db.session.delete(device)
    db.session.commit()

    return {"message": "device and related records deleted successfully"}, 200


@api.get("/<device>/data")
@use_device
def get_latest_data(device):
    """ get the latest data from device """
    if not device.data:
        return {"message": "no device data"}, 404

    return jsonify(device.data)


@api.post("/<device>/data")
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
        setattr(update_record, key, data[key])

    db.session.commit()

    # return settings to the device
    return {'message': 'update successful!'}, 200


@api.get("/<device>/data/last")
@use_device
def get_data(device):
    """ get the latest data from device """
    try:
        # TODO: find a non hack to do this
        data = json.loads(current_app.json_encoder().encode(device.data[-1]))
        data["secs_since_update"] = secs_since_update(device.data[-1])
        return data, 200
    except IndexError:
        return {"message": "no device data"}, 404


@api.get("/<device>/settings")
@use_device
def get_settings(device):
    """ get a devices settings """
    return jsonify(device.settings)


@api.post("/<device>/settings")
@use_device
def set_settings(device):
    """ update a devices settings """
    data = request.get_json()
    for key in data:
        setattr(device.settings, key, data[key])

    db.session.commit()

    return {"message": "success"}, 200
