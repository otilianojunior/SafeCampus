import face_recognition as reconhecedor
import colored
import secrets
import random
import simpy
from src.util.JsonUtil import JsonUtil
from src.util.FotosUtil import FotosUtil


class GateSecuritySystem:
    def __init__(self):
        self.FOTOS_PORTAO = None
        self.ARQUIVO_CONFIGURACAO = 'config/configuracao.json'
        self.individuos_registrados = {}

    def load_config(self):
        try:
            json_util = JsonUtil(self.ARQUIVO_CONFIGURACAO)
            preparado = json_util.load_file()
            configuracao = json_util.data
            return preparado, configuracao
        except Exception as ex:
            raise Exception('Erro: load config', ex)

    def load_fotos_gate(self):
        try:
            dir_fotos = 'assets/fotos/gate'
            fotos_util = FotosUtil(dir_fotos)
            self.FOTOS_PORTAO = fotos_util.carregar_fotos()
            return self.FOTOS_PORTAO
        except Exception as ex:
            raise Exception('Erro: Load Fotos Gate', ex)

    def simular_entrada(self):
        try:
            foto = random.choice(self.FOTOS_PORTAO)
            individuo = {
                "foto": foto,
                'aluno': None,
                'servidor': None
            }
            return individuo
        except Exception as ex:
            raise Exception('Erro: simular visita', ex)

    def individuo_reconhecido_anteriormente(self, individuo):
        try:
            reconhecido = False
            for individuo_reconhecido in self.individuos_registrados.values():
                if individuo['codigo'] == individuo_reconhecido['codigo']:
                    reconhecido = True
                    break
            return reconhecido
        except Exception as ex:
            raise Exception('Erro: INdividuo Reconhecido Anteriormente', ex)

    def reconhecer_individuos(self, visitantes, configuracao):
        try:
            print('Realizando reconhecimento de pacientes...')
            fotos_visitantes = reconhecedor.load_image_file(visitantes['foto'])
            caracteristicas_visitantes = reconhecedor.face_encodings(fotos_visitantes)

            pacientes_encontrados = []
            for individuo in configuracao['pacientes']:
                if self.individuo_reconhecido_anteriormente(individuo):
                    print(f'Paciente {individuo["nome"]}, já foi reconhecido anteriormente')
                else:
                    fotos = individuo['fotos']
                    total_reconhecimentos = 0

                    for foto in fotos:
                        foto = reconhecedor.load_image_file(foto)
                        caracteristicas = reconhecedor.face_encodings(foto)[0]

                        reconhecimentos = reconhecedor.compare_faces(
                            caracteristicas_visitantes, caracteristicas
                        )

                        if True in reconhecimentos:
                            total_reconhecimentos += 1

                    if total_reconhecimentos / len(fotos) >= 0.6:
                        pacientes_encontrados.append(reconhecedor)

            return (len(pacientes_encontrados) > 0), pacientes_encontrados
        except Exception as ex:
            raise Exception('Erro: Reconhecer Pacientes', ex)


if __name__ == '__main__':
    GATE = GateSecuritySystem()
    GATE.load_config()

