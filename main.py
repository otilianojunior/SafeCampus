import pymongo
from bson.binary import Binary

# Conecte-se ao servidor MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Acesse o banco de dados "SafeCampusBD"
db = client["SafeCampusBD"]

# Acesse a coleção "alunos"
alunos = db["alunos"]

# Caminho para o arquivo de imagem
caminho_da_imagem = "src/assets/fotos/beatles(1).jpeg"

# Abra o arquivo de imagem
with open(caminho_da_imagem, "rb") as arquivo_imagem:
    # Leia o conteúdo da imagem como dados binários
    dados_binarios = Binary(arquivo_imagem.read())

# Crie um documento para o aluno com a imagem binária
aluno_doc = {
    "nome": "João",
    "matricula": "A12345",
    "curso": "Engenharia",
    "foto": dados_binarios
}

# Insira o documento na coleção "alunos"
alunos.insert_one(aluno_doc)

# Feche a conexão com o servidor MongoDB
client.close()