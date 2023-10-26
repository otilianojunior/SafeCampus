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
            fotos_alunos = self.load_fotos_alunos()
            fotos_servidores = self.load_fotos_servidores()
            fotos_suspeitos = self.load_fotos_suspeitos()

            individuo = self.simular_entrada(fotos_portao)
            alunos_reconhecidos = self.reconhecer_alunos(individuo, configuracao)
            servidores_reconhecidos = self.reconhecer_servidores(individuo, fotos_servidores)
            suspeitos_reconhecidos = self.reconhecer_suspeitos(individuo, fotos_suspeitos)
            self.reconhecer_visitante_nao_identificado(individuo, fotos_alunos, fotos_servidores, fotos_suspeitos)

            self.imprimir_resultados(individuo, alunos_reconhecidos, servidores_reconhecidos, suspeitos_reconhecidos)
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
                'aluno': None,
                'servidor': None,
                'suspeito': None,
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

    def reconhecer_alunos(self, individuo, configuracao):
        try:
            foto_individuo = facerec.load_image_file(individuo["foto"])
            caracteristicas_visitante = facerec.face_encodings(foto_individuo)

            alunos_reconhecidos = []

            for aluno in configuracao['alunos']:
                if self.individuo_reconhecido_anteriormente(aluno):
                    print(f'Aluno {aluno["nome"]}, já foi reconhecido anteriormente')
                else:
                    fotos = aluno['fotos']
                    total_alunos_reconhecidos = 0
                    for foto in fotos:
                        foto = facerec.load_image_file(foto)
                        caracteristicas = facerec.face_encodings(foto)
                        if caracteristicas:
                            reconhecimentos = facerec.compare_faces(caracteristicas_visitante, caracteristicas[0])
                            if True in reconhecimentos:
                                total_alunos_reconhecidos += 1

                    if total_alunos_reconhecidos / len(fotos) >= 0.6:
                        alunos_reconhecidos.append(aluno)

            return (len(alunos_reconhecidos) > 0), alunos_reconhecidos
        except Exception as ex:
            raise Exception('Erro: Reconhecer Alunos', ex)

    def reconhecer_servidores(self, individuo, configuracao):
        try:
            foto_individuo = facerec.load_image_file(individuo["foto"])
            caracteristicas_visitante = facerec.face_encodings(foto_individuo)

            servidores_reconhecidos = []

            for servidor in configuracao['servidores']:
                if self.individuo_reconhecido_anteriormente(servidor):
                    print(f'Servidor {servidor["nome"]}, já foi reconhecido anteriormente')
                else:
                    fotos = servidor['fotos']
                    total_servidores_reconhecidos = 0
                    for foto in fotos:
                        foto = facerec.load_image_file(foto)
                        caracteristicas = facerec.face_encodings(foto)
                        if caracteristicas:
                            for caracteristica in caracteristicas:
                                reconhecimentos = facerec.compare_faces(caracteristicas_visitante, caracteristica)
                                if True in reconhecimentos:
                                    total_servidores_reconhecidos += 1

                    if total_servidores_reconhecidos / len(fotos) >= 0.6:
                        servidores_reconhecidos.append(servidor)

            return (len(servidores_reconhecidos) > 0), servidores_reconhecidos
        except Exception as ex:
            raise Exception('Erro: Reconhecer Servidores', ex)

    def reconhecer_suspeitos(self, visitante, fotos_suspeitos):
        try:

            foto_visitante = facerec.load_image_file(visitante["foto"])
            caracteristicas_visitante = facerec.face_encodings(foto_visitante)

            reconhecidos_suspeitos = []

            for suspeito in fotos_suspeitos:
                reconhecido, confianca = self.reconhecer_individual(caracteristicas_visitante, suspeito["fotos"])
                if reconhecido:
                    reconhecidos_suspeitos.append(suspeito)

            return reconhecidos_suspeitos
        except Exception as ex:
            raise Exception('Erro: Reconhecer Suspeitos', ex)

    def reconhecer_individual(self, caracteristicas_visitante, fotos_individuo):
        try:
            total_de_reconhecimentos = 0
            for foto in fotos_individuo:
                foto = facerec.load_image_file(foto)
                caracteristicas = facerec.face_encodings(foto)

                if not caracteristicas:
                    continue

                reconhecimentos = facerec.compare_faces(
                    caracteristicas_visitante, caracteristicas)
                if True in reconhecimentos:
                    total_de_reconhecimentos += 1

            confianca = total_de_reconhecimentos / len(fotos_individuo) if len(fotos_individuo) > 0 else 0
            reconhecido = confianca >= 0.6
            return reconhecido, confianca
        except Exception as ex:
            raise Exception('Erro: reconhecer individual', ex)

    def reconhecer_visitante_nao_identificado(self, visitante, fotos_alunos, fotos_servidores, fotos_suspeitos):
        try:
            alunos_reconhecidos = self.reconhecer_alunos(visitante, fotos_alunos)
            servidores_reconhecidos = self.reconhecer_servidores(visitante, fotos_servidores)
            suspeitos_reconhecidos = self.reconhecer_suspeitos(visitante, fotos_suspeitos)

            if not alunos_reconhecidos and not servidores_reconhecidos and not suspeitos_reconhecidos:
                return True
            else:
                return False
        except Exception as ex:
            raise Exception('Erro: reconhecer visitante nao identificado', ex)

    def imprimir_resultados(self, visitante, alunos_reconhecidos, servidores_reconhecidos, suspeitos_reconhecidos):
        try:
            print("Resultado para o visitante:")
            print(f"Foto: {visitante['foto']}")
            if alunos_reconhecidos:
                print("Visitante reconhecido como aluno:")
                for aluno in alunos_reconhecidos:
                    print("Matrícula:", aluno['matricula'])
                    print("Nome:", aluno['nome'])
                    print("Idade:", aluno['idade'])
                    print("Área:", aluno['area'])
                    print("Curso:", aluno['curso'])
                    print()

            if servidores_reconhecidos:
                print("Visitante reconhecido como servidor:")
                for servidor in servidores_reconhecidos:
                    print("Nome:", servidor['nome'])
                    print("Cargo:", servidor['cargo'])
                    print("Idade:", servidor['idade'])
                    print("Área:", servidor['area'])
                    print("Curso:", servidor['curso'])
                    print("Tipo:", servidor['tipo'])
                    print()

            if suspeitos_reconhecidos:
                print("Visitante reconhecido como suspeito:")
                for suspeito in suspeitos_reconhecidos:
                    print("Nome:", suspeito['nome'])
                    print("Idade:", suspeito['idade'])
                    print("Infracao:", suspeito['infracao'])
                    print()
        except Exception as ex:
            raise Exception('Erro: Imprimir Resultados', ex)
