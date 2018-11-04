# HELLA IMPORTSSSSS
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import struct
from scipy.fftpack import fft
import sys
import time

# Arduino Stuff
import serial
import time
PORT = "COM3"
RATE = 9600

# PLOT AESTHETIC

plt.style.use('dark_background')
DIVERSITY = 0


ser = serial.Serial(PORT, RATE)

# OOP IN PYTHON , LET'S GO!

class AudioStream(object):

    def __init__(self):

        # The Mic. is used to Grab Soundwaves   

        # "Hyperparameters"
        self.CHUNK = 1024*2                 # Soundwaves are split into 2048 "frames"
        self.FORMAT = pyaudio.paInt16       # Each "frame" has 16-bit precision
        self.CHANNELS = 1                   # Audio is obtained from 1 Channel (Mic) 
        self.RATE = 44100                   # 44,100 FPS (Hz)
        self.pause = False    

        self.p = pyaudio.PyAudio()          # 'p' is our *main* audio-object
  
        # Open Microphone per "Hyperparameters"
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )
        self.init_plots()
        self.start_plot()


        ''' 
        Our Program plots 2 Functions:
            (A) Raw Sound Signal                                > processed from Mic
            (B) Frequency/Volume (Spectrum Analyzer)            > Fourier-Transform of (A)
        '''

    # PLOT SETUP

    def init_plots(self):

        # Each Plot has Unique DOMAIN (set of x's) 
        domainSignal = np.arange(0, 2 * self.CHUNK, 2)      # [0 , 2, 4 ... 4092 , 4094]
        domainFft = np.linspace(0, self.RATE, self.CHUNK)   # [0.00000000e+00 2.15437225e+01 4.30874450e+01 ... 4.40569126e+04 4.40784563e+04 4.41000000e+04]

        # 2 Plots are Drawn on same CANVAS
        self.fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 7))
        self.fig.canvas.mpl_connect('button_press_event', self.onClick)
        # Initialize the 2 Plots (no data yet)
        self.lineSignal, = ax1.plot(domainSignal, np.random.rand(self.CHUNK), '-', lw=2)
        self.lineFft, = ax2.semilogx(domainFft, np.random.rand(self.CHUNK), '-', lw=2)      # "semilogx" morphs x-axis (freq.) to log-scale

        # GRAPH LABELS
        ax1.set_title('SOUND SIGNAL')
        ax1.set_xlabel('TIME'); ax1.set_ylabel('VOL.')
        ax1.set_ylim(0, 255); ax1.set_xlim(0, 2 * self.CHUNK)

        ax2.set_title('SPECTRUM ANALYZER')
        ax2.set_xlabel('FREQ.'); ax2.set_ylabel('VOL.')
        ax1.set_ylim(0, 255); ax1.set_xlim(0, 2 * self.CHUNK)

        plt.setp(ax1, yticks=[0, 128, 255],xticks=[0, self.CHUNK, 2 * self.CHUNK])
        plt.setp(ax2, yticks=[0, 1],); ax2.set_xlim(20, self.RATE / 2)
        # show axes ??????????????????????????????????????????????????????
        thismanager = plt.get_current_fig_manager()
        thismanager.window.setGeometry(5, 120, 1910, 1070)
        plt.show(block=False)


    # DATA PROCESSING

    def start_plot(self):


        global DIVERSITY, ser

        # Avg.FPS = #Frames/Total-Time
        print('stream started')
        frameCount = 0; startTime = time.time()


        # Begin Reading Data
        numIntervals = 8                    # must be divisor of 2048: 1, 2, 4, 8, 16, 32, 64, etc.
        stats = [0]*numIntervals            # track instances of each color-interval 

        while not self.pause:

            # DIVERSIFY FREQ. 
            if(frameCount % 2 == 0):
                DIVERSITY += 1
            if(DIVERSITY == numIntervals):
                DIVERSITY = 0

            #  ................... SIGNAL PROCESSING .....................

            # Obtain a Raw Sound Signal from Mic. (Data = Binary)
            dataBin = self.stream.read(self.CHUNK) # array of y-values (binary)
            dataInt = struct.unpack(str(2 * self.CHUNK) + 'B', dataBin)             # time-ordered list of volume for frequencies
            dataNp = np.array(dataInt, dtype='b')[::2] + 128
            self.lineSignal.set_ydata(dataNp) # Our Plot can take Data as a Np Array
        
            # Perform SIGNAL PROCESSING on Raw to get Freq. Spectrum
            yf = fft(dataInt) # fft = fast fourier transform
            self.lineFft.set_ydata(np.abs(yf[0:self.CHUNK]) / (128 * self.CHUNK))


            #  ................... RGB ENCODING .....................

            # COLOR INTERVALS: Frquency-Range is Split into 8 Intervals (8 Colors)
            colorIntervals = np.split(np.abs(yf[0:self.CHUNK]) / (128 * self.CHUNK), numIntervals, 0)    # [ interval-0 , interval-1 ... interval-7 ]
            intervalVals = [0]*numIntervals;

            # MOST PROMINENT INTERVAL in SIGNAL: its color is sent to the Arduino to rep the whole signal
            RGB = [ 0 , 0 ]             # Output Var : [index of colorInterval, total volume] 
            i = 0

            # Finding the Most Prominenent Freq. Interval
            for colorInterval in colorIntervals:
                # Find Prominence of Interval
                sumVolume = 0
                for frame in colorInterval:
                    sumVolume += frame
                intervalVals[i] = int(sumVolume)
                # Update the Most Prominent Interval
                if(sumVolume > RGB[1] and i != 0):
                    RGB[1] = int(sumVolume)               # increment every X-Frames
                    RGB[0] = i - DIVERSITY
                i += 1  # index of interval we're processing

                

            # np.delete(colorIntervals, RGB[0])
            # np.delete(intervalVals, RGB[0])
            # i=0

            # for colorInterval in colorIntervals:
            #     # Find Prominence of Interval
            #     sumVolume = 0
            #     for frame in colorInterval:
            #         sumVolume += frame
            #     intervalVals[i] = int(sumVolume)
            #     # Update the Most Prominent Interval
            #     if(sumVolume > RGB[1] and i != 0):
            #         RGB[1] = int(sumVolume)               # increment every X-Frames
            #         RGB[0] = i - 0
            #     i += 1  # index of interval we're processing


            #  ....................... TERMINAL OUTPUT .........................

            # RGB Interval Stats


            print(" FRAME #", frameCount, " | FPS:", int(frameCount / (time.time() - startTime)), "\n ---------------------\n")
            stats[RGB[0]] += 1
            print(" [R, G, B, V, O, P, Y, M]")
            print("", stats, "\n")
            print(" RGB:", RGB)
            print(" Intrv Vol.:", intervalVals, "\n\n\n")


            #  ....................... ARDUINO OUTPUT .........................
            outputString = ""
            outputString += str(RGB[0]) + str(RGB[-1])
            ser.write(outputString.encode())

            #  ....................... PLOT DATA ...............................

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            frameCount += 1

        else:
            self.fr = frameCount / (time.time() - startTime) # Avg.FPS = #Frames/Total-Time
            print('average frame rate = {:.0f} FPS'.format(self.fr))
            self.exit_app()



    def exit_app(self):
        print('stream closed')
        self.p.close(self.stream)

    def onClick(self, event):
        self.pause = True



if __name__ == '__main__': # INSTANTIATE BOIS1
    AudioStream()