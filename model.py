from datetime import datetime
import click
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import UUIDType, EmailType
from flask.cli import with_appcontext
import uuid

db = SQLAlchemy()


def get_device_names():
    devices = Device.query.all()
    return [device.name for device in devices]


def get_device(name):
    return Device.query.filter_by(name='koga-miyata').first()


def secs_since_update(device_data):
    return (datetime.utcnow() - device_data.timestamp).seconds


class Device(db.Model):
    """ Stores information about devices """
    id = db.Column(UUIDType, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    api_key = db.Column(UUIDType, nullable=False, default=uuid.uuid4)
    data = db.relationship('DeviceData', backref='device', lazy=True)
    settings = db.relationship(
        'DeviceSettings', backref='device', lazy=True, uselist=False)

    user_id = db.Column(UUIDType, db.ForeignKey('user.id'), nullable=False)

    def __json__(self):
        return ["id", "name", "api_key"]


class DeviceData(db.Model):
    """ Stores data provided by device """
    id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    battery_voltage = db.Column(db.Float)
    battery_percentage = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    device_id = db.Column(db.Integer, db.ForeignKey('device.id'),
                          nullable=False)

    def __json__(self):
        return ['id', 'lon', 'lat', 'battery_voltage', 'battery_percentage', 'timestamp']


class DeviceSettings(db.Model):
    """ Stores device settings """
    id = db.Column(db.Integer, primary_key=True)
    update_interval = db.Column(db.Integer, nullable=False, default=3600)

    device_id = db.Column(db.Integer, db.ForeignKey('device.id'),
                          nullable=False)

    def __json__(self):
        return ['update_interval']


class User(db.Model):
    """ Stores user data """
    id = db.Column(UUIDType, primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(EmailType, nullable=False, unique=True)
    verified = db.Column(db.Boolean, nullable=False, default=False)

    devices = db.relationship('Device', backref='user', lazy=True)


@click.command("init-db")
@with_appcontext
def init_db():
    db.create_all()


@click.command("wipe-db")
@with_appcontext
def wipe_db():
    db.drop_all()
