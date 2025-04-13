import glfw 
from OpenGL.GL import *
import time
from config import *
from objetos.tunel import Tunel

def main():
    if not glfw.init():
        return
    window = glfw.create_window(LARGURA, ALTURA, "Flappy", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, LARGURA, 0, ALTURA, -1, 1)

    tuneis = []
    evento = time.time()
    frame = time.time()

    while not glfw.window_should_close(window):
        tempo_atual = time.time()
        delta_tempo = tempo_atual - frame
        frame = tempo_atual

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        if tempo_atual - evento > TUNEL_INTERVALO:
            tuneis.append(Tunel())
            evento = tempo_atual

        for tunel in tuneis:
            tunel.update(delta_tempo)
            tunel.draw()

        tuneis = [t for t in tuneis if not t.is_offscreen()]

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
