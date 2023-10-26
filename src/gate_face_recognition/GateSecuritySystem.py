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
        self.configuracao = None
        self.FOTOS_ALUNOS = None
        self.FOTOS_SUSPEITOS = None

    def load_config(self):
        try:
            json_util = JsonUtil(self.ARQUIVO_CONFIGURACAO)
            preparado = json_util.load_file()
            self.configuracao = json_util.data
            return preparado, self.configuracao
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

    def load_fotos_alunos(self):
        try:
            dir_fotos = 'assets/fotos/alunos'
            fotos_util = FotosUtil(dir_fotos)
            self.FOTOS_ALUNOS = fotos_util.carregar_fotos()
            return self.FOTOS_ALUNOS
        except Exception as ex:
            raise Exception('Erro: Load Fotos Alunos', ex)

    def load_fotos_servidores(self):
        try:
            dir_fotos = 'assets/fotos/servidores'
            fotos_util = FotosUtil(dir_fotos)
            self.FOTOS_SERVIDORES = fotos_util.carregar_fotos()
            return self.FOTOS_SERVIDORES
        except Exception as ex:
            raise Exception('Erro: Load Fotos Servidores', ex)

    def load_fotos_suspeitos(self):
        try:
            dir_fotos = 'assets/fotos/suspeitos'
            fotos_util = FotosUtil(dir_fotos)
            self.FOTOS_SUSPEITOS = fotos_util.carregar_fotos()
            return self.FOTOS_SUSPEITOS
        except Exception as ex:
            raise Exception('Erro: Load Fotos Suspeitos', ex)

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

    def reconhecer_alunos(self, visitante):
        try:
            foto_visitante = reconhecedor.load_image_file(visitante["foto"])
            caracteristicas_visitante = reconhecedor.face_encodings(foto_visitante)

            reconhecidos_alunos = []

            for aluno in self.FOTOS_ALUNOS:
                reconhecido, confianca = self.reconhecer_individual(
                    caracteristicas_visitante, aluno["fotos"])
                if reconhecido:
                    reconhecidos_alunos.append(aluno)

            return reconhecidos_alunos

        except Exception as ex:
            raise Exception('Erro: Reconhecer Alunos', ex)

    def reconhecer_servidores(self, visitante):
        try:
            foto_visitante = reconhecedor.load_image_file(visitante["foto"])
            caracteristicas_visitante = reconhecedor.face_encodings(foto_visitante)

            reconhecidos_servidores = []

            for servidor in self.FOTOS_SERVIDORES:
                reconhecido, confianca = self.reconhecer_individual(
                    caracteristicas_visitante, servidor["fotos"])
                if reconhecido:
                    reconhecidos_servidores.append(servidor)

            return reconhecidos_servidores

        except Exception as ex:
            raise Exception('Erro: Reconhecer Servidores', ex)

    def reconhecer_suspeitos(self, visitante):
        try:

            foto_visitante = reconhecedor.load_image_file(visitante["foto"])
            caracteristicas_visitante = reconhecedor.face_encodings(foto_visitante)

            reconhecidos_suspeitos = []

            for suspeito in self.FOTOS_SUSPEITOS:
                reconhecido, confianca = self.reconhecer_individual(
                    caracteristicas_visitante, suspeito["fotos"])
                if reconhecido:
                    reconhecidos_suspeitos.append(suspeito)

            return reconhecidos_suspeitos

        except Exception as ex:
            raise Exception('Erro: Reconhecer Suspeitos', ex)

    def reconhecer_individual(self, caracteristicas_visitante, fotos_individuo):
        total_de_reconhecimentos = 0

        for foto in fotos_individuo:
            foto = reconhecedor.load_image_file(foto)
            caracteristicas = reconhecedor.face_encodings(foto)

            if not caracteristicas:
                continue

            reconhecimentos = reconhecedor.compare_faces(
                caracteristicas_visitante, caracteristicas)
            if True in reconhecimentos:
                total_de_reconhecimentos += 1

        confianca = total_de_reconhecimentos / len(fotos_individuo) if len(fotos_individuo) > 0 else 0
        reconhecido = confianca >= 0.6

        return reconhecido, confianca


if __name__ == '__main__':
    GATE = GateSecuritySystem()
    GATE.load_config()
