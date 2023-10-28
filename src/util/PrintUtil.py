import colored


class PrintUtil:
    @staticmethod
    def print_alunos(alunos):
        print(colored.stylize("Indivíduos reconhecidos como alunos:", colored.bg("yellow") + colored.fg("black")))
        print()
        for aluno in alunos:
            for key, value in aluno.items():
                if key in ("codigo", "nome", "idade", "area", "curso"):
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
                if key in ("nome", "idade", "area", "curso", "tipo"):
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
                if key in ("nome", "idade", "infracao"):
                    key = colored.stylize(key, colored.fg("light_blue"))
                    value = colored.stylize(value, colored.fg("green"))
                    print(f"{key}: {value}")
            print()
