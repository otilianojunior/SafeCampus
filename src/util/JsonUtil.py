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
        portao_dir = 'src/assets/fotos/gate_campus/'
        fotos_portao = []
        for filename in os.listdir(portao_dir):
            if filename.endswith('.jpeg') or filename.endswith('.jpg'):
                foto_path = os.path.join(portao_dir, filename)
                fotos_portao.append(foto_path)
        return fotos_portao

    def salvar_dados(self, individuo):
        try:
            script_dir = os.path.dirname(__file__)
            base_dir = os.path.dirname(script_dir)
            full_path = os.path.join(base_dir, self.file_path)

            if not os.path.exists(full_path):
                with open(full_path, 'w') as file:
                    json.dump([], file)

            with open(full_path, 'r') as file:
                try:
                    self.data = json.load(file)
                except json.decoder.JSONDecodeError:
                    self.data = []

            novo_individuo = {
                'codigo': individuo['codigo'],
                'nome': individuo['nome'],
                'categoria': individuo['tipo'],
                'hora_entrada': individuo['hora_entrada'].strftime('%H:%M:%S'),
                'hora_saida': individuo['hora_saida'].strftime('%H:%M:%S'),
            }

            if self.data is not None:
                self.data.append(novo_individuo)
            else:
                self.data = [novo_individuo]

            with open(full_path, 'w') as file:
                json.dump(self.data, file, indent=2)

        except Exception as ex:
            raise Exception('Erro: Salvar Dados', ex)

    def __del__(self):
        if self.file:
            self.file.close()
