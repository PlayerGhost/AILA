# AILA - Artificial Intelligence Law Assistant

## Como Utilizar:
1. **Instalando os pacotes necessários (parte do back-end):**
    - Certifique-se de ter os seguintes módulos instalados: `request`, `flask`, `flask-cors` e `roman`.
    - Você pode usar o seguinte comando para instalá-los: `pip install request flask flask-cors roman`.

2. **Baixando os arquivos necessários:**
    - **Parte 1:**
        - Baixe o arquivo a seguir: [legislacoes.json](https://unifor-crawler-law.s3.amazonaws.com/data/legislacoes.json) (use Ctrl + S).
        - Após o download, adicione o arquivo à pasta `back_end/servicos_GCL`.
    - **Parte 2:**
        - Baixe os arquivos do link: [arquivos](https://drive.google.com/drive/folders/1ZTJZT-i2BaQnKsHHl57c6kkrVya-RkTd?usp=sharing)
        - Depois de baixar todos os arquivos, mova-os para a pasta `back_end/servicos_AILA`.

3. **Executando o AILA:**
    - Abra o terminal e execute o `app.py` na pasta `back_end/servicos_GCL`.
    - Em seguida, abra outro terminal e execute o `app.py` na pasta `back_end/servicos_AILA`.
    - Feito isso, vá para o arquivo `main.py` na raiz do programa, insira seus textos e execute!

## Estrutura de Saída do AILA:
Após executar o `main.py` com o seu texto, a função retornará um dicionário com a seguinte estrutura:

```python
{
    'extensao': {
        'artigos_e_dispositivos': [
            {
                'marcador': 'LEI n° 9.455',
                'posicao': [[0, 12]],
                'sugestoes': ['LEI n° 9.455/1997'],
                'tipo': 'sugestao_dispositivo'
            }
        ],
        'jurisprudencias_texto': [
            {
                'KGL': True,
                'link': 'https://scon.stj.jus.br/SCON/GetInteiroTeorDoAcordao?num_registro=200901969409&dt_publicacao=25/08/2011',
                'local': 'SP',
                'numero': '1.266.666',
                'posicao': [[20, 53]],
                'tipo_recurso': 'RECURSO ESPECIAL',
                'tribunal': 'STJ'
            }
        ]
    }
}
```