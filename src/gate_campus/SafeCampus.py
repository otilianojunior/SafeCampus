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
        self.DIR_ARQUIVO_HORARIOS = config.ARQUIVO_HORARIOS

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
            foto_entrada = {
                "foto": random.choice(self.fotos_portao),
                "hora_entrada": DateUtil().gerar_horario_entrada(),
                "dia": DateUtil().gerar_data()
            }
            PrintUtil.print_foto_entrada(foto_entrada)
            return foto_entrada
        except Exception as ex:
            raise Exception('Erro: simular entrada', ex)

    def reconhecer_todas_categorias(self, ambiente_de_simulacao, foto_entrada, configuracao):
        resultados = []

        categorias = ["alunos", "professores", "suspeitos", "visitantes"]

        for categoria in categorias:
            resultados.extend(list(getattr(self, f'reconhecer_{categoria}')(ambiente_de_simulacao, foto_entrada, configuracao)))

        return resultados

    def reconhecer_alunos(self, ambiente_de_simulacao, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA, self.TEMPO_DETECCAO_INDIVIDUOS, self.PROBABILIDADE_SAIDA)
        print_function = PrintUtil.print_alunos
        yield from reconhecedor.reconhecer_individuos(ambiente_de_simulacao, foto_entrada, configuracao, "alunos", print_function)

    def reconhecer_professores(self, ambiente_de_simulacao, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA, self.TEMPO_DETECCAO_INDIVIDUOS, self.PROBABILIDADE_SAIDA)
        print_function = PrintUtil.print_professores
        yield from reconhecedor.reconhecer_individuos(ambiente_de_simulacao, foto_entrada, configuracao, "professores", print_function)

    def reconhecer_suspeitos(self, ambiente_de_simulacao, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA, self.TEMPO_DETECCAO_INDIVIDUOS, self.PROBABILIDADE_SAIDA)
        print_function = PrintUtil.print_suspeitos
        yield from reconhecedor.reconhecer_individuos(ambiente_de_simulacao, foto_entrada, configuracao, "suspeitos", print_function)

    def reconhecer_visitantes(self, ambiente_de_simulacao, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA, self.TEMPO_DETECCAO_INDIVIDUOS, self.PROBABILIDADE_SAIDA)
        print_function = PrintUtil.print_visitantes
        yield from reconhecedor.reconhecer_individuos(ambiente_de_simulacao, foto_entrada, configuracao, "visitantes", print_function)

    def simular_saida(self, ambiente_de_simulacao, configuracao):
        while True:
            print(f"Indivíduo tentando sair da instituição em {ambiente_de_simulacao.now}")

            if len(self.individuos_registrados):
                for id_atendimento, individuo in list(self.individuos_registrados.items()):
                    if individuo["tempo_para_liberacao"] and ambiente_de_simulacao.now >= individuo["tempo_para_liberacao"]:
                        individuo_saiu = (random.randint(1, 100)) >= self.PROBABILIDADE_SAIDA
                        if individuo_saiu:
                            date_util = DateUtil()
                            hora_entrada = individuo['hora_entrada']
                            individuo['hora_saida'] = date_util.gerar_horario_saida(hora_entrada)
                            PrintUtil.print_saida(individuo)

                            json_util = JsonUtil(self.DIR_ARQUIVO_HORARIOS)
                            json_util.salvar_dados(individuo)

                            del self.individuos_registrados[id_atendimento]
                        else:
                            novo_foto_entrada = self.simular_entrada(self.fotos_portao)
                            yield from self.reconhecer_todas_categorias(ambiente_de_simulacao, novo_foto_entrada, configuracao)
            yield ambiente_de_simulacao.timeout(self.TEMPO_LIBERACAO_INDIVIDUOS)
