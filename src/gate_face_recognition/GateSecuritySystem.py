import face_recognition as reconhecedor
import colored
import secrets
import random
import simpy
import json


class GateSecuritySystem:
    def __int__(self):
        FOTOS_PORTAO = [
            'src/assets/fotos/foto_portao1.jpeg',
            'src/assets/fotos/foto_portao2.jpeg',
            'src/assets/fotos/foto_portao3.jpeg',
            'src/assets/fotos/foto_portao4.jpeg',
            'src/assets/fotos/foto_portao5.jpeg',
            'src/assets/fotos/foto_portao6.jpeg',
            'src/assets/fotos/foto_portao7.jpeg',
            'src/assets/fotos/foto_portao8.jpeg',
            'src/assets/fotos/foto_portao9.jpeg',
            'src/assets/fotos/foto_portao10.jpeg',
            'src/assets/fotos/foto_portao11.jpeg',
            'src/assets/fotos/foto_portao12.jpeg',
            'src/assets/fotos/foto_portao13.jpeg',
            'src/assets/fotos/foto_portao14.jpeg',
            'src/assets/fotos/foto_portao15.jpeg',
            'src/assets/fotos/foto_portao16.jpeg',
            'src/assets/fotos/foto_portao17.jpeg',
            'src/assets/fotos/foto_portao18.jpeg',
            'src/assets/fotos/foto_portao19.jpeg',
            'src/assets/fotos/foto_portao20.jpeg',
            'src/assets/fotos/foto_portao21.jpeg'
        ]
        ARQUIVO_CONFIGURACAO = 'src/config/configuracao.json'

