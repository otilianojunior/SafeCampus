  Feature: reconhecer suspeitos


  Scenario: Suspeitos chegam em uma instituicao e sao reconhecidos por uma camera.

  Given o ambiente de reconhecimento do suspeito esteja preparado
  When uma foto src/assets/fotos/gate/foto_portao_2.jpeg de um suspeito for capturada
  Then pelo menos, um suspeito deve ser reconhecido