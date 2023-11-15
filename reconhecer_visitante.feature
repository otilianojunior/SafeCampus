  Feature: reconhecer visitantes


  Scenario: Visitantes chegam em uma instituicao e sao reconhecidos por uma camera.

  Given o ambiente de reconhecimento de um visitante esteja preparado
  When uma foto src/assets/fotos/gate/foto_portao_3.jpeg de um visitante for capturada
  Then pelo menos, um visitante deve ser reconhecido