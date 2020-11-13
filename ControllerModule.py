
import win32api
from  ViewModule  import View
from tkinter import filedialog, messagebox
import time
class Controller() :

    def __init__(self ):
        self.view = View(self)
        print("view is created")
        self.model
        self.isRecording = False
        self.runSimulator()
    def runSimulator(self):
        self.view.initializeMainWindow()
    def setModel(self, view):
        self.model = Model(view )
    def setRobotConfiguration(self, robotConfiguration):
        self.model.setRobotConfiguration(robotConfiguration)
    def startCommunication(self):
        return self.model.startCommunication()
    def openFile(self, option ):
        self.model.openFile(option)
    def recordAnimation(self):
        self.view.recordButton["state"] = "disabled"
        self.view.stopRecordButton["state"]  = "normal"
        self.isRecording = True
    def stopRecordAnimation(self):
        self.view.recordButton["state"] = "normal"
        self.view.stopRecordButton["state"] = "disabled"
        self.isRecording = False
    def startAnimation(self):
        self.view.animationMenu.entryconfig("Lancer l'animation", state = "disabled")
        self.view.animationMenu.entryconfig("Arrêter l'animation", state="normal")
        self.view.animationMenu.entryconfig("Réinitialiser l'animation", state="normal")
        self.view.runButton["state"] = "disabled"
        self.view.stopButton["state"] = "normal"
        self.view.restartButton["state"] = "normal"
        self.model.startAnimation()
    def mousePressed(self, event):
        self.mouseDragged(event)
    def mouseExit(self, event):
        if self.isRecording == True:
            if win32api.GetKeyState(0x01) <0 :
                messagebox.showwarning("POSITION IMPOSSIBLE", "\nla position que vous anticipez n'est pas accessible \n \nvous avez dépassé l'espace de travail")
    def mouseDragged(self, event) :
        self.view.XLabel["text"] = str(event.x - self.view.canvasWidth/2)
        self.view.YLabel["text"] = str(self.view.canvasHeight /2 - event.y)
        if self.isRecording == True:
            self.model.mouseDragged(event)
    def stopAnimation(self):
        self.view.animationMenu.entryconfig("Lancer l'animation", state="normal")
        self.view.animationMenu.entryconfig("Arrêter l'animation", state="disabled")
        self.view.animationMenu.entryconfig("Réinitialiser l'animation", state="normal")
        self.view.runButton["state"] = "normal"
        self.view.stopButton["state"] = "disabled"
        self.view.restartButton["state"] = "normal"
        self.model.stopAnimation()
    def restartAnimation(self):
        self.view.animationMenu.entryconfig("Lancer l'animation", state="normal")
        self.view.animationMenu.entryconfig("Arrêter l'animation", state="normal")
        self.view.runButton["state"] = "normal"
        self.view.stopButton["state"] = "normal"
        self.model.restartAnimation()
    def setPenColor(self):
        self.model.penColor = self.view.color.get()
        print(self.model.penColor)
    def setPenSize(self):
        self.model.penSize = self.view.size.get()
        print(self.model.penSize)
    def setShape(self):
        self.view.clairCanvas()
    def file_command(self):
        return
    def about(self):
        self.model.about()
    def setWhereToSend(self):
        self.model.isToFile = True if self.view.isImport.get() == 1 else False
        self.model.isToArduino =True if  self.view.isExport.get() == 1 else False
        print("envoyer vers : arduino " + str(self.model.isToArduino) + " vers fichier " + str(self.model.isToFile))
    def setSource(self):
        self.model.readFromFile = False if self.view.source.get() == "draw" else True
        self.model.readDraw = True if self.view.source.get() == "draw" else False
    def setMove(self):
        self.model.isPen = True if self.view.move.get() == "pen" else False
        self.isElectromangnet =False if self.view.source.get() == "pen" else True
    def setMode(self):
        self.model.isSysnchronized = True if self.view.mode.get() == "direct" else False
        print("mode syncro" + str(self.model.isSysnchronized))
controller = Controller()
