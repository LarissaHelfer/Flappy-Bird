from config import *
import random
from OpenGL.GL import *

class Tunel:
    def __init__(self):
        self.x = LARGURA
        self.largura = TUNEL_LARGURA
        self.gap_y = random.randint(150, ALTURA - 150)
        self.passou = False

    def atualiza(self, delta_tempo):
        self.x -= TUNEL_VELOCIDADE * delta_tempo

    def esta_tela(self):
        return self.x + self.largura < 0

    def verifica_colisao(self, hitbox_dragao):
        # Pega os limites do dragão
        x1 = hitbox_dragao["x1"]
        x2 = hitbox_dragao["x2"]
        y1 = hitbox_dragao["y1"]
        y2 = hitbox_dragao["y2"]

        topo_gap = self.gap_y + TUNEL_GAP / 2
        base_gap = self.gap_y - TUNEL_GAP / 2

        dentro_horizontal = (x2 > self.x) and (x1 < self.x + self.largura)

        colidiu_cima = y2 > topo_gap
        colidiu_baixo = y1 < base_gap

        if dentro_horizontal and (colidiu_cima or colidiu_baixo):
            return True

        return False

    def desenha(self):
        glPushAttrib(GL_ENABLE_BIT)
        
        glDisable(GL_TEXTURE_2D)
        glColor3f(0.0, 1.0, 0.0)
        
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.gap_y + TUNEL_GAP / 2)
        glVertex2f(self.x + self.largura, self.gap_y + TUNEL_GAP / 2)
        glVertex2f(self.x + self.largura, ALTURA)
        glVertex2f(self.x, ALTURA)
        glEnd()
        
        glBegin(GL_QUADS)
        glVertex2f(self.x, 0)
        glVertex2f(self.x + self.largura, 0)
        glVertex2f(self.x + self.largura, self.gap_y - TUNEL_GAP / 2)
        glVertex2f(self.x, self.gap_y - TUNEL_GAP / 2)
        glEnd()
        
        glPopAttrib()