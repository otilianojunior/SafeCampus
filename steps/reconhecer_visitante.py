from behave import When, Then
from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


@When('uma foto {foto} de um visitante for capturada')
def when_foto_capturada_visitante(contexto, foto):
    contexto.foto_entrada = SafeCampus().simular_entrada([foto])
    contexto.visitantes = SafeCampus().load_fotos(Configuration().DIR_FOTOS_VISITANTES)

    assert contexto.foto_entrada is not None


@Then('pelo menos, um visitante deve ser reconhecido')
def the_visitante_reconhecido(contexto):
    ocorreram_reconhecimentos, contexto.visitante_reconhecidos, contexto.individuos_registrados = SafeCampus().reconhecer_visitantes(contexto.foto_entrada, contexto.configuracao)

    assert ocorreram_reconhecimentos is True


@Then('Nenhum visitante deve ser reconhecido')
def the_visitante_reconhecido(contexto):
    ocorreram_reconhecimentos, contexto.visitante_reconhecidos, contexto.individuos_registrados = SafeCampus().reconhecer_visitantes(contexto.foto_entrada, contexto.configuracao)

    assert contexto.visitante_reconhecidos == []
