from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType
import uuid

devices = []
db = SQLAlchemy()


def get_device_names():
    return [device.name for device in devices]


def get_device(name):
    for device in devices:
        if device.name == name:
            return device


class DeviceModel(db.Model):
    """ Stores information about devices """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    api_key = db.Column(UUIDType, nullable=False, default=uuid.uuid4)
    data = db.relationship('DeviceDataModel', lazy=True)
    settings = db.relationship('DeviceSettingsModel', lazy=True)


class DeviceDataModel(db.Model):
    """ Stores data provided by device """
    id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    battery_voltage = db.Column(db.Float)
    battery_percentage = db.Column(db.Float)

    device_id = db.Column(db.Integer, db.ForeignKey('device_model.id'),
                          nullable=False)


class DeviceSettingsModel(db.Model):
    """ Stores device settings """
    id = db.Column(db.Integer, primary_key=True)
    update_interval = db.Column(db.Integer, nullable=False, default=3600)

    device_id = db.Column(db.Integer, db.ForeignKey('device_model.id'),
                          nullable=False)


class Device():
    def __init__(self, name):
        self.name = name
        self.data = DeviceData()
        self.settings = DeviceSettings()
        self.auth = DeviceAuth()

    def serialize(self):
        return {
            "name": self.name,
            "data": self.data.__dict__,
            "settings": self.settings.__dict__,
            "auth": self.auth.__dict__,
        }


class DeviceData():
    def __init__(self):
        self.lat = None
        self.lon = None
        self.battery_voltage = None
        self.battery_percentage = None


class DeviceSettings():
    def __init__(self):
        self.update_interval = 0


class DeviceAuth():
    def __init__(self):
        self.api_key = str(uuid.uuid4())
