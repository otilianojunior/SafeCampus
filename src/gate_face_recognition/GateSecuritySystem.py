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
        self.FOTOS_SERVIDORES = None

    def main(self):
        try:
            self.load_config()
            self.load_fotos_gate()
            self.load_fotos_alunos()
            self.load_fotos_servidores()
            self.load_fotos_suspeitos()

            visitante = self.simular_entrada()
            alunos_reconhecidos = self.reconhecer_alunos(visitante)
            servidores_reconhecidos = self.reconhecer_servidores(visitante)
            suspeitos_reconhecidos = self.reconhecer_suspeitos(visitante)

            self.imprimir_resultados(visitante, alunos_reconhecidos, servidores_reconhecidos, suspeitos_reconhecidos)
        except Exception as ex:
            raise Exception("Erro: em GateSecurity System", ex)

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
        try:
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
        except Exception as ex:
            raise Exception('Erro: reconhecer individual', ex)

    def reconhecer_visitante_nao_identificado(self, visitante):
        try:
            alunos_reconhecidos = self.reconhecer_alunos(visitante)
            servidores_reconhecidos = self.reconhecer_servidores(visitante)
            suspeitos_reconhecidos = self.reconhecer_suspeitos(visitante)

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
            raise Exception('Erro: Imprimir Resultados',ex)


if __name__ == '__main__':
    SafeCampus = GateSecuritySystem()
    SafeCampus.main()


