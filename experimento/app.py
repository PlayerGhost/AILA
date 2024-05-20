from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import os

import socket

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/experimento', methods = ['POST'])
def convert_json_to_csv():
    # Define o nome do arquivo CSV
    fileName = 'pesquisas_data'

    try:
        # Verifica se o conteúdo da requisição é JSON
        if request.is_json:
            data = request.get_json()

            # Verifica se o JSON possui uma lista de dicionários
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):

                # Obtenha o tempo atual
                tempo_atual = datetime.now()

                # Formate a data e hora para o formato desejado
                formato_data_hora = "%d/%m/%Y, %H:%M:%S"
                tempo_formatado = tempo_atual.strftime(formato_data_hora)
                if not os.path.exists(fileName+'.csv'):
                    # cria o arquivo com o resultados da pesquisa
                    df = pd.DataFrame(data)
                    df['horarioRecebido'] = str(tempo_formatado)
                    # print(df)
                    df.to_csv(fileName+".csv", index=False)
                    return jsonify({'message': 'Arquivo CSV gerado com sucesso!', 'filename': fileName})

                else:
                    df = pd.read_csv(fileName+'.csv')
                    df2 = pd.DataFrame(data)
                    df2['horarioRecebido'] = str(tempo_formatado)

                    # se vinher mais de um precisa ter um for
                    # adiciona na ultima linha
                    df.loc[len(df)] = df2.loc[0]

                    # Salva o DataFrame como um arquivo CSV
                    df.to_csv(fileName+".csv", index=False)

                    return jsonify({'message': 'Arquivo CSV gerado com sucesso!', 'filename': fileName})

        # Retorna uma mensagem de erro caso o conteúdo não seja JSON válido
        return jsonify({'error': 'Conteúdo inválido. Envie um JSON válido.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 5002)
