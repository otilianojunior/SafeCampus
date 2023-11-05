import simpy
import random
import face_recognition as facerec
from src.util.JsonUtil import JsonUtil
from src.util.DateUtil import DateUtil
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
        self.dir_fotos_visitantes = config.DIR_FOTOS_VISITANTES
        self.individuos_registrados = {}

    def main(self):
        try:
            preparado, configuracao = self.load_config()

            fotos_portao = self.load_fotos(self.dir_fotos_gate)
            self.load_fotos(self.dir_fotos_alunos)
            self.load_fotos(self.dir_fotos_servidores)
            self.load_fotos(self.dir_fotos_suspeitos)

            foto_entrada = self.simular_entrada(fotos_portao)
            self.recorta_salva_rostos(foto_entrada)

            alunos_reconhecidos = self.reconhecer_individuos(foto_entrada, configuracao, tipo='alunos')
            servidores_reconhecidos = self.reconhecer_individuos(foto_entrada, configuracao, tipo='servidores')
            suspeitos_reconhecidos = self.reconhecer_individuos(foto_entrada, configuracao, tipo='suspeitos')

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

    def load_fotos(self, dir_fotos):
        try:
            fotos_util = FotosUtil(dir_fotos)
            fotos = fotos_util.carregar_fotos()
            return fotos
        except Exception as ex:
            raise Exception(f'Erro: Load Fotos {dir_fotos}', ex)

    def detectar_rostos(self, imagem):
        face_locations = facerec.face_locations(imagem)
        return face_locations

    def carregar_caracteristicas_rosto(self, foto):
        foto_individuo = facerec.load_image_file(foto)
        caracteristicas_visitante = facerec.face_encodings(foto_individuo)
        return caracteristicas_visitante

    def comparar_caracteristicas(self, caracteristicas_visitante, caracteristicas_registradas):
        reconhecimentos = facerec.compare_faces(caracteristicas_visitante, caracteristicas_registradas)
        return reconhecimentos

    def recortar_rostos(self, imagem, face_locations):
        rostos = [imagem[top:bottom, left:right] for top, right, bottom, left in face_locations]
        return rostos

    def salvar_rostos(self, rostos, diretorio_saida):
        fotos_util = FotosUtil(diretorio_saida)
        caminhos_arquivos = [fotos_util.salvar_imagem_rosto(rosto) for rosto in rostos]
        return caminhos_arquivos

    def recorta_salva_rostos(self, foto_entrada):
        try:
            imagem = facerec.load_image_file(foto_entrada['foto'])
            face_locations = self.detectar_rostos(imagem)
            rostos = self.recortar_rostos(imagem, face_locations)
            caminhos_arquivos = self.salvar_rostos(rostos, self.dir_fotos_visitantes)
            return caminhos_arquivos
        except Exception as ex:
            raise Exception('Erro: separa fotos', ex)

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
            raise Exception('Erro: simular visita', ex)

    def reconhecer_individuos(self, foto_entrada, configuracao, tipo):
        try:
            caracteristicas_visitante = self.carregar_caracteristicas_rosto(foto_entrada["foto"])
            individuos_reconhecidos = []

            for individuo_config in configuracao[tipo]:
                if self.individuo_reconhecido_anteriormente(individuo_config):
                    print(f'{tipo.capitalize()} {individuo_config["nome"]}, já foi reconhecido anteriormente')
                else:
                    fotos = individuo_config['fotos']
                    total_reconhecidos = 0

                    for foto in fotos:
                        caracteristicas = self.carregar_caracteristicas_rosto(foto)
                        if caracteristicas:
                            reconhecimentos = self.comparar_caracteristicas(caracteristicas_visitante, caracteristicas[0])
                            if True in reconhecimentos:
                                total_reconhecidos += 1

                    if total_reconhecidos / len(fotos) >= 0.5:
                        individuo_config['hora_entrada'] = foto_entrada["hora_entrada"]
                        individuos_reconhecidos.append(individuo_config)

            return (len(individuos_reconhecidos) > 0), individuos_reconhecidos
        except Exception as ex:
            raise Exception(f'Erro: Reconhecer {tipo.capitalize()}s', ex)

    def individuo_reconhecido_anteriormente(self, foto_entrada):
        try:
            reconhecido = False
            for individuo_reconhecido in self.individuos_registrados.values():
                if foto_entrada['codigo'] == individuo_reconhecido['codigo']:
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
