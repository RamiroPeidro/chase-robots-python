import gamelib
import chase

TECLAS = ["w", "a", "s", "d", "q", "e", "z", "x", "t"]



def mostrar_estado_juego(juego):
    gamelib.draw_begin
   
    gamelib.draw_rectangle(1,1,405,405, fill="black")
    gamelib.draw_line(401,0, 401, 400)
    gamelib.draw_text('CONTROLES:', 500, 30, size=10, fill='salmon')
    gamelib.draw_text('t = teletransportarse', 500, 60, size=8)
    gamelib.draw_text('a = mover izq', 500, 90, size=8)
    gamelib.draw_text('s = mover abajo', 500, 120, size=8)
    gamelib.draw_text('w = mover arriba', 500, 150, size=8)
    gamelib.draw_text('d = mover der',500, 180, size=8)
    gamelib.draw_text('e = mover arriba-der', 500, 210, size=8)
    gamelib.draw_text('q = mover arriba-izq', 500, 240, size=8)
    gamelib.draw_text('x = mover abajo-der:', 500, 270, size=8)
    gamelib.draw_text('z = mover abajo-izq:', 500, 300, size=8)
    gamelib.draw_text('NIVEL ACTUAL:', 500, 330, size=10, fill='salmon')
    gamelib.draw_text(f'{juego.mostrar_nivel()}', 500, 350, size=9)
    gamelib.draw_text('Teletransportes restantes: ', 500, 369, size=10, fill='salmon')
    gamelib.draw_text(f'{juego.teletransportes}', 500, 387, size=9)

    for fila in range(len(juego.grilla)):
        for columna in range(len(juego.grilla)):

            if juego.grilla[fila][columna] == 1:
                gamelib.draw_text("@", (columna * 20) + 10, (fila * 20) + 10, fill='gold')
            if juego.grilla[fila][columna] == 2:
                gamelib.draw_text("+", (columna * 20) + 10, (fila * 20) + 10, fill='red')
            if juego.grilla[fila][columna] == 3:
                gamelib.draw_text("*", (columna * 20) + 10, (fila * 20) + 10, fill='blue')
                
                

    gamelib.draw_end


def main():
    gamelib.title("Chase")
    gamelib.resize(600, 400)

    while gamelib.is_alive():
        n = 0
        juego  = chase.Juego(n)

        while not juego.terminado():
            juego = juego.inicializar_siguiente_nivel(n + 1)
            while not juego.nivel_terminado():
                gamelib.draw_begin()
                mostrar_estado_juego(juego)
                gamelib.draw_end()

                # Terminamos de dibujar la ventana, ahora procesamos los eventos (si el
                # usuario presionó una tecla o un botón del mouse, etc).

                # Esperamos hasta que ocurra un evento

                ev = gamelib.wait()

                if not ev:
                    # El usuario cerró la ventana.
                    break

                if ev.type == gamelib.EventType.KeyPress:
                    tecla = ev.key

                    if tecla in TECLAS:

                        juego.avanzar_un_step(tecla)

                        if juego.nivel_perdido():
                            gamelib.say('Te atrapo un robot, ¡Perdiste el juego!')
                            return

                        juego.mover_robots()

                        if juego.nivel_perdido():
                            gamelib.say('Te atrapo un robot, ¡Perdiste el juego!')
                            return



                if juego.nivel_terminado():

                    gamelib.say('Felicidades, pasaste al siguiente nivel')
                    n+=1
                    break

        gamelib.say('Felicidades, GANASTE EL JUEGO')
        return


gamelib.init(main)
