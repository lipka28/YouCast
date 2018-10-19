from tkinter import *
import threading
import manageCast
import time


class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.master.title("YouCast")
        select_frame = Frame(frame)
        frame['height'] = 600
        frame['width'] = 800
        frame.pack_propagate(0)
        frame.pack()
        select_frame.pack(side=TOP)

        self.cast_manager = manageCast.castDevice()

        self.device_selector = Listbox(select_frame)
        self.device_selector.pack(side=LEFT)

        self.search_button = Button(
            select_frame, text="Search for cast devices", command=self.list_cast_devices
            )
        self.search_button.pack(side=LEFT)

        self.hi_there = Button(select_frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print ("hi there, everyone!")

    def list_cast_devices(self):
        self.search_button['state'] = DISABLED
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

        self.search_button['state'] = ACTIVE


root = Tk()
app = App(root)
root.mainloop()