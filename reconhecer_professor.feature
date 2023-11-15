  Feature: reconhecer professores


  Scenario: Professores chegam em uma instituicao e sao reconhecidos por uma camera.

  Given o ambiente de reconhecimento do professor esteja preparado
  When uma foto src/assets/fotos/gate/foto_portao_1.jpeg de um professor for capturada
  Then pelo menos, um professor deve ser reconhecido