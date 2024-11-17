import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, heart_rates):
        self.heart_rates = heart_rates

    def plot(self):
        plt.ion()  # Turn on interactive mode for real-time plotting
        fig, ax = plt.subplots()
        ax.set_xlabel('Time')
        ax.set_ylabel('Heart Rate')
        line, = ax.plot(self.heart_rates, label='Heart Rate', color='b')

        while True:
            if self.heart_rates:
                # Update plot with new data every loop
                line.set_ydata(self.heart_rates)
                line.set_xdata(range(len(self.heart_rates)))
                plt.draw()
                plt.pause(0.1)
