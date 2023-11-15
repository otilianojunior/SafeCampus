  Feature: reconhecer professores


  Scenario: Professores chegam em uma instituicao e sao reconhecidos por uma camera.
    Given o ambiente de reconhecimento esta preparado
    When uma foto src/assets/fotos/gate/foto_portao_1.jpeg de um professor for capturada
    Then pelo menos, um professor deve ser reconhecido

  Scenario: Não deve reconhecer nenhum professor.
    Given o ambiente de reconhecimento esta preparado
    When uma foto src/assets/fotos/gate/foto_portao.jpeg de um professor for capturada
    Then Nenhum Professor deve ser reconhecido