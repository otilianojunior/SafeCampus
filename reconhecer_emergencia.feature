  Feature: reconhecer emergencias


  Scenario: individuos em Emergencia chegam em uma instituicao e sao reconhecidos por uma camera.

  Given o ambiente de reconhecimento da emergencia esteja preparado
  When uma foto src/assets/fotos/gate/foto_portao_6.jpeg de uma pessoa em emergencia for capturada
  Then pelo menos, uma pessoa em emergencia deve ser reconhecida