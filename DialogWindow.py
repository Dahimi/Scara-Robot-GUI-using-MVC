from  tkinter import *
import tkinter.font as font
from tkinter import ttk
from PIL import ImageTk,Image
from tkinter import filedialog, messagebox
import time
class DialogWindow(Toplevel) :
    def __init__(self , view):
        super().__init__(view.root)
        self.view = view
        self.title("Configuaration")
        self.geometry("600x600")
        self.setFrames()
        self.grab_set()
        self.focus_set()
        self.parentFrame , self.portTextField, self.dataRateCombo, self.type
        self.arm1TextField , self.arm2TextField , self.distanceTextField
        self.imageFrame, self.scaraImage
        self.import1 =r"C:\Users\pc\PycharmProjects\Scara-Robot-GUI-using-MVC\import.txt"
        self.import2 = " "
        self.export1 =r"C:\Users\pc\PycharmProjects\Scara-Robot-GUI-using-MVC\file1.txt"
        self.export2 =r"C:\Users\pc\PycharmProjects\Scara-Robot-GUI-using-MVC\file2.txt"
        self.okButton , self.cancelButton
        self.responce = -1
    def startCommunication(self):
        print("communicating with arduino")
        popupProgressBar = Toplevel(self)
        progress_bar = ttk.Progressbar(popupProgressBar, orient = HORIZONTAL, length = 250, mode ='determinate')
        if self.view.controller.startCommunication() == 1 :
            connectionLabel = Label(popupProgressBar, text ="Etablissement de la communication avec la carte arduino")
            connectionLabel.pack(padx = 10 , pady = 10)
            progress_bar.pack(padx = 10  , pady = 10)
            for i in range(1,6) :
                progress_bar['value'] = i*20
                popupProgressBar.update()
                time.sleep(1)
            popupProgressBar.destroy()
            messagebox.showinfo("Communication avec Arduino" , "La connexion avec la carte arduino est \n bien établie")
            return 1
        else :
            messagebox.showerror("Communication avec Arduino" , "Le port que vous avez saisi n'est pas accessible pour le moment\n Veuillez choisir un autre")
            return 0
    def setFrames(self):
        self.parentFrame = LabelFrame(self)
        message_font = font.Font(size=20)

        message_1 = Message(self.parentFrame,
                               text='Configuration des paramètres',
                               bg='#ecffd9',
                               font=message_font,
                               justify=CENTER,
                               width=400,
                               padx=20
                               )
        message_1.grid(row = 0 , column = 1)
        self.parentFrame.pack()


        fileFrame = LabelFrame(self.parentFrame, text ="Les fichiers externes:",  width = 500 , height = 100 , padx = 20 , pady= 10)
        importLabel = Label(fileFrame , text ="fichier à importer" )
        def import1():
            self.import1 = filedialog.askopenfilename(initialdir = "/Users\pc\PycharmProjects\Scara-Robot-GUI-using-MVC" , title =" selectionner le fichier 1")

        def import2():
            self.import2 = filedialog.askopenfilename(initialdir="/Users\pc\PycharmProjects\Scara-Robot-GUI-using-MVC", title=" selectionner le fichier 1")

        def export1():
            self.export1 = filedialog.askopenfilename(initialdir="/Users\pc\PycharmProjects\Scara-Robot-GUI-using-MVC",
                                                      title=" selectionner le fichier 1")

        def export2():
            self.export2 = filedialog.askopenfilename(initialdir="/Users\pc\PycharmProjects\Scara-Robot-GUI-using-MVC",
                                                      title=" selectionner le fichier 1")
        importButton1 = Button(fileFrame , text = "Fichier 1" , command = import1)
        #importButton2 = Button(fileFrame, text="Fichier 2" , command =import2 )
        importLabel.grid(row = 0 , column  = 0 , columnspan = 2 )
        importButton1.grid(row = 0 , column = 2, columnspan = 2)
        #importButton2.grid(row=0, column=3)
        exportLabel = Label(fileFrame, text="fichier à exporter")
        exportButton1 = Button(fileFrame, text="Fichier 1", command = export1)
        exportButton2 = Button(fileFrame, text="Fichier 2" , command = export2)
        exportLabel.grid(row=1, column=0, columnspan=2)
        exportButton1.grid(row=1, column=2)
        exportButton2.grid(row=1, column=3)
        fileFrame.grid(row = 1 , column = 1)


        arduinoFrame = LabelFrame(self.parentFrame, text = "Communication avec la carte Arduino", width = 500 , height = 100 , padx = 20 , pady= 10)
        portLabel = Label(arduinoFrame, text = "Le port de la Carte Arduino ")
        self.portTextField = Entry(arduinoFrame)
        self.portTextField.insert(0,"COM9")
        dataRateLabel = Label(arduinoFrame, text = "Débit de communication ")
        self.dataRateCombo = ttk.Combobox(arduinoFrame , values = ( "9600", "115200","1000000" ))
        self.dataRateCombo.current(1)
        portLabel.grid(row = 0 , column = 0)
        self.portTextField.grid(row = 0 , column = 1)
        dataRateLabel.grid(row = 0 , column = 2)
        self.dataRateCombo.grid(row = 0 , column = 3)
        arduinoFrame.grid(row = 2 , column = 1)


        dimensionFrame = LabelFrame(self.parentFrame, text = "Les dimensions du robot", width = 500 , height = 100 , padx = 20 , pady= 10)
        Label(dimensionFrame, text = "Choisir le type de Robot Scara à controller :").grid(row = 0 , column = 0 , columnspan = 3)
        types = {
            "Robot Scara parallèle": "parallel",
            "Robot Scara série" : "articulated"
        }
        self.type = StringVar()
        self.type.set("articulated")
        i = 0
        for (text, value) in types.items():
            Radiobutton(dimensionFrame, text=text, variable=self.type,
                        value=value).grid(row = 1, column = 2*i , columnspan = 2)
            i = i +1
        Label(dimensionFrame, text="Choisir les dimensions du robot  :").grid(row=2, column=0, columnspan=3)
        Label(dimensionFrame, text = "Longeur L1 (mm):").grid(row = 3 , column = 0)
        Label(dimensionFrame, text="Longeur L2 (mm):").grid(row=3, column=2)
        self.arm1TextField = Entry(dimensionFrame)
        self.arm2TextField = Entry(dimensionFrame)
        self.arm1TextField.insert(0, "110")
        self.arm2TextField.insert(0, "110")
        self.arm1TextField.grid(row = 3, column = 1)
        self.arm2TextField.grid(row=3, column=3)
        Label(dimensionFrame, text="distance D -pour Scara parallèle(mm):").grid(row=4, column=0, columnspan = 3)
        self.distanceTextField = Entry(dimensionFrame)
        self.distanceTextField.grid(row = 4 , column = 3)
        self.distanceTextField.insert(0, "0")
        dimensionFrame.grid(row = 3 , column = 1)

        self.imageFrame = LabelFrame(self.parentFrame )
        self.scaraImage = ImageTk.PhotoImage(Image.open("scara.jpg"))
        Label(self.imageFrame, image = self.scaraImage).pack()
        self.imageFrame.grid(row = 4, column = 1)

        def next() :
            if (self.setRobotConfiguration() == 0):
                print("repeat")
                return
            if self.startCommunication() == 0 :
               return
            self.responce = 1
            self.destroy()
            self.grab_release()
        def cancel() :
            self.responce = -1
            print(self.responce)
            self.destroy()
            self.grab_release()
        cornerFrame = LabelFrame(self.parentFrame, padx = 10 , pady = 10)
        self.okButton = Button(cornerFrame, text = " OK ", command = next )
        self.cancelButton = Button (cornerFrame, text = " Cancel " , command = cancel)

        Label(cornerFrame, text ="\t\t\t\t\t\t\t\t\t").grid(row = 1 , column = 3)
        self.okButton.grid(row = 1 , column = 4)
        self.cancelButton.grid(row = 1 , column = 5)
        cornerFrame.grid(row = 5, column = 1)
    def setRobotConfiguration(self):
        robotConfiguration = RobotConfiguration(self.import1, self.import2, self.export1, self.export2, self.arm1TextField.get(), self.arm2TextField.get(), self.distanceTextField.get(),
                                                self.portTextField.get(), self.dataRateCombo.get(), self.type)
        if(robotConfiguration.getState() == 0):
            return 0
        self.view.controller.setRobotConfiguration(robotConfiguration)
        return 1
class RobotConfiguration() :
    def __init__(self, importFile1, importFile2, exportFile1, exportFile2, arm1, arm2 ,distance,  arduinoPort , dataRate, type   ):
        self.importFile1 = importFile1
        self.importFile2 = importFile2
        self.exportFile1 =exportFile1
        self.exportFile2 = exportFile2
        try :
            self.arduinoPort = arduinoPort.strip()
            self.dataRate = dataRate.strip()
            self.type = type.get()
            self.arm1 = int(arm1.strip())
            self.arm2 = int(arm2.strip())
            self.distance = int( distance.strip())
            self.state = 1
        except ValueError :
            messagebox.showerror("Erreur dans le format" , "Veuillez saisir des valeur numérique dans le champ des dimensions")
            self.state = 0
    def getState(self):
        return self.state