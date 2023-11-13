from datetime import time
import random
import calendar


class DateUtil:

    def gerar_data(self):
        try:
            ano = random.randint(1900, 2023)
            mes = random.randint(1, 12)
            dias_no_mes = calendar.monthrange(ano, mes)[1]
            dia = random.randint(1, dias_no_mes)

            return f"{dia:02d}/{mes:02d}/{ano}"
        except Exception as ex:
            raise Exception('Erro: Gerar Data Dia da Semana', ex)

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

            # Encontrar o turno correspondente à hora de entrada
            turno_correspondente = None
            for turno, intervalo in turnos.items():
                if intervalo[0] <= hora_entrada <= intervalo[1]:
                    turno_correspondente = turno
                    break

            if turno_correspondente is not None:
                hora_saida = turnos[turno_correspondente][1]
            else:
                # Se não houver correspondência direta com um turno, gerar aleatoriamente
                horario_saida_maximo = None
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
