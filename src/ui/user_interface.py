"""
	@Author: JAPeTo
	@Version: 0.1.0
"""
__author__ = "JAPeTo"
__copyright__ = "Copyright 2016, Mining Agent"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "JAPeTo"
__email__ = "jefferson.amado.pena@correounivalle.edu.co,"
__status__ = "Development"

import time
# import Tkinter as tk
from libs import mtTkinter as tk
# from Tkinter import *
from libs.mtTkinter import *
import tkFont
from copy import deepcopy
class Logic:


	def apply_operator(self,operator,coords):
		"""
		Permite generar un orden de operadores desde
		la interfaz
		:param: operator, cual conjunto de operadores es
		:param: coords, coordenada actual
		"""
		#arriba	 (coords[0],coords[1]-1),\
		#abajo	 (coords[0],coords[1]+1),\
		#izq	 (coords[0]-1,coords[1]),\
		#der	 (coords[0]+1,coords[1])

		
		return {
		################################################################################
		# arriba, abajo, izq, der
		'1':
		[
		(coords[0],coords[1]-1),\
		(coords[0],coords[1]+1),\
		(coords[0]-1,coords[1]),\
		(coords[0]+1,coords[1])
		]
		,
		# arriba, abajo, der, izq
		'2':
		[
		(coords[0],coords[1]-1),\
		(coords[0],coords[1]+1),\
		(coords[0]+1,coords[1]),\
		(coords[0]+1,coords[1])
		]
		,
		# arriba, izq, abajo, der
		'3':
		[
		(coords[0],coords[1]-1),\
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]+1),\
		(coords[0]+1,coords[1])
		]
		,
		# arriba, izq, der, abajo
		'4':
		[
		(coords[0],coords[1]-1),\
		(coords[0]-1,coords[1]),\
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]+1)
		]
		,
		# arriba, der, abajo, izq
		'5':
		[
		(coords[0],coords[1]-1),\
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]+1),\
		(coords[0]-1,coords[1])
		]
		,
		# arriba, der, izq, abajo
		'6':
		[
		(coords[0],coords[1]-1),\
		(coords[0]+1,coords[1]),\
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]+1)
		]
		,
		################################################################################
		# abajo, arriba, izq, der
		'7':
		[
		(coords[0],coords[1]+1),\
		(coords[0],coords[1]-1),\
		(coords[0]-1,coords[1]),\
		(coords[0]+1,coords[1])
		]
		,

		# abajo, arriba, der, izq
		'8':
		[
		(coords[0],coords[1]+1),\
		(coords[0],coords[1]-1),\
		(coords[0]+1,coords[1]),\
		(coords[0]-1,coords[1])
		]
		,
		# abajo, izq, arriba, der
		'9':
		[
		(coords[0],coords[1]+1),\
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]-1),\
		(coords[0]+1,coords[1])
		]
		,
		# abajo, izq, der, arriba
		'10':
		[
		(coords[0],coords[1]+1),\
		(coords[0]-1,coords[1]),\
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]-1)
		]
		,
		# abajo, der, arriba, izq
		'11':
		[
		(coords[0],coords[1]+1),\
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]-1),\
		(coords[0]-1,coords[1])
		]
		,
		# abajo, der, izq, arriba
		'12':
		[
		(coords[0],coords[1]+1),\
		(coords[0]+1,coords[1]),\
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]-1)
		]
		,
		################################################################################
		# izq, arriba, abajo, der
		'13':
		[
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]-1),\
		(coords[0],coords[1]+1),\
		(coords[0]+1,coords[1])
		]
		,
		# izq, arriba, der, abajo
		'14':
		[
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]-1),\
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]+1)
		]
		,
		# izq, abajo, arriba, der
		'15':
		[
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]+1),\
		(coords[0],coords[1]-1),\
		(coords[0]+1,coords[1])
		]
		,
		# izq, abajo, der, arriba
		'16':
		[
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]+1),\
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]-1)
		]
		,
		# izq, der, arriba, abajo
		'17':
		[
		(coords[0]-1,coords[1]),\
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]-1),\
		(coords[0],coords[1]+1)
		]
		,
		# izq, der, abajo, arriba
		'18':
		[
		(coords[0]-1,coords[1]),\
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]+1),\
		(coords[0],coords[1]-1)
		]
		,
		#arriba	 (coords[0],coords[1]-1)
		#abajo	 (coords[0],coords[1]+1)
		#izq	 (coords[0]-1,coords[1])
		#der	 (coords[0]+1,coords[1])
		################################################################################
		# der, arriba, abajo, izq
		'19':
		[
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]-1),\
		(coords[0],coords[1]+1),\
		(coords[0]-1,coords[1])
		]
		,
		# der, arriba, izq, abajo
		'20':
		[
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]-1),\
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]+1)
		]
		,
		# der, abajo, arriba, izq
		'21':
		[
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]+1),\
		(coords[0],coords[1]-1),\
		(coords[0]-1,coords[1])
		]
		,
		# der, abajo, izq, arriba
		'22':
		[
		(coords[0]+1,coords[1]),\
		(coords[0],coords[1]+1),\
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]-1)
		]
		,
		# der, izq, arriba, abajo
		'23':
		[
		(coords[0]+1,coords[1]),\
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]-1),\
		(coords[0],coords[1]+1)
		]
		,
		# der, izq, abajo, arriba
		'24':
		[
		(coords[0]+1,coords[1]),\
		(coords[0]-1,coords[1]),\
		(coords[0],coords[1]+1),\
		(coords[0],coords[1]-1)
		]
		,
		
		
		}[str(operator)]


	
class Position:
	"""
	"""
	def __init__(self, x, y, parent, end_coords):

		self.__coords = (x, y)
		self.__parent = parent
		self.__end_coordss = end_coords
		self.__targets =[False,False,False]
		self.__H = 0
		# self.__list_turtle = []
		
		# if end_coords:
			
		    
		# else:
		#     self.__H = 0

		if parent:
			self.__G = parent.getG()
			self.__targets = parent.getTargets()[:]
			self.__step_turtle = parent.getStepTurtle()
			self.__list_turtle = parent.getListTurtle()

		else:
			self.__G = 0
			self.__step_turtle = 0
			self.__list_turtle = []

		self.__F = self.__G + self.__H


	def setParent(self, parent):
		self.__parent = parent
		if self.__parent:
			self.__G = parent.getG()
			self.__targets = parent.getTargets()

	def addListTurtle(self, coord):
		self.__list_turtle.append(coord)

	def setStepTurtle(self, steps=0):
		self.__step_turtle= steps

	def setG(self, cost=0):
		if self.__parent: 
			self.__G = self.__parent.getG() + cost
		else:
			self.__G = cost

	def setF(self, acum=0):
		self.__F = acum	

	def setTarget(self, targets):
		self.__targets = targets

	def setH(self,h):
		self.__H = h

	def getCoords(self):
		return self.__coords
	
	def getParent(self):
		return self.__parent

	def getTargets(self):
		return deepcopy( self.__targets ) 

	def getStepTurtle(self):
		return deepcopy(self.__step_turtle)

	def getListTurtle(self):
		return deepcopy(self.__list_turtle)

	def getX(self):
		return self.__coords[0]
    
	def getY(self):
		return self.__coords[1]

	def getH(self):
		return self.__H

	def getG(self):
		return self.__G

	def getF(self):
		return self.__F




class Environment(tk.Canvas):
	"""
	"""
	def __init__(self, master, width, height, block_size):
		"""
		"""
		tk.Canvas.__init__(self, master,\
						   width=width*block_size,\
						   height=height*block_size)
		self.__width = block_size * width
		self.__height = block_size * height
		self.__size = block_size

		self.__frees = []
		self.__sharks = []
		self.__turtles = []
		self.__evils = []
		self.__rocks = []


		self.__grid = []
		self.__start = None
		# self.__end_coords = None
		self.__end_coords = [(-1,-1)] * 3
		# print "__end_coords ",self.__end_coords

		border = 1 if block_size > 10 else 0
		for i in range(width):
		    for j in range(height):
				self.__grid.append(self.create_rectangle(\
								    i * block_size + border,\
								    j * block_size + border,\
								    (i+1) * block_size - border,\
								    (j+1) * block_size - border))


	def locate(self, coords, state):
		"""
		"""
		color_dict = {"free": "lightblue", "shark": "salmon1",\
				      "turtle": "green3", "rock": "chocolate",\
				      "Dori":"deepPink","Marlin":"MediumOrchid3",\
				      "Nemo":"MediumOrchid4","men": "red3",
				      "open": "white","closed":"midnightblue",
				      "path":"yellow",
				      "start": "skyblue3", "end": "red"}

		if 0 <= coords[0] < self.__width / self.__size and\
		   0 <= coords[1] < self.__height / self.__size:

		    tag = int(self.__height / self.__size) * coords[0] + coords[1] + 1
 			
		    self.itemconfig(tag, fill=color_dict[state])
		    self.update_idletasks()

	def setStart(self, x, y):
		# if not self.__start:
		self.__start = Position(x, y, None, self.__end_coords)
		self.locate((x, y), "start")
		# else:
			# self.setMen((x,y))

	def getStart(self):
		return self.__start

	def setRock(self, coords, convert=False):
		coords = (coords[0], coords[1])
		if not coords in self.__rocks:
			if convert:
				coords = self.board_coords(coords)
			self.__rocks.append((coords[0], coords[1]))
		
		self.locate(coords, "rock")
			

	def getRocks(self):
		return self.__rocks


	def setFree(self, coords, convert=False):
		coords = (coords[0], coords[1])
		if not coords in self.__frees:
			self.__frees.append((coords[0], coords[1]))
		
		self.locate(coords, "free")

	def getFrees(self):
		return self.__frees

	def setShark(self, coords, convert=False):
		coords = (coords[0], coords[1])
		if not coords in self.__sharks:
			self.__sharks.append((coords[0], coords[1]))
		
		self.locate(coords, "shark")

	def getSharks(self):
		return self.__sharks

	def setTurtle(self, coords, convert=False):
		coords = (coords[0], coords[1])
		if not coords in self.__turtles:
			self.__turtles.append((coords[0], coords[1]))
		
		self.locate(coords, "turtle")

	def getTurtles(self):
		return self.__turtles

	def setMen(self, coords):
		coords = (coords[0], coords[1])
		if not coords in self.__evils:
			self.__evils.append((coords[0], coords[1]))
		
		self.locate(coords, "men")

	def getMens(self):
		return self.__evils

	def setEndCoords(self, x, y,name=""):
		"""
		This create targets in 
		environment
		"""
		if not (x, y) in self.__end_coords:
			# print name," in ", (y, x)
			if name=="Nemo":
				self.__end_coords[0] = (x, y)
			if name == "Marlin":
				self.__end_coords[1] = (x, y)
			if name == "Dori":
				self.__end_coords[2] = (x, y)
		
		# print self.__end_coords
		self.locate((x, y), name)

	def getEndCoords(self):
		# print "self.__end_coords ", self.__end_coords
		return self.__end_coords

	def getSize(self):
		"""
		This return position dimension, 
		see position class
		:return: position size
		"""
		return self.__size

	def getDims(self):
		"""
		This encapsulates the width 
		and height of a Environment 
		in a single array object.
		
		:return: array coords, width and height enviroment properties
		"""
		return (int(self.__width / self.__size),\
				int(self.__height / self.__size))


# if __name__ == "__main__":

    # root = tk.Tk()
    # root.title("Nemo3 v1.0 - Se perdieron todos!")
    # board = Enviroment(root, 5, 5, 100)
    # board.pack()

    # x, y = board.board_coords((0,0))
    # board.setStart(x, y)

    # tk.mainloop()