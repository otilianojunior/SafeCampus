from behave import When, Then
from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


@When('uma foto {foto} de uma pessoa em emergencia for capturada')
def when_foto_capturada_aluno(contexto, foto):
    contexto.foto_entrada = SafeCampus().simular_entrada([foto])
    contexto.emergencias = SafeCampus().load_fotos(Configuration().DIR_FOTOS_EMERGENCIA)

    assert contexto.foto_entrada is not None


@Then('pelo menos, uma pessoa em emergencia deve ser reconhecida')
def the_aluno_reconhecido(contexto):
    ocorreram_reconhecimentos, contexto.emergencias_reconhecidas = SafeCampus().reconhecer_emergencia(contexto.foto_entrada, contexto.configuracao)

    assert ocorreram_reconhecimentos is True


@Then('Nenhuma pessoa deve ser reconhecida em estado de emergencia')
def the_aluno_reconhecido(contexto):
    ocorreram_reconhecimentos, contexto.emergencias_reconhecidas = SafeCampus().reconhecer_emergencia(contexto.foto_entrada, contexto.configuracao)

    assert contexto.emergencias_reconhecidas == []
