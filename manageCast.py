import pychromecast
from pychromecast.controllers.youtube import YouTubeController
import youtube_dl
import time

def convert_to_list(whatever):
    list = []
    for thing in whatever:
        list.append(thing)

    return  list

class castDevice:

    def __init__(self):
        self.available_devices = None
        self.chosen_device = None
        self.cast = None
        self.cast_media = None
        self.video = None
        self.youtube_controler = YouTubeController()
        self.ydl_opts = {
            'noplaylist': True,
        }

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
        self.cast.register_handler(self.youtube_controler)
        print(self.cast.device)

    def play_media(self, search_query):
        search = list(search_query)
        for i in range(len(search)):
            if search[i] == ' ':
                search[i] = '+'

        search = "".join(search)
        target_url = "https://www.youtube.com/results?search_query={}&page=1".format(search)

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydownloader:
            ytdata = ydownloader.extract_info(target_url,download=False)
            self.video=convert_to_list(ytdata['entries'])[0]['id']
            print(self.video)

        self.youtube_controler.play_video(self.video)

    def stop_casting(self):
        self.cast_media.play_media(' ', ' ')

    def pause(self):
        self.cast_media.pause()

    def resume(self):
        self.cast_media.play()
