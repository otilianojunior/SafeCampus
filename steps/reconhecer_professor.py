from behave import When, Then
from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


@When('uma foto {foto} de um Professor for capturada')
def when_foto_capturada_professor(contexto, foto):
    contexto.foto_entrada = SafeCampus().simular_entrada([foto])
    contexto.professores = SafeCampus().load_fotos(Configuration().DIR_FOTOS_PROFESSORES)

    assert contexto.foto_entrada is not None


@Then('pelo menos, um Professor deve ser reconhecido')
def the_professor_reconhecido(contexto):
    ocorreram_reconhecimentos, contexto.professores_reconhecidos, contexto.individuos_registrados = SafeCampus().reconhecer_professores(contexto.foto_entrada, contexto.configuracao)

    assert ocorreram_reconhecimentos is True


@Then('Nenhum Professor deve ser reconhecido')
def the_professor_reconhecido(contexto):
    ocorreram_reconhecimentos, contexto.professores_reconhecidos, contexto.individuos_registrados = SafeCampus().reconhecer_professores(contexto.foto_entrada, contexto.configuracao)

    assert contexto.professores_reconhecidos == []
