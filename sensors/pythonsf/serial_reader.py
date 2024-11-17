import serial

class SerialReader:
    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.port, self.baud_rate)
        self.heart_rates = []

    def read_data(self):
        while True:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                try:
                    parts = line.split(" , ")
                    lat = parts[0].split(":")[1].strip()
                    lon = parts[1].split(":")[1].strip()
                    heart_rate = int(parts[2].split(":")[1].strip())
                    self.heart_rates.append(heart_rate)
                    return lat, lon, heart_rate
                except IndexError:
                    print("Error parsing data.")
