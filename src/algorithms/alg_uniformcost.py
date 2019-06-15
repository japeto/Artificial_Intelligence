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




class UCS():

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
        self.strdebug = ""

        
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
        self.strdebug +="end_coords "+str(end_coords)+"\n"

        # Coordenadas del incio
        start_coords = environment.getStart().getCoords()

        coords = environment.getStart().getCoords()


        self.strdebug +="INICIO "+str(tuple(reversed( start_coords )))+"\n"
        self.strdebug +="OBJETIVOS: "+str(map(tuple,map(reversed, end_coords )))+"\n"

        if self.debug:
            print "INICIO ", tuple(reversed( start_coords ))
            print "OBJETIVOS: ", map(tuple,map(reversed, end_coords ))

        # el estado actual, es el primero de la lista
        # para este primer paso se extrae de la cola el primero
        # current = open_pos[0]
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

            if not (coords == start_coords) and\
                not coords in turtles_coords and\
                not coords in mens_coords and\
                not coords in sharks_coords:
                environment.locate(coords, "closed")  

            arr_closed.append(coords)

            self.expanded+=1  #aumento la cantidad de posiciones creadas

            self.strdebug +="parent: "+str(tuple(reversed(current.getCoords())))\
                         +str(current.getTargets())+"\n"
            self.strdebug +="G:"+str(current.getG())+"\n"

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
                    self.strdebug +="G:"+str(current.getG())+"\n"

                    if self.debug:
                        print "parent>>: ",tuple(reversed(\
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

                    # print tuple(reversed(new_coords))
                    
                    # Si no tienes tortuga el multiplicador es 1
                    mutiplier = 1;
                    if current.getStepTurtle()>0:
                        # Si ya he cogido una tortuga ahora
                        # el multiplicador es 0.5
                        mutiplier=0.5;
                    
                    # si la coordenada es tiburon
                    # costo (10) por multiplicador
                    if new_coords in sharks_coords:
                        new_pos.setG(10*mutiplier)

                    # si la coordenada es tortugga
                    # costo (1) por multiplicador
                    elif new_coords in turtles_coords:
                        # Si es tortuga calcula costo de 
                        # capturar tortuga
                        new_pos.setG(1*mutiplier)
                        ###
                        # Si el padre ya posee tortuga
                        # reste uno de los pasos
                        if current.getStepTurtle()>0:
                            # resto el numero de paso
                            new_pos.setStepTurtle(current.getStepTurtle()-1)

                        # De otra forma verifico que
                        # esta coordenada NO haga parte
                        # de la lista de tortugas que ya 
                        # capturo el padre.
                        elif not ( new_coords in current.getListTurtle()):
                            # La puedo capturar
                            # ahora le doy los 4 pasos
                            new_pos.setStepTurtle(4);
                            # agrego a la lista apatir de aqui
                            new_pos.addListTurtle( new_coords )

                    # si la coordenada es hombre
                    # costo (infinito) por multiplicador    
                    elif new_coords in mens_coords:
                        new_pos.setG(float("inf")*mutiplier)


                    # Para cualquier otra posicion
                    # 
                    else:
                        new_pos.setG(1*mutiplier)
                    

                    self.strdebug += "son: "+str((y, x))+str(new_pos.getTargets())+"\n"

                    if self.debug:
                        print "son: ", (y, x) , new_pos.getTargets()


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
                            open_pos.insert( new_pos, new_pos.getG() )
                            # las coordenadas
                            # open_coords.append(new_coords)
                            open_coords.insert( new_pos.getCoords(), new_pos.getG() )
                            self.creates+=1 # aumento la cantidad de expandidos        
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
                            open_pos.insert( new_pos, new_pos.getG() )
                            # las coordenadas
                            # open_coords.append(new_coords)
                            open_coords.insert( new_pos.getCoords(), new_pos.getG() )
                            self.creates+=1 # aumento la cantidad de expandidos  

            self.strdebug += "queue: "+str(open_coords)+"\n"
            self.strdebug += "+"*50+"\n"
            if self.debug:
                print "queue: ", open_coords
                print "+"*50

            # en el caso que la expansion no
            # de lugar a hijos
            if len(open_pos) == 0:
                return current

            self.curr_step+=1   

            # hago un sleep para detener el 
            time.sleep( self.timesleep )

            # si hay establecido un numero de pasos 
            # se detiene cuando sean iguales
            if self.curr_step == self.steps:
                break

        # en caso de no encontrar una solucion
        # despues de haber espandido todo el ambiente.
        return None