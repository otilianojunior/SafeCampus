from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


if __name__ == "__main__":
    safe_campus = SafeCampus()
    config = Configuration()

    preparado, configuracao = safe_campus.load_config()
    fotos_portao = safe_campus.load_fotos(config.DIR_FOTOS_GATE)
    foto_entrada = safe_campus.simular_entrada(fotos_portao)

    safe_campus.PROBABILIDADE_SAIDA = 60

    safe_campus.reconhecer_alunos(foto_entrada, configuracao)
    safe_campus.reconhecer_professores(foto_entrada, configuracao)
    safe_campus.reconhecer_suspeitos(foto_entrada, configuracao)
    safe_campus.reconhecer_visitantes(foto_entrada, configuracao)
    safe_campus.reconhecer_emergencia(foto_entrada, configuracao)
    # safe_campus.simular_saida()


