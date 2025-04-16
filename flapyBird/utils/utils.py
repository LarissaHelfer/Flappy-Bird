from OpenGL.GL import *

def carregar_bmp(caminho):
    with open(caminho, 'rb') as f:
        f.seek(18)
        largura = int.from_bytes(f.read(4), 'little')
        altura = int.from_bytes(f.read(4), 'little')
        f.seek(54)
        dados = f.read()
    return largura, altura, dados

def criar_textura(largura, altura, dados):
    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largura, altura, 0, GL_BGR, GL_UNSIGNED_BYTE, dados)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return textura_id

def desenhar_fundo(textura_id, largura, altura):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex2f(0, 0)
    glTexCoord2f(1.0, 0.0); glVertex2f(largura, 0)
    glTexCoord2f(1.0, 1.0); glVertex2f(largura, altura)
    glTexCoord2f(0.0, 1.0); glVertex2f(0, altura)
    glEnd()
    glDisable(GL_TEXTURE_2D)

