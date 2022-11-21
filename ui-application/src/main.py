from app import App
import serial

if __name__ == "__main__":
    s = serial.Serial('COM3', 9600, timeout=1)
    app = App(s, "../data/exports/data_60s", 60)
    app.mainloop()