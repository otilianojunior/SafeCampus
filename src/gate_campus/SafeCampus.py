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
        self.DIR_ARQUIVO_HORARIOS = config.ARQUIVO_HORARIOS
        self.individuos_registrados = {}
        self.PROBABILIDADE_SAIDA = None
        self.TEMPO_MEDIO_PERMANENCIA = None
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
            foto_entrada = {
                "foto": random.choice(self.fotos_portao),
                "hora_entrada": DateUtil().gerar_horario_entrada(),
                "dia": DateUtil().gerar_data()
            }
            PrintUtil.print_foto_entrada(foto_entrada)
            return foto_entrada
        except Exception as ex:
            raise Exception('Erro: simular entrada', ex)

    def reconhecer_todas_categorias(self, foto_entrada, configuracao):
        resultados = []

        categorias = ["alunos", "professores", "suspeitos", "visitantes", "emergencia"]

        for categoria in categorias:
            resultados.extend(list(getattr(self, f'reconhecer_{categoria}')(foto_entrada, configuracao)))

        return resultados

    def reconhecer_alunos(self, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA)
        print_function = PrintUtil.print_alunos
        return reconhecedor.reconhecer_individuos(foto_entrada, configuracao, "alunos", print_function)

    def reconhecer_professores(self, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA)
        print_function = PrintUtil.print_professores
        return reconhecedor.reconhecer_individuos(foto_entrada, configuracao, "professores", print_function)

    def reconhecer_suspeitos(self, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA)
        print_function = PrintUtil.print_suspeitos
        return reconhecedor.reconhecer_individuos(foto_entrada, configuracao, "suspeitos", print_function)

    def reconhecer_visitantes(self, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA)
        print_function = PrintUtil.print_visitantes
        return reconhecedor.reconhecer_individuos(foto_entrada, configuracao, "visitantes", print_function)

    def reconhecer_emergencia(self, foto_entrada, configuracao):
        reconhecedor = Reconhecedor(self.individuos_registrados, self.TEMPO_MEDIO_PERMANENCIA)
        print_function = PrintUtil.print_emergencia
        return reconhecedor.reconhecer_emergencia_total(foto_entrada, configuracao, print_function)

    def simular_saida(self):
        if len(self.individuos_registrados):
            for id_atendimento, individuo in list(self.individuos_registrados.items()):
                individuo_saiu = (random.randint(1, 100)) >= self.PROBABILIDADE_SAIDA
                if individuo_saiu:
                    date_util = DateUtil()
                    hora_entrada = individuo['hora_entrada']
                    individuo['hora_saida'] = date_util.gerar_horario_saida(hora_entrada)
                    PrintUtil.print_saida(individuo)

                    json_util = JsonUtil(self.DIR_ARQUIVO_HORARIOS)
                    json_util.salvar_dados(individuo)

                    del self.individuos_registrados[id_atendimento]
