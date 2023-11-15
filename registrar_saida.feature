  Feature: registrar saida


  Scenario: É salvo os hoários de entrada e saida de um indivíduo.

  Given o ambiente de registro esteja preparado
  When e necessario que alguem entre e reconheca a foto src/assets/fotos/gate/foto_portao.jpeg para que ele saia e registre os horarios
  Then o individuo que entrou na instituicao tem a probabilidade 100 de sair, e ser registrados seus horarios de entrada e saida
