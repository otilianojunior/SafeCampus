import face_recognition as facerec
import secrets


class Reconhecedor:
    def __init__(self, individuos_registrados, TEMPO_MEDIO_PERMANENCIA, TEMPO_DETECCAO_INDIVIDUOS):
        self.individuos_registrados = individuos_registrados
        self.TEMPO_MEDIO_PERMANENCIA = TEMPO_MEDIO_PERMANENCIA
        self.TEMPO_DETECCAO_INDIVIDUOS = TEMPO_DETECCAO_INDIVIDUOS

    def reconhecer_individuos(self, ambiente_de_simulacao, foto_entrada, configuracao, categoria, print_function):
        print(f"tentando reconhecer {categoria} no portão...")
        ocorreram_reconhecimentos, individuos = self.reconhecer_individuos_aux(foto_entrada, configuracao, categoria)
        if ocorreram_reconhecimentos:
            for individuo in individuos:
                individuo["hora_entrada"] = foto_entrada['hora_entrada']

                tempo_liberacao = ambiente_de_simulacao.now + self.TEMPO_MEDIO_PERMANENCIA
                individuo["tempo_para_liberacao"] = tempo_liberacao

                id_atendimento = secrets.token_hex(nbytes=16).upper()
                self.individuos_registrados[id_atendimento] = individuo

                print_function(individuo)

                yield individuo

        yield ambiente_de_simulacao.timeout(self.TEMPO_DETECCAO_INDIVIDUOS)


    def reconhecer_individuos_aux(self, foto_entrada, configuracao, categoria):
        caracteristicas_visitante = self.carregar_caracteristicas_rosto(foto_entrada)

        individuos = []
        for individuo in configuracao[categoria]:
            if not self.individuo_reconhecido_anteriormente(individuo):
                fotos = individuo["fotos"]
                total_de_reconhecimentos = 0

                for foto in fotos:
                    foto = facerec.load_image_file(foto)
                    caracteristicas = facerec.face_encodings(foto)
                    if caracteristicas:
                        caracteristicas = caracteristicas[0]
                        reconhecimentos = self.comparar_caracteristicas(caracteristicas_visitante, caracteristicas)
                        if True in reconhecimentos:
                            total_de_reconhecimentos += 1

                if total_de_reconhecimentos / len(fotos) >= 0.6:
                    individuos.append(individuo)
            else:
                print("Individuo reconhecido previamente")

        return (len(individuos) > 0), individuos

    def individuo_reconhecido_anteriormente(self, foto_entrada):
        reconhecido_previamente = False
        for reconhecido in self.individuos_registrados.values():
            if foto_entrada["codigo"] == reconhecido["codigo"]:
                reconhecido_previamente = True
                break
        return reconhecido_previamente

    def carregar_caracteristicas_rosto(self, foto_entrada):
        foto_individuo = facerec.load_image_file(foto_entrada["foto"])
        caracteristicas_visitante = facerec.face_encodings(foto_individuo)
        return caracteristicas_visitante

    def comparar_caracteristicas(self, caracteristicas_visitante, caracteristicas_registradas):
        reconhecimentos = facerec.compare_faces(caracteristicas_visitante, caracteristicas_registradas)
        return reconhecimentos
