import uuid

devices = []


def get_device_names():
    return [device.name for device in devices]


def get_device(name):
    for device in devices:
        if device.name == name:
            return device


class Device():
    def __init__(self, name):
        self.name = name
        self.data = DeviceData()
        self.settings = DeviceSettings()
        self.auth = DeviceAuth()


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
        self.api_key = uuid.uuid4()
