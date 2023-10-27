import os


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

    @staticmethod
    def obter_caminho_relativo(caminho_relativo):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.normpath(os.path.join(script_dir, '..', caminho_relativo))
