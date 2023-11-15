  Feature: reconhecer alunos


  Scenario: Alunos chegam em uma instituicao e sao reconhecidos por uma camera.

  Given o ambiente de reconhecimento do aluno esteja preparado
  When uma foto src/assets/fotos/gate/foto_portao.jpeg de um Aluno for capturada
  Then pelo menos, um Aluno deve ser reconhecido