from behave import Given, When, Then
from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


@Given('o ambiente de reconhecimento de um visitante esteja preparado')
def given_ambiente_preparado_visitante(contexto):
    preparado, contexto.configuracao = SafeCampus().load_config()

    assert preparado


@When('uma foto {foto} de um visitante for capturada')
def when_foto_capturada_visitante(contexto, foto):
    contexto.foto_entrada = SafeCampus().simular_entrada([foto])
    contexto.visitantes = SafeCampus().load_fotos(Configuration().DIR_FOTOS_VISITANTES)

    assert contexto.foto_entrada is not None


@Then('pelo menos, um visitante deve ser reconhecido')
def the_visitante_reconhecido(contexto):
    ocorreram_reconhecimentos, contexto.visitante_reconhecidos = SafeCampus().reconhecer_visitantes(contexto.foto_entrada, contexto.configuracao)

    assert ocorreram_reconhecimentos is True
