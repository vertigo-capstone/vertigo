import time
import threading
from serial_reader import SerialReader
from plotter import Plotter

# Set up SerialReader and Plotter
serial_reader = SerialReader('/dev/ttyUSB0')  # Update to match your system's port
plotter = Plotter(serial_reader.heart_rates)

def read_data():
    while True:
        lat, lon, heart_rate = serial_reader.read_data()
        print(f"Latitude: {lat}, Longitude: {lon}, Heart Rate: {heart_rate}")

def plot_data():
    plotter.plot()

if __name__ == "__main__":
    # Start the serial reading and plotting in separate threads
    plot_thread = threading.Thread(target=plot_data)
    plot_thread.start()

    read_thread = threading.Thread(target=read_data)
    read_thread.start()

    # Keep the main program running
    read_thread.join()
    plot_thread.join()
