from datetime import time
import random


class DateUtil:
    def turnos_entrada(self):
        try:
            turnos = {
                "manha": [time(7, 30), time(12, 00)],
                "tarde": [time(13, 30), time(18, 00)],
                "noite": [time(18, 30), time(22, 00)]

            }
            return turnos
        except Exception as ex:
            raise Exception('Erro: Turnos Entrada', ex)

    def gerar_horario_entrada(self):
        try:
            turnos = self.turnos_entrada()

            turno_escolhido = random.choice(list(turnos.keys()))
            inicio, fim = turnos[turno_escolhido]

            if random.uniform(0, 1) <= 0.5:
                hora_entrada = inicio
            else:
                while True:
                    hora_entrada = time(random.randint(0, 23), random.randint(0, 59))
                    if inicio < hora_entrada < fim:
                        break

            return hora_entrada
        except Exception as ex:
            raise Exception('Erro: Gerar Horario Entrada', ex)

    def gerar_horario_saida(self, hora_entrada):
        try:
            turnos = self.turnos_entrada()
            horario_saida_maximo = None

            if hora_entrada == turnos["manha"][0]:
                hora_saida = turnos["manha"][1]

            elif hora_entrada == turnos["tarde"][0]:
                hora_saida = turnos["tarde"][1]

            elif hora_entrada == turnos["noite"][0]:
                hora_saida = turnos["noite"][1]

            else:
                if turnos["manha"][0] <= hora_entrada < turnos["manha"][1]:
                    horario_saida_maximo = turnos["manha"][1]

                elif turnos["tarde"][0] <= hora_entrada < turnos["tarde"][1]:
                    horario_saida_maximo = turnos["tarde"][1]

                elif turnos["noite"][0] <= hora_entrada < turnos["noite"][1]:
                    horario_saida_maximo = turnos["noite"][1]

                while True:
                    hora_saida = time(random.randint(0, 23), random.randint(0, 59))
                    if hora_entrada < hora_saida <= horario_saida_maximo:
                        break

            return hora_saida
        except Exception as ex:
            raise Exception('Erro: Gerar Horario Saida', ex)
