import colored
import random
from src.util.JsonUtil import JsonUtil
from src.util.DateUtil import DateUtil
from src.util.PrintUtil import PrintUtil
from src.util.FotosUtil import FotosUtil
from src.config.Configuration import Configuration
from src.gate_campus.Reconhecedor import Reconhecedor


class SafeCampus:
    def __init__(self):
        config = Configuration()
        self.dir_arquivo_configuracao = config.ARQUIVO_CONFIGURACAO
        self.individuos_registrados = {}
        self.PROBABILIDADE_SAIDA = None
        self.TEMPO_MEDIO_PERMANENCIA = None
        self.TEMPO_DETECCAO_INDIVIDUOS = None
        self.TEMPO_LIBERACAO_INDIVIDUOS = None
        self.fotos_portao = None

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
            self.fotos_portao = fotos_portao
            date_util = DateUtil(p_hora_certa=0.5)
            hora_entrada = date_util.gerar_horario_entrada()
            foto = random.choice(self.fotos_portao)
            print(f'Foto escolhida para entrada: {foto}')
            foto_entrada = {
                "foto": foto,
                "hora_entrada": hora_entrada
            }
            return foto_entrada
        except Exception as ex:
            raise Exception('Erro: simular entrada', ex)

    def reconhecer_todas_categorias(self, ambiente_de_simulacao, foto_entrada, configuracao):
        resultados = []

        categorias = ["visitantes", "alunos", "professores", "suspeitos"]

        for categoria in categorias:
            resultados.extend(
                list(getattr(self, f'reconhecer_{categoria}')(ambiente_de_simulacao, foto_entrada, configuracao)))

        novo_foto_entrada = self.simular_entrada(self.fotos_portao)
        resultados.extend(
            list(self.reconhecer_todas_categorias(ambiente_de_simulacao, novo_foto_entrada, configuracao)))

        return resultados

    def reconhecer_visitantes(self, ambiente_de_simulacao, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA, self.TEMPO_DETECCAO_INDIVIDUOS)
        print_function = PrintUtil.print_visitantes
        yield from reconhecedor.reconhecer_individuos(ambiente_de_simulacao, foto_entrada, configuracao, "visitantes", print_function)

    def reconhecer_alunos(self, ambiente_de_simulacao, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA, self.TEMPO_DETECCAO_INDIVIDUOS)
        print_function = PrintUtil.print_alunos
        yield from reconhecedor.reconhecer_individuos(ambiente_de_simulacao, foto_entrada, configuracao, "alunos", print_function)

    def reconhecer_professores(self, ambiente_de_simulacao, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA, self.TEMPO_DETECCAO_INDIVIDUOS)
        print_function = PrintUtil.print_professores
        yield from reconhecedor.reconhecer_individuos(ambiente_de_simulacao, foto_entrada, configuracao, "professores", print_function)

    def reconhecer_suspeitos(self, ambiente_de_simulacao, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA, self.TEMPO_DETECCAO_INDIVIDUOS)
        print_function = PrintUtil.print_suspeitos
        yield from reconhecedor.reconhecer_individuos(ambiente_de_simulacao, foto_entrada, configuracao, "suspeitos", print_function)

    def simula_saida(self, ambiente_de_simulacao):
        while True:
            if len(self.individuos_registrados):
                for id_atendimento, individuo in list(self.individuos_registrados.items()):
                    if ambiente_de_simulacao.now >= individuo["tempo_para_liberacao"]:
                        individuo_saiu = (random.randint(1, 100)) <= self.PROBABILIDADE_SAIDA
                        if individuo_saiu:
                            self.individuos_registrados.pop(id_atendimento)

                            print(colored.fg('white'), colored.bg('green'),
                                  f"O {individuo['tipo']} {individuo['nome']} saiu as ", colored.attr('reset') +'no ambiente de simulação: {ambiente_de_simulacao.now}')

            yield ambiente_de_simulacao.timeout(self.TEMPO_LIBERACAO_INDIVIDUOS)

