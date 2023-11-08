import colored
import random
import secrets
import face_recognition as facerec
from src.util.JsonUtil import JsonUtil
from src.util.DateUtil import DateUtil
from src.util.PrintUtil import PrintUtil
from src.util.FotosUtil import FotosUtil
from src.config.Configuration import Configuration


class SafeCampus:
    def __init__(self):
        config = Configuration()
        self.dir_arquivo_configuracao = config.ARQUIVO_CONFIGURACAO
        self.individuos_registrados = {}
        self.PROBABILIDADE_SAIDA = None
        self.TEMPO_MEDIO_PERMANENCIA = None
        self.TEMPO_DETECCAO_INDIVIDUOS = None
        self.TEMPO_LIBERACAO_INDIVIDUOS = None

    def load_config(self):
        try:
            json_util = JsonUtil(self.dir_arquivo_configuracao)
            preparado = json_util.load_file()
            configuracao = json_util.data
            return preparado, configuracao
        except Exception as ex:
            raise Exception('Erro: load config', ex)

    def load_fotos(self, dir_fotos):
        try:
            fotos_util = FotosUtil(dir_fotos)
            fotos = fotos_util.carregar_fotos()
            return fotos
        except Exception as ex:
            raise Exception(f'Erro: Load Fotos {dir_fotos}', ex)

    def simular_entrada(self, fotos_portao):
        try:
            date_util = DateUtil(p_hora_certa=0.5)
            hora_entrada = date_util.gerar_horario_entrada()
            foto = random.choice(fotos_portao)
            print(f'Foto escolhida para entrada: {foto}')
            foto_entrada = {
                "foto": foto,
                "hora_entrada": hora_entrada
            }
            return foto_entrada
        except Exception as ex:
            raise Exception('Erro: simular entrada', ex)

    def individuo_reconhecido_anteriormente(self, foto_entrada):
        reconhecido_previamente = False
        for reconhecido in self.individuos_registrados.values():
            if foto_entrada["codigo"] == reconhecido["codigo"]:
                reconhecido_previamente = True
                break
        return reconhecido_previamente

    def carregar_caracteristicas_rosto(self, foto_entrada):
        foto_individuo = facerec.load_image_file(foto_entrada["foto"])
        caracteristicas_visitante = facerec.face_encodings(foto_individuo)
        return caracteristicas_visitante

    def comparar_caracteristicas(self, caracteristicas_visitante, caracteristicas_registradas):
        reconhecimentos = facerec.compare_faces(caracteristicas_visitante, caracteristicas_registradas)
        return reconhecimentos

    def reconhecer_individuos(self, foto_entrada, configuracao, categoria):
        print("realizando reconhecimento de individuos...")
        caracteristicas_visitante = self.carregar_caracteristicas_rosto(foto_entrada)

        individuos = []
        for individuo in configuracao[categoria]:
            if not self.individuo_reconhecido_anteriormente(individuo):
                fotos = individuo["fotos"]
                total_de_reconhecimentos = 0

                for foto in fotos:
                    foto = facerec.load_image_file(foto)
                    caracteristicas = facerec.face_encodings(foto)[0]
                    reconhecimentos = self.comparar_caracteristicas(caracteristicas_visitante, caracteristicas)
                    if True in reconhecimentos:
                        total_de_reconhecimentos += 1

                if total_de_reconhecimentos / len(fotos) >= 0.6:
                    individuos.append(individuo)
            else:
                print("Individuo reconhecido previamente")

        return (len(individuos) > 0), individuos

    def reconhecer_visitantes(self, ambiente_de_simulacao, foto_entrada,  configuracao):
        while True:
            print(f"tentando reconhecer um visitante no portão, {ambiente_de_simulacao.now}")
            ocorreram_reconhecimentos, individuos = self.reconhecer_individuos(foto_entrada, configuracao, categoria="visitantes")
            if ocorreram_reconhecimentos:
                for individuo in individuos:
                    individuo["hora_entrada"] = foto_entrada['hora_entrada']

                    id_atendimento = secrets.token_hex(nbytes=16).upper()
                    self.individuos_registrados[id_atendimento] = individuo

                    PrintUtil.print_visitantes(individuo)

            yield ambiente_de_simulacao.timeout(self.TEMPO_DETECCAO_INDIVIDUOS)

    def reconhecer_alunos(self, ambiente_de_simulacao, foto_entrada, configuracao):
        while True:
            print(f"tentando reconhecer um aluno no portão, {ambiente_de_simulacao.now}")
            ocorreram_reconhecimentos, individuos = self.reconhecer_individuos(foto_entrada, configuracao, categoria="alunos")
            if ocorreram_reconhecimentos:
                for individuo in individuos:
                    individuo["hora_entrada"] = foto_entrada['hora_entrada']

                    id_atendimento = secrets.token_hex(nbytes=16).upper()
                    self.individuos_registrados[id_atendimento] = individuo

                    PrintUtil.print_alunos(individuo)

            yield ambiente_de_simulacao.timeout(self.TEMPO_DETECCAO_INDIVIDUOS)

    def reconhecer_professores(self, ambiente_de_simulacao, foto_entrada, configuracao):
        while True:
            print(f"tentando reconhecer um professor no portão, {ambiente_de_simulacao.now}")
            ocorreram_reconhecimentos, individuos = self.reconhecer_individuos(foto_entrada, configuracao, categoria="professores")
            if ocorreram_reconhecimentos:
                for individuo in individuos:
                    individuo["hora_entrada"] = foto_entrada['hora_entrada']

                    id_atendimento = secrets.token_hex(nbytes=16).upper()
                    self.individuos_registrados[id_atendimento] = individuo

                    PrintUtil.print_professores(individuo)

            yield ambiente_de_simulacao.timeout(self.TEMPO_DETECCAO_INDIVIDUOS)

    def reconhecer_suspeitos(self, ambiente_de_simulacao, foto_entrada, configuracao):
        while True:
            print(f"tentando reconhecer um suspeito no portão em {ambiente_de_simulacao.now}")
            ocorreram_reconhecimentos, individuos = self.reconhecer_individuos(foto_entrada, configuracao, categoria="suspeitos")
            if ocorreram_reconhecimentos:
                for individuo in individuos:
                    individuo["hora_entrada"] = foto_entrada['hora_entrada']

                    id_atendimento = secrets.token_hex(nbytes=16).upper()
                    self.individuos_registrados[id_atendimento] = individuo

                    PrintUtil.print_suspeitos(individuo)

            yield ambiente_de_simulacao.timeout(self.TEMPO_DETECCAO_INDIVIDUOS)

    def simula_saida(self, ambiente_de_simulacao):
        while True:
            print(f"Individuo saindo da instituição em {ambiente_de_simulacao.now}")

            if len(self.individuos_registrados):
                for id_atendimento, individuo in list(self.individuos_registrados.items()):
                    if ambiente_de_simulacao.now >= individuo["tempo_para_liberacao"]:
                        individuo_saiu = (random.randint(1, 100)) <= self.PROBABILIDADE_SAIDA
                        if individuo_saiu:
                            self.individuos_registrados.pop(id_atendimento)
                            print(colored.fg('white'), colored.bg('green'),
                                  f"O {individuo['tipo']} {individuo['nome']} saiu as ", colored.attr('reset'))

            yield ambiente_de_simulacao.timeout(self.TEMPO_LIBERACAO_INDIVIDUOS)
