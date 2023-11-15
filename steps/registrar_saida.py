from behave import Given, When, Then
from src.gate_campus.SafeCampus import SafeCampus
from src.config.Configuration import Configuration


@Given('o ambiente de registro esteja preparado')
def given_ambiente_registro_preparado(contexto):
    preparado, contexto.configuracao = SafeCampus().load_config()

    assert preparado


@When('e necessario que alguem entre e reconheca a foto {foto} para que ele saia e registre os horarios')
def when_foto_capturada_registro(contexto, foto):
    contexto.foto_entrada = SafeCampus().simular_entrada([foto])
    contexto.alunos = SafeCampus().load_fotos(Configuration().DIR_FOTOS_ALUNOS)

    assert contexto.foto_entrada is not None


@Then('o individuo que entrou na instituicao saiu e foram registrados o horarios')
def the_registra_horario(contexto):
    ocorreram_reconhecimentos, contexto.alunos_reconhecidos, contexto.individuos_registrados = SafeCampus().reconhecer_alunos(contexto.foto_entrada, contexto.configuracao)
    PROBABILIDADE_SAIDA = 100
    contexto.individuo_saiu = SafeCampus().simular_saida(contexto.individuos_registrados, PROBABILIDADE_SAIDA)

    assert contexto.individuo_saiu is True
