import colored


class PrintUtil:

    @staticmethod
    def print_foto_entrada(foto_entrada):
        nome_arquivo = foto_entrada['foto'].split('/')[-1].split('.')[0]
        print(colored.stylize(f"Foto da Entrada: {nome_arquivo}, Dia: {foto_entrada['dia']} e Hora: {foto_entrada['hora_entrada']}", colored.bg("yellow") + colored.fg("black")))
        print()


    @staticmethod
    def print_alunos(alunos):
        print(colored.stylize("Aluno reconhecido:", colored.bg("yellow") + colored.fg("black")))
        print()

        for chave, valor in alunos.items():
            if chave != 'fotos':
                chave = colored.stylize(chave, colored.fg("blue"))
                valor = colored.stylize(valor, colored.fg("green"))
                print(f"{chave}: {valor}")

        print()

    @staticmethod
    def print_professores(professores):
        print(colored.stylize("Professor reconhecido:", colored.bg("yellow") + colored.fg("black")))
        print()

        for chave, valor in professores.items():
            if chave != 'fotos':
                chave = colored.stylize(chave, colored.fg("blue"))
                valor = colored.stylize(valor, colored.fg("green"))
                print(f"{chave}: {valor}")

        print()

    @staticmethod
    def print_suspeitos(suspeitos):
        print(colored.stylize("Suspeito reconhecido:", colored.bg("yellow") + colored.fg("black")))
        print()

        for chave, valor in suspeitos.items():
            if chave != 'fotos':
                chave = colored.stylize(chave, colored.fg("blue"))
                valor = colored.stylize(valor, colored.fg("green"))
                print(f"{chave}: {valor}")

        print()

    @staticmethod
    def print_visitantes(visitantes):
        print(colored.stylize("Visitante reconhecido:", colored.bg("yellow") + colored.fg("black")))
        print()

        for chave, valor in visitantes.items():
            if chave != 'fotos':
                chave = colored.stylize(chave, colored.fg("blue"))
                valor = colored.stylize(valor, colored.fg("green"))
                print(f"{chave}: {valor}")

        print()

    @staticmethod
    def print_saida(individuo):
        print(colored.stylize(f"O(A) {individuo['tipo']}(a), {individuo['nome']} saiu às {individuo['hora_saida']} do dia {individuo['dia']}", colored.bg("green") + colored.fg("white")))
        print()
