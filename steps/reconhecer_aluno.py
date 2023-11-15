from behave import Given, When, Then
from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


@Given('o ambiente de reconhecimento do aluno esteja preparado')
def given_ambiente_preparado_aluno(contexto):
    preparado, contexto.configuracao = SafeCampus().load_config()

    assert preparado


@When('uma foto {foto} de um Aluno for capturada')
def when_foto_capturada_aluno(contexto, foto):
    contexto.foto_entrada = SafeCampus().simular_entrada([foto])
    contexto.alunos = SafeCampus().load_fotos(Configuration().DIR_FOTOS_ALUNOS)

    assert contexto.foto_entrada is not None


@Then('pelo menos, um Aluno deve ser reconhecido')
def the_aluno_reconhecido(contexto):
    ocorreram_reconhecimentos, contexto.alunos_reconhecidos = SafeCampus().reconhecer_alunos(contexto.foto_entrada, contexto.configuracao)

    assert ocorreram_reconhecimentos is True
