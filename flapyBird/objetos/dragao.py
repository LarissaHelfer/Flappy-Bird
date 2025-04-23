from OpenGL.GL import *
from PIL import Image
import numpy as np

largura = 80
altura_sprite = 80
x = 100

def desenhar_dragao(textura_id, y_dragao):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex2f(x, y_dragao)
    glTexCoord2f(1.0, 0.0); glVertex2f(x + largura, y_dragao)
    glTexCoord2f(1.0, 1.0); glVertex2f(x + largura, y_dragao + altura_sprite)
    glTexCoord2f(0.0, 1.0); glVertex2f(x, y_dragao + altura_sprite)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def carregar_textura(path):
    imagem = Image.open(path)
    imagem = imagem.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(imagem.convert("RGBA"), dtype=np.uint8)

    id_textura = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, id_textura)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, imagem.width, imagem.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return id_textura

def get_hitbox(y_dragao):
    margem = 10 
    return {
        "x1": x + margem,
        "x2": x + largura - margem,
        "y1": y_dragao + margem,
        "y2": y_dragao + altura_sprite - margem
    }