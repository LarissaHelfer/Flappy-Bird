from config import *
import random
from OpenGL.GL import *

class Tunel:
    def __init__(self):
        self.x = LARGURA
        self.width = TUNEL_LARGURA
        self.gap_y = random.randint(150, ALTURA - 150)
        self.passed = False

    def atualiza(self, delta_tempo):
        self.x -= TUNEL_VELOCIDADE * delta_tempo

    def esta_tela(self):
        return self.x + self.width < 0

    def verifica_colisao(self, limites):
        cx1, cy1, cx2, cy2 = limites
        eixo_x = cx2 > self.x and cx1 < self.x + self.width
        topo_colisao = cy2 > self.gap_y + TUNEL_GAP / 2
        baixo_colisao = cy1 < self.gap_y - TUNEL_GAP / 2
        return eixo_x and (topo_colisao or baixo_colisao)

    def desenha(self):
        glColor3f(0.0, 1.0, 0.0)

        glBegin(GL_QUADS)
        glVertex2f(self.x, self.gap_y + TUNEL_GAP / 2)
        glVertex2f(self.x + self.width, self.gap_y + TUNEL_GAP / 2)
        glVertex2f(self.x + self.width, ALTURA)
        glVertex2f(self.x, LARGURA)
        glEnd()

        glBegin(GL_QUADS)
        glVertex2f(self.x, 0)
        glVertex2f(self.x + self.width, 0)
        glVertex2f(self.x + self.width, self.gap_y - TUNEL_GAP / 2)
        glVertex2f(self.x, self.gap_y - TUNEL_GAP / 2)
        glEnd()
