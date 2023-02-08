from flask import Flask, request, render_template
from flask_cors import CORS
from main import AILA

app = Flask(__name__)
CORS(app)

@app.route('/aila', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        dado_entrada_json = request.get_json()
        
        texto = dado_entrada_json['mensagem']['conteudo']
        dado_saida_json = AILA(texto)

        return dado_saida_json
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True, port = 5001)