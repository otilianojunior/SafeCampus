import colored


class PrintUtil:
    @staticmethod
    def print_alunos(alunos):
        print(colored.stylize("Alunos reconhecidos:", colored.bg("yellow") + colored.fg("black")))
        print()
        for aluno in alunos:
            for key, value in aluno.items():
                if key in ("codigo", "nome", "idade", "area", "curso", "hora_entrada"):
                    key = colored.stylize(key, colored.fg("light_blue"))
                    value = colored.stylize(value, colored.fg("green"))
                    print(f"{key}: {value}")
            print()

    @staticmethod
    def print_servidores(servidores):
        print(colored.stylize("Servidores reconhecidos:", colored.bg("yellow") + colored.fg("black")))
        print()
        for servidor in servidores:
            for key, value in servidor.items():
                if key in ("nome", "idade", "area", "curso", "tipo", "hora_entrada"):
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
                if key in ("nome", "idade", "infracao", "hora_entrada"):
                    key = colored.stylize(key, colored.fg("light_blue"))
                    value = colored.stylize(value, colored.fg("green"))
                    print(f"{key}: {value}")
            print()
