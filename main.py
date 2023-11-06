import simpy
from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


if __name__ == "__main__":
    safe_campus = SafeCampus()
    config = Configuration()

    preparado, configuracao = safe_campus.load_config()
    fotos_portao = safe_campus.load_fotos(config.DIR_FOTOS_GATE)
    alunos = safe_campus.load_fotos(config.DIR_FOTOS_ALUNOS)
    suspeitos = safe_campus.load_fotos(config.DIR_FOTOS_SUSPEITOS)
    professores = safe_campus.load_fotos(config.DIR_FOTOS_PROFESSORES)

    safe_campus.PROBABILIDADE_SAIDA = 30
    safe_campus.TEMPO_MEDIO_PERMANENCIA = 80
    safe_campus.TEMPO_LIBERACAO_INDIVIDUOS = 60
    safe_campus.TEMPO_DETECCAO_INDIVIDUOS = 40

    ambiente_de_simulacao = simpy.Environment()
    ambiente_de_simulacao.process(safe_campus.reconhecer_visitantes(ambiente_de_simulacao, fotos_portao, configuracao))
    ambiente_de_simulacao.process(safe_campus.reconhecer_alunos(ambiente_de_simulacao, alunos, configuracao))
    ambiente_de_simulacao.process(safe_campus.reconhecer_suspeitos(ambiente_de_simulacao, suspeitos, configuracao))
    ambiente_de_simulacao.process(safe_campus.reconhecer_professores(ambiente_de_simulacao, professores, configuracao))

    ambiente_de_simulacao.process(safe_campus.simula_saida(ambiente_de_simulacao))
    ambiente_de_simulacao.run(until=2000)
