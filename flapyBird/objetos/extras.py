from OpenGL.GL import *
import random
import numpy as np
from PIL import Image

class VidaExtra:
    def __init__(self, x, y, textura, largura=32, altura=32):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.textura = textura
        self.visivel = True

    def atualizar(self, velocidade):
        self.x -= velocidade
        if self.x + self.largura < 0:
            self.visivel = False

    def desenhar_vidas(self):
        if not self.visivel:
            return

        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor3f(1.0, 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, self.textura)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(self.x, self.y)
        glTexCoord2f(1, 0); glVertex2f(self.x + self.largura, self.y)
        glTexCoord2f(1, 1); glVertex2f(self.x + self.largura, self.y + self.altura)
        glTexCoord2f(0, 1); glVertex2f(self.x, self.y + self.altura)
        glEnd()

    def checar_colisao_hitbox(self, hitbox):
        if not self.visivel:
            return False

        return (
            self.x < hitbox["x2"] and
            self.x + self.largura > hitbox["x1"] and
            self.y < hitbox["y2"] and
            self.y + self.altura > hitbox["y1"]
        )