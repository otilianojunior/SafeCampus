from behave import Then
from src.gate_campus.SafeCampus import SafeCampus


@Then('o individuo que entrou na instituicao tem a probabilidade {probabilidade} de sair, e ser registrados seus horarios de entrada e saida')
def the_registra_horario(contexto, probabilidade):
    ocorreram_reconhecimentos, contexto.alunos_reconhecidos, contexto.individuos_registrados = SafeCampus().reconhecer_alunos(contexto.foto_entrada, contexto.configuracao)
    contexto.individuo_saiu = SafeCampus().simular_saida(contexto.individuos_registrados, int(probabilidade))

    assert contexto.individuo_saiu is True


@Then('nem sempre os individuos saem no mesmo turno ou horario, podem ocorrer de nao sair, probabilidade {probabilidade}')
def the_registra_horario(contexto, probabilidade):
    ocorreram_reconhecimentos, contexto.alunos_reconhecidos, contexto.individuos_registrados = SafeCampus().reconhecer_alunos(contexto.foto_entrada, contexto.configuracao)
    contexto.individuo_saiu = SafeCampus().simular_saida(contexto.individuos_registrados, int(probabilidade))

    assert contexto.individuo_saiu is False