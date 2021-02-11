import threading
import os
import win32api
from DialogWindow import *
from tkinter import *
import tkinter.font as font
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import filedialog, messagebox
import time
import serial
from math import *
class View() :
    def __init__(self, controller):
        self.controller = controller
        self.canvasHeight = 600
        self.animationMenu = self.root =  self.canvasWidth = self.dialogWindow = self.isExport = self.isImport = self.theta1 = self.theta2 = " "
        self.mainPannel = self.workspace = self.workspacePanel = self.XLabel = self.YLabel = self.stopRecordImage = self.recordImage = self.stopImage = self.runImage = " "
        self.mode = self.source = self.shape = self.temperature1 = self.temperature2 = self.vitesse1 = self.vitesse2 = self.h = " "
        self.runButton = self.stopButton= self.restartButton = self.color = self.shape = self.size =" "
        self.robotDraw = self.elbow = self.center = self.effectiveWorkspace= self.bannedZone =self.takeY = self.takeX = " "
        controller.setModel(self)
        print("model created")
        #self.initializeMainWindow()
    def initializeMainWindow(self):
        self.root = Tk()
        if self.setDialogWindow() == 1 :
            self.initializeMenu()
            self.initializeToolBar()
            self.setMainPannel()
            self.setStatusBar()
            mainloop()
        else :
            self.root.quit()

    def setDialogWindow(self):
        self.root.title("title")
        self.root.geometry('600x650')
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry("%dx%d" % (self.w, self.h))
        self.root.bind("<F11>", lambda event: self.root.attributes("-fullscreen",
                                                                   not self.root.attributes("-fullscreen")))
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        self.dialogWindow = DialogWindow(self)
        self.root.withdraw()
        self.root.wait_window(self.dialogWindow)
        if self.dialogWindow.responce == -1 :
            return -1
        self.root.update()
        self.root.deiconify()
        return 1
    def initializeMenu(self):
        menuBar = Menu(self.root)
        self.root.config(menu=menuBar)
        # create menuItem
        # file menu
        file_menu = Menu(menuBar, tearoff = False)
        menuBar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau", command=self.newWindow)
        openFile = Menu(file_menu, tearoff = False)
        file_menu.add_cascade(label = "Ouvrir fichier ...", menu = openFile)
        openFile.add_command(label = "Fichier importé 1", command = lambda : self.controller.openFile("import1"))
        openFile.add_command(label="Fichier importé 2", command=lambda : self.controller.openFile("import2"))
        openFile.add_command(label="Fichier exporté 1", command=lambda : self.controller.openFile("export1"))
        openFile.add_command(label="Fichier exporté 2", command=lambda : self.controller.openFile("export2"))
        def quit():
            self.root.quit()
        file_menu.add_command(label="Exit", command=quit)

        # animation menu
        self.animationMenu = Menu(menuBar, tearoff = False)
        menuBar.add_cascade(label="Commande", menu=self.animationMenu)
        self.animationMenu.add_command(label="Lancer l'animation", command=self.controller.startAnimation)
        self.animationMenu.add_separator()
        self.animationMenu.add_command(label="Arrêter l'animation", command=self.controller.stopAnimation)
        self.animationMenu.add_separator()
        self.animationMenu.add_command(label="Réinitialiser l'animation", command=self.controller.restartAnimation)
        # edit menu
        editMenu = Menu(menuBar , tearoff = False)
        menuBar.add_cascade(label="Editer", menu=editMenu)
        colorMenu = Menu(editMenu, tearoff = False)
        editMenu.add_cascade(label = "changer la couleur du pinceau" , menu = colorMenu)
        self.color = StringVar()
        self.color.set("red")
        colorMenu.add_radiobutton(label="Rouge", value="red", variable=self.color, command=self.controller.setPenColor)
        colorMenu.add_radiobutton(label="Bleu", value="blue", variable=self.color, command=self.controller.setPenColor)
        colorMenu.add_radiobutton(label="Vert", value="green", variable=self.color, command=self.controller.setPenColor)
        editMenu.add_separator()
        sizeMenu = Menu(editMenu, tearoff=False)
        editMenu.add_cascade(label="changer la taille du pinceau", menu=sizeMenu)
        self.size = IntVar()
        self.color.set(4)
        sizeMenu.add_radiobutton(label="   2   ", value=2, variable=self.size, command=self.controller.setPenSize)
        sizeMenu.add_radiobutton(label="   4   ", value= 4, variable=self.size, command=self.controller.setPenSize)
        sizeMenu.add_radiobutton(label="   10  ", value=10, variable=self.size, command=self.controller.setPenSize)

        # shape menu
        shapeMenu = Menu(menuBar, tearoff = False)
        menuBar.add_cascade(label="Formes", menu=shapeMenu)
        shapeSubMenu = Menu(shapeMenu)
        shapeMenu.add_cascade(label="choisir la forme", menu=shapeSubMenu)
        self.shape = StringVar()
        shapeSubMenu.add_radiobutton(label="Carré", value="square", variable=self.shape, command=self.controller.setShape)
        shapeSubMenu.add_radiobutton(label="Triangle", value="triangle", variable=self.shape, command=self.controller.setShape)
        shapeSubMenu.add_radiobutton(label="Circle", value="circle", variable=self.shape, command=self.controller.setShape)
        # about
        aboutMenu = Menu(menuBar)
        menuBar.add_cascade(label="A propos", menu=aboutMenu)
        aboutMenu.add_command(label="scara Robot Simulator" , command = self.controller.about)
    def initializeToolBar(self):
        self.runImage = PhotoImage(file = 'run.png')
        self.stopImage = PhotoImage(file = 'stop.png')
        self.recordImage = ImageTk.PhotoImage(Image.open("record.png").resize((34, 28),Image.ANTIALIAS))
        self.stopRecordImage = ImageTk.PhotoImage(Image.open("stopreco.png").resize((34, 28), Image.ANTIALIAS))
        self.restartImage = ImageTk.PhotoImage(Image.open("restart.png").resize((34, 28), Image.ANTIALIAS))
        def _from_rgb(rgb):
            """translates an rgb tuple of int to a tkinter friendly color code
            """
            return "#%02x%02x%02x" % rgb
        toolbar = Frame (self.root, bg = _from_rgb((233,233, 233)))
        self.runButton = Button(toolbar, padx = 10 , pady = 3, image = self.runImage, borderwidth =0 , command =self.controller.startAnimation)
        self.runButton.pack(side = LEFT , padx = 4, pady= 2)
        self.stopButton = Button(toolbar, padx=10, pady=3, image=self.stopImage, borderwidth=0, command=self.controller.stopAnimation)
        self.stopButton.pack(side=LEFT, padx=4, pady=2)
        self.restartButton = Button(toolbar, padx=10, pady=3, image=self.restartImage, borderwidth=0, command=self.controller.restartAnimation)
        self.restartButton.pack(side=LEFT, padx=4, pady=2)
        self.recordButton = Button(toolbar, padx=10, pady=3, image=self.recordImage, borderwidth=0, command=self.controller.recordAnimation)
        self.recordButton.pack(side=LEFT, padx=4, pady=2)
        self.stopRecordButton = Button(toolbar, padx=10, pady=3, image=self.stopRecordImage, borderwidth=0, command=self.controller.stopRecordAnimation)
        self.stopRecordButton.pack(side=LEFT, padx=4, pady=2)
        self.stopRecordButton["state"] = "disabled"
        Label(toolbar,bg = _from_rgb((233,233, 233)),  text = "       ").pack(side = LEFT)
        Button(toolbar, padx=10, pady=3, bg = 'red', borderwidth=0,command= lambda  : self.setPenColor("red")).pack(side=LEFT, padx=8, pady=2)
        Button(toolbar, padx=10, pady=3, bg='blue', borderwidth=0, command=lambda  :self.setPenColor("blue")).pack(side=LEFT, padx=8,  pady=2)
        Button(toolbar, padx=10, pady=3, bg='green', borderwidth=0, command=lambda  :self.setPenColor("green")).pack(side=LEFT, padx=8,pady=2)
        self.stopButton["state"] = 'disabled'
        #toolbar.grid(row  = 0, column= 0 , columnspan = 3 , sticky = W + E )
        toolbar.pack(side=TOP, fill=X)
    def setMainPannel(self):
        self.mainPannel = LabelFrame(self.root, bg = 'black' , width =  400)
        self.mainPannel.pack(fill=BOTH,expand = 1)
        self.setExternalPannel()
        self.setWorkspace()
        self.setRobotStatePanel()
        return
    def setRobotStatePanel(self):
        workspacePanel = LabelFrame(self.mainPannel, text="Etat du Robot", width = 400,height=400, padx=10, pady=10)
        self.theta1 = Label(workspacePanel, width="15", bd=1, relief=SUNKEN)
        self.theta1.grid(row = 0 , column = 1, padx=4, pady=6)
        Label(workspacePanel, text="L'angle Theta1 : ").grid(row = 0 , column = 0, padx=4, pady=6)
        self.theta2= Label(workspacePanel, width="15", bd=1, relief=SUNKEN)
        self.theta2.grid(row = 1 , column = 1, padx=4, pady=6)
        Label(workspacePanel, text="L'angel Theta2 : ").grid(row = 1 , column = 0, padx=4, pady=6)
        self.temperature1 = Label(workspacePanel, width="15", bd=1, relief=SUNKEN)
        self.temperature1.grid(row=2, column=1, padx=4, pady=6)
        Label(workspacePanel, text="La température du moteur 1: ").grid(row=2, column=0, padx=4, pady=6)
        self.temperature2 = Label(workspacePanel, width="15", bd=1, relief=SUNKEN)
        self.temperature2.grid(row=3, column=1, padx=4, pady=6)
        Label(workspacePanel, text="La température du moteur 2 : ").grid(row=3, column=0, padx=4, pady=6)
        self.vitesse1 = Label(workspacePanel, width="15", bd=1, relief=SUNKEN)
        self.vitesse1.grid(row=4, column=1, padx=4, pady=6)
        Label(workspacePanel, text="La vitesse du moteur 1: ").grid(row=4, column=0, padx=4, pady=6)
        self.vitesse2 = Label(workspacePanel, width="15", bd=1, relief=SUNKEN)
        self.vitesse2.grid(row=5, column=1, padx=4, pady=6)
        Label(workspacePanel, text="La vitesse du moteur 2 : ").grid(row=5, column=0, padx=4, pady=6)
        self.realX = Label(workspacePanel, width="15", bd=1, relief=SUNKEN)
        self.realX.grid(row=6, column=1, padx=4, pady=6)
        Label(workspacePanel, text="L'abscisse réel : ").grid(row=6, column=0, padx=4, pady=6)
        self.realY = Label(workspacePanel, width="15", bd=1, relief=SUNKEN)
        self.realY.grid(row=7, column=1, padx=4, pady=6)
        Label(workspacePanel, text="L'ordonné réel : ").grid(row=7, column=0, padx=4, pady=6)
        workspacePanel.pack(side=LEFT, fill=Y)
    def setWorkspace(self):
        self.workspacePanel = LabelFrame(self.mainPannel , text = "Espace de travail",width=630, height=630 , padx = 7 , pady = 7 )
        self.canvasHeight = 600
        self.canvasWidth = 600
        self.controller.setRapport()
        self.workspace = Canvas(self.workspacePanel,width=self.canvasWidth,height=self.canvasHeight, bg = "white")
        self.workspace.create_line(self.canvasWidth /2 ,  0 , self.canvasWidth/2 ,self.canvasHeight , fill="#476042" , width = 3  )
        self.workspace.create_line(0, self.canvasHeight/2, self.canvasWidth , self.canvasHeight/2, fill="#476042",width=3)
        self.makeGrid()
        self.effectiveWorkspace = self.workspace.create_oval(0, 0, self.canvasWidth, self.canvasHeight, dash = (3, 4) , outline = "red")
        self.bannedZone = self.workspace.create_oval(self.canvasWidth /2  - self.controller.getMinRadius(), self.canvasHeight/2  -self.controller.getMinRadius(),
                                                     self.canvasWidth /2  + self.controller.getMinRadius(), self.canvasHeight/2  +self.controller.getMinRadius(), dash=(3, 4),outline="red")
        self.workspace.pack()
        self.workspace.pack_propagate(0)
        self.workspacePanel.pack(fill = Y , side = LEFT)
        self.workspacePanel.pack_propagate(0)
        self.workspace.bind( "<B1-Motion>", self.controller.mouseDragged )
        self.workspace.bind("<Button-1>", self.controller.mousePressed)
        self.workspace.bind("<Leave>", self.controller.mouseExit)

    def makeGrid(self):
        length = self.controller.model.rappot * self.canvasWidth / 2
        realStep = int(int(length / 100) * 10 * 4 / 3)
        step = realStep / self.controller.model.rappot
        i = 1
        self.workspace.create_text(self.canvasWidth / 2 - 9, self.canvasHeight / 2 + 9, text=str(0))
        while step * i < self.canvasWidth / 2:
            self.workspace.create_line(self.canvasWidth / 2 + i * step, self.canvasHeight / 2 - 5,
                                       self.canvasWidth / 2 + i * step, self.canvasHeight / 2 + 5)
            self.workspace.create_line(self.canvasWidth / 2 - i * step, self.canvasHeight / 2 - 5,
                                       self.canvasWidth / 2 - i * step, self.canvasHeight / 2 + 5)
            self.workspace.create_line(self.canvasWidth / 2 - 5, self.canvasHeight / 2 + i * step,
                                       self.canvasWidth / 2 + 5, self.canvasHeight / 2 + i * step)
            self.workspace.create_line(self.canvasWidth / 2 - 5, self.canvasHeight / 2 - i * step,
                                       self.canvasWidth / 2 + 5, self.canvasHeight / 2 - i * step)
            self.workspace.create_text(self.canvasWidth / 2 + i * step, self.canvasHeight / 2 + 12,
                                       text=str(realStep * i))
            self.workspace.create_text(self.canvasWidth / 2 - i * step, self.canvasHeight / 2 + 12,
                                       text=str(-realStep * i))
            self.workspace.create_text(self.canvasWidth / 2 - 18, self.canvasHeight / 2 + i * step,
                                       text=str(-realStep * i))
            self.workspace.create_text(self.canvasWidth / 2 - 15, self.canvasHeight / 2 - i * step,
                                       text=str(realStep * i))
            i = i + 1
        print("printed")

    def paint(self , point):
        python_green = "#476042"
        self.XLabel["text"] = str(point.x - self.canvasWidth / 2)
        self.YLabel["text"] = str(self.canvasHeight / 2 - point.y)
        x1, y1 = (point.x - point.size), (point.y - point.size)
        x2, y2 = (point.x + point.size), (point.y + point.size)
        self.workspace.create_oval(x1, y1, x2, y2, fill=point.color, outline= '')
        # self.controller.mouseDragged(event)
    def setExternalPannel(self):
        externalFrame = LabelFrame(self.mainPannel, text="Les communication externes", width=400, height=400, padx=10,
                                   pady=10)
        Label(externalFrame, text="Le mode de transfert des données : ").grid(row=0, column=1)
        modes = {
            "Mode directe (synchronisé)": "direct",
            "Robot indirecte (non synchronisé) ": "indirect"
        }
        self.mode = StringVar()
        self.mode.set("indirecte")
        i = 0
        for (text, value) in modes.items():
            Radiobutton(externalFrame, text=text, variable=self.mode,
                        value=value , command = self.controller.setMode).grid(row=1, column=2 * i, columnspan=2)
            i = i + 1

        Label(externalFrame, text="La source des données : ").grid(row=2, column=1)
        sources = {
            "Importer du fichier ": "import",
            "Dessiner le chemin ": "draw"
        }
        self.source = StringVar()
        self.source.set("draw")
        i = 0
        for (text, value) in sources.items():
            Radiobutton(externalFrame, text=text, variable=self.source,
                        value=value,command = self.controller.setSource).grid(row=3, column=2 * i, columnspan=2)
            i = i + 1
        Label(externalFrame, text="The end effector is  : ").grid(row=6, column=1)
        move = {
            "Stylo ": "pen",
            "Electroaimant ": "electromagnet"
        }
        self.move = StringVar()
        self.move.set("pen")
        i = 0
        for (text, value) in move.items():
            Radiobutton(externalFrame, text=text, variable=self.move,
                        value=value, command=self.controller.setMove).grid(row=7, column=2 * i, columnspan=2)
            i = i + 1

        Label(externalFrame, text="Envoyer les commandes vers :").grid(row=4, column=1)
        self.isImport = BooleanVar()
        self.isImport.set(True)
        self.isExport = BooleanVar()
        self.isExport.set(False)

        Checkbutton(externalFrame, text="Exporter vers le fichier", variable=self.isImport, onvalue=1, offvalue=0 , command = self.controller.setWhereToSend).grid(
            row=5, column=1)
        Checkbutton(externalFrame, text="Envoyer à l'Arduino", variable=self.isExport, onvalue=1, offvalue=0, command = self.controller.setWhereToSend).grid(
            row=5, column=2)
        #externalFrame.grid(row=0, column=1, columnspan=2, sticky='w')
        pointFrame = LabelFrame(externalFrame, text="Commander un point", padx=10, pady=10)
        Label(pointFrame, text="L'abscisse X : ").grid(row=0, column=0)
        Label(pointFrame, text="L'ordonnée Y':").grid(row=1, column=0)
        Label(pointFrame, text="L'ordonnée Z':").grid(row=2, column=0)
        self.takeX = Entry(pointFrame)
        self.takeY = Entry(pointFrame)
        self.takeZ = Entry(pointFrame)
        self.takeX.grid(row=0, column=1)
        self.takeY.grid(row=1, column=1)
        self.takeZ.grid(row=2, column=1)
        Label(pointFrame, text="").grid(row=3, column=0)
        Button(pointFrame, text= "Saisir" , padx = 5 , pady = 5 , command = self.saisirPoint).grid(row = 4 , column =0 )
        Button(pointFrame, text="Lâcher", padx=5, pady=5, command=self.lacherPoint).grid(row=4, column=1)
        Label(externalFrame, text="").grid(row=8, column=0)
        Label(externalFrame, text="").grid(row=9, column=0)
        Label(externalFrame, text="").grid(row=10, column=0)
        Label(externalFrame, text="").grid(row=11, column=0)
        pointFrame.grid(row=12, column=0, columnspan=2)
        self.recordMvt = BooleanVar()
        self.recordMvt.set(False)
        Checkbutton(externalFrame, text="Enregistrer le mouvement", variable=self.recordMvt, onvalue=1, offvalue=0,
        command=self.controller.isRecordMvt).grid(row=13, column=1)
        externalFrame.pack(fill=Y, side=LEFT)
        externalFrame.pack_propagate(0)

    def saisirPoint(self):
        try :
           x = int( self.takeX.get().strip() )
           y = int(self.takeY.get().strip())
           self.controller.saisirPoint(x, y)
        except ValueError:
            messagebox.showerror("FORMAT NON ACCEPTABLE " , "Vérifiez bien que les coordonnées saisi sont bien des nombres ")

    def lacherPoint(self):
        try:
            x = int(self.takeX.get().strip())
            y = int(self.takeY.get().strip())
            self.controller.lacherPoint(x, y)
        except ValueError:
            messagebox.showerror("FORMAT NON ACCEPTABLE ",
                                 "Vérifiez bien que les coordonnées saisi sont bien des nombres ")

    def setStatusBar(self):
        statusBar = Frame(self.root)
        self.XLabel = Label(statusBar, width="15", bd=1, relief=SUNKEN)
        self.XLabel.pack(side=RIGHT, padx=4, pady=2)
        Label(statusBar, text= "La coordonnées X: ").pack(side = RIGHT , padx = 4, pady = 2)
        self.YLabel = Label(statusBar, width="15", bd=1, relief=SUNKEN)
        self.YLabel.pack(side=RIGHT, padx=4, pady=2)
        Label(statusBar, text="La coordonnées Y: ").pack(side=RIGHT, padx=4, pady=2)
        statusBar.pack(side=BOTTOM, fill=X)
        return
    def _from_rgb(self,rgb):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        return "#%02x%02x%02x" % rgb
    def newWindow(self) :
        self.root.destroy()
        self.initializeMainWindow()
        print("ye")
    def setPenColor(self, color):
        self.color.set(color)
        self.controller.setPenColor()
    def resetRealCoordinates(self, realPoint):
        self.realX["text"] = format(realPoint.x , '.2f')
        self.realY["text"] = format(realPoint.y , '.2f')
        self.theta1["text"] = format(realPoint.theta1*180/pi , '.2f')
        self.theta2["text"] = format(realPoint.theta2 * 180 / pi, '.2f')
    def setRobotState(self, robotState):
        listOfStates = robotState.split(' ')
        self.temperature1["text"] = listOfStates[0]
        self.temperature2["text"] = listOfStates[1]
        self.vitesse1["text"] = listOfStates[2]
        self.vitesse2["text"] = listOfStates[3]
        print(listOfStates[-1])
    def clairCanvas(self):
        self.workspace.delete("all")
        self.bannedZone = self.workspace.create_oval(self.canvasWidth / 2 - self.controller.getMinRadius(),
                                                     self.canvasHeight / 2 - self.controller.getMinRadius(),
                                                     self.canvasWidth / 2 + self.controller.getMinRadius(),
                                                     self.canvasHeight / 2 + self.controller.getMinRadius(),
                                                     dash=(3, 4), outline="red")
        self.workspace.create_line(self.canvasWidth / 2, 0, self.canvasWidth / 2, self.canvasHeight, fill="#476042",width=3)
        self.workspace.create_line(0, self.canvasHeight / 2, self.canvasWidth, self.canvasHeight / 2, fill="#476042",width=3)
        self.makeGrid()
        self.effectiveWorkspace = self.workspace.create_oval(0, 0, self.canvasWidth, self.canvasHeight, dash = (3, 4) , outline = "red")
    def drawRobot(self, point, elbow):
        if self.robotDraw == " ":
            self.robotDraw = self.workspace.create_line(self.canvasWidth/2,self.canvasHeight/2,elbow.x , elbow.y , point.x, point.y,fill= "blue", width = 10 )
            self.elbow = self.workspace.create_oval(elbow.x - 5, elbow.y - 5, elbow.x + 5, elbow.y + 5, fill="black")
            self.center = self.workspace.create_oval(- 7, -7, 7, 7, fill="black")
        else :
            self.workspace.coords(self.robotDraw,self.canvasWidth/2,self.canvasHeight/2,elbow.x , elbow.y , point.x, point.y )
            self.workspace.coords(self.elbow,elbow.x - 7, elbow.y - 7, elbow.x + 7, elbow.y + 7 )
            self.workspace.coords(self.center,self.canvasWidth/2- 10,self.canvasHeight/2 -10,self.canvasWidth/2 +10, self.canvasHeight/2+10)

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
    def getMinRadius(self):
        minRadius = self.model.robotConfiguration.arm1 -self.model.robotConfiguration.arm2
        return  abs(minRadius) / self.model.rappot
    def setRapport(self):
        self.model.setRapport()
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
    def saisirPoint(self , x , y):
        if self.model.isElectromangnet :
            realPoint = RealPoint( "red" ,x , y )
        else : realPoint = RealPoint( self.model.penColor ,x , y )
        point = self.model.createPoint(realPoint)
        if (point.x - self.view.canvasWidth / 2) ** 2 + (point.y - self.view.canvasHeight / 2) ** 2 < (self.getMinRadius()) ** 2 :
            messagebox.showwarning("POSITION IMPOSSIBLE",
                                   "\nla position que vous anticipez n'est pas accessible \n \nvous avez dépassé l'espace de travail")
            return
        if (point.x -self.view.canvasWidth/2)**2 + (point.y- self.view.canvasHeight/2)**2 > (self.view.canvasWidth /2)**2 :
            messagebox.showwarning("POSITION IMPOSSIBLE",
                                   "\nla position que vous anticipez n'est pas accessible \n \nvous avez dépassé l'espace de travail")
            return
        self.model.points.append(point)
        self.view.paint(point)
    def lacherPoint(self, x , y):
        if self.model.isElectromangnet :
            realPoint = RealPoint( "green" ,x , y )
            print(realPoint.color)
        else : realPoint = RealPoint( self.model.penColor ,x , y )
        point = self.model.createPoint(realPoint)
        if (point.x - self.view.canvasWidth / 2) ** 2 + (point.y - self.view.canvasHeight / 2) ** 2 < (
        self.getMinRadius()) ** 2:
            messagebox.showwarning("POSITION IMPOSSIBLE",
                                   "\nla position que vous anticipez n'est pas accessible \n \nvous avez dépassé l'espace de travail")
            return
        if (point.x - self.view.canvasWidth / 2) ** 2 + (point.y - self.view.canvasHeight / 2) ** 2 > (
                self.view.canvasWidth / 2) ** 2:
            messagebox.showwarning("POSITION IMPOSSIBLE",
                                   "\nla position que vous anticipez n'est pas accessible \n \nvous avez dépassé l'espace de travail")
            return
        self.model.points.append(point)
        self.view.paint(point)
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
        if self.isRecording == True:
            if (event.x -self.view.canvasWidth/2)**2 + (event.y- self.view.canvasHeight/2)**2 > (self.view.canvasWidth /2)**2 :
                #messagebox.showwarning("POSITION IMPOSSIBLE","\nla position que vous anticipez n'est pas accessible \n \nvous avez dépassé l'espace de travail")
                return
            if (event.x -self.view.canvasWidth/2)**2 + (event.y- self.view.canvasHeight/2)**2 < (self.getMinRadius())**2 :
                print((event.x -self.view.canvasWidth/2)**2 + (event.y- self.view.canvasHeight/2)**2 )
                print( self.getMinRadius())
                return
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
        if self.view.shape.get() == "circle" :
            self.model.drawCircle()
        elif self.view.shape.get() == "square" :
            self.model.drawSquare()
        elif self.view.shape.get() == 'triangle' :
            self.model.drawTriangle()
    def file_command(self):
        return
    def about(self):
        self.model.about()
    def isRecordMvt(self):
        self.model.recordMouvment = True if self.view.recordMvt.get() == 1 else False
        self.model.startRecordMvt()
    def setWhereToSend(self):
        self.model.isToFile = True if self.view.isImport.get() == 1 else False
        self.model.isToArduino =True if  self.view.isExport.get() == 1 else False
        print("envoyer vers : arduino " + str(self.model.isToArduino) + " vers fichier " + str(self.model.isToFile))
    def setSource(self):
        self.model.readFromFile = False if self.view.source.get() == "draw" else True
        self.model.readDraw = True if self.view.source.get() == "draw" else False
    def setMove(self):
        self.model.isPen = True if self.view.move.get() == "pen" else False
        self.model.isElectromangnet =False if self.view.move.get() == "pen" else True
    def setMode(self):
        self.model.isSysnchronized = True if self.view.mode.get() == "direct" else False
        print("mode syncro" + str(self.model.isSysnchronized))
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
        self.penSize = 0.5
        self.robotSpeed = 80.0
        self.points =[]
        self.rappot = 1
        self.isPen = True
        self.isElectromangnet = False
        self.recordMouvment = False
        self.shouldStopAnimation = True
        self.shouldRestartAnimation = False
        self.simulationThread = SimulationThread(self)
        self.simulationThread.daemon = True ;
        self.simulationThread.start()
        self.recordThread = None
    def setRobotConfiguration(self, robotConfiguration):
        self.robotConfiguration = robotConfiguration
    def setRapport(self):
        self.rappot = (self.robotConfiguration.arm1 + self.robotConfiguration.arm2) / self.view.canvasWidth * 2
    def openFile(self, option):
        if option == "import1" :
            os.system(self.robotConfiguration.importFile1)
        elif option == "import2" :
            os.system(self.robotConfiguration.importFile2)
        elif option == "export1":
            os.system(self.robotConfiguration.exportFile1)
        elif option =="export2" :
            os.system(self.robotConfiguration.exportFile2)

    def startRecordMvt(self):
        self.recordThread = RecordingThread(self)
        self.recordThread.daemon = True;
        self.recordThread.start()
    def mouseDragged(self, event):
        point = Point(self.penSize, self.penColor, event.x , event.y)
        self.points.append(point)
        if self.isSysnchronized == True :
            realPoint = self.createRealPoint(point)
            self.calculateCorrespondingAngles(realPoint)
            theta1 = format(realPoint.theta1 * 180 / pi, '.2f')
            theta2 = format(realPoint.theta2 * 180 / pi, '.2f')
            state = 3
            if realPoint.color == "green" :
                state = 5
            dataToArduino = theta1 + " " + theta2 + " " + str(state) + "\n"
            if self.isToArduino :
                self.startCommunicationWithArduino(dataToArduino)
            print("go to point" + dataToArduino)
            l1 = self.robotConfiguration.arm1
            elbow = RealPoint(realPoint.color, cos(realPoint.theta1) * l1, sin(realPoint.theta1) * l1)
            self.view.drawRobot(point, self.createPoint(elbow))
        self.view.paint(point)
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
            self.ArduinoSerial = serial.Serial(self.robotConfiguration.arduinoPort, self.robotConfiguration.dataRate, timeout=20)
            time.sleep(2)
            print(self.ArduinoSerial.readline().decode("ascii"))
            return 1
        except serial.SerialException :
            return 0

    def createPoint(self, realPoint):
        x = (realPoint.x / self.rappot + self.view.canvasWidth / 2)
        y =  (self.view.canvasHeight / 2 - realPoint.y / self.rappot )
        return Point(self.penSize, realPoint.color, x, y, realPoint.z , realPoint.state)
    def createRealPoint(self, point):
        x = (point.x - self.view.canvasWidth/2)*self.rappot
        y = self.rappot * (self.view.canvasHeight /2 - point.y)
        return RealPoint(point.color,x, y , point.z, point.state)
    def calculateCorrespondingAngles(self, realPoint):
        x, y , l1 , l2= realPoint.x , realPoint.y , self.robotConfiguration.arm1 ,self.robotConfiguration.arm2
        t1 = (x**2 + y**2 - l1**2 - l2**2 )
        t2 = 2*l1*l2
        theta2 = acos(t1/t2)
        theta1 = atan2(y, x ) - atan2(l2 * sin(theta2) , l1 + l2 * cos(theta2))
        if (theta1 >= 0):
            realPoint.theta1 = theta1
        else :
            realPoint.theta1 = theta1 + 2 * pi
        realPoint.theta2 = theta2
    def drawCircle(self) :
        self.points = []
        rayon = self.robotConfiguration.arm1 + self.robotConfiguration.arm2/2
        partialAngle = 2 * pi / 40;
        x, y = 0, 0
        for i in range(41) :
            x = rayon * cos(partialAngle * i)
            y = rayon * sin(partialAngle * i)
            self.points.append (self.createPoint(RealPoint(self.penColor,x, y)))
        print("circle")
    def drawSquare(self):
        self.points = []
        x = -60
        y = 60
        for i in range(60) :
            self.points.append(self.createPoint( RealPoint(self.penColor, x, y)))
            x += 2
        for i in range(60):
            self.points.append(self.createPoint(RealPoint(self.penColor, x, y)))
            y -= 2
        for i in range(60):
            self.points.append(self.createPoint(RealPoint(self.penColor, x, y)))
            x -= 2
        for i in range(60):
            self.points.append(self.createPoint(RealPoint(self.penColor, x, y)))
            y += 2
    def drawTriangle(self):
        pass
    def createPointFromAngles(self, realPoint):
        l1, l2, theta1 , theta2 =  self.robotConfiguration.arm1 ,self.robotConfiguration.arm2, realPoint.theta1, realPoint.theta2
        x = l1 * cos(theta1) + l2*cos(theta1 + theta2)
        y = l1 * sin(theta1) + l2*sin(theta1 + theta2)
        return self.createPoint(RealPoint("black", x , y))
    def startCommunicationWithArduino(self, dataToArduino):
        response = "error"
        self.ArduinoSerial.write(dataToArduino.encode())
        response = self.ArduinoSerial.readline().decode("ascii")
        return response
    def preparePoint(self):
        print("data prepared")
        self.points =[]
        imporFile = open(self.robotConfiguration.importFile1, "r")
        for line in imporFile:
            line = line[:]
            list = line.split(';')
            print(list[2])
            print(line)
            if  int(list[2]) == 0 :
                state = 1
            else : state = 0
            realPoint = RealPoint(self.penColor, float(list[0]) , float(list[1]) , z= 0 , state = state )
            self.points.append(self.createPoint(realPoint))
        imporFile.close()

class Point() :
    def __init__(self, size, color , x , y, z = 0 , state = -1) :
        self.size , self.color , self.x , self.y , self.z , self.state = size , color , x , y , z , state
    def toString(self):
        print("x :", self.x, "  y ", self.y)
class RealPoint():
    def __init__(self, color, x, y, z=0,state = -1):
        self.x, self.y, self.z = x, y, z
        self.theta1 = self.theta2 = 0
        self.color =color
        self.state = state
    def timeFromPreviousPoint(self, previousPoint, speed):
        if previousPoint == "" : return 0
        return sqrt((self.x - previousPoint.x)**2 + (self.y - previousPoint.y)**2)/speed
class RecordingThread(threading.Thread):
    def __init__(self, model):
        threading.Thread.__init__(self)
        self.model = model
    def run(self):
        while self.model.recordMouvment == True:
            response = self.model.startCommunicationWithArduino(".")
            response = response[:len(response) - 1].strip()
            realPoint = RealPoint(self.model.penColor, 0, 0 , 0 , 0)
            list = response.split(" ")
            realPoint.theta1 = float(list[0]) * pi/180
            realPoint.theta2 = float(list[1])* pi/180
            point = self.model.createPointFromAngles(realPoint)
            l1 = self.model.robotConfiguration.arm1
            elbow = RealPoint(realPoint.color, cos(realPoint.theta1) * l1, sin(realPoint.theta1) * l1)
            self.model.points.append(point)
            self.model.view.drawRobot(point, self.model.createPoint(elbow))
            self.model.view.paint(point)
            print(response)

class SimulationThread(threading.Thread):

    def __init__(self, model):
            threading.Thread.__init__(self)
            self.model = model
    def run(self):
        if self.model.isSysnchronized == False :
            for i in range(100) :
                self.wait()
                print("quit wait")
                print(self.model.readFromFile)
                if self.model.readFromFile == True:
                    self.model.preparePoint()
                iteratedPoints = self.model.points[:]
                self.model.view.clairCanvas()
                times = 0
                realPoint = nextRealPoint = previouPoint = ""
                exportFile1 = open(self.model.robotConfiguration.exportFile1, "w")
                exportFile2 = open(self.model.robotConfiguration.exportFile2, "w")
                i = 1
                for point in iteratedPoints :
                    if self.wait()  == 0:
                        print("quit")
                        break
                    if i < len(iteratedPoints) :
                        nextRealPoint = self.model.createRealPoint(iteratedPoints[i])
                        i += 1
                    else :
                        nextRealPoint = ""
                    realPoint = self.model.createRealPoint(point)
                    self.model.calculateCorrespondingAngles(realPoint)
                    if nextRealPoint != "" :
                        self.model.calculateCorrespondingAngles(nextRealPoint)
                    l1 = self.model.robotConfiguration.arm1
                    elbow = RealPoint(realPoint.color,cos(realPoint.theta1)*l1 , sin(realPoint.theta1) * l1)
                    if self.model.isToFile == True :
                        file1line = str(times) + "," + str(realPoint.theta1*180/pi) + "\n"
                        file2line = str(times) + "," + str(realPoint.theta2*180/pi)+ "\n"
                        times += realPoint.timeFromPreviousPoint(nextRealPoint, self.model.robotSpeed)
                        #print(file1line)
                        exportFile1.write(file1line)
                        exportFile2.write(file2line)
                        pass
                    if self.model.isToArduino == True :
                        theta1 = format(realPoint.theta1 * 180 / pi , '.2f')
                        theta2 = format(realPoint.theta2 * 180 / pi, '.2f')

                        if self.model.isPen == True :
                            deltaTheta = 0
                            if nextRealPoint != "" :
                                deltaTheta = max(abs(realPoint.theta1- nextRealPoint.theta1)*180/pi,abs(realPoint.theta2- nextRealPoint.theta2)*180/pi)
                            afterstate = 1 if deltaTheta < 5 else 0
                            dataToArduino = theta1 + " "+ theta2 +  " "+ str(afterstate)+ "\n"
                            response = self.model.startCommunicationWithArduino(dataToArduino)
                            response = response[:len(response)-1].strip()
                            if  response == "error" :
                                messagebox.showerror("ERREUR", "Une erreur est survenue au niveau de la carte Arduino")
                                break
                            print(afterstate)
                            self.model.view.setRobotState(response)
                        if self.model.isElectromangnet == True:
                           afterstate = '1' if realPoint.color == "red" else '0'
                           if realPoint.color == "red":
                               if point == iteratedPoints[0] or point == iteratedPoints[len(iteratedPoints) - 1]:
                                   afterstate = 2
                               elif previouPoint.color != point.color:
                                   afterstate = 2
                               else : afterstate = 3
                           if realPoint.color == "green":
                               if point == iteratedPoints[0] or point == iteratedPoints[len(iteratedPoints) - 1]:
                                   afterstate = 4
                               elif previouPoint.color != point.color:
                                   afterstate = 4
                               else:
                                   afterstate = 5
                           dataToArduino = theta1 + " " + theta2 + " " + str(afterstate) + "\n"
                           print(afterstate)
                           response = self.model.startCommunicationWithArduino(dataToArduino)
                           if response == "error":
                               messagebox.showerror("ERREUR", "Une erreur est survenue au niveau de la carte Arduino")
                               break
                           self.model.view.setRobotState(response)

                    self.model.view.paint(point)
                    previouPoint = realPoint
                    self.model.view.resetRealCoordinates(realPoint)
                    self.model.view.drawRobot(point, self.model.createPoint(elbow))
                #if self.model.isToArduino :
                #    dataToArduino += "\n"
                #    self.model.startCommunicationWithArduino(dataToArduino, len(iteratedPoints))
                self.stopAnimation()
                self.model.view.robotDraw = " "
                exportFile1.close()
                exportFile2.close()
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
controller = Controller()