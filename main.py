import requests
#import json

#Execute apenas depois das duas APIs estarem em execução!

# Defina os dados de entrada
data = {
    "mensagem": {
        # conteudo para ser avaliado!
        "conteudo": '''LEI n° 9.455, 1997. STJ RECURSO ESPECIAL 1.266.666 SP'''
    }
}

# Faça a solicitação POST para a API
response = requests.post("http://localhost:5001/aila", json=data)

# Exiba a resposta
print(response.json())