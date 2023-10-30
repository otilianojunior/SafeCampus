import os
import secrets
from PIL import Image
import numpy as np


class FotosUtil:
    def __init__(self, dir_path):
        self.dir_path = self.obter_caminho_relativo(dir_path)
        self.data = None

    def carregar_fotos(self):
        try:
            fotos = []
            for filename in os.listdir(self.dir_path):
                if filename.endswith('.jpeg') or filename.endswith('.jpg'):
                    foto_path = os.path.join(self.dir_path, filename)
                    fotos.append(foto_path)
            return fotos
        except Exception as ex:
            raise Exception('Erro: Carregar fotos', ex)

    def salvar_foto(self, foto, tipo):
        try:
            nome_arquivo = f"{tipo}_{secrets.token_hex(8)}.jpeg"
            caminho_foto = os.path.join(self.dir_path, nome_arquivo)
            img = Image.fromarray(np.uint8(foto))
            img.save(caminho_foto)
            return caminho_foto
        except Exception as ex:
            raise Exception('Erro: Salvar foto', ex)

    @staticmethod
    def obter_caminho_relativo(caminho_relativo):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.normpath(os.path.join(script_dir, '..', caminho_relativo))
