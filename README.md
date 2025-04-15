# Projeto Prefect com API Externa
Este projeto tem como objetivo desenvolver scripts em Python utilizando a [biblioteca Prefect](https://docs.prefect.io/v3/get-started) para consumir uma API externa.

A API utilizada neste projeto é a do [Magic: The Gathering](https://docs.magicthegathering.io/).

## Dependências
* Python 3
* Terminal 

> **Observação**:
todos os comandos que vamos executar será no terminal


## Ambiente Virtual
Para rodar o projeto, é necessário criar um ambiente virtual.

**Por que usar ambientes virtuais?**

1. Isolamento de dependências: Cada projeto possui seu próprio conjunto de pacotes e versões, sem interferir com outros projetos ou o Python global.

2. Reprodutibilidade: Você pode gerar um requirements.txt que descreve exatamente o que foi instalado.

3. Segurança e limpeza: Evita poluir o ambiente global com pacotes que são utilizados apenas neste projeto.

4. Gerenciamento de versões do Python: Permite criar ambientes com diferentes versões do Python (caso tenha múltiplas instaladas).

### criando o ambiente
No terminal rode o comando 
```
python3 -m venv prefect-env
```

Você acabou de criar um ambiente virtual chamado **prefect-env**. Para acessa-ló basta acessar:

```
source prefect-env/bin/activate
```
***

## Instalando o Prefect e Rodando o Server

Estando dentro do ambiente virtual poderemos começar a executar o nosso projeto. Vamos executar e visualizar o Prefect localmente. 

Precisamos instalar o prefect para conseguir subir o servidor e ver nosso fluxo de trabalho acontecendo, para isso execute
```
pip install -U prefect
```

Agora podemos executar o server no prefect:

```
prefect server start
```

O server pode ser acessado pelo endereço:
    **<http://127.0.0.1>**

### Executando o projeto

1. rode as bibliotecas de requisitos
```
pip3 install -r requirements.txt
```

2. renomei o arquivo `.env.public` para `.env` apenas

3. rode o arquivo de flow 
```
python3 flows.py
```

## Melhorias:

- [ ] Realizar alguns processamentos e transformações dos dados da API
- [ ] Salvar os dados processados no Firebase
- [ ] Caso seja interessante fazer analises, salvar os dados na Cloud (Prefect ou GCP)
- [ ] Implementar um script para executar o server automaticamente e logo após já executar o arquivo main.py
