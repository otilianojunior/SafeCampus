import json
import os


class JsonUtil:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.file = None

    def load_file(self):
        try:
            script_dir = os.path.dirname(__file__)
            base_dir = os.path.dirname(script_dir)
            full_path = os.path.join(base_dir, self.file_path)
            self.file = open(full_path, 'r')
            self.data = json.load(self.file)
            return True
        except Exception as ex:
            raise Exception('Erro: Load File', ex)

    def carregar_fotos_portao(self):
        portao_dir = 'src/assets/fotos/gate/'
        fotos_portao = []
        for filename in os.listdir(portao_dir):
            if filename.endswith('.jpeg') or filename.endswith('.jpg'):
                foto_path = os.path.join(portao_dir, filename)
                fotos_portao.append(foto_path)
        return fotos_portao

    def __del__(self):
        if self.file:
            self.file.close()
