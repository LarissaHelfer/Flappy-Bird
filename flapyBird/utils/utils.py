from OpenGL.GL import *
import struct

def carregar_bmp(caminho):
    try:
        with open(caminho, 'rb') as f:
            if f.read(2) != b'BM':
                raise ValueError("Não é um arquivo BMP válido")
            
            f.seek(28)
            bits_por_pixel = struct.unpack('<H', f.read(2))[0]
            
            if bits_por_pixel != 24:
                raise ValueError(f"O BMP deve ter 24 bits por pixel (encontrado: {bits_por_pixel})")
            
            f.seek(18)
            largura = struct.unpack('<i', f.read(4))[0]
            altura = struct.unpack('<i', f.read(4))[0]
            
            f.seek(54)
            
            bytes_por_linha = largura * 3
            padding = (4 - (bytes_por_linha % 4)) % 4
            
            dados = bytearray()
            for linha_num in range(altura-1, -1, -1):
                f.seek(54 + (bytes_por_linha + padding) * linha_num)
                dados.extend(f.read(bytes_por_linha))
            
        return largura, altura, bytes(dados)
    
    except Exception as e:
        raise ValueError(f"Erro ao carregar BMP {caminho}: {str(e)}")

def criar_textura(largura, altura, dados):
    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largura, altura, 0,
                GL_BGR, GL_UNSIGNED_BYTE, dados)
    
    return textura_id

def desenhar_fundo(textura_id, largura, altura):
    glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT)
    
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textura_id)
    
    glColor3f(1.0, 1.0, 1.0)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0); glVertex2f(0, 0)
    glTexCoord2f(1.0, 1.0); glVertex2f(largura, 0)
    glTexCoord2f(1.0, 0.0); glVertex2f(largura, altura)
    glTexCoord2f(0.0, 0.0); glVertex2f(0, altura)
    glEnd()
    
    glPopAttrib()