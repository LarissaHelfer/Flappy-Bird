import glfw
from OpenGL.GL import *
import time
from config import *
from objetos.tunel import Tunel
from utils.utils import carregar_bmp, criar_textura, desenhar_fundo

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(LARGURA, ALTURA, "Flappy", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    glViewport(0, 0, LARGURA, ALTURA)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, LARGURA, 0, ALTURA, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    try:
        textura_inicio = criar_textura(*carregar_bmp("flapyBird/assets/FrameInicial.bmp"))
        textura_jogo = criar_textura(*carregar_bmp("flapyBird/assets/FrameContinuo.bmp"))
        textura_fim = criar_textura(*carregar_bmp("flapyBird/assets/YouDied.bmp"))
    except Exception as e:
        print(f"Erro ao carregar texturas: {e}")
        glfw.terminate()
        return

    estado = "inicio"
    tuneis = []
    ultimo_tunel = time.time()
    frame_anterior = time.time()
    inicio_jogo = None

    def key_callback(window, key, scancode, action, mods):
        nonlocal estado, ultimo_tunel, frame_anterior, inicio_jogo
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            if estado == "inicio":
                estado = "jogando"
                inicio_jogo = time.time()
                frame_anterior = time.time()
                tuneis = []
            elif estado == "fim":
                estado = "inicio"

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_DEPTH_TEST)
        
        tempo_atual = time.time()
        delta_tempo = tempo_atual - frame_anterior
        frame_anterior = tempo_atual

        if estado == "inicio":
            desenhar_fundo(textura_inicio, LARGURA, ALTURA)
        elif estado == "jogando":
            desenhar_fundo(textura_jogo, LARGURA, ALTURA)
            
            if tempo_atual - ultimo_tunel > TUNEL_INTERVALO:
                tuneis.append(Tunel())
                ultimo_tunel = tempo_atual
            
            glPushAttrib(GL_ENABLE_BIT)
            for tunel in tuneis[:]:
                tunel.atualiza(delta_tempo)
                tunel.desenha()
                if tunel.esta_tela():
                    tuneis.remove(tunel)
            glPopAttrib()
            
            if tempo_atual - inicio_jogo > 10:
                estado = "fim"
                
        elif estado == "fim":
            desenhar_fundo(textura_fim, LARGURA, ALTURA)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()