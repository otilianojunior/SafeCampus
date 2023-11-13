import simpy
from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


if __name__ == "__main__":
    safe_campus = SafeCampus()
    config = Configuration()

    preparado, configuracao = safe_campus.load_config()
    fotos_portao = safe_campus.load_fotos(config.DIR_FOTOS_GATE)
    foto_entrada = safe_campus.simular_entrada(fotos_portao)

    alunos = safe_campus.load_fotos(config.DIR_FOTOS_ALUNOS)
    professores = safe_campus.load_fotos(config.DIR_FOTOS_PROFESSORES)
    suspeitos = safe_campus.load_fotos(config.DIR_FOTOS_SUSPEITOS)
    visitantes = safe_campus.load_fotos(config.DIR_FOTOS_VISITANTES)

    safe_campus.PROBABILIDADE_SAIDA = 55
    safe_campus.TEMPO_MEDIO_PERMANENCIA = 60
    safe_campus.TEMPO_LIBERACAO_INDIVIDUOS = 60
    safe_campus.TEMPO_DETECCAO_INDIVIDUOS = 40

    ambiente_de_simulacao = simpy.Environment()
    ambiente_de_simulacao.process(safe_campus.reconhecer_alunos(ambiente_de_simulacao, foto_entrada, configuracao))
    ambiente_de_simulacao.process(safe_campus.reconhecer_professores(ambiente_de_simulacao, foto_entrada, configuracao))
    ambiente_de_simulacao.process(safe_campus.reconhecer_suspeitos(ambiente_de_simulacao, foto_entrada, configuracao))
    ambiente_de_simulacao.process(safe_campus.reconhecer_visitantes(ambiente_de_simulacao, foto_entrada, configuracao))
    ambiente_de_simulacao.process(safe_campus.simular_saida(ambiente_de_simulacao, configuracao))

    ambiente_de_simulacao.run(until=500)

