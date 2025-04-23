from PIL import ImageFont, ImageDraw, Image
from OpenGL.GL import *

def carregar_image(caminho):
    try:
        img = Image.open(caminho).convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)
        largura, altura = img.size
        dados = img.tobytes("raw", "RGBA", 0, -1)
        return largura, altura, dados
    except Exception as e:
        raise ValueError(f"Imagem não encontrada")

def criar_textura(largura, altura, dados):
    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, largura, altura, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, dados)
    
    return textura_id

def desenhar_fundo(textura_id, largura, altura):
    glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    glColor4f(1.0, 1.0, 1.0, 1.0)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0); glVertex2f(0, 0)
    glTexCoord2f(1.0, 1.0); glVertex2f(largura, 0)
    glTexCoord2f(1.0, 0.0); glVertex2f(largura, altura)
    glTexCoord2f(0.0, 0.0); glVertex2f(0, altura)
    glEnd()

    glPopAttrib()

def desenhar_fundo_invertido(textura_id, largura, altura):
        glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura_id)

        glColor4f(1.0, 1.0, 1.0, 1.0)

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0);glVertex2f(0, 0)
        glTexCoord2f(1.0, 0.0); glVertex2f(largura, 0)
        glTexCoord2f(1.0, 1.0);glVertex2f(largura, altura)
        glTexCoord2f(0.0, 1.0);glVertex2f(0, altura)
        glEnd()

        glPopAttrib()

def desenhar_texto(x, y, texto, tamanho=24, cor=(255, 255, 255)):
    fonte = ImageFont.truetype("arial.ttf", tamanho)
    
    bbox = fonte.getbbox(texto)
    largura = bbox[2] - bbox[0]
    altura = bbox[3] - bbox[1]

    img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((0, -bbox[1]), texto, font=fonte, fill=cor)

    dados = img.transpose(Image.FLIP_TOP_BOTTOM).tobytes()
    glRasterPos2f(x, y)
    glDrawPixels(largura, altura, GL_RGBA, GL_UNSIGNED_BYTE, dados)
