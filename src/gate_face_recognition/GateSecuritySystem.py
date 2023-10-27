import colored
import secrets
import random
import simpy
import face_recognition as facerec
from src.util.JsonUtil import JsonUtil
from src.util.FotosUtil import FotosUtil
from src.config.Configuration import Configuration


class GateSecuritySystem:
    def __init__(self):
        config = Configuration()
        self.dir_arquivo_configuracao = config.ARQUIVO_CONFIGURACAO
        self.dir_fotos_gate = config.DIR_FOTOS_GATE
        self.dir_fotos_alunos = config.DIR_FOTOS_ALUNOS
        self.dir_fotos_servidores = config.DIR_FOTOS_SERVIDORES
        self.dir_fotos_suspeitos = config.DIR_FOTOS_SUSPEITOS
        self.individuos_registrados = {}

    def main(self):
        try:
            preparado, configuracao = self.load_config()
            fotos_portao = self.load_fotos_gate()
            self.load_fotos_alunos()
            self.load_fotos_servidores()
            self.load_fotos_suspeitos()

            individuo = self.simular_entrada(fotos_portao)
            alunos_reconhecidos = self.reconhecer_alunos(individuo, configuracao)
            servidores_reconhecidos = self.reconhecer_servidores(individuo, configuracao)
            suspeitos_reconhecidos = self.reconhecer_suspeitos(individuo, configuracao)

            self.imprimir_resultados(alunos_reconhecidos, servidores_reconhecidos, suspeitos_reconhecidos)
        except Exception as ex:
            raise Exception("Erro: em GateSecurity System", ex)

    def load_config(self):
        try:
            json_util = JsonUtil(self.dir_arquivo_configuracao)
            preparado = json_util.load_file()
            configuracao = json_util.data
            return preparado, configuracao
        except Exception as ex:
            raise Exception('Erro: load config', ex)

    def load_fotos_gate(self):
        try:
            fotos_util = FotosUtil(self.dir_fotos_gate)
            fotos_portao = fotos_util.carregar_fotos()
            return fotos_portao
        except Exception as ex:
            raise Exception('Erro: Load Fotos Gate', ex)

    def load_fotos_alunos(self):
        try:
            fotos_util = FotosUtil(self.dir_fotos_alunos)
            fotos_alunos = fotos_util.carregar_fotos()
            return fotos_alunos
        except Exception as ex:
            raise Exception('Erro: Load Fotos Servidores', ex)

    def load_fotos_servidores(self):
        try:
            fotos_util = FotosUtil(self.dir_fotos_servidores)
            fotos_servidores = fotos_util.carregar_fotos()
            return fotos_servidores
        except Exception as ex:
            raise Exception('Erro: Load Fotos Servidores', ex)

    def load_fotos_suspeitos(self):
        try:
            fotos_util = FotosUtil(self.dir_fotos_suspeitos)
            fotos_suspeitos = fotos_util.carregar_fotos()
            return fotos_suspeitos
        except Exception as ex:
            raise Exception('Erro: Load Fotos Suspeitos', ex)

    def simular_entrada(self, fotos_portao):
        try:
            foto = random.choice(fotos_portao)
            individuo = {
                "foto": foto,
                'alunos': None,
                'servidores': None,
                'suspeitos': None,
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
            raise Exception('Erro: Individuo Reconhecido Anteriormente', ex)

    def reconhecer_individuos(self, individuo, configuracao, tipo):
        try:
            foto_individuo = facerec.load_image_file(individuo["foto"])
            caracteristicas_visitante = facerec.face_encodings(foto_individuo)

            individuos_reconhecidos = []

            for individuo_config in configuracao[tipo]:
                if self.individuo_reconhecido_anteriormente(individuo_config):
                    print(f'{tipo.capitalize()} {individuo_config["nome"]}, já foi reconhecido anteriormente')
                else:
                    fotos = individuo_config['fotos']
                    total_reconhecidos = 0

                    for foto in fotos:
                        foto = facerec.load_image_file(foto)
                        caracteristicas = facerec.face_encodings(foto)
                        if caracteristicas:
                            reconhecimentos = facerec.compare_faces(caracteristicas_visitante, caracteristicas[0])
                            if True in reconhecimentos:
                                total_reconhecidos += 1

                    if total_reconhecidos / len(fotos) >= 0.6:
                        individuos_reconhecidos.append(individuo_config)

            return (len(individuos_reconhecidos) > 0), individuos_reconhecidos
        except Exception as ex:
            raise Exception(f'Erro: Reconhecer {tipo.capitalize()}s', ex)

    def reconhecer_alunos(self, individuo, configuracao):
        return self.reconhecer_individuos(individuo, configuracao, 'alunos')

    def reconhecer_servidores(self, individuo, configuracao):
        return self.reconhecer_individuos(individuo, configuracao, 'servidores')

    def reconhecer_suspeitos(self, individuo, configuracao):
        return self.reconhecer_individuos(individuo, configuracao, 'suspeitos')

    def imprimir_resultados(self, alunos_reconhecidos, servidores_reconhecidos, suspeitos_reconhecidos):
        try:
            if alunos_reconhecidos[0] is True:
                print("Indivíduos reconhecidos como alunos:")
                for aluno in alunos_reconhecidos[1]:
                    print("Matrícula:", aluno['codigo'])
                    print("Nome:", aluno['nome'])
                    print("Idade:", aluno['idade'])
                    print("Área:", aluno['area'])
                    print("Curso:", aluno['curso'])
                    print()

            if servidores_reconhecidos[0] is True:
                print("Servidores reconhecidos:")
                for servidor in servidores_reconhecidos[1]:
                    print("Nome:", servidor['nome'])
                    print("Idade:", servidor['idade'])
                    print("Área:", servidor['area'])
                    print("Curso:", servidor['curso'])
                    print("Tipo:", servidor['tipo'])
                    print()

            if suspeitos_reconhecidos[0] is True:
                print("Suspeitos reconhecidos:")
                for suspeito in suspeitos_reconhecidos[1]:
                    print("Nome:", suspeito['nome'])
                    print("Idade:", suspeito['idade'])
                    print("Infracao:", suspeito['infracao'])
                    print()
        except Exception as ex:
            raise Exception('Erro: Imprimir Resultados', ex)

