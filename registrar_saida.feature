  Feature: registrar saida


  Scenario: É salvo os hoários de entrada e saida de um indivíduo.
    Given o ambiente de reconhecimento esta preparado
    When uma foto src/assets/fotos/gate/foto_portao.jpeg de um Aluno for capturada
    Then o individuo que entrou na instituicao tem a probabilidade 100 de sair, e ser registrados seus horarios de entrada e saida

  Scenario: É salvo os hoários de entrada e saida de um indivíduo, mas se tiver a probabilidade baixa nao sai.
    Given o ambiente de reconhecimento esta preparado
    When uma foto src/assets/fotos/gate/foto_portao.jpeg de um Aluno for capturada
    Then nem sempre os individuos saem no mesmo turno ou horario, podem ocorrer de nao sair, probabilidade 0
