import face_recognition as facerec
import secrets


class Reconhecedor:
    def __init__(self, individuos_registrados):
        self.individuos_registrados = individuos_registrados

    def reconhecer_individuos(self, foto_entrada, configuracao, categoria, print_function):
        print(f"tentando reconhecer {categoria} no portão...")
        ocorreram_reconhecimentos, individuos = self.reconhecer_individuos_aux(foto_entrada, configuracao, categoria)

        if ocorreram_reconhecimentos:
            for individuo in individuos:
                individuo["hora_entrada"] = foto_entrada['hora_entrada']
                individuo["dia"] = foto_entrada['dia']

                id_atendimento = secrets.token_hex(nbytes=16).upper()
                self.individuos_registrados[id_atendimento] = individuo
                print_function(individuo)
        return ocorreram_reconhecimentos, individuos, self.individuos_registrados

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
                print("Indivíduo já reconhecido")

        return True, individuos

    def individuo_reconhecido_anteriormente(self, individuo):
        reconhecido_previamente = False
        for reconhecido in self.individuos_registrados.values():
            if individuo["codigo"] == reconhecido["codigo"]:
                reconhecido_previamente = True
                break
        return reconhecido_previamente

    def reconhecer_emergencia_total(self, foto_entrada, configuracao, print_function):
        print("Tentando reconhecer emergência no portão...")
        ocorreram_reconhecimentos, individuos = self.reconhecer_individuos_aux(foto_entrada, configuracao, "emergencia")

        if ocorreram_reconhecimentos:
            for individuo in individuos:
                print_function(individuo)

        return ocorreram_reconhecimentos, individuos

    def carregar_caracteristicas_rosto(self, foto_entrada):
        foto_individuo = facerec.load_image_file(foto_entrada["foto"])
        caracteristicas_visitante = facerec.face_encodings(foto_individuo)
        return caracteristicas_visitante

    def comparar_caracteristicas(self, caracteristicas_visitante, caracteristicas_registradas):
        reconhecimentos = facerec.compare_faces(caracteristicas_visitante, caracteristicas_registradas)
        return reconhecimentos
