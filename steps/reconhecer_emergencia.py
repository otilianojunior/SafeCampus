from behave import Given, When, Then
from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


@Given('o ambiente de reconhecimento da emergencia esteja preparado')
def given_ambiente_preparado_aluno(contexto):
    preparado, contexto.configuracao = SafeCampus().load_config()

    assert preparado


@When('uma foto {foto} de uma pessoa em emergencia for capturada')
def when_foto_capturada_aluno(contexto, foto):
    contexto.foto_entrada = SafeCampus().simular_entrada([foto])
    contexto.emergencias = SafeCampus().load_fotos(Configuration().DIR_FOTOS_EMERGENCIA)

    assert contexto.foto_entrada is not None


@Then('pelo menos, uma pessoa em emergencia deve ser reconhecida')
def the_aluno_reconhecido(contexto):
    ocorreram_reconhecimentos, contexto.emergencias_reconhecidas = SafeCampus().reconhecer_emergencia(contexto.foto_entrada, contexto.configuracao)

    assert ocorreram_reconhecimentos is True
