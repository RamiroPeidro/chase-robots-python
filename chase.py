import random
import gamelib

def hay_obstaculo(y, x, grilla):
  '''Devuelve True si la posicion esta
  ocupada por un obstaculo'''
  if grilla[y][x] == 3:
      return True
  return False    


def hay_robot(y, x, grilla):
  '''Devuelve True si la posicion esta ocupada
  por un robot'''
  return grilla[y][x]== 2

def esta_en_posicion_valida(y, x, grilla):
  '''Devuelve True si la posicion es válida (si esta
  dentro de los límites de la grilla y si no hay un obstaculo)'''
  #verifico que este dentro de la grilla
  if x>=0 and y>=0:
    if x<20 and y <20:
      if not hay_obstaculo(y, x, grilla):
        #verifico que no haya obstaculos
        return True
      else:
        return False
  return False    

  
def cantidad_robots(grilla):
    '''Devuelve la cantidad de robots que hay actualmente en la grilla'''
    robots = 0
    for i in range(len(grilla)):
        for k in range(len(grilla[i])):
            if grilla[i][k] == 2:
                robots+=1
    return robots   


def trazar_ruta(x, y, i, k):
    '''x,y posición del robot
    i, k posición jugador'''

    if i > x:
        x = x + 1
    elif i < x:
        x = x - 1

    if k > y:
        y = y + 1
    elif k < y:
        y = y - 1

    return x, y


def validar_movimiento(i, k):
    '''Valida el movimiento '''
    if 0 <= i < 20 and 0 <= k < 20:
        return True
    return False


def posicion_jugador(grilla):
    '''Asigna aleatoriamente al jugador en la grilla'''
    grilla[random.choice(range(20))][random.choice(range(20))] = 1
    for i in range(len(grilla)):
        for k in range(len(grilla[i])):
            if grilla[i][k] == 1:
                return [i, k]
    return False


def posiciones_robot(grilla, n):
    '''Asigna aleatroiamente a los robots en la grilla'''
    posiciones = []
    for i in range(3 * n):
        grilla[random.choice(range(20))][random.choice(range(20))] = 2
    for i in range(len(grilla)):
        for k in range(len(grilla[i])):
            if grilla[i][k] == 2:
                posiciones.append((i, k))
    return posiciones

def posiciones_obstaculos(grilla, n):
    '''Asigna aleatoriamente los obstaculos
    en la grilla'''
    posiciones = []
    for i in range(5 * n):
        grilla[random.choice(range(20))][random.choice(range(20))] = 3
    for i in range(len(grilla)):
        for k in range(len(grilla[i])):
            if grilla[i][k] == 3:
                posiciones.append((i, k))
    return posiciones            

class Juego:
    def __init__(self, n):
        self.grilla = [[0 for _ in range(20)] for _ in range(20)]
        self.jugador = posicion_jugador(self.grilla)
        self.robots = posiciones_robot(self.grilla, n)
        self.obstaculos = posiciones_obstaculos(self.grilla, n)
        self.nivel = n
        self.teletransportes = 5

    def __str__(self):
        return (
            f'La grilla es: \n{self.grilla} \nEl jugador esta en la posicion {self.jugador} \nLos robots estan en las posiciones {self.robots}\n Los obstaculos estan en las posiciones {self.obstaculos}'
        )

    def mostrar_jugador(self):
        return self.jugador

    def mostrar_grilla(self):
        return self.grilla

    def mostar_robots(self):
        return self.robots

    def mostrar_obstaculos(self):
        return self.obstaculos  

    def mostrar_nivel(self):
        return self.nivel

    def coordenadas_robots(self):
        '''Devuelve las coordenadas actuales de los robots'''
        posiciones = []
        for i in range(len(self.grilla)):
            for k in range(len(self.grilla[i])):
                if self.grilla[i][k] == 2:
                    posiciones.append((i, k))
        return posiciones

    def nivel_terminado(self):
        '''Devuelve True si el nivel termino, False
        en caso contrario'''
        for i in range(len(self.grilla)):
            for k in range(len(self.grilla[i])):
                if self.grilla[i][k] == 2:
                    return False
        return True

    def terminado(self):
        '''Devuelve True si el juego terminó, False en caso contrario.
        El juego termina cuando el usuario completa todos los niveles'''
        if self.nivel == 5:
            return True
        return False

    def inicializar_siguiente_nivel(self, n):
        ''''Recibe el mivel y devuelve una nueva instancia del juego acorde'''
        return Juego(n)


    def nivel_perdido(self):
        '''Devuelve True si el jugador perdió el nivel,
        False en caso contrario'''
        for i in range(len(self.grilla)):
            for k in range (len(self.grilla[i])):
                if self.grilla[i][k] == 1:
                    return False
        return True   


    def avanzar_un_step(self, accion):
        '''Segun la accion, actualiza la posicion del jugador, si
        colisiona con un obstaculo lo puede empujar, y si colisiona con un robot, 
        el jugador no está mas en la grilla'''
        grilla = self.grilla
        y, x = self.jugador
        if accion == 's':
            if esta_en_posicion_valida(y+1, x, grilla):
                if hay_robot(y+1, x, grilla):
                    grilla[y][x] = 2
                    #Jugador no esta mas en la grilla
                else:
                    grilla[y][x] = 0
                    grilla[y+1][x] = 1
                    self.jugador = [y+1, x]
            if x>=0 and y+1>=0:
                if x<20 and y+1<20:        
                    if hay_obstaculo(y+1, x, grilla):
                        if esta_en_posicion_valida(y+2, x, grilla):
                            #el obstaculo puede ser desplazado por el jugador
                            grilla[y][x] = 0
                            grilla[y+1][x] = 1
                            grilla[y+2][x] = 3
                            self.jugador= [y+1, x]         
                    
        if accion == 'a':
            if esta_en_posicion_valida(y, x-1, grilla):
                if hay_robot(y, x-1, grilla):
                    grilla[y][x] = 2
                else:
                    grilla[y][x] = 0
                    grilla[y][x-1] = 1
                    self.jugador = [y, x-1]
            if hay_obstaculo(y, x-1, grilla):
                if esta_en_posicion_valida(y, x-2, grilla):
                    #el obstaculo puede ser desplazado por el jugador
                    grilla[y][x] = 0
                    grilla[y][x-1] = 1
                    grilla[y][x-2] = 3
                    self.jugador= [y, x-1]         

        if accion == 'd':
            if esta_en_posicion_valida(y, x+1, grilla):
                if hay_robot(y, x+1, grilla):
                    grilla[y][x] = 2
                else:
                    grilla[y][x] = 0
                    grilla[y][x+1] = 1
                    self.jugador = [y, x+1]
            if x+1>=0 and y>=0:
                if x+1<20 and y<20:
                    if hay_obstaculo(y, x+1, grilla):
                        if esta_en_posicion_valida(y, x+2, grilla):
                            #el obstaculo puede ser desplazado por el jugador
                            grilla[y][x] = 0
                            grilla[y][x+1] = 1
                            grilla[y][x+2] = 3
                            self.jugador= [y, x+1]         

        if accion == 'w':
            if esta_en_posicion_valida(y-1, x, grilla):
                if hay_robot(y-1, x, grilla):
                    grilla[y][x] = 2
                else:
                    grilla[y][x] = 0
                    grilla[y-1][x] = 1
                    self.jugador = [y-1, x]
            if hay_obstaculo(y-1, x, grilla):
                if esta_en_posicion_valida(y-2, x, grilla):
                    #el obstaculo puede ser desplazado por el jugador
                    grilla[y][x] = 0
                    grilla[y-1][x] = 1
                    grilla[y-2][x] = 3
                    self.jugador= [y-1, x]         
                    
                    
        if accion == 't':
            #Jugador tiene una cantidad limitada de teletransportes
            if self.teletransportes == 0:
                gamelib.say('No te quedan mas teletransportes!')
                return
            else:       
                dy = random.choice(range(20))
                dx = random.choice(range(20))
                if esta_en_posicion_valida(dy, dx, grilla):
                    if hay_robot(dy, dx, grilla):
                        grilla[y][x] = 2
                    else:
                        grilla[y][x] = 0
                        grilla[dy][dx] = 1
                        self.jugador = [dy, dx]
                        self.teletransportes-=1
        
        if accion == 'q':
            if esta_en_posicion_valida(y-1, x-1, grilla):
                if hay_robot(y-1, x-1, grilla):
                    grilla[y][x] = 2
                else:
                    grilla[y][x] = 0
                    grilla[y-1][x-1] = 1
                    self.jugador = [y-1, x-1]
            if hay_obstaculo(y-1, x-1, grilla):
                if esta_en_posicion_valida(y-2, x-2, grilla):
                    #el obstaculo puede ser desplazado por el jugador
                    grilla[y][x] = 0
                    grilla[y-1][x-1] = 1
                    grilla[y-2][x-2] = 3
                    self.jugador= [y-1, x-1]        
                    

        if accion == 'e':
            if esta_en_posicion_valida(y-1, x+1, grilla):
                if hay_robot(y-1, x+1, grilla):
                    grilla[y][x] = 2
                else:
                    grilla[y][x] = 0
                    grilla[y-1][x+1] = 1
                    self.jugador = [y-1, x+1]
            if x+1>=0 and y+1>=0:
                if x+1<20 and y+1<20:        
                    if hay_obstaculo(y-1, x+1, grilla):
                        if esta_en_posicion_valida(y-2, x+2, grilla):
                            #el obstaculo puede ser desplazado por el jugador
                            grilla[y][x] = 0
                            grilla[y-1][x+1] = 1
                            grilla[y-2][x+2] = 3
                            self.jugador= [y-1, x+1]

        if accion == 'x':
            if esta_en_posicion_valida(y+1, x+1, grilla):
                if hay_robot(y+1, x+1, grilla):
                    grilla[y][x] = 2
                else:
                    grilla[y][x] = 0
                    grilla[y+1][x+1] = 1
                    self.jugador = [y+1, x+1]  
            if x+1>=0 and y+1>=0:
                if x+1<20 and y+1<20:
                    if hay_obstaculo(y+1, x+1, grilla):
                        if esta_en_posicion_valida(y+2, x+2, grilla):
                            #el obstaculo puede ser desplazado por el jugador
                            grilla[y][x] = 0
                            grilla[y+1][x+1] = 1
                            grilla[y+2][x+2] = 3
                            self.jugador= [y+1, x+1]


        if accion == 'z':
            if esta_en_posicion_valida(y+1, x-1, grilla):
                if hay_robot(y+1, x-1, grilla):
                    grilla[y][x] = 2
                else:
                    grilla[y][x] = 0
                    grilla[y+1][x-1] = 1
                    self.jugador = [y+1, x-1]  
            if x-1>=0 and y+1>=0:
                if x-1<20 and y+1<20:        
                    if hay_obstaculo(y+1, x-1, grilla):
                        if esta_en_posicion_valida(y+2, x-2, grilla):
                            #el obstaculo puede ser desplazado por el jugador
                            grilla[y][x] = 0
                            grilla[y+1][x-1] = 1
                            grilla[y+2][x-2] = 3
                            self.jugador= [y+1, x-1]     

    def mover_robots(self):
        '''Realiza el movimiento de los robots'''
        i, k = self.jugador

        posiciones_de_robots = self.coordenadas_robots()

        for fila in range(len(self.grilla)):
            for col in range(len(self.grilla)):
                if self.grilla[fila][col] == 2:
                    self.grilla[fila][col] = 0


        nuevas_pos = []
        for y, x in posiciones_de_robots:
            nuevas_pos.append(trazar_ruta(y, x, i, k))


        # Limpio todos los robots anteriores de la grilla

        for y, x in nuevas_pos:

            if self.grilla[y][x] == 2:
                self.grilla[y][x] = 3

            if self.grilla[y][x] == 0:
                self.grilla[y][x] = 2

            if self.grilla[y][x] == 1:
                self.grilla[y][x] = 2

            if self.grilla[y][x] == 3:
                self.grilla[y][x] = 3




