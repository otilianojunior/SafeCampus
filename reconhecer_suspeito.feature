  Feature: reconhecer suspeitos


  Scenario: Suspeitos chegam em uma instituicao e sao reconhecidos por uma camera.
    Given o ambiente de reconhecimento esta preparado
    When uma foto src/assets/fotos/gate/foto_portao_2.jpeg de um suspeito for capturada
    Then pelo menos, um suspeito deve ser reconhecido

  Scenario: Nao foram reconhecidos suspeitos
    Given o ambiente de reconhecimento esta preparado
    When uma foto src/assets/fotos/gate/foto_portao.jpeg de um suspeito for capturada
    Then Nenhum suspeito deve ser reconhecido