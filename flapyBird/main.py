import glfw
from OpenGL.GL import *
import time
import random
import math

from config import *
from objetos.tunel import Tunel
from objetos.extras import VidaExtra
from objetos.dragao import desenhar_dragao, carregar_textura_dragao, get_hitbox
from utils.utils import carregar_image, criar_textura, desenhar_fundo, desenhar_texto

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
        textura_inicio = criar_textura(*carregar_image("flapyBird/assets/FrameInicial.png"))
        textura_jogo = criar_textura(*carregar_image("flapyBird/assets/FrameContinuo.png"))
        textura_fim = criar_textura(*carregar_image("flapyBird/assets/YouDied.bmp"))
        textura_vida = criar_textura(*carregar_image("flapyBird/assets/vida_24bit.bmp"))
        textura_dragao = carregar_textura_dragao("flapyBird/assets/dragon1.png")
    except Exception as e:
        print(f"Erro nas texturas, veja aqui")
        glfw.terminate()
        return

    estado = "inicio"
    tuneis = []
    vidas_extras = []
    ultimo_tunel = time.time()
    frame_anterior = time.time()
    inicio_jogo = None
    contador_tuneis = 0
    vidas = 3
    y_dragao = 300
    velocidade = 0
    colidindo_agora = False
    colidiu_anteriormente = False
    invulneravel = False
    tempo_invulneravel = 0

    def key_callback(window, key, scancode, action, mods):
        nonlocal estado, ultimo_tunel, frame_anterior, inicio_jogo
        nonlocal tuneis, vidas_extras, vidas, contador_tuneis, velocidade, y_dragao
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            if estado == "inicio":
                estado = "jogando"
                inicio_jogo = time.time()
                frame_anterior = time.time()
                tuneis = []
                vidas_extras = []
                vidas = 3
                contador_tuneis = 0
                velocidade = IMPULSO
                y_dragao = 300
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

            y_flutuante = 300 + 20 * math.sin(tempo_atual * 2)
            desenhar_dragao(textura_dragao, y_flutuante)

            alpha = abs(math.sin(tempo_atual * 3))
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glColor4f(1.0, 1.0, 1.0, alpha)
            desenhar_texto(LARGURA // 2 - 60, ALTURA // 2 -(-50), "START", tamanho=32)
            glColor4f(1.0, 1.0, 1.0, 1.0)

        elif estado == "jogando":
            desenhar_fundo(textura_jogo, LARGURA, ALTURA)
            desenhar_dragao(textura_dragao, y_dragao)
            # dragao.atualizar(delta_tempo)
            # dragao.desenhar()

            if tempo_atual - ultimo_tunel > TUNEL_INTERVALO:
                tuneis.append(Tunel())

                if contador_tuneis % 5 == 0:
                    y_aleatorio = random.randint(150, ALTURA - 150)
                    vidas_extras.append(VidaExtra(LARGURA, y_aleatorio, textura_vida))

                ultimo_tunel = tempo_atual

            glPushAttrib(GL_ENABLE_BIT)

            hitbox_dragao = get_hitbox(y_dragao)

            for tunel in tuneis[:]:
                tunel.atualiza(delta_tempo)
                tunel.desenha()

                if tunel.verifica_colisao(hitbox_dragao) and not invulneravel:
                    colidindo_agora = True

                if not tunel.passou and tunel.x + tunel.largura < 100:
                    tunel.passou = True
                    contador_tuneis += 1

                if tunel.esta_tela():
                    tuneis.remove(tunel)

            if colidindo_agora:
                vidas -= 1
                invulneravel = True
                tempo_invulneravel = tempo_atual
                colidindo_agora = False
                if vidas <= 0:
                    estado = "fim"

            glPopAttrib()

            for vida in vidas_extras[:]:
                vida.atualizar(TUNEL_VELOCIDADE * delta_tempo)
                vida.desenhar_vidas()

                if vida.checar_colisao_hitbox(hitbox_dragao):
                    vidas += 1
                    vida.visivel = False

                if not vida.visivel:
                    vidas_extras.remove(vida)


            if tempo_atual - inicio_jogo > 200:
                estado = "fim"

            velocidade += GRAVIDADE * delta_tempo
            y_dragao += velocidade * delta_tempo

            if y_dragao < 0:
                y_dragao = 0
                velocidade = 0
            if y_dragao > ALTURA - 80:
                y_dragao = ALTURA - 80
                velocidade = 0

            if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
                velocidade = IMPULSO

            glColor3f(1.0, 1.0, 1.0)
            desenhar_texto(20, ALTURA - 40, f"Vidas: {vidas}", tamanho=28)
            desenhar_texto(20, ALTURA - 80, f"Pontos: {contador_tuneis}", tamanho=28)


        elif estado == "fim":
            desenhar_fundo(textura_fim, LARGURA, ALTURA)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()