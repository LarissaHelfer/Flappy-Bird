from OpenGL.GL import *
import random
import numpy as np
from PIL import Image

caminho = "assets/vida.png"

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
        glTexCoord2f(0, 1); glVertex2f(self.x, self.y)
        glTexCoord2f(1, 1); glVertex2f(self.x + self.largura, self.y)
        glTexCoord2f(1, 0); glVertex2f(self.x + self.largura, self.y + self.altura)
        glTexCoord2f(0, 0); glVertex2f(self.x, self.y + self.altura)
        glEnd()

    def checar_colisao(self, dragao):
        if not self.visivel:
            return False
        return (
            self.x < dragao.x + dragao.largura and
            self.x + self.largura > dragao.x and
            self.y < dragao.y + dragao.altura and
            self.y + self.altura > dragao.y
        )

def carregar_textura(caminho):
    imagem = Image.open(caminho)
    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = imagem.convert("RGBA").tobytes()
    largura, altura = imagem.size

    textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return textura
