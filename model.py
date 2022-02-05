

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
        self.lat = None
        self.lon = None
        self.battery_voltage = None
        self.battery_percentage = None
