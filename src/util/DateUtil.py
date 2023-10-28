from datetime import datetime, time, timedelta
import random

class DateUtil:
    def gerar_horario_entrada(self):
        intervalos = [
            (time(8, 0), time(12, 0)),
            (time(13, 30), time(18, 0)),
            (time(18, 30), time(22, 0))
        ]

        # Escolha um intervalo aleatório
        intervalo_escolhido = random.choice(intervalos)

        # Gere uma hora aleatória dentro do intervalo escolhido
        hora_entrada = datetime.combine(datetime.today(), intervalo_escolhido[0])
        minutos_aleatorios = random.randint(0, (intervalo_escolhido[1].hour - intervalo_escolhido[0].hour) * 60)
        hora_entrada += timedelta(minutes=minutos_aleatorios)

        return hora_entrada

    def gerar_horario_saida(self, hora_entrada):
        # Defina o limite máximo de saída como 22:00
        limite_maximo_saida = time(22, 0)

        while True:
            hora_saida = datetime.combine(datetime.today(), limite_maximo_saida)
            # Adicione um valor aleatório entre 60 e 240 minutos (1 a 4 horas)
            minutos_aleatorios = random.randint(60, 240)
            hora_saida += timedelta(minutes=minutos_aleatorios)

            if hora_entrada < hora_saida:
                return hora_saida

# Exemplo de uso:
date_util = DateUtil()
hora_entrada = date_util.gerar_horario_entrada()
hora_saida = date_util.gerar_horario_saida(hora_entrada)

print(f"Hora de entrada: {hora_entrada.strftime('%H:%M')}")
print(f"Hora de saída: {hora_saida.strftime('%H:%M')}")
