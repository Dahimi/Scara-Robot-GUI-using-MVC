from tkinter import filedialog, messagebox
from ViewModule import *
import threading
import os
from tkinter import filedialog, messagebox
import time
import serial
class Model() :
    def __init__(self, view ):
        self.view = view
        self.robotConfiguration =""
        self.ArduinoSerial = ""
        self.isRecording = False
        self.isSysnchronized  = False
        self.isToArduino = False
        self.isToFile = True
        self.readFromFile = False
        self.readDraw = True
        self.penColor = "red"
        self.penSize = 10
        self.points =[]
        self.rappot = 1
        self.isPen = True
        self.isElectromangnet = False
        self.shouldStopAnimation = True
        self.shouldRestartAnimation = False
        self.simulationThread = SimulationThread(self)
        self.simulationThread.daemon = True ;
        self.simulationThread.start()
    def setRobotConfiguration(self, robotConfiguration):
        self.robotConfiguration = robotConfiguration
    def openFile(self, option):
        if option == "import1" :
            os.system(self.robotConfiguration.importFile1)
        elif option == "import2" :
            os.system(self.robotConfiguration.importFile2)
        elif option == "export1":
            os.system(self.robotConfiguration.exportFile1)
        elif option =="export2" :
            os.system(self.robotConfiguration.exportFile2)
    def mouseDragged(self, event):
        point = Point(self.penSize, self.penColor, event.x , event.y)
        self.points.append(point)
        point.toString()
        self.view.paint(point)
        print(len(self.points))
    def restartAnimation(self):
        self.shouldStopAnimation = True
        self.shouldRestartAnimation = True
    def startAnimation(self):
        self.shouldStopAnimation = False
        print (self.shouldStopAnimation)
    def stopAnimation(self):
        self.shouldStopAnimation = True
    def about(self):
        messagebox.showinfo("A propos " , "Ce programme est un simulateur du robot Scara " + self.robotConfiguration.type +"\n\n"
                            +"Ce robot a les dimensions suivantes : * Bras1 : " + str(self.robotConfiguration.arm1) + "* Bras2 : " + str(self.robotConfiguration.arm2)
                            +"\n le port de la carte Arduino est: " + self.robotConfiguration.arduinoPort +
                            "\n le débit de communication est : " + self.robotConfiguration.dataRate)

    def startCommunication(self):
        try :
            self.ArduinoSerial = serial.Serial(self.robotConfiguration.arduinoPort, self.robotConfiguration.dataRate, timeout=1)
            time.sleep(2)
            print("connection est établie")
            return 1
        except serial.SerialException :
            return 0

    def createPoint(self, realPoint):
        x = (realPoint.x / self.rappot + self.view.canvasWidth / 2)
        y =  (self.view.canvasHeight / 2 - realPoint.y / self.rappot )
        return Point(self.penSize, self.penColor, x, y, realPoint.z)
    def createRealPoint(self, point):
        x = (point.x - self.view.canvasWidth/2)*self.rappot
        y = self.rappot * (self.view.canvasHeight /2 - point.y)
        return RealPoint(x, y , point.z )


class Point() :
    def __init__(self, size, color , x , y, z = 0) :
        self.size , self.color , self.x , self.y , self.z = size , color , x , y , z
    def toString(self):
        print("x :", self.x, "  y ", self.y)
class RealPoint():
    def __init__(self, x, y, z=0):
        self.x, self.y, self.z = x, y, z

class SimulationThread(threading.Thread):

    def __init__(self, model):
            threading.Thread.__init__(self)
            self.model = model
    def run(self):
        if self.model.isSysnchronized == False :
            for i in range(10) :
                self.wait()
                iteratedPoints = self.model.points[:]
                self.model.view.clairCanvas()
                for point in iteratedPoints :
                    if self.wait()  == 0:
                        print("quit")
                        break;
                    realPoint = self.model.createRealPoint(point)
                    if self.model.isToFile == True :
                        pass
                    if self.model.isToArduino == True :
                        pass
                    self.model.view.paint(point)
                    time.sleep(0.2)
                self.stopAnimation()
        print("run methods")
    def wait(self):
        while (self.model.shouldStopAnimation == True):
            if self.model.shouldRestartAnimation == True: break
            time.sleep(0.01)
        if self.model.shouldRestartAnimation == True:
            self.model.shouldRestartAnimation = False
            self.model.points = []
            self.model.view.clairCanvas()
            return 0
    def stopAnimation(self):
        self.model.view.animationMenu.entryconfig("Lancer l'animation", state="normal")
        self.model.view.animationMenu.entryconfig("Arrêter l'animation", state="disabled")
        self.model.view.animationMenu.entryconfig("Réinitialiser l'animation", state="normal")
        self.model.view.runButton["state"] = "normal"
        self.model.view.stopButton["state"] = "disabled"
        self.model.view.restartButton["state"] = "normal"
        self.model.stopAnimation()