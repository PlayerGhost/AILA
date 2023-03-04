import re
import math
import requests
import datetime

url = 'https://sinapses-backend.ia.pje.jus.br/rest/modelo/executarServico/-cnj-pnud-acad-unifor/GEN_GCL_UNIFOR/1'	
header = {'Authorization': 'Basic NjQyNzY2NDMzNjg6Z3VnYUAxOTEyNzk='}

### ENCONTRA DISPOSITIVO ###
def yyToyyyy(texto):
    if int(texto) <= 22:
        texto = r'20{}'.format(texto)
    else:
        texto = r'19{}'.format(texto)
    
    return texto

def BotaPontoMilhar(texto):
    texto = re.sub(r'(\d{1,2})(?=(\d{3})+(?!\d))',
                   r'\1.',
                   texto)
    
    return texto

def EncontraDispositivo(texto):
    dicionario = {}
    
    w = r'[A-Za-zÀ-ÄÇ-ÏÒ-ÖÙ-Üà-äç-ïò-öù-ü]'
    bl = r'(?:(?<!{})(?={}))'.format(w, w)
    br = r'(?:(?<={})(?!{}))'.format(w, w)
    
    # ABREVIATURA
    abreviaturas = {'cp': ('Decreto-Lei', '2.848', 1940),
                    'cpb': ('Decreto-Lei', '2.848', 1940),
                    'cpm': ('Decreto-Lei', '1.001', 1969),
                    'cpc': ('Lei', '5.869', 1973),
                    'ncpc': ('Lei', '13.105', 2015),
                    'cf': ('Constituição', '1988', 1988),
                    'cc': ('Lei', '10.406', 2002),
                    'cdc': ('Lei', '8.078', 1990),
                    'ctn': ('Lei', '5.172', 1966),
                    'ldb': ('Lei', '9.394', 1996),
                    'cpp': ('Decreto-Lei', '3.689', 1941),
                    'cppm': ('Decreto-Lei', '1.002', 1969),
                    'eca': ('Lei', '8.069', 1990),
                    'lep': ('Lei', '7.210', 1984),
                    'clt': ('Decreto-Lei', '5.452', 1943),
                    'pne': ('Lei', '13.005', 2014),
                    'lrf': ('Lei Complementar', '101', 2000),
                    'loas': ('Lei', '8.742', 1993),
                    'ctb': ('Lei', '9.053', 1997),
                    'lef': ('Lei', '6.830', 1980)}
    
    for chave, valor in abreviaturas.items():
        padrao = r'{}{}{}'.format(bl, chave, br)
        for m in re.finditer(padrao, texto, flags = re.I):
            dispositivo = valor[0]
            numero = valor[1]
            data = valor[2]
            
            posicao = (m.start(),m.end())
            texto_bruto = texto[m.start():m.end()]

            if texto_bruto in dicionario:
                dicionario[texto_bruto]['posicao'].append(posicao)
            else:
                dicionario[texto_bruto] = {'padronizado': (0, dispositivo, numero, data),
                                           'posicao': [posicao]}
    # ABREVIATURA
    
    # NOME
    nomes = {'c[óo]digo penal': ('Decreto-Lei' ,'2.848', 1940),
             'c[óo]digo penal militar': ('Decreto-Lei' ,'1.001', 1969),
             'novo c[óo]digo de processo civil': ('Lei' ,'13.105', 2015),
             'c[óo]digo de processo civil': ('Lei' ,'5.869', 1973),
             'constitui[çc][ãa]o federal': ('Constituição', '1988', 1988),
             'constitui[çc][ãa]o(?! federal)': ('Constituição', '1988', 1988),
             'carta magna': ('Constituição', '1988', 1988),
             'lei maior': ('Constituição', '1988', 1988),
             'c[óo]digo eleitoral': ('Lei' ,'4.737', 1965),
             'c[óo]digo civil': ('Lei' ,'10.406', 2002),
             'c[óo]digo de defesa do consumidor': ('Lei' ,'8.078', 1990),
             'c[óo]digo tribut[áa]rio nacional': ('Lei' ,'5.172', 1966),
             'lei de diretrizes e bases da educa[çc][ãa]o nacional': ('Lei' ,'9.394', 1996),
             'c[óo]digo de processo penal': ('Decreto-Lei' ,'3.689', 1941),
             'c[óo]digo de processo penal militar': ('Decreto-Lei' ,'1.002', 1969),
             'estatuto da crian[çc]a e do adolescente': ('Lei' ,'8.069', 1990),
             'lei de execu[çc][ãa]o penal': ('Lei' ,'7.210', 1984),
             'consolida[çc][ãa]o das leis do trabalho': ('Decreto-Lei' ,'5.452', 1943),
             'c[óo]digo de tr[âa]nsito brasileiro': ('Lei' ,'9.053', 1997),
             'c[óo]digo florestal': ('Lei' ,'12.651', 2012),
             'c[óo]digo de [áa]guas': ('Decreto' ,'24.643', 1934),
             'c[óo]digo de minas': ('Decreto-Lei' ,'227', 1967),
             'c[óo]digo brasileiro de aeron[áa]utica': ('Lei' ,'7.565', 1986),
             'c[óo]digo brasileiro de telecomunica[çc][õo]es': ('Lei' ,'4.117', 1962),
             'estatuto da advocacia e da ordem dos advogados do brasil': ('Lei' ,'8.906', 1994),
             'estatuto da cidade': ('Lei' ,'10.257', 2001),
             'estatuto de defesa do torcedor': ('Lei' ,'10.671', 2003),
             'estatuto do desarmamento': ('Lei' ,'10.826', 2003),
             'estatuto do estrangeiro': ('Lei' ,'13.445', 2017),
             'estatuto do idoso': ('Lei' ,'10.741', 2003),
             'estatuto da igualdade racial': ('Lei' ,'12.288', 2010),
             'estatuto do [íi]ndio': ('Lei' ,'6.001', 1973),
             'estatuto da juventude': ('Lei' ,'12.852', 2013),
             'estatuto dos militares': ('Lei' ,'6.880', 1980),
             'estatuto dos museus': ('Lei' ,'11.904', 2009),
             'estatuto nacional da microempresa e da empresa de pequeno porte': ('Lei Complementar' ,'123', 2006),
             'estatuto da pessoa com defici[êe]ncia': ('Lei' ,'13.146', 2015),
             'estatuto dos refugiados de 1951': ('Lei' ,'9.474', 1997),
             'estatuto da terra': ('Lei' ,'4.504', 1964),
             'lei maria da penha': ('Lei' ,'11.340', 2006),
             'lei antidrogas': ('Lei' ,'11.343', 2006),
             'lei de aliena[çc][ãa]o parental': ('Lei' ,'12.318', 2010),
             'lei do parcelamento do solo urbano': ('Lei' ,'6.766', 1979),
             'marco legal da primeira inf[âa]ncia': ('Lei' ,'13.257', 2016),
             'plano nacional de educa[çc][ãa]o': ('Lei' ,'13.005', 2014),
             'pol[íi]tica nacional do idoso': ('Lei' ,'8.842', 1994),
             'medida provis[óo]ria do trilh[ãa]o': ('Medida Provisória' ,'795', 2017),
             'lei org[âa]nica da assist[êe]ncia social': ('Lei' ,'8.742', 1993),
             'lei do calote': ('Lei' ,'9.870', 1999),
             'lei geral do turismo': ('Lei' ,'11.771', 2008),
             'pol[íi]tica nacional do meio ambiente': ('Lei' ,'6.938', 1981),
             'pol[íi]tica nacional de recursos h[íi]dricos': ('Lei' ,'9.433', 1997),
             'lei das inelegibilidades': ('Lei Complementar' ,'64', 1990),
             'lei das elei[çc][õo]es': ('Lei' ,'9.504', 1997),
             'lei de responsabilidade fiscal': ('Lei Complementar' ,'101', 2000),
             'lei de protesto de t[íi]tulos': ('Lei' ,'9.492', 1997),
             'pol[íi]tica nacional de preven[çc][ãa]o da automutila[çc][ãa]o e do suic[íi]dio': ('Lei' ,'13.819', 2019)}
    
    for chave, valor in nomes.items():
        padrao = r'{}{}{}'.format(bl, chave, br)

        for m in re.finditer(padrao, texto, flags = re.I):
            dispositivo = valor[0]
            numero = valor[1]
            data = valor[2]

            posicao = (m.start(),m.end())
            texto_bruto = texto[m.start():m.end()]

            if texto_bruto in dicionario:
                dicionario[texto_bruto]['posicao'].append(posicao)
            else:
                dicionario[texto_bruto] = {'padronizado': (1, dispositivo, numero, data),
                                           'posicao': [posicao]}
    # NOME
    
    # NUMERO

    leis = ['Lei',
            'Decreto',
            'Decreto-Lei',
            'Lei Delegada',
            'Lei Complementar',
            'Medida Provisória',
            'Emenda Constitucional']
    
    for lei in leis:
        if lei == 'Lei':
            padrao = r'{}(?<!Decreto[\- ])(Lei)'.format(bl)
            padrao = padrao + r'(?! Delegada| Complementar| Estadual| Municipal)'
        elif lei == 'Decreto':
            padrao = r'{}(Decreto)(?!\-Lei)'.format(bl)
        else:
            padrao = r'{}({})'.format(bl, lei)
        
        padrao = padrao + r'{}\D{{0,15}}(\d+(?:\.\d+)?)'.format(br)
        padrao = padrao + r'[-\/]?(\d+)?'

        for m in re.finditer(padrao, texto, flags = re.I):
            dispositivo = m.groups()[0]
            numero = m.groups()[1]
            if '.' not in numero:
                numero = BotaPontoMilhar(numero)
            data = m.groups()[2]
            
            posicao = (m.start(),m.end())
            texto_bruto = texto[m.start():m.end()]
            
            if data:
                if len(data) == 2:
                    data = yyToyyyy(data)
                
                if texto_bruto in dicionario:
                    dicionario[texto_bruto]['posicao'].append(posicao)
                else:
                    dicionario[texto_bruto] = {'padronizado': (2, dispositivo, numero, data),
                                               'posicao': [posicao]}
            else:
                if texto_bruto in dicionario:
                    dicionario[texto_bruto]['posicao'].append(posicao)
                else:
                    dicionario[texto_bruto] = {'padronizado': (2, dispositivo, numero),
                                               'posicao': [posicao]}
    # NUMERO
    
    return dicionario
### ENCONTRA DISPOSITIVO ###

### ENCONTRA ARTIGO ###
def EncontraArtigo(texto):
    
    dicionario = {}

    padrao_artigo = r'[aA][rR][tT](?:[iI][gG][oO])?\.?\D{0,15}(\d+(?:\.\d+)?)[°º]?(\-\D)?'
    padrao_paragrafo = r'(?:[pP][aA][rR][aAáÁ][gG][rR][aA][fF][oO]|(?<!§)§) *([uUúÚ][nN][iI][cC][oO]|\d+)[°º]?'
    padrao_inciso = r'(?:[iI][nN][cC](?:[iIíÍ][sS][oO])?\.?)? *([MDCLXVI]+)'
    padrao_alinea = r'(?:[aA][lL][iIíÍ][nN][eE][aA])? *([a-z]+)'
    padrao_item = r'(?:[iI][tT][eE][mM])? *(\d+)'
    
    padrao_paragrafo_indireto = r'(?:[pP][aA][rR][aAáÁ][gG][rR][aA][fF][oO]|(?<!§)§) *([uUúÚ][nN][iI][cC][oO]|\d+)[°º]?'
    padrao_inciso_indireto = r'[iI][nN][cC](?:[iIíÍ][sS][oO])?\.? *([MDCLXVI]+)'
    padrao_alinea_indireto = r'[aA][lL][iIíÍ][nN][eE][aA] *([a-z]+)'
    padrao_item_indireto = r'[iI][tT][eE][mM] *(\d+)'

    
    padrao_indireto = '(?:{})?(?:, *)?(?:{})?(?:, *)?(?:{})?(?:, *)?(?:{})?(.{{1,4}})?'.format(padrao_item_indireto,
                                                                                               padrao_alinea_indireto,
                                                                                               padrao_inciso_indireto,
                                                                                               padrao_paragrafo_indireto)

    padrao_direto = '(?:, *{})?(?:, *{})?(?:, *{})?(?:, *{})?'.format(padrao_paragrafo,
                                                                      padrao_inciso,
                                                                      padrao_alinea,
                                                                      padrao_item)
    
    
    padrao = padrao_indireto + padrao_artigo + padrao_direto
    
    for m in re.finditer(padrao, texto):
        item_indireto = m.groups()[0]
        alinea_indireto = m.groups()[1]
        inciso_indireto = m.groups()[2]
        paragrafo_indireto = m.groups()[3]
        
        conectivo_indireto = m.groups()[4]
        
        artigo = m.groups()[5]
        
        argumento_artigo = m.groups()[6]
        paragrafo = m.groups()[7]
        inciso = m.groups()[8]
        alinea = m.groups()[9]
        item = m.groups()[10]
        
        if paragrafo_indireto:
            if paragrafo_indireto.isalpha():
                paragrafo_indireto = 'unico'
        
        if paragrafo:
            if paragrafo.isalpha():
                paragrafo = 'unico'
        
        if (not item_indireto) and (not alinea_indireto) and (not inciso_indireto) and (not paragrafo_indireto):
            if conectivo_indireto:
                posicao = (m.start() + len(conectivo_indireto), m.end())
                texto_bruto = texto[m.start() + len(conectivo_indireto):m.end()]
            else:
                posicao = (m.start(),m.end())
                texto_bruto = texto[m.start():m.end()]
            
            if texto_bruto in dicionario:
                dicionario[texto_bruto]['posicao'].append(posicao)
            else:
                dicionario[texto_bruto] = {'padronizado': (artigo, argumento_artigo, paragrafo, inciso, alinea, item),
                                           'posicao': [posicao],
                                           'flag_indireta': 0}
        else:
            posicao = (m.start(),m.end())
            texto_bruto = texto[m.start():m.end()]
        
        
            if texto_bruto in dicionario:
                dicionario[texto_bruto]['posicao'].append(posicao)
            else:
                dicionario[texto_bruto] = {'padronizado': (artigo, argumento_artigo, paragrafo_indireto, 
                                                           inciso_indireto, alinea_indireto, item_indireto),
                                           'posicao': [posicao],
                                           'flag_indireta': 1}
   
    
    return dicionario
### ENCONTRA ARTIGO ###

### PADRONIZA NOME LEI ###
def PadronizaNomeLei(texto_bruto_dispositivo):
    w = r'[A-Za-zÀ-ÄÇ-ÏÒ-ÖÙ-Üà-äç-ïò-öù-ü]'
    bl = r'(?:(?<!{})(?={}))'.format(w, w)
    br = r'(?:(?<={})(?!{}))'.format(w, w)

    nomes = {'c[óo]digo penal': 'Código Penal',
             'c[óo]digo penal militar': 'Código Penal Militar',
             'novo c[óo]digo de processo civil': 'Novo Código de Processo Civil',
             'c[óo]digo de processo civil': 'Código de Processo Civil',
             'constitui[çc][ãa]o federal': 'Constituição Federal',
             'constitui[çc][ãa]o(?! federal)': 'Constituição Federal',
             'carta magna': 'Constituição Federal',
             'lei maior': 'Constituição Federal',
             'c[óo]digo eleitoral': 'Código Eleitoral',
             'c[óo]digo civil': 'Código Civil',
             'c[óo]digo de defesa do consumidor': 'Código de Defesa do Consumidor',
             'c[óo]digo tribut[áa]rio nacional': 'Código Tributário Nacional',
             'lei de diretrizes e bases da educa[çc][ãa]o nacional': 'Lei de Diretrizes e Bases da Educação Nacional',
             'c[óo]digo de processo penal': 'Código de Processo Penal',
             'c[óo]digo de processo penal militar': 'Código de Processo Penal Militar',
             'estatuto da crian[çc]a e do adolescente': 'Estatuto da Criança e do Adolescente',
             'lei de execu[çc][ãa]o penal': 'Lei de Execução Penal',
             'consolida[çc][ãa]o das leis do trabalho': 'Consolidação das Leis do Trabalho',
             'c[óo]digo de tr[âa]nsito brasileiro': 'Código de Trânsito Brasileiro',
             'c[óo]digo florestal': 'Código Florestal',
             'c[óo]digo de [áa]guas': 'Código de Águas',
             'c[óo]digo de minas': 'Código de Minas',
             'c[óo]digo brasileiro de aeron[áa]utica': 'Código Brasileiro de Aeronáutica',
             'c[óo]digo brasileiro de telecomunica[çc][õo]es': 'Código Brasileiro de Telecomunicações',
             'estatuto da advocacia e da ordem dos advogados do brasil': 'Estatuto da Advocacia e da Ordem dos Advogados do Brasil',
             'estatuto da cidade': 'Estatuto da Cidade',
             'estatuto de defesa do torcedor': 'Estatuto de Defesa do Torcedor',
             'estatuto do desarmamento': 'Estatuto do Desarmamento',
             'estatuto do estrangeiro': 'Estatuto do Estrangeiro',
             'estatuto do idoso': 'Estatuto do Idoso',
             'estatuto da igualdade racial': 'Estatuto da Igualdade Racial',
             'estatuto do [íi]ndio': 'Estatuto do Índio',
             'estatuto da juventude': 'Estatuto da Juventude',
             'estatuto dos militares': 'Estatuto dos Militares',
             'estatuto dos museus': 'Estatuto dos Museus',
             'estatuto nacional da microempresa e da empresa de pequeno porte': 'Estatuto Nacional da Microempresa e da Empresa de Pequeno Porte',
             'estatuto da pessoa com defici[êe]ncia': 'Estatuto da Pessoa com Deficiência',
             'estatuto dos refugiados de 1951': 'Estatuto dos Refugiados',
             'estatuto da terra': 'Estatuto da Terra',
             'lei maria da penha': 'Lei Maria da Penha',
             'lei antidrogas': 'Lei Antidrogas',
             'lei de aliena[çc][ãa]o parental': 'Lei de Alienação Parental',
             'lei do parcelamento do solo urbano': 'Lei do Parcelamento do Solo Urbano',
             'marco legal da primeira inf[âa]ncia': 'Marco Legal da Primeira Infância' ,
             'plano nacional de educa[çc][ãa]o': 'Plano Nacional de Educação',
             'pol[íi]tica nacional do idoso': 'Política Nacional do Idoso',
             'medida provis[óo]ria do trilh[ãa]o': 'Medida Prisória do Trilhão',
             'lei org[âa]nica da assist[êe]ncia social': 'Lei Orgânica da Assistência Social',
             'lei do calote': 'Lei do Calote',
             'lei geral do turismo': 'Lei Geral do Turismo',
             'pol[íi]tica nacional do meio ambiente': 'Política Nacional do Meio Ambiente',
             'pol[íi]tica nacional de recursos h[íi]dricos': 'Política Nacional de Recursos Hídricos',
             'lei das inelegibilidades': 'Lei das Inelegibilidades',
             'lei das elei[çc][õo]es': 'Lei das Eleições',
             'lei de responsabilidade fiscal': 'Lei de Resposnabilidade Fiscal',
             'lei de protesto de t[íi]tulos': 'Lei de Protesto de Títulos',
             'pol[íi]tica nacional de preven[çc][ãa]o da automutila[çc][ãa]o e do suic[íi]dio': 'Política Nacional de Prevenção da Automutilação e do Suicídio'}

    for chave, valor in nomes.items():
        padrao = r'{}{}{}'.format(bl, chave, br)

        for m in re.finditer(padrao, texto_bruto_dispositivo, flags = re.I):
            valor_padronizado = valor
            
    return valor_padronizado
### PADRONIZA NOME LEI ###

### MODELO DE DISTANCIA ###
def ModeloDistancia(artigos, dispositivo, dispositivo_GCL, dicionario_artigos_pareados):
    delta = 10
    pares = []
     
    chave_dispositivo = list(dispositivo.keys())[0]
    valor_dispositivo = list(dispositivo.values())[0]
    
    len_dispositivo = len(chave_dispositivo)
  
    for posicao_dispositivo in valor_dispositivo['posicao']:
        distancia_minima = math.inf
        chave_minima_artigo = None
        posicao_minima_artigo = None
        
        for chave_artigo, valor_artigo in artigos.items():
            len_artigo = len(chave_artigo)
            
            for posicao_artigo in valor_artigo['posicao']:
#                 distancia = abs(posicao_artigo[0] - posicao_dispositivo[0])
                
                # checando quem está na frente
                if posicao_artigo[0] < posicao_dispositivo[0]:
                    distancia = posicao_dispositivo[0] - posicao_artigo[1]
                    if distancia <= delta and distancia < distancia_minima:
                        distancia_minima = distancia
                        chave_minima_artigo = chave_artigo
                        valor_minimo_artigo = valor_artigo
                        posicao_minima_artigo = posicao_artigo
                else:
                    distancia = posicao_artigo[0] - posicao_dispositivo[1]
                    if distancia <= delta and distancia < distancia_minima:
                        distancia_minima = distancia
                        chave_minima_artigo = chave_artigo
                        valor_minimo_artigo = valor_artigo
                        posicao_minima_artigo = posicao_artigo

        if chave_minima_artigo and posicao_minima_artigo:
            if dicionario_artigos_pareados[posicao_minima_artigo] == 0:
                par = ((chave_minima_artigo, valor_minimo_artigo['padronizado'], posicao_minima_artigo, valor_minimo_artigo['flag_indireta']),
                       (chave_dispositivo, dispositivo_GCL, posicao_dispositivo))
                dicionario_artigos_pareados[posicao_minima_artigo] = 1
                pares.append(par)

    return pares
### MODELO DE DISTANCIA ###

### CONSULTA GCL ###

def ConsultaDispositivo(legislacao):
    flag = legislacao[0]
    tipo = legislacao[1]
    numero = legislacao[2]
    
    if len(legislacao) == 4:
        data = int(legislacao[3])
    else:
        data = None
    
    artigo = None
    argumento_artigo = None
    paragrafo = None
    inciso = None
    alinea = None
    item = None
    
    dicionario_tipo = {'lei': 0,
                       'decreto': 1,
                       'lei complementar': 2,
                       'decreto-lei': 3,
                       'lei delegada': 4,
                       'medida provisória AE32': 5,
                       'medida provisoria PE32': 6,
                       'constituição': 7,
                       'decreto legislativo': 8,
                       'lei estadual': 9,
                       'lei complementar estadual': 10,
                       'emenda constitucional': 11}
    
    idx_tipo = dicionario_tipo[tipo.lower()]
    
    data = data if data else 0
    artigo = artigo if artigo else '0'
    argumento_artigo = argumento_artigo if argumento_artigo else '0'
    paragrafo = paragrafo if paragrafo else '0'
    inciso = inciso if inciso else '0'
    alinea = alinea if alinea else '0'
    item = item if item else '0'
    
    # chamada no serviço flask
    
    #url = 'http://localhost:5000/?'
    #url += 'tipo={}&'.format(idx_tipo)
    #url += 'lei={}&'.format(numero)
    #url += 'ano={}&'.format(data)
    #url += 'artigo={}&'.format(artigo)
    #url += 'complemento={}&'.format(argumento_artigo)
    #url += 'paragrafo={}&'.format(paragrafo)
    #url += 'inciso={}&'.format(inciso)
    #url += 'alinea={}&'.format(alinea)
    #url += 'item={}'.format(item)
    
    #consulta = eval(requests.get(url).content.decode())
    
    mensagem = {'tipo': idx_tipo, 'lei': numero, 'ano': data, 'artigo': artigo, 'complemento': argumento_artigo, 
                'paragrafo': paragrafo, 'inciso': inciso, 'alinea': alinea, 'item': item }
    
    resposta = requests.post(url, json=mensagem, headers=header)    
    consulta = eval(resposta.text)['extensao']
    
    dispositivos = []
    
    if consulta:
        for dispositivo in consulta:   
            lei = eval(list(dispositivo.keys())[0])
            dispositivos.append({'dispositivo': (flag, tipo, lei[0], lei[1], lei[2]),
                                 'ementa': list(dispositivo.values())[0]})

    return dispositivos

def ConsultaArtigo(legislacao):
    texto_bruto = legislacao[0][0]
    artigo = legislacao[0][1][0]
    argumento_artigo = legislacao[0][1][1]
    paragrafo = legislacao[0][1][2]
    inciso = legislacao[0][1][3]
    alinea = legislacao[0][1][4]
    item = legislacao[0][1][5]
    
    tipo = legislacao[1][1][0]
    numero = legislacao[1][1][1]
    data = legislacao[1][1][2]
    
    flag_indireta = legislacao[0][3]
    
    if (len(artigo) > 3) and '.' not in artigo:
        artigo = re.sub(r'(\d{1,2})(?=(\d{3})+(?!\d))',
                        r'\1.',
                        artigo)
    
    tupla = (tipo, numero, data, artigo, argumento_artigo, paragrafo, inciso, alinea, item)
    
    data = data if data else 0
    artigo = artigo if artigo else '0'
    argumento_artigo = argumento_artigo if argumento_artigo else '0'
    paragrafo = paragrafo if paragrafo else '0'
    inciso = inciso if inciso else '0'
    alinea = alinea if alinea else '0'
    item = item if item else '0'
    
    #url = 'http://localhost:5000/?'
    #url += 'tipo={}&'.format(tipo)
    #url += 'lei={}&'.format(numero)
    #url += 'data={}&'.format(data.strftime('%d/%m/%Y'))
    #url += 'artigo={}&'.format(artigo)
    #url += 'complemento={}&'.format(argumento_artigo)
    #url += 'paragrafo={}&'.format(paragrafo)
    #url += 'inciso={}&'.format(inciso)
    #url += 'alinea={}&'.format(alinea)
    #url += 'item={}'.format(item)
    
    #consulta = eval(requests.get(url).content.decode())
    
    mensagem = {'tipo': tipo, 'lei': numero, 'data': data.strftime('%d/%m/%Y'), 'artigo': artigo, 'complemento': argumento_artigo, 
                'paragrafo': paragrafo, 'inciso': inciso, 'alinea': alinea, 'item': item }
    
    resposta = requests.post(url, json=mensagem, headers=header)
    consulta = eval(resposta.text)['extensao']
    
    artigos = []
    if list(consulta[0].values())[0] != 'None':
        if len(list(consulta[0].values())[0]) == 2:
            artigos.append({'artigo': tupla[3:],
                              'texto_artigo': list(consulta[0].values())[0][0],
                              'jurisprudencias': list(consulta[0].values())[0][1],
                              'flag_indireta': flag_indireta})
        else:
            artigos.append({'artigo': tupla[3:],
                              'texto_artigo': list(consulta[0].values())[0],
                              'jurisprudencias': [],
                              'flag_indireta': flag_indireta})
        
    return artigos

def ConsultaGCL(legislacao):  
    if len(legislacao) >= 3:
        sugestoes = ConsultaDispositivo(legislacao)           
    else:
        sugestoes = ConsultaArtigo(legislacao) 
    
    
    return sugestoes
### CONSULTA GCL ###

### AILA ###
def AILA(texto):
    dado_saida_json = []
    
    dicionario_dispositivos = EncontraDispositivo(texto)
    dicionario_artigos = EncontraArtigo(texto)
    
    dicionario_artigos_pareados = {}
    
    for artigo in dicionario_artigos.values():
        for posicao in artigo['posicao']:
            dicionario_artigos_pareados[posicao] =  0
    
    for texto_bruto_dispositivo, dispositivo in dicionario_dispositivos.items():
        sugestoes_dispositivos = ConsultaGCL(dispositivo['padronizado'])
        
        if len(sugestoes_dispositivos) > 0:
            sugestoes_padronizadas_dispositivos = []
            for sugestao_dispositivo in sugestoes_dispositivos:
                s = sugestao_dispositivo['dispositivo']
                if s[0] == 0:
                    sugestoes_padronizadas_dispositivos.append('{}'.format(texto_bruto_dispositivo.upper()))
                elif s[0] ==1:
                    sugestoes_padronizadas_dispositivos.append('{}'.format(PadronizaNomeLei(texto_bruto_dispositivo)))
                else:
                    sugestoes_padronizadas_dispositivos.append('{} n° {}/{}'.format(s[1].title(),
                                                                                    s[3],
                                                                                    s[4].year))
            
            if len(sugestoes_dispositivos) == 1:
                sugestao_dispositivo = sugestoes_dispositivos[0]
                sugestao_padronizada_dispositivo = sugestoes_padronizadas_dispositivos[0]
                
             
                if texto_bruto_dispositivo == sugestao_padronizada_dispositivo:
                    # retorna uma consulta do dispositivo
                    dado_saida_json.append({'tipo': 'consulta_dispositivo',
                                            'marcador': texto_bruto_dispositivo,
                                            'posicao': dispositivo['posicao'],
                                            'sugestoes': [sugestao_dispositivo['ementa']],
                                            'jurisprudencias': {}})
                else:
                    # retorna uma sugestão padronizada de dispositivo
                    dado_saida_json.append({'tipo': 'sugestao_dispositivo',
                                            'marcador': texto_bruto_dispositivo,
                                            'posicao': dispositivo['posicao'],
                                            'sugestoes': [sugestao_padronizada_dispositivo]})
         
                legislacoes = ModeloDistancia(dicionario_artigos,
                                              {texto_bruto_dispositivo: dispositivo},
                                              sugestao_dispositivo['dispositivo'][2:],
                                              dicionario_artigos_pareados)

                for legislacao in legislacoes:
                    sugestoes_artigos = ConsultaGCL(legislacao)
                    
                    
                    texto_bruto_artigo = legislacao[0][0]
                    
                    if len(sugestoes_artigos) == 1:
                        
                        sugestao_artigo = sugestoes_artigos[0]
                        jurisprudencias = sugestao_artigo['jurisprudencias']
                        
                        # sugestao_artigo['artigo'] = (art, com, par, inc, ali, ite)
                        
                        if sugestao_artigo['flag_indireta'] == 0:

                            ##### REVISAR A NECESSIDADE DO TRY/EXCEPT
                            # try:
                            #     if int(sugestao_artigo['artigo'][0]) < 10:
                            #         sugestao_padronizada_artigo = 'Art. {}°'.format(sugestao_artigo['artigo'][0])
                            # except:
                            #     sugestao_padronizada_artigo = 'Art. {}'.format(sugestao_artigo['artigo'][0])
                            ##### REVISAR A NECESSIDADE DO TRY/EXCEPT

                            if '.' in sugestao_artigo['artigo'][0]:
                                sugestao_padronizada_artigo = 'Art. {}'.format(sugestao_artigo['artigo'][0])
                            else:
                                if int(sugestao_artigo['artigo'][0]) < 10:
                                    sugestao_padronizada_artigo = 'Art. {}°'.format(sugestao_artigo['artigo'][0])
                                else:
                                    sugestao_padronizada_artigo = 'Art. {}'.format(sugestao_artigo['artigo'][0])

                            if sugestao_artigo['artigo'][1]:
                                sugestao_padronizada_artigo += '-{}'.format(sugestao_artigo['artigo'][1])

                            if sugestao_artigo['artigo'][2]:
                                if sugestao_artigo['artigo'][2] == 'unico':
                                    sugestao_padronizada_artigo += ', parágrafo único'
                                else:
                                    if int(sugestao_artigo['artigo'][2]) < 10:
                                        sugestao_padronizada_artigo += ', § {}°'.format(sugestao_artigo['artigo'][2])
                                    else:
                                        sugestao_padronizada_artigo += ', § {}'.format(sugestao_artigo['artigo'][2])

                            if sugestao_artigo['artigo'][3]:
                                sugestao_padronizada_artigo += ', {}'.format(sugestao_artigo['artigo'][3])

                            if sugestao_artigo['artigo'][4]:
                                sugestao_padronizada_artigo += ', {}'.format(sugestao_artigo['artigo'][4])

                            if sugestao_artigo['artigo'][5]:
                                sugestao_padronizada_artigo += ', {}'.format(sugestao_artigo['artigo'][5])


                            if texto_bruto_artigo == sugestao_padronizada_artigo:
                                # retorna consulta da legislacao
                                dado_saida_json.append({'tipo': 'consulta_legislacao',
                                                        'marcador': sugestao_padronizada_dispositivo + 
                                                        ' | ' + sugestao_padronizada_artigo,
                                                        'posicao': [legislacao[1][2], legislacao[0][2]],
                                                        'sugestoes': [sugestao_artigo['texto_artigo']],
                                                        'jurisprudencias': jurisprudencias})
        
                                # retira consulta dispositivo caso ele seja pareado
                                indice_consulta_excluir = None
                                for indice, dicionario in enumerate(dado_saida_json):
                                    if dicionario['tipo'] == 'consulta_dispositivo':
                                        if dicionario['marcador'] == legislacao[1][0]: # texto bruto do dispositivo
                                            dicionario['posicao'].remove(legislacao[1][2])
                                            if len(dicionario['posicao']) == 0:
                                                indice_consulta_excluir = indice
                                                break
                                
                                if indice_consulta_excluir != None:
                                    dado_saida_json.pop(indice_consulta_excluir)

                                
                            else:
                                # retorna sugestoes
                                dado_saida_json.append({'tipo': 'sugestao_artigo',
                                                        'marcador': texto_bruto_artigo,
                                                        'posicao': legislacao[0][2],
                                                        'sugestoes': [sugestao_padronizada_artigo]})
                        else:
                            sugestao_padronizada_artigo = ''
                            
                            # ESCREVER CASOS DE CITAÇÃO INDIRETA #
                            if sugestao_artigo['artigo'][5]:
                                sugestao_padronizada_artigo += 'item {}, '.format(sugestao_artigo['artigo'][5])
                                
                            
                            if sugestao_artigo['artigo'][4]:
                                sugestao_padronizada_artigo += 'alínea {}, '.format(sugestao_artigo['artigo'][4])
                                
                            if sugestao_artigo['artigo'][3]:
                                if sugestao_artigo['artigo'][2]:
                                    sugestao_padronizada_artigo += 'inciso {}, '.format(sugestao_artigo['artigo'][3])
                                else:
                                    sugestao_padronizada_artigo += 'inciso {}'.format(sugestao_artigo['artigo'][3])
                                
                            if sugestao_artigo['artigo'][2]:
                                if sugestao_artigo['artigo'][2] == 'unico':
                                    sugestao_padronizada_artigo += 'parágrafo único'
                                else:
                                    if int(sugestao_artigo['artigo'][2]) < 10:
                                        sugestao_padronizada_artigo += '§ {}°'.format(sugestao_artigo['artigo'][2])
                                    else:
                                        sugestao_padronizada_artigo += '§ {}'.format(sugestao_artigo['artigo'][2])
                                        
                            if int(sugestao_artigo['artigo'][0]) < 10:
                                sugestao_padronizada_artigo += ' do Art. {}°'.format(sugestao_artigo['artigo'][0])
                            else:
                                sugestao_padronizada_artigo += ' do Art. {}'.format(sugestao_artigo['artigo'][0])

                            if sugestao_artigo['artigo'][1]:
                                sugestao_padronizada_artigo += '-{}'.format(sugestao_artigo['artigo'][1]) 
                                
                            if texto_bruto_artigo == sugestao_padronizada_artigo:
                                # retorna consulta do artigo
                                dado_saida_json.append({'tipo': 'consulta_legislacao',
                                                        'marcador':sugestao_padronizada_dispositivo + 
                                                        ' | ' + sugestao_padronizada_artigo,
                                                        'posicao': [legislacao[1][2], legislacao[0][2]],
                                                        'sugestoes': [sugestao_artigo['texto_artigo']],
                                                        'jurisprudencias': sugestao_artigo['jurisprudencias']})

                                # retira consulta dispositivo caso ele seja pareado
                                indice_consulta_excluir = None
                                for indice, dicionario in enumerate(dado_saida_json):
                                    if dicionario['tipo'] == 'consulta_dispositivo':
                                        if dicionario['marcador'] == legislacao[1][0]: # texto bruto do dispositivo
                                            dicionario['posicao'].remove(legislacao[1][2])
                                            if len(dicionario['posicao']) == 0:
                                                indice_consulta_excluir = indice
                                                break
                                                
                                if indice_consulta_excluir != None:
                                    dado_saida_json.pop(indice_consulta_excluir)
                                
                            else:
                                # retorna sugestoes
                                dado_saida_json.append({'tipo': 'sugestao_artigo',
                                                        'marcador': texto_bruto_artigo,
                                                        'posicao': legislacao[0][2],
                                                        'sugestoes': [sugestao_padronizada_artigo]})
                        
                    else:
                        # retornar erro em artigo
                        dado_saida_json.append({'tipo': 'erro_legislacao',
                                                'marcador': texto_bruto_artigo,
                                                'posicao': legislacao[0][2],
                                                'sugestoes': []})
            else:
                # retornar sugestoes de dispositivo
                dado_saida_json.append({'tipo': 'sugestao_dispositivo',
                                        'marcador': texto_bruto_dispositivo,
                                        'posicao': dispositivo['posicao'],
                                        'sugestoes': sugestoes_padronizadas_dispositivos})
    
        else:
            # retornar erro em dispositivo
            dado_saida_json.append({'tipo': 'erro_dispositivo',
                                    'marcador': texto_bruto_dispositivo,
                                    'posicao': dispositivo['posicao'],
                                    'sugestoes': []})
        
    for texto_bruto_artigo, artigo in dicionario_artigos.items():
        for posicao in artigo['posicao']:
            if dicionario_artigos_pareados[posicao] == 0:                
                # retorna consulta do artigo
                dado_saida_json.append({'tipo': 'erro_pareamento',
                                        'marcador': texto_bruto_artigo,
                                        'posicao': posicao,
                                        'sugestoes': []})
    
#     print(dicionario_artigos_pareados)

    #isso deve estar dentro do serviço flask
    #return {'extensao':{'dadoSaidaJson': dado_saida_json}}
    
    return dado_saida_json
### AILA ###

