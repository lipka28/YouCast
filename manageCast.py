import pychromecast
import time


class castDevice:

    def __init__(self):
        self.available_devices = None
        self.chosen_device = None
        self.cast = None
        self.cast_media = None

    def find_devices(self):
        self.available_devices = pychromecast.get_chromecasts()

    def get_device_list_names(self):
        names = []

        for cc in self.available_devices:
            names.append(cc.device.friendly_name)

        return names

    def choose_casting_device(self):
        self.cast = next(cc for cc in self.available_devices if cc.device.friendly_name == self.chosen_device)
        self.cast.wait()
        self.cast_media = self.cast.media_controller
        print(self.cast.device)

    def play_media(self):

        self.cast_media.play_media('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4', 'video/mp4')

    def stop_casting(self):
        self.cast_media.play_media('','')

    def pause(self):
        self.cast_media.pause()

    def resume(self):
        self.cast_media.play()
