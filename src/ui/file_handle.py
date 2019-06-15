"""
	This modules the manipulating of files, read or write 
	a file and modifying their content.

	An FileHandle object which can be readonly or readwrite. 
	Any attempt to perform a write action on a readonly 
	LockedFile object will fail.

"""
__author__ = "JAPeTo"
__copyright__ = "Copyright 2016,Mining Agent"

__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "JAPeTo"
__email__ = "jefferson.amado.pena@correounivalle.edu.co,"
__status__ = "Development"


import sys

class FileHandle():
	"""
		This Class allow operations a files through path, 
		creating a FileHandle instance.

		encapsulates a path and an matrix content.
	"""

	def __init__(self,debug=True,readonly=True):
		"""
			Construct a new 'FileHandle' object.

			:param debug:
			:param readonly:
		"""
		self.matrix = None			# matriz de contenido
		self.debug = debug			# es depurable, para ver mensajes

		if readonly:			#modo de lectura
			self.mode = 'r'
		else:
			self.mode = 'w'



	def open(self,in_path=None):
		"""
			Method that open file 

			:param filepath:
		"""

		self.in_path = in_path	# ruta del archivo
		if self.debug:
			print "Reading file in path "+str(in_path)

		with open(self.in_path, self.mode) as file_txt:
			arrlines = file_txt.readlines()	# leo todo el archivo
			try:
				self.env_size = int(arrlines.pop(0))	# tamanio del ambiente
			except ValueError:
				raise ValueError("La primera linea debe ser numerica")

			# self.matrix = [[0]*env_size]*env_size
			self.matrix = []*self.env_size
			nlines = self.env_size
			rlines = 0
			for line in arrlines:
				line = line.replace("\n","") # elimina el salto de linea
				cols = line.split(" ") # cada una de las columnas

				if cols[0] == "#":
					nlines+=1
					if self.debug:
						print "coment> ",line
					continue
				else:
					if self.debug:
						print "reading> ",line

				# verificacion del numero de columnas
				# if len(cols) == self.env_size: 
					# self.matrix.append(cols)
				# else:
					# raise EOFError('Environmet bad formed!')

				# solo guarda el numero que se ha indicado en el ambiente
				rlines += 1
				self.matrix.append(cols[0:self.env_size])
				if nlines == rlines:
					break

		if not len(self.matrix) == self.env_size: 
			raise EOFError('Environmet bad formed!, wrong rows')


		if self.debug:
			print "End Reading ... "

	
	def get_metadata(self):
		"""
			The getMetadata method allows to retrieve 
			some metadata about the FileHandle object.

			:return array:
		"""
		return self.matrix


	def write(self,out_path=None,matrix=None):
		"""
			It's an arbitrary writing method which starts 
			writing in the file at the location.

			:param filepath: 
			:param matrix:
		"""
		self.out_path = out_path	# ruta del archivo
		if self.debug:
			print "writing file in path "+str(out_path)

		with open(self.out_path, 'w') as out_txt:
			# escribo la dimension del ambiente
			out_txt.write("{}\n".format( str(len(matrix)) ))
			# y escribo la matriz de entrada en el archivo
			for line in matrix:
				out_txt.write("{}\n".format( ' '.join(line) ))

		if self.debug:
			print "End writing ... "



#################################################
# TEST
# reader = FileHandle(True, True)
# reader.open(sys.argv[1])
# data = reader.get_metadata()
# reader.write(sys.argv[2], data)