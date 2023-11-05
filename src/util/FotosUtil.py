import os
import secrets
from PIL import Image


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

    def salvar_imagem_rosto(self, rosto):
        try:
            token = secrets.token_hex(16)
            nome_arquivo = f"rosto_{token}.jpg"
            imagem_rosto = Image.fromarray(rosto)
            caminho_arquivo = os.path.join(self.dir_path, nome_arquivo)
            imagem_rosto.save(caminho_arquivo)
            return caminho_arquivo
        except Exception as ex:
            raise Exception('Erro: Salvar imagem de rosto', ex)

    @staticmethod
    def obter_caminho_relativo(caminho_relativo):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.normpath(os.path.join(script_dir, '..', caminho_relativo))
