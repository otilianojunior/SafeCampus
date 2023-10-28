from datetime import datetime, time, timedelta
import random


class DateUtil:
    def gerar_horario_entrada(self):
        turnos = {
            "manha": (time(8, 0), time(12, 0)),
            "tarde": (time(13, 0), time(18, 0)),
            "noite": (time(18, 30), time(22, 0))
        }

        # Escolha um turno aleatório
        turno_escolhido = random.choice(list(turnos.keys()))
        intervalo_escolhido = turnos[turno_escolhido]

        # Gere uma hora aleatória dentro do intervalo escolhido
        hora_entrada = datetime.combine(datetime.today(), intervalo_escolhido[0])
        minutos_aleatorios = random.randint(0, (intervalo_escolhido[1].hour - intervalo_escolhido[0].hour) * 60)
        hora_entrada += timedelta(minutes=minutos_aleatorios)

        return hora_entrada

    def gerar_horario_saida(self, hora_entrada):
        # Obtenha o limite máximo de saída como 22:00
        limite_maximo_saida = time(22, 0)

        # Gere um horário de saída aleatório que seja após o horário de entrada
        hora_saida = datetime.combine(datetime.today(), limite_maximo_saida)

        while hora_saida <= hora_entrada or hora_saida.hour >= 22:
            minutos_aleatorios = random.randint(0, (limite_maximo_saida.hour - hora_entrada.time().hour) * 60)
            hora_saida = datetime.combine(datetime.today(), hora_entrada.time()) + timedelta(minutes=minutos_aleatorios)

        return hora_saida


# Exemplo de uso:
date_util = DateUtil()
hora_entrada = date_util.gerar_horario_entrada()
hora_saida = date_util.gerar_horario_saida(hora_entrada)

print(f"Hora de entrada: {hora_entrada.strftime('%H:%M')}")
print(f"Hora de saída: {hora_saida.strftime('%H:%M')}")
