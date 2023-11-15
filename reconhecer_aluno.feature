  Feature: reconhecer alunos


  Scenario: Alunos chegam em uma instituicao e sao reconhecidos por uma camera.
    Given o ambiente de reconhecimento esta preparado
    When uma foto src/assets/fotos/gate/foto_portao.jpeg de um Aluno for capturada
    Then pelo menos, um Aluno deve ser reconhecido

  Scenario: Nao foram reconhecidos alunos
    Given o ambiente de reconhecimento esta preparado
    When uma foto src/assets/fotos/gate/foto_portao_6.jpeg de um Aluno for capturada
    Then Nenhum Aluno deve ser reconhecido