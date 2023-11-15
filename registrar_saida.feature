  Feature: registrar saida


  Scenario: É salvo os hoários de entrada e saida de um indivíduo.

  Given o ambiente de registro esteja preparado
  When e necessario reconhecer a foto src/assets/fotos/gate/foto_portao.jpeg de algum individuo para que ele saia e registre os horarios
  Then o individuo que entrou na instituicao e saiu e registrado o horario