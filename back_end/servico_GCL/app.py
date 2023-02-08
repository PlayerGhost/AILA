from Legis_Class import Legis
from flask import Flask, request
from main import consulta_texto_lei, dic_leis


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        tipo = int(get_request(request, "tipo"))
        lei = get_request(request, "lei")
        ano = int(get_request(request, "ano"))

        artigo = get_request(request, "artigo")
        arg_artigo = get_request(request, "complemento")
        paragrafo = get_request(request, "paragrafo")
        inciso = get_request(request, "inciso")
        alinea = get_request(request, "alinea")
        item = get_request(request, "item")

        legislacao = (tipo, lei, ano, artigo, arg_artigo, paragrafo, inciso, alinea, item)
        resultado = consulta_texto_lei(dic_leis, legislacao)

        if resultado is None:
            return 'None'

        return f'{resultado}'.encode().decode()

    if request.method == 'POST':
        tipo = int(post_request(request, "tipo"))
        lei = post_request(request, "lei")
        ano = int(post_request(request, "ano"))

        artigo = post_request(request, "artigo")
        arg_artigo = post_request(request, "complemento")
        paragrafo = post_request(request, "paragrafo")
        inciso = post_request(request, "inciso")
        alinea = post_request(request, "alinea")
        item = post_request(request, "item")

        legislacao = (tipo, lei, ano, artigo, arg_artigo, paragrafo, inciso, alinea, item)
        resultado = consulta_texto_lei(dic_leis, legislacao)

        if resultado is None:
            return 'None'

        return f'{resultado}'.encode().decode()


def get_request(method, key_type):
    key = method.args.get(key_type)
    if key is None:
        key = '0'
        return key
    else:
        return key


def post_request(method, key_type):
    key = method.form.get(key_type)
    if key is None:
        key = '0'
        return key
    else:
        return key


app.run(host='localhost', port=5000)


# http://localhost:5000/?tipo=1&lei=301

# http://localhost:5000/?tipo=0&lei=90&artigo=1&item=1

# http://localhost:5000/?tipo=0&lei=9.455&ano=1997&artigo=1&paragrafo=1

# http://localhost:5000/?tipo=0&lei=10.406&ano=2002&artigo=49&complemento=A

# http://localhost:5000/?tipo=0&lei=8.078&data=11/09/1990&artigo=81&complemento=0&paragrafo=unico&inciso=III

# http://localhost:5000/?tipo=0&lei=10.406&ano=2002&artigo=44&complemento=0&paragrafo=2&inciso=0&alinea=0&item=0

# http://localhost:5000/?tipo=0&lei=10.406&ano=2002&artigo=1.000&complemento=0&paragrafo=0&inciso=0&alinea=0&item=0

# https://d012-2804-248-fb70-4f00-cefb-b234-b407-966.sa.ngrok.io/?tipo=0&lei=12.826&ano=2013&artigo=4&complemento=0&paragrafo=2&inciso=II&alinea=0&item=0

# http://localhost:5000/?tipo=0&lei=12.826&ano=2013&artigo=4&complemento=0&paragrafo=2&inciso=II&alinea=0&item=0

# http://localhost:5000//?tipo=0&lei=10.736&ano=2003&artigo=1&complemento=0&paragrafo=2&inciso=0&alinea=0&item=0

# http://localhost:5000//?tipo=0&lei=14.166&ano=2021&artigo=6&complemento=0&paragrafo=7&inciso=ii&alinea=b&item=2

# http://localhost:5000/?tipo=0&lei=10.736&ano=2003&artigo=1&complemento=0&paragrafo=2&inciso=0&alinea=0&item=0

# https://fe0b-2804-248-fb82-d600-91e6-1b93-de29-4fd2.sa.ngrok.io/?tipo=0&lei=12.587&ano=2012&artigo=17&complemento=0&paragrafo=unico&inciso=0&alinea=0&item=0

# https://fe0b-2804-248-fb82-d600-91e6-1b93-de29-4fd2.sa.ngrok.io/?tipo=0&lei=14.166&ano=2021&artigo=6&complemento=0&paragrafo=7&inciso=ii&alinea=b&item=2

# https://fe0b-2804-248-fb82-d600-91e6-1b93-de29-4fd2.sa.ngrok.io/?tipo=0&lei=8.078&ano=1990&artigo=4&complemento=0&paragrafo=0&inciso=ii&alinea=d&item=0
