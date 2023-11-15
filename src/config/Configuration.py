import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Configuration:
    ARQUIVO_CONFIGURACAO = os.getenv('ARQUIVO_CONFIGURACAO')
    ARQUIVO_HORARIOS = os.getenv('ARQUIVO_HORARIOS')
    DIR_FOTOS_GATE = os.getenv('DIR_FOTOS_GATE')
    DIR_FOTOS_ALUNOS = os.getenv('DIR_FOTOS_ALUNOS')
    DIR_FOTOS_PROFESSORES = os.getenv('DIR_FOTOS_PROFESSORES')
    DIR_FOTOS_SUSPEITOS = os.getenv('DIR_FOTOS_SUSPEITOS')
    DIR_FOTOS_VISITANTES = os.getenv('DIR_FOTOS_VISITANTES')
    DIR_FOTOS_EMERGENCIA = os.getenv('DIR_FOTOS_EMERGENCIA')
