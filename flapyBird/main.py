import glfw
from OpenGL.GL import *
import time
import random
import math

from config import *
from objetos.tunel import Tunel
from objetos.extras import VidaExtra
from objetos.dragao import desenhar_dragao, carregar_textura, get_hitbox
from utils.utils import carregar_image, criar_textura, desenhar_fundo, desenhar_texto, desenhar_fundo_invertido

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
        textura_jogo = carregar_textura("flapyBird/assets/fundoSimples.png")
        textura_fim = criar_textura(*carregar_image("flapyBird/assets/YouDied.bmp"))
        textura_vida = carregar_textura("flapyBird/assets/vida.png")
        textura_dragao = carregar_textura("flapyBird/assets/dragon1.png")
        textura_tunel = carregar_textura("flapyBird/assets/textura_tuneis.png")
    except Exception as e:
        print(f"Erro nas texturas, veja aqui")
        glfw.terminate()
        return

    # Variáveis do jogo
    tunel_velocidade = TUNEL_VELOCIDADE_INICIAL
    tunel_intervalo = TUNEL_INTERVALO
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

    def reiniciar_jogo():
        nonlocal tunel_velocidade, tunel_intervalo, estado, tuneis, vidas_extras
        nonlocal ultimo_tunel, frame_anterior, inicio_jogo, contador_tuneis
        nonlocal vidas, y_dragao, velocidade, colidindo_agora, colidiu_anteriormente
        nonlocal invulneravel, tempo_invulneravel

        tunel_velocidade = TUNEL_VELOCIDADE_INICIAL
        tunel_intervalo = TUNEL_INTERVALO
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
        nonlocal estado, inicio_jogo, frame_anterior, velocidade
        if key == glfw.KEY_SPACE and action == glfw.PRESS:
            if estado == "inicio":
                estado = "jogando"
                inicio_jogo = time.time()
                frame_anterior = time.time()
                velocidade = IMPULSO
            elif estado == "fim":
                reiniciar_jogo()

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glColor3f(1.0, 1.0, 1.0)
        glDisable(GL_DEPTH_TEST)

        tempo_atual = time.time()
        delta_tempo = tempo_atual - frame_anterior
        frame_anterior = tempo_atual

        if invulneravel and tempo_atual - tempo_invulneravel > 1:
            invulneravel = False

        if estado == "inicio":
            desenhar_fundo(textura_inicio, LARGURA, ALTURA)

            y_flutuante = 300 + 20 * math.sin(tempo_atual * 2)
            desenhar_dragao(textura_dragao, y_flutuante)

            alpha = abs(math.sin(tempo_atual * 3))
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glColor4f(1.0, 1.0, 1.0, alpha)
            desenhar_texto(LARGURA // 2 - 60, ALTURA // 2 - (-50), "START", tamanho=32)
            glColor4f(1.0, 1.0, 1.0, 1.0)

        elif estado == "jogando":
            desenhar_fundo_invertido(textura_jogo, LARGURA, ALTURA)
            desenhar_dragao(textura_dragao, y_dragao)

            if tempo_atual - ultimo_tunel > tunel_intervalo:
                novo_tunel = Tunel(textura_tunel)
                tuneis.append(novo_tunel)

                if contador_tuneis % 5 == 0:
                    abertura_y = (novo_tunel.abertura_superior + novo_tunel.abertura_inferior) / 2
                    y_vida = abertura_y - 16
                    vidas_extras.append(VidaExtra(LARGURA, y_vida, textura_vida))

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

            if contador_tuneis % 10 == 0 and contador_tuneis != 0:
                if (contador_tuneis // 10) > ((contador_tuneis - 1) // 10):
                    tunel_velocidade += 7
                    if contador_tuneis < 20:
                        tunel_intervalo = max(1, tunel_intervalo - 0.1)
                    else:
                        tunel_intervalo = 0.8

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
            for i in range(vidas):
                x_vida = 20 + i * 40
                y_vida = ALTURA - 40
                glBindTexture(GL_TEXTURE_2D, textura_vida)
                glEnable(GL_TEXTURE_2D)

                glBegin(GL_QUADS)
                glTexCoord2f(0.0, 0.0); glVertex2f(x_vida, y_vida)
                glTexCoord2f(1.0, 0.0); glVertex2f(x_vida + 32, y_vida)
                glTexCoord2f(1.0, 1.0); glVertex2f(x_vida + 32, y_vida + 32)
                glTexCoord2f(0.0, 1.0); glVertex2f(x_vida, y_vida + 32)
                glEnd()

                glDisable(GL_TEXTURE_2D)

            desenhar_texto(20, ALTURA - 80, f"Pontos: {contador_tuneis}", tamanho=28)

        elif estado == "fim":
            desenhar_fundo(textura_fim, LARGURA, ALTURA)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()