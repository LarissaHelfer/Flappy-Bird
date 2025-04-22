import glfw
from OpenGL.GL import *
import time
import random

from config import *
from objetos.tunel import Tunel
from objetos.extras import VidaExtra, carregar_textura
from objetos.dragao import desenhar_dragao, carregar_textura_dragao, get_hitbox
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
        textura_inicio = criar_textura(*carregar_bmp("assets/FrameInicial.bmp"))
        textura_jogo = criar_textura(*carregar_bmp("assets/FrameContinuo.bmp"))
        textura_fim = criar_textura(*carregar_bmp("assets/YouDied.bmp"))
        textura_dragao = carregar_textura_dragao("assets/dragon1.png")

    except Exception as e:
        print(f"Erro ao carregar texturas: {e}")
        glfw.terminate()
        return

    estado = "inicio"
    tuneis = []
    ultimo_tunel = time.time()
    frame_anterior = time.time()
    inicio_jogo = None
    contador_tuneis = 0
    vidas = 3
    y_dragao = 300  # Posição vertical inicial (meio da tela)
    velocidade = 0
    gravidade = -800  # Pixels por segundo² (negativo = descendo)
    impulso = 300
    colidindo_agora = False
    colidiu_anteriormente = False
    invulneravel = False
    tempo_invulneravel = 0

    def key_callback(window, key, scancode, action, mods):
        nonlocal estado, ultimo_tunel, frame_anterior, inicio_jogo, tuneis, vidas, contador_tuneis
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            if estado == "inicio":
                estado = "jogando"
                inicio_jogo = time.time()
                frame_anterior = time.time()
                tuneis = []
                vidas = 3
                contador_tuneis = 0
                # dragao.pular()
                velocidade = impulso
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

        if invulneravel and tempo_atual - tempo_invulneravel > 1:  # 1 segundo de invulnerabilidade
            invulneravel = False

        if estado == "inicio":
            desenhar_fundo(textura_inicio, LARGURA, ALTURA)

        elif estado == "jogando":
            desenhar_fundo(textura_jogo, LARGURA, ALTURA)
            desenhar_dragao(textura_dragao, y_dragao)
            # dragao.atualizar(delta_tempo)
            # dragao.desenhar()

            if tempo_atual - ultimo_tunel > TUNEL_INTERVALO:
                tuneis.append(Tunel())

                if contador_tuneis % 5 == 0:
                    y_aleatorio = random.randint(150, ALTURA - 150)

                ultimo_tunel = tempo_atual

            glPushAttrib(GL_ENABLE_BIT)


            for tunel in tuneis[:]:
                tunel.atualiza(delta_tempo)
                tunel.desenha()

                # Verifica colisão com o túnel
                if tunel.verifica_colisao(get_hitbox(y_dragao)):
                    colidindo_agora = True

                # Verifica se já passou o túnel (para pontuar)
                if not tunel.passou and tunel.x + tunel.largura < 100:
                    tunel.passou = True
                    contador_tuneis += 1

                # Remove se saiu da tela
                if tunel.esta_tela():
                    tuneis.remove(tunel)

            if colidindo_agora and not invulneravel:
                vidas -= 1
                print("Vida perdida. Vidas restantes:", vidas)
                invulneravel = True
                tempo_invulneravel = tempo_atual
                colidindo_agora = False
                if vidas <= 0:
                    estado = "fim"
            else:
                colidiu_anteriormente = False
            glPopAttrib()

            if tempo_atual - inicio_jogo > 200:
                estado = "fim"

            # dragon
            # Aplica física
            velocidade += gravidade * delta_tempo
            y_dragao += velocidade * delta_tempo

            # Limita o dragão dentro da tela
            if y_dragao < 0:
                y_dragao = 0
                velocidade = 0
            if y_dragao > 600 - 80:  # 80 = altura do sprite  // 600 altura da tela
                y_dragao = 600 - 80
                velocidade = 0

            if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
                velocidade = impulso


        elif estado == "fim":
            desenhar_fundo(textura_fim, LARGURA, ALTURA)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()