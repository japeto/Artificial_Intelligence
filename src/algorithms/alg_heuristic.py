import time
from ui.user_interface import *
import heapq

class PriorityQueue:

    def __init__(self):
        self._queue = []
        self._index = 0

    def insert(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
        return self

    def remove(self):
        return heapq.heappop(self._queue)[-1]

    def firstElement(self):
         return heapq.heappop(self._queue)

    def is_empty(self):
        return len(self._queue) == 0

    def __str__(self):
        out=""
        for pos in self._queue:
            if type(pos[2]) == tuple:
                out += str((pos[0], tuple(reversed( pos[2] ))))
            else:
                out += str((pos[0], tuple(reversed( pos[2].getCoords() ))))

            
        return out


    def __len__(self):
        return len(self._queue)

    def index(self,coord=(0,0)):
        for tpl in self._queue:
            if tpl[2] == coord:
                return self._queue.index(tpl)




class HUC():

    def __init__(self, debug=True):
        """
        Constructor para este algoritmo
        """
        self.timesleep = 0.1        # velocidad de cambio
        self.steps = 0              # cantidad de pasos
        self.stop = False           # bandera para detenerlo desde la 
                                    # interfaz

        self.curr_step = 0          # paso actual
        self.debug = debug          # variable para realizar la depuracion

        self.expanded = 0           # cantidad de posiciones expandidas
        self.creates = 1             # cantidad de posiciones creadas
        self.type_heuristic =0      # seleccion de la Heuristica
        self.strdebug = ""


    def setHtype(self,type_heuristic=0):
        self.type_heuristic = type_heuristic
        
    def setSteps(self, steps):
        """
        Establece el numero de paso que debe dar
        el algoritmo antes para detenerse
        :param: step cantidad de pasos
        """
        self.steps = self.curr_step + steps

    def setTimeSleep(self, time):
        """
        Efecto de demora
        :param: tiempo
        """
        self.timesleep = time

    def stopExec(self):
        """
        Condicion de parada desde la interfaz
        """
        self.stop = True
        
    def getStrdebug(self):
        return self.strdebug

    def start(self,environment, operator):
        """
        Aqui inicia el algoritmo
        :param: ambiente, aqui esta el mapa
        :param: operadores seleccionados desde la interfaz
        """

        # agrego a la lista el nodo inicial [H]
        # open_pos = [environment.getStart()]  
        # esta una lista paralela para las coordenadas
        # open_coords = [open_pos[0].getCoords()] 

        # agrego a la lista el nodo inicial [H]
        open_pos = PriorityQueue().insert(environment.getStart(), 0)
        # esta una lista paralela para las coordenadas
        open_coords = PriorityQueue().insert(environment.getStart().getCoords(), 0 )


        # Ancho del ambiente
        environment_width = environment.getDims()[0]
        # Alto del ambiente
        environment_height = environment.getDims()[1]

        ## 
        # Arreglo de ladrillos
        obstacles_coords = environment.getRocks()
        # Arreglo de tiburones
        sharks_coords = environment.getSharks()
        # Arreglo de tortugas
        turtles_coords = environment.getTurtles()
        # Arreglo de hombres
        mens_coords = environment.getMens()

        # Arreglo de coordenadas ya exploradas
        arr_closed =[]

        # Arreglo corrdenadas de las metas, insertadas en orden [7,6,5]
        end_coords = environment.getEndCoords()
        
        # Coordenadas del incio
        start_coords = environment.getStart().getCoords()

        index = 0
        tmp_coord = end_coords[index]
        self.strdebug += "end_coords "+str(end_coords)
        if self.debug:
            print "end_coords ",end_coords

        dx = tmp_coord[1] - start_coords[1]
        dy = tmp_coord[0] - start_coords[0]
        if self.type_heuristic :
            environment.getStart().setH((abs(dx) + abs(dy))*0.5)
        else:
            environment.getStart().setH(0.5 *( ( dx**2+dy**2)**1/2))

        self.strdebug +="INICIO "+str(tuple(reversed( start_coords )))+"\n"
        self.strdebug +="OBJETIVOS: "+str(map(tuple,map(reversed, end_coords )))+"\n"
        self.strdebug +="H>>"+str(environment.getStart().getH())

        if self.debug:
            print "INICIO ", tuple(reversed( start_coords ))
            print "OBJETIVOS: ", map(tuple,map(reversed, end_coords ))
            print "H>>",environment.getStart().getH()

        # el estado actual, es el primero de la lista
        # para este primer paso se extrae de la cola el primero
        # current = open_pos[0]
        # self, x, y, parent, end_coords)
        # coordenadas del primero de la lista
        # coords = current.getCoords()

        self.curr_step = 0 # cantidad de pasos hasta el momento
        self.strdebug +="+"*50+"\n"   # linea 

        if self.debug:
            print "+"*50   # linea 
        operadores = Logic();
        while len(open_pos) > 0:    # mientras halla algo en la cola

            if self.stop:           # Si desde la interfaz envian la parada
                return

            current = open_pos.remove()
            # print "current ",current.getCoords()               

            coords = open_coords.remove()
            # print "coords ",coords

            arr_closed.append(coords)

            if not (coords == start_coords) and\
                not coords in turtles_coords and\
                not coords in mens_coords and\
                not coords in sharks_coords:
                environment.locate(coords, "closed") 

            
            self.expanded+=1 # aumento la cantidad de expandidos
            self.strdebug +="parent: "+str(tuple(reversed(current.getCoords())))\
                         +str(current.getTargets())+"\n"

            if self.debug:
                print "parent: ",tuple(reversed(current.getCoords()))\
                             , current.getTargets()

            ####
            # Si esta coordenada (la del current) hace parte de las 
            # coordenadas meta y posee padre (podria estar demas)
            #
            # Esta permite verificar si es meta 
            if coords in end_coords and current.getParent():
                ###
                # El arreglo de coordenadas [Nemo, Marlin, Dori] 
                #
                # current.getTargets().index(False) da la posicion del primer
                # False -> SI esta posicion es igual a la la de Nemo, en la 
                # primera met encontrada cambie el arreglo de metas
                # encontradas en esta posicion

                if end_coords.index(coords) == current.getTargets().index(False):
                    
                    # Hago una copia profunda de
                    # el arreglo de metas encontradas
                    arr_targets = current.getTargets()

                    # Cual es la posicion de la meta encontrada en
                    # el arreglo de metas
                    pos = arr_targets.index(False)
                    
                    # Cambio esta posicion
                    arr_targets[ pos ] = True

                    # Establezo esta copia como
                    # en esta posicion
                    current.setTarget( arr_targets )
                    
                    self.strdebug += "target found>>: "+str(tuple(reversed(\
                        current.getCoords())))+str(current.getTargets())+"\n"

                    self.strdebug += "H>>"+str(current.getH())+"\n"
                    if self.debug:
                        print "target_found: ",tuple(reversed(\
                            current.getCoords())) , current.getTargets()                

                # Si todas las metas son encontradas
                # retorne la posicion donde la encontro
                if all( current.getTargets() ):
                    if self.debug:
                        print "#"*50
                        print " Nodos expandidos: ", self.expanded
                        print " Nodos creados: ", self.creates,

                    self.strdebug += "#"*50+"\n" 
                    self.strdebug += " Nodos expandidos: "+str(self.expanded)+"\n"
                    self.strdebug += " Nodos creados: "+str(self.creates)
                    return current

            #se saca la lista de los padres del nodo current para realizar el
            #algoritmo evitando ciclos
            parents=[]
            parents_coords =[]
            end= deepcopy(current)
            while end and end.getParent():
                parents.append(end.getParent())
                parents_coords.append(end.getParent().getCoords())
                end = end.getParent()

            self.strdebug+= "parents:"+str(parents_coords)   
            if self.debug:
                print "parents:",parents_coords

            ###
            # Esta parte realiza la expancion para la posicion
            # actual

            for x,y in operadores.apply_operator(operator,coords):

                if (x, y) not in obstacles_coords and\
                    (x, coords[1]) not in obstacles_coords and\
                    (coords[0], y) not in obstacles_coords and\
                    0 <= x < environment_width and 0 <= y < environment_height:
                    
                    # Creo una nueva posicion
                    new_pos = Position(x, y, current, end_coords)

                    # Obtengo las corrdenadas de esa posicion
                    new_coords = (x, y)
                    if new_coords in sharks_coords:
                        new_pos.setG(10)

                    elif new_coords in turtles_coords:
                        new_pos.setG(1)

                    elif new_coords in mens_coords:
                        new_pos.setG(float("inf"))
                    else:
                        new_pos.setG(1)
                    # print "-",new_posg.etH()
                    # index = new_pos.getTargets().index(False)

                    # tmp_coord = end_coords[index]

                    index = new_pos.getTargets().index(False)
                    tmp_coord = end_coords[index]
                    self.strdebug += "end_coords "+str(end_coords)+"\n"
                    if self.debug:
                        print "end_coords ",end_coords

                    dx = tmp_coord[1] - new_coords[1]
                    dy = tmp_coord[0] - new_coords[0]
                    if self.type_heuristic :
                        new_pos.setH((abs(dx) + abs(dy))*0.5)
                    else:
                        new_pos.setH(0.5 *( ( dx**2+dy**2)**1/2))
                    
                    

                    self.strdebug += "son: "+str((y, x))+" "+str(new_pos.getTargets())+"\n"
                    self.strdebug += "H>>>"+str(new_pos.getH())+"\n"

                    if self.debug:
                        print "son: ", (y, x) , new_pos.getTargets()
                        print "H>>>",new_pos.getH()

                    # if current.getParent() and new_coords == current.getParent().getCoords():
                    if new_coords in parents_coords:
                        index_parent = parents_coords.index(new_coords)
                        parent_temp = parents[index_parent]
                        if  self.debug:
                            print new_coords," ", parents_coords, "<-->"\
                                ,new_pos.getTargets()," == ", parent_temp.getTargets()

                        if not ( new_pos.getTargets() == parent_temp.getTargets() ):
                            if not (new_coords == start_coords) and\
                                not new_coords in turtles_coords and\
                                not new_coords in mens_coords and\
                                not new_coords in arr_closed and\
                                not new_coords in sharks_coords:
                                environment.locate(new_coords, "open")
                            ###
                            # Es una cola agrego al final
                            # el nodo o posicion
                            # open_pos.append(new_pos)
                            open_pos.insert( new_pos, new_pos.getH() )
                            # las coordenadas
                            # open_coords.append(new_coords)
                            open_coords.insert( new_pos.getCoords(), new_pos.getH() )
                            self.creates+=1  #aumento la cantidad de posiciones creadas
                    else:
                            if not (new_coords == start_coords) and\
                                not new_coords in turtles_coords and\
                                not new_coords in mens_coords and\
                                not new_coords in arr_closed and\
                                not new_coords in sharks_coords:
                                environment.locate(new_coords, "open")
                            ###
                            # Es una cola agrego al final
                            # el nodo o posicion
                            # open_pos.append(new_pos)
                            open_pos.insert( new_pos, new_pos.getH() )
                            # las coordenadas
                            # open_coords.append(new_coords)
                            open_coords.insert( new_pos.getCoords(), new_pos.getH() )
                            self.creates+=1  #aumento la cantidad de posiciones creadas  


            self.strdebug += "queue: "+str(open_coords)+"\n"
            self.strdebug += "+"*50+"\n"

            if self.debug:
                print "queue: ", open_coords
                print "+"*50

            # en el caso que la expansion no
            # de lugar a hijos
            if len(open_pos) == 0:
                return current

            self.curr_step += 1   

            # hago un sleep para detener el 
            time.sleep( self.timesleep )

            # si hay establecido un numero de pasos 
            # se detiene cuando sean iguales
            if self.curr_step == self.steps:
                break

        # en caso de no encontrar una solucion
        # despues de haber espandido todo el ambiente.
        return None