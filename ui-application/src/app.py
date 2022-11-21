from PIL import Image, ImageTk
from tkinter.ttk import Button
from tkinter import Tk, BOTTOM, LEFT, RIGHT, Label, Frame

from threadObjects import CollectData, UpdateResults

class App(Tk):  
    def __init__(self, s, data_export_path, export_duration):
        super().__init__()
        framePaddings = {'padx': 10, 'pady': 10}
        paddings = {'padx': 5, 'pady': 5}
        box_size = 200
        img_size = 200
        classFrame = Frame(self)
        classFrame.pack(**framePaddings)
        gestures = [
            "rub_palms",
            "palm_over_dorsum_left",
            "palm_over_dorsum_right",
            "palm_to_palm_fingers",
            "fingers_interlocked",
            "thumb_rub_left",
            "thumb_rub_right",
            "palms_with_fingers_left",
            "palms_with_fingers_right",
            "misc",
        ]
        boxes = []
        for i in range(len(gestures)//2):
            gesture1, gesture2 = gestures[i*2], gestures[i*2+1]

            image1 = Image.open(f"./img/{gesture1}.jpg").resize((img_size, img_size))
            image1 = ImageTk.PhotoImage(image1)
            box1 = Label(classFrame, image=image1, text=gesture1, font=('Times 12'), width=box_size, height=box_size, compound='center')
            box1.image=image1
            box1.grid(column=i+1, row=1, **paddings)
            
            image2 = Image.open(f"./img/{gesture2}.jpg").resize((img_size, img_size))
            image2 = ImageTk.PhotoImage(image2)
            box2 = Label(classFrame, text=gesture2, image=image2, font=('Times 12'), width=box_size, height=box_size, compound='center')
            box2.image=image2
            box2.grid(column=i+1, row=2, **paddings)
            boxes.extend([box1, box2])

        notificationFrame = Frame(self)
        notificationFrame.pack(**paddings)
        notificationLabel = Label(notificationFrame)
        notificationLabel.pack(**paddings)

        resultsFrame = Frame(self)
        resultsFrame.pack(**framePaddings)

        buttonFrame = Frame(self)
        buttonFrame.pack(side = BOTTOM, **framePaddings)
        collectDataBtn = Button(buttonFrame, text="Collect data", command=self.collect_data)
        collectDataBtn.pack(side = LEFT)
        listenBtn = Button(buttonFrame, text="Listen", command=self.listen)
        listenBtn.pack(side = LEFT)
        closeBtn = Button(buttonFrame, text="Close", command=self.destroy)
        closeBtn.pack(side = RIGHT)

        self.boxes = boxes
        self.listen = False
        self.collect_data = False
        self.s = s
        self.export_duration = export_duration
        self.gestures = gestures
        self.notificationLabel = notificationLabel
        self.data_export_path = data_export_path

    def readLine(self):
        sensor_step = self.s.readline().decode().strip().split(",")
        return sensor_step
    
    def collect_data(self):
        self.collect_data = not self.collect_data
        collect_data_thread = CollectData(self)
        collect_data_thread.start()

    def listen(self):
        self.listen = not self.listen
        update_results_thread = UpdateResults(self)
        update_results_thread.start()

    def highlight_box(self, index, color="yellow"):
        for image_box in self.boxes:
            image_box.config(background="white")
        selected_image_box = self.boxes[index]
        selected_image_box.config(background=color)

    def show_error(self, message):
        self.notificationLabel.configure(text=message, background="pink")

    def show_message(self, message):
        self.notificationLabel.configure(text=message, background="white")

    def destroy(self):
        self.s.close()
        super().destroy()