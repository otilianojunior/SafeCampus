import colored


class PrintUtil:
    @staticmethod
    def print_alunos(alunos):
        print(colored.stylize("Alunos reconhecidos:", colored.bg("yellow") + colored.fg("black")))
        print()
        for aluno in alunos:
            for key, value in aluno.items():
                if key in ("codigo", "nome", "idade", "escola", "casa", "hora_entrada"):
                    key = colored.stylize(key, colored.fg("light_blue"))
                    value = colored.stylize(value, colored.fg("green"))
                    print(f"{key}: {value}")
            print()

    @staticmethod
    def print_professores(professores):
        print(colored.stylize("Professores reconhecidos:", colored.bg("yellow") + colored.fg("black")))
        print()
        for professor in professores:
            for key, value in professor.items():
                if key in ("codigo", "nome", "idade", "escola", "materia", "hora_entrada"):
                    key = colored.stylize(key, colored.fg("light_blue"))
                    value = colored.stylize(value, colored.fg("green"))
                    print(f"{key}: {value}")
            print()

    @staticmethod
    def print_suspeitos(suspeitos):
        print(colored.stylize("Suspeitos reconhecidos:", colored.bg("yellow") + colored.fg("black")))
        print()
        for suspeito in suspeitos:
            for key, value in suspeito.items():
                if key in ("codigo", "nome", "idade", "escola", "casa", "hora_entrada"):
                    key = colored.stylize(key, colored.fg("light_blue"))
                    value = colored.stylize(value, colored.fg("green"))
                    print(f"{key}: {value}")
            print()

    @staticmethod
    def print_visitantes(visitantes):
        print(colored.stylize("Visitantes reconhecidos:", colored.bg("yellow") + colored.fg("black")))
        print()
        for visitante in visitantes:
            for key, value in visitante.items():
                if key in ("codigo", "nome", "idade", "escola", "hora_entrada"):
                    key = colored.stylize(key, colored.fg("light_blue"))
                    value = colored.stylize(value, colored.fg("green"))
                    print(f"{key}: {value}")
            print()
