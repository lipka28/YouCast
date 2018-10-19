import pychromecast


class castDevice:

    def __init__(self):
        self.available_devices = None
        self.chosen_device = None

    def find_devices(self):
        self.available_devices = pychromecast.get_chromecasts()

    def get_device_list_names(self):
        names = []

        for cc in self.available_devices:
            names.append(cc.device.friendly_name)

        return names
