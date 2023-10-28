import secrets
import random
import simpy
import face_recognition as facerec
from src.util.JsonUtil import JsonUtil
from src.util.PrintUtil import PrintUtil
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
        return self.load_fotos(self.dir_fotos_alunos)

    def load_fotos_servidores(self):
        return self.load_fotos(self.dir_fotos_servidores)

    def load_fotos_suspeitos(self):
        return self.load_fotos(self.dir_fotos_suspeitos)

    def load_fotos(self, dir_fotos):
        try:
            fotos_util = FotosUtil(dir_fotos)
            fotos = fotos_util.carregar_fotos()
            return fotos
        except Exception as ex:
            raise Exception(f'Erro: Load Fotos {dir_fotos}', ex)

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

    def reconhecer_alunos(self, individuo, configuracao):
        return self.reconhecer_individuos(individuo, configuracao, 'alunos')

    def reconhecer_servidores(self, individuo, configuracao):
        return self.reconhecer_individuos(individuo, configuracao, 'servidores')

    def reconhecer_suspeitos(self, individuo, configuracao):
        return self.reconhecer_individuos(individuo, configuracao, 'suspeitos')

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

                    if total_reconhecidos / len(fotos) >= 0.5:
                        individuos_reconhecidos.append(individuo_config)

            return (len(individuos_reconhecidos) > 0), individuos_reconhecidos
        except Exception as ex:
            raise Exception(f'Erro: Reconhecer {tipo.capitalize()}s', ex)

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

    def imprimir_resultados(self, alunos_reconhecidos, servidores_reconhecidos, suspeitos_reconhecidos):
        try:
            if alunos_reconhecidos[0] is True:
                PrintUtil.print_alunos(alunos_reconhecidos[1])

            if servidores_reconhecidos[0] is True:
                PrintUtil.print_servidores(servidores_reconhecidos[1])

            if suspeitos_reconhecidos[0] is True:
                PrintUtil.print_suspeitos(suspeitos_reconhecidos[1])
        except Exception as ex:
            raise Exception('Erro: Imprimir Resultados', ex)

