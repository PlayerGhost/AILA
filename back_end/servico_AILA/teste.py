import requests
#import json

# Defina os dados de entrada
data = {
    "mensagem": {
        "conteudo": '''O Plenário do Supremo Tribunal Federal, em 27/7/2012, ao julgar o HC n. 111.840/ES, por maioria, declarou incidentalmente a inconstitucionalidade do art. 2º, § 1º Lei n. 8.072/1990, com a redação que lhe foi dada pela Art. 1° Lei n. 11.464/2007, afastando, dessa forma, a obrigatoriedade do regime inicial fechado para os condenados por crimes hediondos e equiparados.'''
    }
}

# Faça a solicitação POST para a API
response = requests.post("http://localhost:5001/aila", json=data)

# Exiba a resposta
print(response.json())
