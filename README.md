# SafeCampus
> Status do Projeto: Em andamento :heavy_check_mark:

### Descrição
- <p align="justify">Sistema de segurança e monitoramento que supervisiona o acesso à instituição de ensino, proporcionando um controle eficiente e preciso da entrada de alunos e servidores, registrando a presença de forma sistemática e confiável, incluindo o horário de entrada e saída de cada pessoa. Além disso, o sistema é capaz de rastrear a entrada de visitantes, enquanto realiza verificações em tempo real para identificar qualquer pessoa que possa levantar suspeitas. Também integra o processo de 'Alertas de Emergência'.

### Linguagem
<img src="https://img.shields.io/static/v1?label=python&message=Linguagem&color=grenn&style=for-the-badge&logo=PYTHON"/>

### Funcionalidade :clipboard:
- <p align="justify">Reconhecimento Facial Multifacetado: Efetivamente identifica e reconhece as faces de múltiplos indivíduos simultaneamente.</p>
- <p align="justify">Registro de Presença: Registro do horário de entrada e saída de cada pessoa.</p>
- <p align="justify">Rastreamento de Visitantes: Verificação de indivíduos com histórico ou características suspeitas. </p>
- <p align="justify">Alertas de Emergência: Este processo monitora o rosto das pessoas que estão saindo ou entrando para analisar estado de emergência.</p>


### Como Rodar a Aplicação :arrow_forward:

<p align="justify">Caso não tenha, baixe e instale o Python:</p>

```
https://www.python.org/downloads/
```

<p align="justify">No terminal, clone o projeto:</p>

```
git clone https://github.com/otilianojunior/SafeCampus.git
```


<p align="justify">É necessário criar um ambiente virtual (virtual environment - venv), na raiz do projeto:</p>

```
python3 -m venv venv
```
<p align="justify">Ative o ambiente virtual:</p>

```
source venv/bin/activate
```
<p align="justify">Agora é necessário instalar as dependências do projeto:</p>

```
pip install -r requirements.txt
```

<p align="justify">Crie seu arquivo .env seguindo o exemplo do .env.example. </p>

<p align="justify">E por fim execute o arquivo main.py na raiz do projeto:</p>

```
python3 main.py
```