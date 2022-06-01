from distutils.command.config import config
from signal import SIGINT, SIGKILL, SIGTERM, raise_signal, signal
from bluetooth import *
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random 
from tkinter import *
from threading import Thread
from datetime import datetime
import sys
import pyautogui
import pickle
import time




# Data Model

model_filename = "/home/bulut/Documents/test_interface/knn.h5"
knn_model = pickle.load(open(model_filename, 'rb'))

# Main Frame

root = Tk()
root.geometry("1000x600")
root.title('Genero - Signal Interface')
root.state('normal')
root.config(background='#fafafa')

signalValue = [0]

def getElapsedTimeText(time):
    text1 = "Signal Value: "
 
    return text1

l = Label(root, text = getElapsedTimeText(0.0))
l.config(font =("Courier", 14), background='#fafafa')


# Button Functions
recordFlag = [False, False]

def startRecording():
    recordFlag[0] = True    

def discardRecording():

    fullText = """
        Signal Value : 
    """ 
    recordFlag[0] = False    
    l.config(text = fullText)
    data.clear()
    data.append(-1)


# Bluetooth Connection Part

#MAC address of ESP32
addr = "30:C6:F7:2F:7E:B6"
service_matches = find_service( address = addr )

buf_size = 1024;

if len(service_matches) == 0:
    print("couldn't find the SampleServer service =(")
    sys.exit(0)

for s in range(len(service_matches)):
    print("\nservice_matches: [" + str(s) + "]:")
    print(service_matches[s])
    
first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

port=1
print("connecting to \"%s\" on %s, port %s" % (name, host, port))

# Create the client socket
sock=BluetoothSocket(RFCOMM)
sock.connect((host, port))

print("connected")

data = [-1]
totalSec = 80
framePerSec = 25
totalFrame = totalSec * framePerSec

def saveMove(arr, move, path):
    with open(path, "a") as file_object:
        file_object.write(move)
        for value in arr:
            file_object.write(str(value)) 
            file_object.write(",") 
        file_object.write("\n")

def saveDataToFiles():
    now = datetime.now()
    path = "/home/yey/Desktop/test_interface/testFiles/test_" + str(now)
    index1 = 50
    index2 = 100
    index3 = 150
    index4 = 200
    index5 = 250

    padding = 0
    saveMove(data[         padding: index1 + padding], "odak_repeat1:", path)
    saveMove(data[index1 + padding: index2 + padding], "odak_repeat2:", path)
    saveMove(data[index2 + padding: index3 + padding], "odak_repeat3:", path)
    saveMove(data[index3 + padding: index4 + padding], "odak_repeat4:", path)
    saveMove(data[index4 + padding: index5 + padding], "odak_repeat5:", path)

    padding = 250
    saveMove(data[         padding: index1 + padding], "rahat_repeat1:", path)
    saveMove(data[index1 + padding: index2 + padding], "rahat_repeat2:", path)
    saveMove(data[index2 + padding: index3 + padding], "rahat_repeat3:", path)
    saveMove(data[index3 + padding: index4 + padding], "rahat_repeat4:", path)
    saveMove(data[index4 + padding: index5 + padding], "rahat_repeat5:", path)

    padding = 500
    saveMove(data[         padding: index1 + padding], "ackapa_repeat1:", path)
    saveMove(data[index1 + padding: index2 + padding], "ackapa_repeat2:", path)
    saveMove(data[index2 + padding: index3 + padding], "ackapa_repeat3:", path)
    saveMove(data[index3 + padding: index4 + padding], "ackapa_repeat4:", path)
    saveMove(data[index4 + padding: index5 + padding], "ackapa_repeat5:", path)

    padding = 750
    saveMove(data[         padding: index1 + padding], "parmak1_repeat1:", path)
    saveMove(data[index1 + padding: index2 + padding], "parmak1_repeat2:", path)
    saveMove(data[index2 + padding: index3 + padding], "parmak1_repeat3:", path)
    saveMove(data[index3 + padding: index4 + padding], "parmak1_repeat4:", path)
    saveMove(data[index4 + padding: index5 + padding], "parmak1_repeat5:", path)

    padding = 1000
    saveMove(data[         padding: index1 + padding], "parmak2_repeat1:", path)
    saveMove(data[index1 + padding: index2 + padding], "parmak2_repeat2:", path)
    saveMove(data[index2 + padding: index3 + padding], "parmak2_repeat3:", path)
    saveMove(data[index3 + padding: index4 + padding], "parmak2_repeat4:", path)
    saveMove(data[index4 + padding: index5 + padding], "parmak2_repeat5:", path)

    padding = 1250
    saveMove(data[         padding: index1 + padding], "parmak3_repeat1:", path)
    saveMove(data[index1 + padding: index2 + padding], "parmak3_repeat2:", path)
    saveMove(data[index2 + padding: index3 + padding], "parmak3_repeat3:", path)
    saveMove(data[index3 + padding: index4 + padding], "parmak3_repeat4:", path)
    saveMove(data[index4 + padding: index5 + padding], "parmak3_repeat5:", path)

    padding = 1500
    saveMove(data[         padding: index1 + padding], "parmak4_repeat1:", path)
    saveMove(data[index1 + padding: index2 + padding], "parmak4_repeat2:", path)
    saveMove(data[index2 + padding: index3 + padding], "parmak4_repeat3:", path)
    saveMove(data[index3 + padding: index4 + padding], "parmak4_repeat4:", path)
    saveMove(data[index4 + padding: index5 + padding], "parmak4_repeat5:", path)

    padding = 1750
    saveMove(data[         padding: index1 + padding], "parmak5_repeat1:", path)
    saveMove(data[index1 + padding: index2 + padding], "parmak5_repeat2:", path)
    saveMove(data[index2 + padding: index3 + padding], "parmak5_repeat3:", path)
    saveMove(data[index3 + padding: index4 + padding], "parmak5_repeat4:", path)
    saveMove(data[index4 + padding: index5 + padding], "parmak5_repeat5:", path)

def move_hand(prediction):
    if(prediction == 0) :
        pyautogui.press("g")
    if(prediction == 1) :
        pyautogui.press("h")
    if(prediction == 2) :
        pyautogui.press("b")
    if(prediction == 3) :
        pyautogui.press("space")
    if(prediction == 4) :
        pyautogui.press("v")
    if(prediction == 5) :
        pyautogui.press("c")
    if(prediction == 6) :
        pyautogui.press("x")
    if(prediction == 7) :
        pyautogui.press("z")


def rx_and_echo():
    signal_sum = 0
    a = [[]]
    start = time.time() + 10.0
    end = time.time()
    difference = 0
    while True:
        var_data = sock.recv(buf_size)
        if var_data: 
            #data.append(length)
            int_data = int(re.search(r'\d+', str(var_data)).group()) 
            l.config(text = "Signal Value: " + str(int_data))
            signalValue.append(int_data)

            end = time.time()
#
            if(len(signalValue) > 50):
                difference = abs(signalValue[-1] - signalValue[-50])

            if(difference > 25):
                timeDiff = end - start
                if(timeDiff > 5) : 
                    print(timeDiff)
                    pyautogui.press("b")
                    time.sleep(1)
                    pyautogui.press("b")
                    start = time.time()


            #int_data = int(re.search(r'\d+', str(var_data)).group()) 



bt_thread = Thread(target = rx_and_echo)
bt_thread.start()


#ccccccc


# Graphc
xs = []
ys = []

def animate(i, xs, ys, data):
    # Add x and y to lists
    xs.append(i) 
    if(len(data) == 0):
        ys.append(0)
    else:
        ys.append(data[-1])  
    # Limit x and y lists to 20 items
    xs = xs[-200:]
    ys = ys[-200:]

    # Draw x and y lists
    #ax.clear()
    #ax.plot(xs, ys)

    line.set_data(xs, ys)
    ax.set_xlim(i-200, i)

    # Format plot
    plt.title('Frame Index')
    plt.ylabel('Signal Volume')

# Set up plot to call animate() function periodically
#ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=200)
#plt.show()


def exitProgram():
    root.destroy()
    raise_signal(SIGTERM)

# Text



# Graph

style.use('ggplot')
fig = plt.figure(figsize=(10, 4.5), dpi=100)
ax = fig.add_subplot(1, 1, 1)
ax.set_ylim(0, 4000)
line, = ax.plot(ys, xs, 'r')
#ser = serial.Serial('com3', 9600)


# Plotting

plotcanvas = FigureCanvasTkAgg(fig, root)
plotcanvas.get_tk_widget().pack()
ani = animation.FuncAnimation(fig, animate, fargs=(xs,ys, signalValue), interval=40, blit=False)

l.pack(side = LEFT, expand= True)

root.mainloop()