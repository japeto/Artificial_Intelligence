"""
"""
__author__ = "JAPeTo"
__copyright__ = "Copyright 2016,Mining Agent"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "JAPeTo"
__email__ = "jefferson.amado.pena@correounivalle.edu.co,"
__status__ = "Development"

import os
import time
import threading
import sys
import inspect
from libs.mtTkinter import *

from Tkinter import *
import tkFont

from tkFileDialog import askopenfilename
from tkFileDialog import asksaveasfile

from ui.file_handle import *
from ui.user_interface import *

from algorithms.alg_breadth import *
from algorithms.alg_uniformcost import *
from algorithms.alg_depth import *
from algorithms.alg_heuristic import *
from algorithms.alg_astar import *



class MiningAgent():

    def __init__(self, debug=False):

        self.reader = FileHandle(debug)

        self.algorithm = None
        self.algorithms = 1

        self.timesleep = 0.1
        self.moverorders = 1
        self.path = []
        self.runthread = None
        self.threads = []
        self.pathstop = False
        self.allow_repaint = False

        self.debug = debug
        self.output = ""

        self.root = tk.Tk()

        self.root.title("Mining Agent")

        def openfile():
            filename = askopenfilename(parent=self.root, initialdir='../inputs')
            if filename:
                self.reader.open(filename)
                self.createMap()

        def popupmsg():
            popup = tk.Tk()
            popup.wm_title("")

            title = Label(popup, text='-- Map colors --')
            title.pack()

            robot = Label(popup, text='robot', fg='white', bg='skyblue3')
            robot.pack()
            rocks = Label(popup, text='rocks', fg='white', bg='chocolate')
            rocks.pack()
            shark = Label(popup, text='shark', fg='white', bg='gold3')
            shark.pack()
            turtle = Label(popup, text='turtle', fg='white', bg='green3')
            turtle.pack()
            men = Label(popup, text='men', fg='white', bg='red3')
            men.pack()

            separator = Label(popup, text='-- Algorithms --')
            separator.pack()

            free = Label(popup, text='free', fg='black', bg='lightblue')
            free.pack()
            path = Label(popup, text='path', fg='white', bg='skyblue')
            path.pack()

            openn = Label(popup, text='openn', fg='black', bg='white')
            openn.pack()
            closed = Label(popup, text='closed', fg='white', bg='midnightblue')
            closed.pack()

            separator = Label(popup, text='-- Targets --')
            separator.pack()

            Dori = Label(popup, text='Dori', fg='white', bg='deepPink')
            Dori.pack()
            Marlin = Label(popup, text='Marlin', fg='white', bg='MediumOrchid3')
            Marlin.pack()
            Nemo = Label(popup, text='Nemo', fg='white', bg='MediumOrchid4')
            Nemo.pack()

            popup.geometry('{}x{}+{}+{}'.format(100, 300,
                                                self.root.winfo_rootx() + self.root.winfo_width(),
                                                self.root.winfo_rooty()))
            popup.mainloop()

        menubar = tk.Menu(self.root, background='#222', foreground='#ccc',
                          activebackground='#004c99', activeforeground='white')

        # create a pulldown menu, and add it to the menu bar
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=openfile)
        # fileMenu.add_command(label="Save", command=hello)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=fileMenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Acerca de...", command=popupmsg)
        menubar.add_cascade(label="Ayuda", menu=helpmenu)

        # display the menu
        self.root.config(menu=menubar)
        ##########################################################
        self.environment = Environment(self.root, 5, 5, 100)
        self.environment.pack()

        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()

        # para centrar la ventana
        # self.root.geometry("550x520+%d+%d" % ( (w-550)/2, (h-520)/2 ) )
        self.root.configure(background='#222')
        # pintar la ventana
        self.root.mainloop()

    def recreateMenu(self):

        def hello():
            print
            "hello!"

        def savefile():
            f = asksaveasfile(parent=self.root, initialdir='../outputs', mode='w', defaultextension=".txt")
            if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return
            f.write(self.output)
            f.close()

        def openfile():
            filename = askopenfilename(parent=self.root, initialdir='../inputs')
            if filename:
                self.reader.open(filename)
                self.createMap()

        def selectAlgoritmh(value):
            self.algorithms = value
            # print "####################### ", value
            if self.algorithms == 1:
                algorithmsMenu.entryconfig(0, foreground='red')
                algorithmsMenu.entryconfig(1, foreground='black')
                algorithmsMenu.entryconfig(2, foreground='black')
                algorithmsMenu.entryconfig(4, foreground='black')
                algorithmsMenu.entryconfig(5, foreground='black')
                algorithmsMenu.entryconfig(6, foreground='black')
                algorithmsMenu.entryconfig(7, foreground='black')
            if self.algorithms == 2:
                algorithmsMenu.entryconfig(0, foreground='black')
                algorithmsMenu.entryconfig(1, foreground='red')
                algorithmsMenu.entryconfig(2, foreground='black')
                algorithmsMenu.entryconfig(4, foreground='black')
                algorithmsMenu.entryconfig(5, foreground='black')
                algorithmsMenu.entryconfig(6, foreground='black')
                algorithmsMenu.entryconfig(7, foreground='black')
            if self.algorithms == 3:
                algorithmsMenu.entryconfig(0, foreground='black')
                algorithmsMenu.entryconfig(1, foreground='black')
                algorithmsMenu.entryconfig(2, foreground='red')
                algorithmsMenu.entryconfig(4, foreground='black')
                algorithmsMenu.entryconfig(5, foreground='black')
                algorithmsMenu.entryconfig(6, foreground='black')
                algorithmsMenu.entryconfig(7, foreground='black')
            if self.algorithms == 4:
                algorithmsMenu.entryconfig(0, foreground='black')
                algorithmsMenu.entryconfig(1, foreground='black')
                algorithmsMenu.entryconfig(2, foreground='black')
                algorithmsMenu.entryconfig(4, foreground='red')
                algorithmsMenu.entryconfig(5, foreground='black')
                algorithmsMenu.entryconfig(6, foreground='black')
                algorithmsMenu.entryconfig(7, foreground='black')
            if self.algorithms == 5:
                algorithmsMenu.entryconfig(0, foreground='black')
                algorithmsMenu.entryconfig(1, foreground='black')
                algorithmsMenu.entryconfig(2, foreground='black')
                algorithmsMenu.entryconfig(4, foreground='black')
                algorithmsMenu.entryconfig(5, foreground='black')
                algorithmsMenu.entryconfig(6, foreground='red')
                algorithmsMenu.entryconfig(7, foreground='black')
            if self.algorithms == 6:
                algorithmsMenu.entryconfig(0, foreground='black')
                algorithmsMenu.entryconfig(1, foreground='black')
                algorithmsMenu.entryconfig(2, foreground='black')
                algorithmsMenu.entryconfig(4, foreground='black')
                algorithmsMenu.entryconfig(5, foreground='red')
                algorithmsMenu.entryconfig(6, foreground='black')
                algorithmsMenu.entryconfig(7, foreground='black')
            if self.algorithms == 7:
                algorithmsMenu.entryconfig(0, foreground='black')
                algorithmsMenu.entryconfig(1, foreground='black')
                algorithmsMenu.entryconfig(2, foreground='black')
                algorithmsMenu.entryconfig(4, foreground='black')
                algorithmsMenu.entryconfig(5, foreground='black')
                algorithmsMenu.entryconfig(6, foreground='black')
                algorithmsMenu.entryconfig(7, foreground='black')
                algorithmsMenu.entryconfig(7, foreground='red')

        def selectMoves(orders):
            self.moverorders = orders
            movesMenu.entryconfig(0, foreground='black')
            movesMenu.entryconfig(1, foreground='black')
            movesMenu.entryconfig(2, foreground='black')
            movesMenu.entryconfig(3, foreground='black')
            movesMenu.entryconfig(4, foreground='black')
            movesMenu.entryconfig(5, foreground='black')
            movesMenu.entryconfig(6, foreground='black')
            movesMenu.entryconfig(7, foreground='black')
            movesMenu.entryconfig(8, foreground='black')
            movesMenu.entryconfig(9, foreground='black')
            movesMenu.entryconfig(10, foreground='black')
            movesMenu.entryconfig(11, foreground='black')
            movesMenu.entryconfig(12, foreground='black')
            movesMenu.entryconfig(13, foreground='black')
            movesMenu.entryconfig(14, foreground='black')
            movesMenu.entryconfig(15, foreground='black')
            movesMenu.entryconfig(16, foreground='black')
            movesMenu.entryconfig(17, foreground='black')
            movesMenu.entryconfig(18, foreground='black')
            movesMenu.entryconfig(19, foreground='black')
            movesMenu.entryconfig(20, foreground='black')
            movesMenu.entryconfig(21, foreground='black')
            movesMenu.entryconfig(22, foreground='black')
            movesMenu.entryconfig(23, foreground='black')
            movesMenu.entryconfig(24, foreground='black')

            movesMenu.entryconfig((orders - 1), foreground='red')

        def start_alg():
            if self.reader.get_metadata():
                self.repaintMap()
                self.find(self.environment, self.moverorders)

        def start():
            if len(self.threads) == 0:
                # print ">>>>>>>>>>>>>>>>" ,self.threads, self.runthread
                self.runthread = threading.Thread(target=start_alg)
                self.runthread.daemon = True
                self.threads.append(self.runthread)
                self.runthread.start()
            elif self.runthread and not self.runthread.is_alive():
                self.threads = []
                self.algorithm.stopExec()
                self.pathstop = True

        def pause():
            if self.runthread and self.runthread.is_alive():
                # self.algorithm.setTimeSleep( 20 )
                pass

        def stop():
            if self.runthread and self.runthread.is_alive():
                self.threads = []
                self.algorithm.stopExec()
                self.pathstop = True

        def speed():
            if self.runthread and self.runthread.is_alive():
                self.algorithm.setTimeSleep(0.0)
                self.timesleep = 0.0

        def slow():
            if self.runthread and self.runthread.is_alive():
                self.algorithm.setTimeSleep(self.timesleep)

                if self.timesleep < 10:
                    self.timesleep += 0.05
                    print "s: ",self.timesleep
                else:
                    self.timesleep = 10
                    print "s: ", self.timesleep

        def quik():
            if self.runthread and self.runthread.is_alive():
                self.algorithm.setTimeSleep(self.timesleep)

                if self.timesleep > 0:
                    self.timesleep -= 0.05
                    print "q: ",self.timesleep
                else:
                    self.timesleep = 0
                    print "q: ", self.timesleep

        def clear():
            self.allow_repaint = True
            if self.reader.get_metadata():
                self.threads = []
                self.algorithm.stopExec()
                self.pathstop = True
                self.repaintMap()

        def popupmsg():
            popup = tk.Tk()
            popup.wm_title("")

            title = Label(popup, text='-- Map colors --')
            title.pack()

            robot = Label(popup, text='robot', fg='white', bg='skyblue3')
            robot.pack()
            rocks = Label(popup, text='rocks', fg='white', bg='chocolate')
            rocks.pack()
            shark = Label(popup, text='shark', fg='white', bg='gold3')
            shark.pack()
            turtle = Label(popup, text='turtle', fg='white', bg='green3')
            turtle.pack()
            men = Label(popup, text='men', fg='white', bg='red3')
            men.pack()

            separator = Label(popup, text='-- Algorithms --')
            separator.pack()

            free = Label(popup, text='free', fg='black', bg='lightblue')
            free.pack()
            path = Label(popup, text='path', fg='white', bg='skyblue')
            path.pack()

            openn = Label(popup, text='openn', fg='black', bg='white')
            openn.pack()
            closed = Label(popup, text='closed', fg='white', bg='midnightblue')
            closed.pack()

            separator = Label(popup, text='-- Targets --')
            separator.pack()

            Dori = Label(popup, text='Dori', fg='white', bg='deepPink')
            Dori.pack()
            Marlin = Label(popup, text='Marlin', fg='white', bg='MediumOrchid3')
            Marlin.pack()
            Nemo = Label(popup, text='Nemo', fg='white', bg='MediumOrchid4')
            Nemo.pack()

            popup.geometry('{}x{}+{}+{}'.format(100, 300,
                                                self.root.winfo_rootx() + self.root.winfo_width(),
                                                self.root.winfo_rooty()))
            popup.mainloop()

        menubar = tk.Menu(self.root, background='#222', foreground='#ccc',
                          activebackground='#004c99', activeforeground='white')

        # menubar = tk.Menu(self.root, background='#000099', foreground='white',
        # activebackground='#004c99', activeforeground='white')

        # create a pulldown menu, and add it to the menu bar
        fileMenu = tk.Menu(menubar, tearoff=0)

        fileMenu.add_command(label="Open", command=openfile)
        fileMenu.add_command(label="Save", command=savefile)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.root.quit)

        menubar.add_cascade(label="File", menu=fileMenu)

        algorithmsMenu = tk.Menu(menubar, tearoff=0)
        algorithmsMenu.add_command(label="Breadth-first", command=lambda: selectAlgoritmh(1))
        algorithmsMenu.entryconfig(0, foreground='red')
        algorithmsMenu.add_command(label="Depth-first", command=lambda: selectAlgoritmh(2))
        algorithmsMenu.add_command(label="UniformCostSearch", command=lambda: selectAlgoritmh(3))
        algorithmsMenu.add_separator()
        algorithmsMenu.add_command(label="Heuristic", command=lambda: selectAlgoritmh(4))
        algorithmsMenu.add_command(label="Heuristic2", command=lambda: selectAlgoritmh(6))
        algorithmsMenu.add_command(label="A Star", command=lambda: selectAlgoritmh(5))
        algorithmsMenu.add_command(label="A Star2", command=lambda: selectAlgoritmh(7))

        menubar.add_cascade(label="Algorithms", menu=algorithmsMenu)

        operMenu = tk.Menu(menubar, tearoff=0)
        operMenu.add_command(label="Start ", command=start)
        # operMenu.add_command(label="Pause ",command=pause)
        operMenu.add_command(label="Stop ", command=stop)
        operMenu.add_separator()
        operMenu.add_command(label="Slow (--)", command=slow)
        operMenu.add_command(label="Normal", command=speed)
        operMenu.add_command(label="Quick (++)", command=quik)
        operMenu.add_separator()
        operMenu.add_command(label="Clear", command=clear)
        menubar.add_cascade(label="Operations", menu=operMenu)

        movesMenu = tk.Menu(menubar, tearoff=0)
        # arriba, abajo, izq, der
        movesMenu.add_command(label="arriba, abajo, izq, der", command=lambda: selectMoves(1))
        movesMenu.entryconfig(0, foreground='red')
        # arriba, abajo, der, izq
        movesMenu.add_command(label="arriba, abajo, der, izq", command=lambda: selectMoves(2))
        # arriba, izq, abajo, der
        movesMenu.add_command(label="arriba, izq, abajo, der", command=lambda: selectMoves(3))
        # arriba, izq, der, abajo
        movesMenu.add_command(label="arriba, izq, der, abajo", command=lambda: selectMoves(4))
        # arriba, der, abajo, izq
        movesMenu.add_command(label="arriba, der, abajo, izq", command=lambda: selectMoves(5))
        # arriba, der, izq, abajo
        movesMenu.add_command(label="arriba, der, izq, abajo", command=lambda: selectMoves(6))

        # abajo, arriba, izq, der
        movesMenu.add_command(label="abajo, arriba, izq, der", command=lambda: selectMoves(7))
        # abajo, arriba, der, izq
        movesMenu.add_command(label="abajo, arriba, der, izq", command=lambda: selectMoves(8))
        # abajo, izq, arriba, der
        movesMenu.add_command(label="abajo, izq, arriba, der", command=lambda: selectMoves(9))
        # abajo, izq, der, arriba
        movesMenu.add_command(label="abajo, izq, der, arriba", command=lambda: selectMoves(10))
        # abajo, der, arriba, izq
        movesMenu.add_command(label="abajo, der, arriba, izq", command=lambda: selectMoves(11))
        # abajo, der, izq, arriba
        movesMenu.add_command(label="abajo, der, izq, arriba", command=lambda: selectMoves(12))

        # izq, arriba, abajo, der
        movesMenu.add_command(label="izq, arriba, abajo, der", command=lambda: selectMoves(13))
        # izq, arriba, der, abajo
        movesMenu.add_command(label="izq, arriba, der, abajo", command=lambda: selectMoves(14))
        # izq, abajo, arriba, der
        movesMenu.add_command(label="izq, abajo, arriba, der", command=lambda: selectMoves(15))
        # izq, abajo, der, arriba
        movesMenu.add_command(label="izq, abajo, der, arriba", command=lambda: selectMoves(16))
        # izq, der, arriba, abajo
        movesMenu.add_command(label="izq, der, arriba, abajo", command=lambda: selectMoves(17))
        # izq, der, abajo, arriba
        movesMenu.add_command(label="izq, der, abajo, arriba", command=lambda: selectMoves(18))

        # der, arriba, abajo, izq
        movesMenu.add_command(label="der, arriba, abajo, izq", command=lambda: selectMoves(19))
        # der, arriba, izq, abajo
        movesMenu.add_command(label="der, arriba, izq, abajo", command=lambda: selectMoves(20))
        # der, abajo, arriba, izq
        movesMenu.add_command(label="der, abajo, arriba, izq", command=lambda: selectMoves(21))
        # der, abajo, izq, arriba
        movesMenu.add_command(label="der, abajo, izq, arriba", command=lambda: selectMoves(22))
        # der, izq, arriba, abajo
        movesMenu.add_command(label="der, izq, arriba, abajo", command=lambda: selectMoves(23))
        # der, izq, abajo, arriba
        movesMenu.add_command(label="der, izq, abajo, arriba", command=lambda: selectMoves(24))

        menubar.add_cascade(label="Moves", menu=movesMenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Acerca de...", command=popupmsg)
        menubar.add_cascade(label="Ayuda", menu=helpmenu)

        # display the menu
        self.root.config(menu=menubar)

    def repaintMap(self):
        if self.allow_repaint:
            data = self.reader.get_metadata()
            for idr, row in enumerate(data):
                for idc, col in enumerate(row):
                    if int(col) == 0:
                        self.environment.setStart(idc, idr)
                    elif int(col) == 1:
                        self.environment.setRock((idc, idr))
                    elif int(col) == 2:
                        self.environment.setFree((idc, idr))
                    elif int(col) == 3:
                        self.environment.setShark((idc, idr))
                    elif int(col) == 4:
                        self.environment.setTurtle((idc, idr))
                    elif int(col) == 5:
                        self.environment.setEndCoords(idc, idr, "Dori")
                    elif int(col) == 6:
                        self.environment.setEndCoords(idc, idr, "Marlin")
                    elif int(col) == 7:
                        self.environment.setEndCoords(idc, idr, "Nemo")
                    elif int(col) == 8:
                        self.environment.setMen((idc, idr))

    def createMap(self):

        data = self.reader.get_metadata()

        if self.runthread and not self.runthread.is_alive():
            self.threads = []
            self.algorithm.stopExec()
            self.pathstop = True

        if len(data) > 1 and len(data) < 3:
            for ele in self.root.winfo_children():
                ele.destroy()
            dimension = len(data)

            self.recreateMenu()
            self.environment = Environment(self.root, dimension, dimension, 190)
            self.environment.pack()

        if len(data) > 2 and len(data) < 6:
            for ele in self.root.winfo_children():
                ele.destroy()
            dimension = len(data)

            self.recreateMenu()
            self.environment = Environment(self.root, dimension, dimension, 100)
            self.environment.pack()

        if len(data) > 5 and len(data) < 20:
            for ele in self.root.winfo_children():
                ele.destroy()
            dimension = len(data)

            self.recreateMenu()
            self.environment = Environment(self.root, dimension, dimension, 50)
            self.environment.pack()

        elif len(data) > 19 and len(data) < 50:
            for ele in self.root.winfo_children():
                ele.destroy()
            dimension = len(data)

            self.recreateMenu()
            self.environment = Environment(self.root, dimension, dimension, 20)
            self.environment.pack()

        elif len(data) > 49 and len(data) < 100:
            for ele in self.root.winfo_children():
                ele.destroy()
            dimension = len(data)

            self.recreateMenu()
            self.environment = Environment(self.root, dimension, dimension, 10)
            self.environment.pack()

        elif len(data) > 99 and len(data) < 110:
            for ele in self.root.winfo_children():
                ele.destroy()
            dimension = len(data)

            self.recreateMenu()
            self.environment = Environment(self.root, dimension, dimension, 7)
            self.environment.pack()

        elif len(data) > 110:
            for ele in self.root.winfo_children():
                ele.destroy()
            dimension = len(data)

            self.recreateMenu()
            self.environment = Environment(self.root, dimension, dimension, 5)
            self.environment.pack()

        for idr, row in enumerate(data):
            for idc, col in enumerate(row):

                if int(col) == 0:
                    self.environment.setStart(idc, idr)
                elif int(col) == 1:
                    self.environment.setRock((idc, idr))
                elif int(col) == 2:
                    self.environment.setFree((idc, idr))
                elif int(col) == 3:
                    self.environment.setShark((idc, idr))
                elif int(col) == 4:
                    self.environment.setTurtle((idc, idr))
                elif int(col) == 5:
                    self.environment.setEndCoords(idc, idr, "Dori")
                elif int(col) == 6:
                    self.environment.setEndCoords(idc, idr, "Marlin")
                elif int(col) == 7:
                    self.environment.setEndCoords(idc, idr, "Nemo")
                elif int(col) == 8:
                    self.environment.setMen((idc, idr))

    def popupResult(self, txt_result=""):
        result = tk.Tk()
        result.wm_title('Resultados')

        tmp_lb = Label(result, text=txt_result)
        tmp_lb.pack();
        result.pack();

    # result.geometry('{}x{}+{}+{}'.format(400, 300,
    # self.root.winfo_rootx()+self.root.winfo_width(), self.root.winfo_rooty()))
    # result.mainloop()

    def find(self, environment=None, operators=1):
        self.output = ""
        self.allow_repaint = True
        end = None
        start = time.time()

        if self.algorithms == 1:
            if self.debug:
                print
                "selected algorithm BFS"

            self.algorithm = BFS(self.debug)
            end = self.algorithm.start(environment, operators)

        elif self.algorithms == 2:
            if self.debug:
                print
                "selected algorithm DFS"

            self.algorithm = DFS(self.debug)
            end = self.algorithm.start(environment, operators)

        elif self.algorithms == 3:
            if self.debug:
                print
                "selected algorithm UCS"

            self.algorithm = UCS(self.debug)
            end = self.algorithm.start(environment, operators)

        elif self.algorithms == 4:
            if self.debug:
                print
                "selected algorithm HUC"

            self.algorithm = HUC(self.debug)
            self.algorithm.setHtype(0)

            end = self.algorithm.start(environment, operators)

        elif self.algorithms == 5:
            if self.debug:
                print
                "selected algorithm A_Star"

            self.algorithm = A_Star(self.debug)
            self.algorithm.setHtype(0)
            end = self.algorithm.start(environment, operators)


        elif self.algorithms == 6:
            if self.debug:
                print
                "selected algorithm HUC2"

            self.algorithm = HUC(self.debug)
            self.algorithm.setHtype(1)

            end = self.algorithm.start(environment, operators)

        elif self.algorithms == 7:
            if self.debug:
                print
                "selected algorithm A_Star2"

            self.algorithm = A_Star(self.debug)
            self.algorithm.setHtype(1)
            end = self.algorithm.start(environment, operators)

        self.path = []

        end_coords = environment.getEndCoords()

        start_coords = self.environment.getStart().getCoords()

        self.output += self.algorithm.getStrdebug()
        self.repaintMap()

        if end:
            cost = end.getG()
            if self.debug:
                print
                "\n Costo total solucion: ",
                print
                cost,

            self.output += "\n Costo total solucion:"
            self.output += str(cost) + "\n"

        while end:
            self.path.append(end.getCoords())
            end = end.getParent()

        list_path = list(map((lambda x: (x[1], x[0])), self.path))
        if self.debug:
            print
            " Pasos solucion: ",
            print
            ' -> '.join(map(str, reversed(list_path)))

        self.output += " Pasos solucion:"
        self.output += ' -> '.join(map(str, reversed(list_path)))

        for coords in self.path:
            if not coords in start_coords:
                self.environment.locate(coords, "path")

        # print self.output
        self.threads = []

        end = time.time()
        if self.debug:
            print
            "\nTiempo de ejecucion fue: ", (end - start)
        self.output += "\nTiempo de ejecucion fue: " + str(end - start)

# trate de hacer una ventana para mostrar en otro lado que no sea la consola pero se me jode :/
# self.popupResult(self.output)


if __name__ == "__main__":
    nemo = MiningAgent(False)
