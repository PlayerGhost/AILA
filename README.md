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

## Estrutura de Entrada do AILA:

{
    "mensagem": {
        "conteudo": ESTADO DO CEARÁ
                    PODER JUDICIÁRIO
                    TRIBUNAL DE JUSTIÇA
                    FÓRUM DAS TURMAS RECURSAIS PROF. DOLOR BARREIRA
                    1Ş Turma Recursal
                    ACÓRDÃO
                    Nº PROCESSO: 3000887-45.2018.8.06.0167
                    CLASSE: RECURSO INOMINADO CÍVEL
                    RECORRENTE: ALCIDES FERNANDES DA SILVA
                    RECORRIDO: BANCO BMG SA
                    PROCLAMAÇÃO DO JULGAMENTO:
                    Acordam os membros da 1Ş Turma Recursal dos Juizados Especiais Cíveis e Criminais do Estado do Ceará, por unanimidade de votos, tomar conhecimento do                             Recurso Inominado, para NEGAR-LHE provimento, conforme Acórdão lavrado pelo Juiz Relator.
                    PROCESSO nº. 3000887-45.2018.8.06.0167 (PJE)
                    RECURSO INOMINADO
                    RECORRENTE: ALCIDES FERNANDES DA SILVA
                    RECORRIDO (A): BANCO BMG SA
                    ORIGEM: JUIZADO ESPECIAL CÍVEL E CRIMINAL DA COMARCA DE SOBRAL
                    JUIZ RELATOR: IRANDES BASTOS SALES
                    SÚMULA DE JULGAMENTO. DIREITO DO CONSUMIDOR. AÇÃO ANULATÓRIA DE CONTRATO C/C REPETIÇÃO DE INDÉBITO C/C REPARAÇÃO DE DANOS MORAIS. CONTRATO DE EMPRÉSTIMO                         CONSIGNADO. ALTERAÇÃO DA VERDADE REAL. ILEGITIMIDADE PASSIVA DA INSTITUIÇÃO FINANCEIRA ALEGADA PELA RECORRIDA. HIPOSSUFICIÊNCIA TÉCNICA E JURÍDICA                           DO CONSUMIDOR. TEORIA DA APARÊNCIA.  LEGITIMIDADE DAQUELE QUE SE APRESENTA COMO PRESTADOR DO SERVIÇO. LEGITIMIDADE CONFIGURADA. PRELIMINAR                                   REJEITADA. VERIFICADA EXISTÊNCIA DA CONTRATAÇÃO EM PRIMEIRO GRAU. TRÂNSITO EM JULGADO DE TAL CAPÍTULO DA SENTENÇA. INSURGÊNICA QUANTO À MULTA POR 
                        LITIGÂNCIA DE MÁ-FÉ. ALTERAÇÃO DA VERDADE DOS FATOS. HIPÓTESE PREVISTA NO ART. 80, INCISO II, DO CPCB. MANUTENÇÃO DA MULTA DE 2% (DOIS POR CENTO),                           POR LITIGÂNCIA DE MÁ-FÉ APLICADA NO PRIMEIRO GRAU. RECURSO INOMINADO CONHECIDO E IMPROVIDO. SENTENÇA DE ORIGEM MANTIDA POR SEUS PRÓPRIOS E JURÍDICOS                         FUNDAMENTOS.
                    ACÓRDÃO
                        Os membros da Primeira Turma Recursal dos Juizados Especiais Cíveis e Criminais do Estado do Ceará, por unanimidade de votos, e nos termos da                                 manifestação do Juiz relator, acordam em CONHECER E NEGAR PROVIMENTO ao recurso inominado - RI, mantendo-se a sentença vergastada.
                    Condeno a parte recorrente vencida a pagar custas e honorários advocatícios em 20% (vinte por cento) do valor atualizado da causa (art. 55, Lei                              9.099/95), com a exigibilidade suspensa na forma do art. 98, §3º do CPC.
                    Fortaleza, CE., 21 de julho de 2020.
                    Bel. Irandes Bastos Sales
                    Juiz Relator
                    RELATÓRIO E VOTO
                    Trata-se de Ação Anulatória De Contrato C/C Repetição De Indébito C/C Reparação De Danos Morais proposta por ALCIDES FERNANDES DA SILVA em face de BANCO                     BMG SA.
                    Alega o autor, à exordial de Id. 1630928, que estavam sendo descontados de seu benefício previdenciário pela instituição financeira demandada valores                         decorrentes de dois contratos de empréstimos consignados, o de nº 214100265, no valor de R$ 2.251,73 (dois mil duzentos e cinquenta e um reais e                             setenta e três centavos) a ser quitado em 60 parcelas mensais de R$ 71,47 (setenta e um reais e quarenta e sete centavos) e o de nº 229525632, no valor                      de R$ 498,79 (quatrocentos e noventa e oito reais e setenta e nove centavos) a ser quitado em 58 parcelas mensais de R$ 16,46 (dezesseis reais e                             quarenta e seis centavos). Sustenta que nunca realizou tais contratações e que se tratam de empréstimoertence ao BANCO ITAU BMG CONSIGNADO, empresa com                      personalidade jurídica diversa e independente do Banco BMG. Defende a inexistência de dano moral no caso em comento. Por fim, pugna pelo reconhecimento                     da ilegitimidade processual do BANCO BMG S/A e a condenação da demandada ao reembolso das despesas e pagamento dos honorários ao procurador do réu.
                    Apesar de devidamente intimada, a requerente não apresentou réplica a contestação, conforme certidão constante no Id. 1630954.
                    Sobreveio sentença de primeiro grau (Id. 1630955), na qual o juízo sentenciante verificou que o promovente propôs outras ações para desconstituição de                       empréstimo consignado, dentre elas a de nº 3000870-09.2018.8.06.0167, em que o banco Itaú Consignado juntou os contratos objeto das consignações                             celebradas com o autor, inclusive aquelas questionadas nestes autos. Verificou que os contratos de nº 214100265 e de nº 229525632, celebrados com BMG,                       foram amortizados pelos novos contratos celebrados com o Itaú Consignado, conforme demonstrou o Itaú nos autos do processo nº 3000870-09.2018.8.06.0167,                     nos Id. 1719927 e Id. 1719929. Reluz o juiz de base que não verificou verossimilhança nas alegações do autor, inclusive levando em consideração o enorme                     lapso temporal entre as contratações e o ajuizamento das ações. Em decorrência, julgou improcedente a ação e condenou o autor em multa por litigância de                     má-fé no valor equivalente a 2% (dois por cento) sobre o valor da causa, por alteração da verdade dos fatos e por utilizar-se do processo para conseguir                     objetivo ilegal.
                    Irresignado, o autor interpôs Recurso Inominado (Id. 1630960) asseverando que não agiu com má-fé, pois o autor, por não possuir estudos e por não                             entender toda a confusão bancária produzida pelas entidades, buscou o judiciário no presente caso, e em todos os outros, porque, mesmo tendo feito                          empréstimos, os valores e as instituições não correspondiam com o que o mesmo havia contratado, e que, para um leigo no assunto e com pouca instrução, é                     de difícil entendimento. Pede o afastamento da multa por litigância de má-fé e indenização por danos morais sob o fundamento de as instituições                               bancárias não terem cumprido com o dever de informação.
                    Contrarrazões apresentada ao Id. 1630964, pugnando pelo reconhecimento da ilegitimidade passiva do réu e, alternativamente, pela manutenção da sentença.
                    É o que importa relatar. Passo aos fundamentos da súmula de julgamento.
                    Preparo dispensado pela incidência do benefício da gratuidade de justiça. Desse modo, presentes os pressupostos objetivos e subjetivos de                                     admissibilidade, conheço do Recurso Inominado.
                    O recorrido alega, em preliminar, ilegitimidade passiva para compor o polo passivo da demanda, sob o fundamento de o contrato em questão pertencer ao                         Banco ITAU BMG CONSIGNADO.
                    Sabe-se que fora entabulada a unificação das atividades de crédito consignado do banco BMG e do Itaú BMG Consignado S.A., joint venture do BMG com o                         Itaú Unibanco, acordo este amplamente veiculado pela mídia e constante no próprio site do banco ITAU.
                    Vale ressaltar que, a despeito do acordo de unificação efetuado entre as instituições financeiras, aplicam-se as disposições do Código de Defesa do                         Consumidor, o que faz concluir pela hipossuficiência técnica e econômica do consumidor frente ao banco réu, cabendo a este a prova de que o contrato em                         questão não está sob a sua ingerência.
                    Ademais, conforme se verifica no histórico de consignações emitido pelo INSS, sob o Id. 1630932, o contrato discutido nos autos é firmado junto ao banco                     318 – BANCO BMG. Portanto, aplica-se ao caso a Teoria da Aparência, em que é considerado fornecedor do serviço aquele que se apresenta ao consumidor                         como tal, razão pela qual, se rejeita a preliminar de ilegitimidade passiva.
                    Passa-se ao mérito.
                    A sentença de primeiro grau verificou a validade do débito autoral e julgou improcedentes os pedidos iniciais. Ainda, concluiu por aplicar multa por                         litigância de má-fé ao autor sob o fundamento de que este alterou a verdade dos fatos e utilizou-se do processo visando fins ilegais.
                    Irresignado, o recorrente se insurgiu apenas quanto à aplicação da referida multa e pleiteou a condenação do recorrido em indenização por danos morais                         sob o fundamento de que este faltou com o dever de informação junto ao autor.
                    As relações contratuais são incontestes, tendo operado o trânsito em julgado do capítulo da sentença que rejeitou a declaração de inexistência das                             contratações. Ainda, o recorrente confirma que formalizou os referidos contratos em sede recursal, asseverando apenas que não reconheceu o empréstimo                         em seu histórico de consignações por falta de informação do réu. Alegação esta que não merece prosperar, pois os contratos acostados no referido                             histórico possuem os mesmos dados, valores, quantidade de parcelas e numeração correspondentes ao pacto inicialmente entabulado com o banco original,                     ITAU BMG.
                    Por fim, acerca da condenação ao pagamento de multa por litigância de má-fé, Theotônio Negrão e José Roberto Ferreira Gouvêa assim lecionam:
                    Para a condenação em litigância de má-fé, faz-se necessário o preenchimento de três requisitos, quais sejam: que a conduta da parte se subsuma a uma das                     hipóteses elencadas no art. 17 do CPC (antigo)."


## Estrutura de Saída do AILA:
Após executar o `main.py` com o seu texto, a função retornará um dicionário com a seguinte estrutura:

```json
{
  "extensao": {
    "artigos_e_dispositivos": [
      {
        "jurisprudencias": {},
        "marcador": "CPC",
        "posicao": [
          [2196, 2199],
          [8901, 8904],
          [9548, 9551],
          [10804, 10807]
        ],
        "sugestoes": ["Institui o Código de Processo Civil."],
        "tipo": "consulta_dispositivo"
      },
      {
        "marcador": "art. 98, §3º",
        "posicao": [2180, 2192],
        "sugestoes": [],
        "tipo": "erro_legislacao"
      },
      {
        "marcador": "art. 17",
        "posicao": [8890, 8897],
        "sugestoes": ["Art. 17"],
        "tipo": "sugestao_artigo"
      },
      {
        "marcador": "art. 80, do",
        "posicao": [9536, 9547],
        "sugestoes": [],
        "tipo": "erro_legislacao"
      },
      {
        "marcador": "art. 98, §3º",
        "posicao": [10788, 10800],
        "sugestoes": [],
        "tipo": "erro_legislacao"
      },
      {
        "jurisprudencias": {},
        "marcador": "CF",
        "posicao": [[8972, 8974]],
        "sugestoes": ["Constituição da República Federativa do Brasil."],
        "tipo": "consulta_dispositivo"
      },
      {
        "marcador": "art. 5º, LV",
        "posicao": [8976, 8987],
        "sugestoes": ["Art. 5°, LV"],
        "tipo": "sugestao_artigo"
      },
      {
        "jurisprudencias": {},
        "marcador": "Código de Processo Civil",
        "posicao": [[9080, 9104]],
        "sugestoes": ["Institui o Código de Processo Civil."],
        "tipo": "consulta_dispositivo"
      },
      {
        "jurisprudencias": {},
        "marcador": "Código Civil",
        "posicao": [[10316, 10328]],
        "sugestoes": ["Institui o Código Civil."],
        "tipo": "consulta_dispositivo"
      },
      {
        "marcador": "artigo 104, do",
        "posicao": [10301, 10315],
        "sugestoes": [],
        "tipo": "erro_legislacao"
      },
      {
        "jurisprudencias": {},
        "marcador": "Código de Defesa do Consumidor",
        "posicao": [[6821, 6851]],
        "sugestoes": ["Dispõe sobre a proteção do consumidor e dá outras providências.Texto compilado"],
        "tipo": "consulta_dispositivo"
      },
      {
        "marcador": "Lei 9.099/95",
        "posicao": [[2124, 2136], [10732, 10744]],
        "sugestoes": ["Lei n° 9.099/1995"],
        "tipo": "sugestao_dispositivo"
      },
      {
        "marcador": "art. 55, L",
        "posicao": [2115, 2125],
        "sugestoes": [],
        "tipo": "erro_legislacao"
      },
      {
        "marcador": "art. 55, L",
        "posicao": [10723, 10733],
        "sugestoes": [],
        "tipo": "erro_legislacao"
      },
      {
        "marcador": "ART. 80, INCISO II",
        "posicao": [1459, 1477],
        "sugestoes": [],
        "tipo": "erro_pareamento"
      },
      {
        "marcador": "Art. 80",
        "posicao": [9634, 9641],
        "sugestoes": [],
        "tipo": "erro_pareamento"
      }
    ],
    "jurisprudencias_texto": [
      {
        "KGL": false,
        "link": null,
        "local": "RS",
        "numero": "76.234",
        "posicao": [[9450, 9471]],
        "tipo_recurso": "RECURSO ESPECIAL",
        "tribunal": "STJ"
      }
    ]
  }
}

