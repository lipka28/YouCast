from tkinter import *
import threading
import manageCast
import time


class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.master.title("YouCast")
        frame.pack()

        self.yc_state = IntVar()

        select_frame = Frame(frame)
        select_frame.pack(side=TOP)
        search_area = Frame(frame)
        search_area.pack(side=TOP)
        media_buttons = Frame(frame)
        select_frame.pack(side=TOP)

        self.cast_manager = manageCast.castDevice()
        self.device_selector = Listbox(select_frame)
        self.device_selector.pack(side=LEFT)

        self.search_button = Button(select_frame, text="Search for cast devices", command=self.list_cast_devices)
        self.search_button.pack(side=LEFT)

        self.btn_select = Button(select_frame, text="Select Device", command=self.choose_device)
        self.btn_select.pack(side=LEFT)

        self.youtube_check = Checkbutton(search_area, text="Youtube search", variable=self.yc_state)
        self.youtube_check.pack(side=LEFT)

        self.txt_url = Entry(search_area)
        self.txt_url['width'] = 50
        self.txt_url.insert(0, "What you want?")
        self.txt_url.pack(side=LEFT)

        media_buttons.pack(side=TOP)
        self.btn_play = Button(media_buttons, text="Play new video", command=self.play_url)
        self.btn_play.pack(side=LEFT)

        self.btn_ytadd = Button(media_buttons, text="Add to Youtube playlist", command=self.play_next)
        self.btn_ytadd.pack(side=LEFT)

        self.btn_stop = Button(media_buttons, text="Stop", command=self.cast_manager.stop_casting)
        self.btn_stop.pack(side=LEFT)

        self.btn_stop = Button(media_buttons, text="Pause", command=self.cast_manager.pause)
        self.btn_stop.pack(side=LEFT)

        self.btn_stop = Button(media_buttons, text="Resume", command=self.cast_manager.resume)
        self.btn_stop.pack(side=LEFT)

    def choose_device(self):
        self.cast_manager.chosen_device = self.device_selector.selection_get()
        self.cast_manager.choose_casting_device()

    def list_cast_devices(self):
        self.search_button['state'] = DISABLED
        self.search_button['text'] = "Searching..."
        self.device_selector.delete(0, END)
        workerThred = threading.Thread(target=self.cast_manager.find_devices, args=(), kwargs={})
        workerThred.start()
        checkingThread = threading.Thread(target=self.list_results_when_ready, args=([workerThred]), kwargs={})
        checkingThread.start()

    def list_results_when_ready(self, child):
        child.join()
        deviceList = self.cast_manager.get_device_list_names()
        for device in deviceList:
            self.device_selector.insert(END, device)

        self.search_button['text'] = "Search for cast devices"
        self.search_button['state'] = ACTIVE

    def play_url(self):
        if self.yc_state.get() == 1:
            workerThred = threading.Thread(target=self.cast_manager.play_on_youtube, args=([self.txt_url.get()]), kwargs={})
            workerThred.start()
        else:
            self.cast_manager.simple_play(self.txt_url.get())

    def play_next(self):
        workerThred = threading.Thread(target=self.cast_manager.add_to_playlist, args=([self.txt_url.get()]), kwargs={})
        workerThred.start()


root = Tk()
app = App(root)
root.mainloop()
