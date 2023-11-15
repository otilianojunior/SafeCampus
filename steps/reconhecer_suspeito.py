from behave import Given, When, Then
from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


@Given('o ambiente de reconhecimento do suspeito esteja preparado')
def given_ambiente_preparado_suspeito(contexto):
    preparado, contexto.configuracao = SafeCampus().load_config()

    assert preparado


@When('uma foto {foto} de um suspeito for capturada')
def when_foto_capturada_suspeito(contexto, foto):
    contexto.foto_entrada = SafeCampus().simular_entrada([foto])
    contexto.suspeitos = SafeCampus().load_fotos(Configuration().DIR_FOTOS_SUSPEITOS)

    assert contexto.foto_entrada is not None


@Then('pelo menos, um suspeito deve ser reconhecido')
def the_suspeito_reconhecido(contexto):
    ocorreram_reconhecimentos, contexto.suspeitos_reconhecidos = SafeCampus().reconhecer_suspeitos(contexto.foto_entrada, contexto.configuracao)

    assert ocorreram_reconhecimentos is True
