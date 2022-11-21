import numpy as np
from pandas import DataFrame, Series
from threading import Thread

class UpdateResults(Thread):
    def __init__(self, app):
        super().__init__()

        self.app = app
        self.s = app.s
        self.show_message = app.show_message
        self.highlight_box = app.highlight_box
        self.gestures = app.gestures

    def run(self):
        sensor_readings, i = np.zeros((len(self.gestures))), 0
        while self.app.listen:
            data = self.s.readline().decode().strip().split()
            if data != []:
                try:
                    sensor_readings[i] = float(data[1])
                except:
                    pass
                i += 1
            else:
                index = sensor_readings.argmax()
                gesture = self.gestures[index]
                self.show_message(gesture)
                self.highlight_box(index)
                sensor_readings, i = np.zeros((len(self.gestures))), 0

class CollectData(Thread):
    def __init__(self, app):
        super().__init__()

        self.readLine = app.readLine
        self.show_message = app.show_message
        self.gestures = app.gestures
        self.data_export_path = app.data_export_path
        self.highlight_box = app.highlight_box
        self.export_duration = app.export_duration

    def run(self):
        sensor_step = self.readLine()
        self.show_message("WAITING FOR ARDUINO")
        while sensor_step[0] != "# 1": #wait till it is a begining
            sensor_step = self.readLine()

        columns = ["aX", "aY", "aZ", "gX", "gY", "gZ"]
        for i, gesture in enumerate(self.gestures):
            df = DataFrame(columns=columns)

            self.highlight_box(i, "gray")
            while sensor_step[0][0] == "#":
                if sensor_step[0][1] == " ":
                    self.show_message(f"READY FOR {gesture} in {sensor_step[0][2]}")
                sensor_step = self.readLine()
                
            self.highlight_box(i, "yellow")
            self.show_message(f"START {gesture} ({self.export_duration}s)")
            sensor_step_float = tuple(map(float, sensor_step))
            df = df.append(Series(sensor_step_float, index=columns),ignore_index=True)
            while True:
                sensor_step = self.readLine()
                if sensor_step[0][0] == "#": break
                sensor_step_float = tuple(map(float, sensor_step))
                df = df.append(Series(sensor_step_float, index=columns),ignore_index=True)

            self.show_message(f"STOP {gesture}")
            df.to_csv(f"{self.data_export_path}/{gesture}.csv", index=False)
            
        self.highlight_box(i, "white")
        self.show_message(f"DONE!")