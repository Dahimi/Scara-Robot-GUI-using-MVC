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

class View() :
    def __init__(self, controller):
        self.controller = controller
        controller.setModel(self)
        print("model created")
        #self.initializeMainWindow()
        self.animationMenu = self.root= self.canvasHeight= self.canvasWidth= self.dialogWindow= self.isExport= self.isImport= self.theta1= self.theta2= " "
        self.mainPannel= self.workspace= self.workspacePanel= self.XLabel= self.YLabel= self.stopRecordImage= self.recordImage =self.stopImage= self.runImage= " "
        self.mode= self.source= self.temperature1= self.temperature2= self.vitesse1= self.vitesse2= self.h = " "
        self.runButton = self.stopButton, self.restartButton =self.color = self.shape= self.size= "  "
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
        shape = StringVar()
        shapeSubMenu.add_radiobutton(label="Carré", value="square", variable=shape, command=self.controller.setShape)
        shapeSubMenu.add_radiobutton(label="Triangle", value="triangle", variable=shape, command=self.controller.setShape)
        shapeSubMenu.add_radiobutton(label="Circle", value="circle", variable=shape, command=self.controller.setShape)
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
        workspacePanel.pack(side=LEFT, fill=Y)
    def setWorkspace(self):
        self.workspacePanel = LabelFrame(self.mainPannel , text = "Espace de travail",width=600, height=400 , padx = 10 , pady = 10 )
        self.canvasHeight = 600
        self.canvasWidth = 600
        self.workspace = Canvas(self.workspacePanel,width=self.canvasWidth,height=self.canvasHeight, bg = "white")
        self.workspace.create_line(self.canvasWidth /2 ,  0 , self.canvasWidth/2 ,self.canvasHeight , fill="#476042" , width = 3  )
        self.workspace.create_line(0, self.canvasHeight/2, self.canvasWidth , self.canvasHeight/2, fill="#476042",width=3)
        #self.workspace.create_line(self.canvasWidth/2,self.canvasHeight/2,(self.canvasWidth/4)*3,self.canvasHeight/3,self.canvasWidth/ 2,self.canvasHeight/6, fill= "blue" , width = 10)
        #self.workspacePanel.grid(row=0, column=3, columnspan=4, sticky='E')
        self.workspace.pack()
        self.workspace.pack_propagate(0)
        self.workspacePanel.pack(fill = Y , side = LEFT)
        self.workspacePanel.pack_propagate(0)
        self.workspace.bind( "<B1-Motion>", self.controller.mouseDragged )
        self.workspace.bind("<Button-1>", self.controller.mousePressed)
        self.workspace.bind("<Leave>", self.controller.mouseExit)
        return

    def paint(self , point):
        python_green = "#476042"
        x1, y1 = (point.x - 3), (point.y - 3)
        x2, y2 = (point.x + 3), (point.y + 3)
        self.workspace.create_oval(x1, y1, x2, y2, fill=point.color)
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
                        value=value,command = self.controller.setSource()).grid(row=3, column=2 * i, columnspan=2)
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
                        value=value, command=self.controller.setMove()).grid(row=7, column=2 * i, columnspan=2)
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
        externalFrame.pack(fill=Y, side=LEFT)
        externalFrame.pack_propagate(0)

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
    def newWindow(self) :
        self.root.destroy()
        self.initializeMainWindow()
        print("ye")
    def setPenColor(self, color):
        self.color.set(color)
        self.controller.setPenColor()

    def clairCanvas(self):
        self.workspace.delete("all")
        self.workspace.create_line(self.canvasWidth / 2, 0, self.canvasWidth / 2, self.canvasHeight, fill="#476042",width=3)
        self.workspace.create_line(0, self.canvasHeight / 2, self.canvasWidth, self.canvasHeight / 2, fill="#476042",width=3)
