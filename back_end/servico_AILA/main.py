import re
import json
import math
import requests
#from datetime import date


### VALIDAR KGL ###
#path_arq_kgl = ''

# padrao: tipo - numero
def get_sumulas_stj():
    with open('./sumulas_stj.json', encoding='utf-8') as file:
        sumulas_stj = json.load(file).keys()
    return set(sumulas_stj)

# padrao: tipo - numero
def get_sumulas_stf():
    with open('./sumulas_stf.json', encoding='utf-8') as file:
        sumulas_stf = json.load(file).keys()
    return set(sumulas_stf)

# padrao: tipo - numero
def get_sumulas_tjce():
    with open('./sumulas_tjce.json', encoding='utf-8') as file:
        sumulas_tjce = json.load(file).keys()
    return set(sumulas_tjce)

# padrao : tipo - recurso - numero - estado
def get_acordaos_stj():
    with open('./acordaos_stj_v4.json', encoding='utf-8') as file:
        acordaos_stj = json.load(file).keys()
    return set(acordaos_stj)

# padrao : tipo - recurso - numero
def get_acordaos_stf():
    stf_set = set()
    with open('./acordaos_stf_v2.json', encoding='utf-8') as file:
        acordaos_stf = json.load(file).values()
    for dicio in acordaos_stf:
        stf_set.add('19_{}_{}'.format(retorna_sigla_padronizada(dicio['sigla_classe'], get_siglas_principais()), dicio['numero_processo']))
    return stf_set

# padrao : tipo - numero
def get_acordaos_tjce():
    tjce_set = set()
    with open('./acordaos_todos_tjce.json', encoding='utf-8') as file:
        acordaos_tjce = json.load(file).values()
    for dicio in acordaos_tjce:
        tjce_set.add('13_{}'.format(dicio['num_processo']))
    return tjce_set

# padrao : tipo - numero
def get_sumulas_vinculantes_stf():
    tjce_set = set()
    with open('./sumulas_vinculantes_stf.json', encoding='utf-8') as file:
        sumulas_vinculantes_stf = json.load(file)
    for dicio in sumulas_vinculantes_stf:
        tjce_set.add('18_{}'.format(dicio['sumula']))
    return tjce_set

def get_links_stj():
    with open('./acordaos_stj_v4.json', encoding='utf-8') as file:
        acordaos_stj = json.load(file)
        
    links_acordaos_stj = {}
    for a in acordaos_stj:
        links_acordaos_stj[a] = acordaos_stj[a]['link']
    return links_acordaos_stj

def get_links_stf():
    with open('./acordaos_stf_v2.json', encoding='utf-8') as file:
        acordaos_stf = json.load(file)
        
    links_acordaos_stf = {}
    for a in acordaos_stf:
        links_acordaos_stf[a] = acordaos_stf[a]['url']
    return links_acordaos_stf

def get_links_sum_vinc_stf():
    with open('./sumulas_vinculantes_stf.json', encoding='utf-8') as file:
        sum_vinc_stf = json.load(file)
        
    links_sum_vinc_stf = {}
    for a in sum_vinc_stf:
        links_sum_vinc_stf[f'18_{a["sumula"]}'] = a['url']
    return links_sum_vinc_stf

def valida_kgl(jurisprudencias):
    sumulas_stj = get_sumulas_stj()
    sumulas_stf = get_sumulas_stf()
    sumulas_tjce = get_sumulas_tjce()
    acordaos_stj = get_acordaos_stj()
    acordaos_stf = get_acordaos_stf()
    acordaos_tjce = get_acordaos_tjce()
    sumulas_vinc_stf = get_sumulas_vinculantes_stf()
    links_acordaos_stj = get_links_stj()
    links_acordaos_stf = get_links_stf()
    links_sum_vinc_stf = get_links_sum_vinc_stf()
    
    jurisprudencias_validadas = []
    for j in jurisprudencias:
        tribunal = j['tribunal']
        recurso = j['tipo_recurso']
        numero = j['numero']
        local = j['local']
        kgl = False
        link = None

        if recurso == 'SÚMULA':
            if tribunal == 'STJ':
                kgl = f'14_{numero}' in sumulas_stj
            elif kgl == False and tribunal == 'STF':
                kgl = f'17_{numero}' in sumulas_stf
            elif kgl == False and tribunal == 'TJCE':
                kgl = f'15_{numero}' in sumulas_tjce
        elif recurso == 'SÚMULA VINCULANTE':
            if tribunal == 'STF':
                kgl = f'18_{numero}' in sumulas_vinc_stf
                
                if kgl and f'18_{numero}' in links_sum_vinc_stf.keys():
                    link = links_sum_vinc_stf[f'18_{numero}']
        elif kgl == False and tribunal == 'STJ':
            kgl = f'16_{recurso}_{numero}_{local}' in acordaos_stj
            
            if kgl and f'16_{recurso}_{numero}_{local}' in links_acordaos_stj.keys():
                link = links_acordaos_stj[f'16_{recurso}_{numero}_{local}']       
        elif kgl == False and tribunal == 'STF':
            kgl = f'18_{recurso}_{numero}-{local}' in acordaos_stf
            
            if kgl and f'18_{recurso}_{numero}-{local}' in links_acordaos_stf:
                link = links_acordaos_stf[f'18_{recurso}_{numero}-{local}']
        elif kgl == False and tribunal == 'TJCE':
            kgl = f'13_{numero}' in acordaos_tjce

        j['KGL'] = kgl
        j['link'] = link
        jurisprudencias_validadas.append(j)

    return jurisprudencias_validadas

### VALIDAR KGL ###

### JURISPRUDENCIA ###
def get_estados_brasileiros():
    estados_brasileiros = [('AC', 'Acre'),
                         ('AL', 'Alagoas'),
                         ('AP', 'Amap[áa]'),
                         ('AM', 'Amazonas'),
                         ('BA', 'Bahia'),
                         ('CE', 'Cear[áa]'),
                         ('DF', 'Distrito Federal'),
                         ('ES', 'Esp[íi]rito Santo'),
                         ('GO', 'Goi[áa]s'),
                         ('MA', 'Maranh[ãa]o'),
                         ('MT', 'Mato Grosso'),
                         ('MS', 'Mato Grosso do Sul'),
                         ('MG', 'Minas Gerais'),
                         ('PA', 'Par[áa]'),
                         ('PB', 'Para[íi]ba'),
                         ('PR', 'Paran[áa]'),
                         ('PE', 'Pernambuco'),
                         ('PI', 'Piau[íi]'),
                         ('RJ', 'Rio de Janeiro'),
                         ('RN', 'Rio Grande do Norte'),
                         ('RS', 'Rio Grande do Sul'),
                         ('RO', 'Rond[ôo]nia'),
                         ('RR', 'Roraima'),
                         ('SC', 'Santa Catarina'),
                         ('SP', 'S[ãa]o Paulo'),
                         ('SE', 'Sergipe'),
                         ('TO', 'Tocantins')]

    return estados_brasileiros, [estado for estados_br in estados_brasileiros for estado in estados_br[:2]]

def get_tribunais_federais():
    tribunais_federais = ['STJ', 'Supremo Tribunal de Justiça', 'Superior Tribunal de Justiça',
                        'STF', 'Supremo Tribunal Federal', 'Superior Tribunal Federal',
                        'TRF', 'Tribunal Regional Federal']
    return tribunais_federais

def get_tribunais_estaduais():
    estados_brasileiros, _ = get_estados_brasileiros()

    arr_tribunais_estaduais = [r'TJ ?[-/–E]? ?' + estado[0] for estado in estados_brasileiros]
    arr_tribunais_estaduais.extend([r'Tribunal de Justi[cç]a d[aeo] ' + estado[1] for estado in estados_brasileiros])

    return arr_tribunais_estaduais

def get_siglas_principais():
    return remove_sobreposicao({'ACÓRDÃO': ['Ac[óo]rd[aã]o'],
                    'AGRAVO DE INSTRUMENTO': ['Ag. de instrumento', 'AI'],
                    'Ag em RECURSO ESPECIAL': ['Agravo em R Especial', 'AResp'],
                    'Ag em RECURSO EXTRAORDINÁRIO': ['Agravo em Recurso Extraordin[áa]rio', 'ARE', 'AG no RE', 'A no RE'],
                    'APELAÇÃO': ['Apela[çc][ãa]o', 'ap', 'apl'],
                    'APELAÇÃO CÍVEL': ['APELAÇÃO CIVEL', 'Apela[çc][ãa]o c[íi]vel', 'AC', 'ap. cível', 'apel. c[íi]vel', 'APC'],
                    'APELAÇÃO CRIMINAL': ['Apela[çc][ãa]o criminal', 'apela[çc][ãa]o crime', 'acr', 'APR'],
                    'AÇÃO CIVIL ORIGINÁRIA': ['A[cç][aã]o Civil Origin[áa]ria'],
                    'AÇÃO DE IMPROBIDADE ADMINISTRATIVA': ['A[cç][aã]o de Improbidade Administrativa'],
                    'AÇÃO DIRETA DE INCONSTITUCIONALIDADE': ['A[cç][aã]o Direta de Inconstitucionalidade', 'ADI'],
                    'AÇÃO PENAL': ['A[cç][aã]o Penal', 'APn'],
                    'AÇÃO PENAL ORIGINÁRIA': ['A[cç][aã]o Penal Origin[áa]ria'],
                    'AÇÃO RESCISÓRIA': ['A[cç][aã]o Rescis[óo]ria', 'AR'],
                    'CARTA ROGATÓRIA': ['Carta Rogat[óo]ria', 'CR'],
                    'CAUTELAR INOMINADA CRIMINAL': ['Cautelar Inominada Criminal'],
                    'CONFLITO DE ATRIBUIÇÃO': ['Conflito de Atribui[cç][ãa]o', 'CAt'],
                    'CONFLITO DE COMPETÊNCIA': ['Conflito de Compet[êe]ncia', 'CC'],
                    'EXCEÇÃO DA VERDADE': ['Exce[cç][ãa]o da Verdade', 'ExVerd'],
                    'EXCEÇÃO DE IMPEDIMENTO': ['Exce[cç][ãa]o de Impedimento', 'ExImp'],
                    'EXCEÇÃO DE SUSPEIÇÃO': ['Exce[cç][ãa]o de Suspei[cç][ãa]o', 'ExSusp'],
                    'EXECUÇÃO EM AÇÃO RESCISÓRIA': ['Execu[cç][ão]o em A[cç][ãa]o Rescis[oó]ria', 'ExecAR'],
                    'EXECUÇÃO EM MANDADO DE SEGURANÇA': ['Execu[cç][ãa]o em Mandado de Seguran[cç]a', 'ExecMS'],
                    'EXECUÇÃO EM MEDIDA CAUTELAR': ['Execu[cç][ãa]o em Medida Cautelar', 'ExecMC'],
                    'EMBARGOS À EXECUÇÃO EM MANDADO DE SEGURANÇA': ['Embargos [aà] Execu[cç][ãa]o em Mandado de Seguran[cç][ãa]a'],
                    'EMBARGOS À EXECUÇÃO EM AÇÃO RESCISÓRIA': ['Embargos [aà] Execu[cç][ãa]o em A[cç][ãa]o Rescis[oó]ria'],
                    'EDv em RECURSO ESPECIAL': ['Embargos de Diverg[êe]ncia em Recurso Especial', 'Embargos de Diverg[êe]ncia em REsp', 'EResp', 'Embargos de Recurso Especial', 'EResps'],
                    'EDv em AGRAVO': ['Embargos de Diverg[êe]ncia em Agravo'],
                    'EMBARGOS DO ACUSADO': ['Embargos do Acusado'],
                    'EMBARGOS INFRINGENTES E DE NULIDADE': ['Embargos Infringentes e de Nulidade'],
                    'EMBARGOS INFRINGENTES EM AR': ['Embargos Infringentes em A[çc][ãa]o Rescis[óo]ria'],
                    'HABEAS CORPUS': ['Habeas Corpus', 'HC', 'habeas-corpus'],
                    'HABEAS DATA': ['Habeas Data', 'HD'],
                    'HOMOLOGAÇÃO DE DECISÃO ESTRANGEIRA': ['Homologa[cç][ãa]o de Decis[ãa]o Estrangeira'],
                    'INCIDENTE DE DESLOCAMENTO DE COMPETÊNCIA': ['Incidente de Deslocamento de Compet[êe]ncia', 'IDC'],
                    'INQUÉRITO': ['Inqu[ée]rito', 'Inq'],
                    'INTERPELAÇÃO JUDICIAL': ['Interpela[cç][ãa]o Judicial', 'IJ'],
                    'INTERVENÇÃO FEDERAL': ['Interven[cç][ãa]o Federal', 'IF'],
                    'MEDIDA CAUTELAR': ['Medida Cautelar', 'MC'],
                    'MEDIDAS INVESTIGATIVAS SOBRE ORGANIZAÇÕES CRIMINOSAS': ['Medidas Investigativas sobre Organiza[cç][õo]es Criminosas'],
                    'MEDIDAS PROTETIVAS DE URGÊNCIA - LEI MARIA DA PENHA': ['Medidas Protetivas de Urg[êe]ncia - Lei Maria da Penha'],
                    'MANDADO DE INJUNÇÃO': ['Mandado de Injun[cç][ãa]o', 'MI'],
                    'MANDADO DE SEGURANÇA': ['Mandado de Seguran[cç][ãa]a', 'MS'],
                    'PEDIDO DE BUSCA E APREENSÃO CRIMINAL': ['Pedido de Busca e Apreensão Criminal'],
                    'PEDIDO DE PRISÃO PREVENTIVA': ['Pedido de Prisão Preventiva'],
                    'PEDIDO DE QUEBRA DE SIGILO DE DADOS E/OU TELEFÔNICO': ['Pedido de Quebra de Sigilo de Dados e/ou Telef[ôo]nico'],
                    'PEDIDO DE TUTELA PROVISÓRIA': ['Pedido de Tutela Provis[óo]ria'],
                    'PEDIDO DE UNIFORMIZAÇÃO DE INTERPRETAÇÃO DE LEI': ['Pedido de Uniformiza[cç][ãa]o de Interpreta[cç][ãa]o de Lei'],
                    'PETIÇÃO': ['Peti[cç][ãa]o', 'Pet'],
                    'PRECATÓRIO': ['Precat[óo]rio', 'Prc'],
                    'RECLAMAÇÃO': ['Reclama[cç][ãa]o', 'Reclama[çc][ãa]o', 'Rcl'],
                    'RECLAMAÇÃO TRABALHISTA': ['Reclama[cç][aã]o Trabalhista'],
                    'RECURSO ESPECIAL': ['REsp'],
                    'RECURSO EXTRAORDINÁRIO': ['Recurso Extraordin[áa]rio', 'RE'],
                    'RECURSO EXTRAORDINÁRIO COM AGRAVO': ['Recurso Extraordin[áa]rio com Agravo', 'Recurso Extraordin[aá]rio com Agravo'],
                    'RECURSO ORDINÁRIO': ['Recurso Ordin[áa]rio', 'RO'],
                    'Recurso em HABEAS CORPUS' : ['RHC'],
                    'Recurso em HABEAS DATA': ['RHD'],
                    'Recurso em MANDADO DE INJUNÇÃO': ['RMI'],
                    'Recurso em MANDADO DE SEGURANÇA' : ['RMS'],
                    'REPRESENTAÇÃO': ['Representa[cç][ãa]o', 'Rp'],
                    'RESTITUIÇÃO DE COISAS APREENDIDAS': ['Restitui[cç][ãa]o de Coisas Apreendidas'],
                    'REVISÃO CRIMINAL': ['Revis[ãa]o Criminal', 'RvCr'],
                    'SENTENÇA ESTRANGEIRA': ['Senten[cç]a Estrangeira'],
                    'SENTENÇA ESTRANGEIRA CONTESTADA': ['Senten[cç][ãa]o Estrangeira Contestada', 'SEC'],
                    'SINDICÂNCIA': ['Sindic[âa]ncia', 'Sd'],
                    'SUSPENSÃO DE LIMINAR': ['SL'],
                    'SUSPENSÃO DE LIMINAR E DE SENTENÇA': ['Suspens[ãa]o de Liminar e de Senten[cç][ãa]a', 'SUSPENS[ÃA]O DE LIMINAR E DE SENTEN[ÇC]A', 'SLS'],
                    'SUSPENSÃO DE SEGURANÇA': ['Suspens[ãa]o de Seguran[cç]a', 'SS'],
                    'SUSPENSÃO DE TUTELA ANTECIPADA' : ['Suspens[ãa]o de Tutela Antecipada', 'STA'],
                    'SÚMULA': ['S[úu]mula', 'S[úu]mula', 'S[úu]m', 'Sumular', 'EN', 'S[úu]mulas'],
                    'SÚMULA VINCULANTE': ['S[úu]mula Vinculante', 'S[úu]mula vinculante'],
                    })

def get_siglas_acessorias():
    return remove_sobreposicao({'Acordo': [],
                     'ARE': ['Agravo em Recurso Especial'],
                     'AgInt' : ['Agravo Interno'],
                     'AgRg' : ['Agravo Regimental', 'AgR', 'Ag.Reg.'],
                     'AgRE' : ['AgRE'],
                     'AgRgRD' : [],
                     'AI': ['Arguição de Inconstitucionalidade'],
                     'Desis': ['Desist[êe]ncia'],
                     'Denun': ['Den[uú]ncia'],
                     'EDcl': ['Embargos de Declara[cç][aã]o', 'ED', 'EDec', 'Emb.Dec.'],
                     'EDv': ['Embargos de Diverg[êe]ncia', 'Emb.Div', 'EDv'],
                     'EAg' : ['Embargos de Diverg[êe]ncia no Agravo'],
                     'EInf' : ['Embargos Infringentes'],
                     'ImpExe': ['Impugna[cç][aã]o [àa] Execu[cç][ãa]o'],
                     'IAC' : ['Incidente de Assu[cç][ãa]o de Compet[êe]ncia'],
                     'IUJur' : ['Incidente de Uniformiza[cç][ãa]o de Jurisprud[êe]ncia', 'IUJ'],
                     'OF': [],
                     'ParExe': [],
                     'PExt': ['Pedido de Extens[aã]o'],
                     'PDist': [ 'Pedido de Distin[cç][ãa]o'],
                     'Pet': ['Petição'],
                     'PetExe' : [],
                     'PExtDe' : [],
                     'ProAfR' : ['Proposta de Afeta[cç][aã]o'],
                     'RCD' : ['Reconsidera[çc][ãa]o de Despacho', 'RD', 'RCDesp'],
                     'Recurso': [],
                     'RE' : ['Recurso Extraordin[áa]rio'],
                     'REsp': ['Recurso Especial'],
                     'RO': ['Recurso Ordin[aá]rio'],
                     'RtPaut': [],
                     'QO': ['Quest[aã]o de Ordem'],
                     'TutPrv': ['Tutela Provis[oó]ria'],
                     'Ag': ['Agravo'],
                     'Manif': [],
                     '2ºJulg': []})

def get_conectivos():
    return ['no', 'nos', 'em', 'na']

def bota_ponto_milhar(texto):
    texto = re.sub(r'(\d{1,2})(?=(\d{3})+(?!\d))',
                   r'\1.',
                   texto)
    return texto

def verifica_numero_processo(value: str) -> int:
    #Regular expression: NNNNNNN-DD.AAAA.J.TR.0000
    expression = r"\d{7}-?\d{2}.?\d{4}.?\d{1}.?\d{2}.?\d{4}"

    numero = ''.join(caractere for caractere in value if caractere.isnumeric())
    if re.search(expression, numero):
        return 1
    return 0

def conta_valores_none(jurisprudencia):
    """Conta quantos valores None existem em uma jurisprudência."""
    return sum(1 for valor in jurisprudencia.values() if valor is None)

def verifica_sobreposicao_jurisprudencia(jurisprudencias_encontradas):
    # Conjunto para armazenar os índices dos itens a serem removidos
    itens_a_remover = set()

    # Verificar duplicatas e sobreposições em uma única passagem
    for id1, valor1 in enumerate(jurisprudencias_encontradas):
        if id1 in itens_a_remover:
            continue
        inicio1, fim1 = valor1['posicao'][0]

        for id2 in range(id1 + 1, len(jurisprudencias_encontradas)):
            if id2 in itens_a_remover:
                continue
            valor2 = jurisprudencias_encontradas[id2]
            inicio2, fim2 = valor2['posicao'][0]

            # Verificar se são exatamente iguais
            if valor1 == valor2:
                itens_a_remover.add(id2)
            # Verificar sobreposição e a manutenção das informações do tribunal
            elif ((inicio2 <= inicio1 <= fim2) or (inicio2 <= fim1 <= fim2)) and valor1['numero'] == valor2['numero']:
                # Determinar qual jurisprudência remover com base nos valores None
                none_count1 = conta_valores_none(valor1)
                none_count2 = conta_valores_none(valor2)
                if none_count1 > none_count2:
                    itens_a_remover.add(id1)
                else:
                    itens_a_remover.add(id2)

    # Remover as jurisprudências marcadas para remoção
    for indice in sorted(itens_a_remover, reverse=True):
        del jurisprudencias_encontradas[indice]

    return jurisprudencias_encontradas


def remove_sobreposicao(dicionario):
    for chave in dicionario.keys():
        dicionario[chave].sort(key=len, reverse=True)
    return {k: v for k, v in sorted(dicionario.items(), key=lambda item: len(item[0]), reverse=True)}


def get_dados_padronizados(pos_inicio, pos_fim, tribunal, tipo_recurso, numero, local):
    posicao = (pos_inicio, pos_fim)
    local = local.upper() if local is not None else local
    tribunal = tribunal.upper() if tribunal is not None else tribunal

    if tribunal is not None:
        if tribunal in ['SUPERIOR TRIBUNAL DE JUSTIÇA', 'SUPREMO TRIBUNAL DE JUSTIÇA']:
            tribunal = 'STJ'
        elif tribunal in ['SUPERIOR TRIBUNAL FEDERAL', 'SUPREMO TRIBUNAL FEDERAL']:
            tribunal = 'STF'
        elif tribunal == 'TRIBUNAL REGIONAL FEDERAL':
            tribunal = 'TRF'
        else:
            estados = get_estados_brasileiros()[1]
            estados_completo = []
            for i in range(1, len(estados), 2):
              estados_completo.append(estados[i])
              padrao_tribunal_estadual = r'TRIBUNAL\s*DE\s*JUSTI[CÇ]A\s*[D][OEA]\s({})'.format('|'.join(estados_completo).upper())
            if re.search(padrao_tribunal_estadual, tribunal):
              estado_tribunal = tribunal[23:] # 23 pq é correspondente a primeira letra do estado.
              estados_brasileiros, _ = get_estados_brasileiros()
              abrev_estado = 'vazio'
              for estado in estados_brasileiros:
                padrao = re.compile(estado[1].upper())
                if padrao.search(estado_tribunal):
                  abrev_estado = estado[0]

              if abrev_estado != 'vazio':
                tribunal = 'TJ' + abrev_estado
                tribunal = 'TJ' + abrev_estado
        tribunal = tribunal.replace(' ', '').replace('-', '').replace('/', '').replace('–', '')
        if len(tribunal) > 4:
            tribunal = tribunal[:2] + tribunal[-2:]


    numero = numero.replace('\n', '')
    if not verifica_numero_processo(numero):
        numero = bota_ponto_milhar(numero)

    if tribunal is None:
        if tipo_recurso.endswith('RECURSO ESPECIAL') or tipo_recurso.endswith('Ag em RECURSO ESPECIAL'):
            tribunal = 'STJ'
        if tipo_recurso.endswith('RECURSO EXTRAORDINÁRIO') or tipo_recurso.endswith('Ag em RECURSO EXTRAORDINÁRIO'): #, 'ARE', 'AG no RE', 'A no RE', 'ACO']:
            tribunal = 'STF'

    return {'tribunal': tribunal,
          'tipo_recurso': tipo_recurso,
          'numero': numero,
          'local': local,
          'posicao': [posicao]}
    
def retorna_sigla_padronizada(sigla, siglas):
  for chave, valores in siglas.items():
    if sigla.lower() == chave.lower():
      return chave

    for valor in valores:
      if re.compile(f'^\\b({valor})\\b$', re.IGNORECASE).match(sigla):
        return chave

  return None

def remove_overlap(accessories):
    non_overlapping = []
    for acc1 in accessories:
        overlap = False
        for acc2 in accessories:
            if acc1 != acc2:
                start1, end1 = acc1['posicao']
                start2, end2 = acc2['posicao']
                if start1 <= start2 < end1 or start1 < end2 <= end1:
                    overlap = True
                    if len(acc1['sigla_acessoria']) < len(acc2['sigla_acessoria']):
                        if acc1 not in non_overlapping:
                            non_overlapping.append(acc2)
                    break
        if not overlap:
            non_overlapping.append(acc1)
    return non_overlapping


def padroniza_nomeclatura_jurisprudencia(acessorias, conectivos, grupo_principais, posicao_principais):

    reconstructed_text = ""

    all_items = sorted(acessorias + conectivos, key=lambda x: x['posicao'][0])
    for item in all_items:
        if 'sigla_padronizada' in item:
            reconstructed_text += item['sigla_padronizada'] + " "
        else:
            reconstructed_text += item['conectivo'].lower() + " "

    reconstructed_text += grupo_principais

    posicao_inicial = all_items[0]['posicao'][0] if all_items else posicao_principais[0]
    posicao_final = posicao_principais[1]

    return {'tipo_recurso': reconstructed_text, 'posicao': (posicao_inicial, posicao_final)}

def verifica_siglas(grupos, texto, siglas_principais, siglas_acessorias, conectivos):
    grupo_principais = grupos.group("principais")
    posicao_principais = grupos.start("principais")

    acessorias = []
    for sigla in siglas_acessorias:
        padrao = "\\b{}\\b |{}".format(sigla, '|'.join("\\b{}\\b ".format(s) for s in siglas_acessorias[sigla]))
        for acessoria_match in re.finditer(padrao, texto[:posicao_principais], re.IGNORECASE):
            acessoria = acessoria_match.group(0)
            if acessoria:
                acessorias.append({'sigla_acessoria': acessoria[:-1],
                                       'sigla_padronizada': retorna_sigla_padronizada(acessoria[:-1], siglas_acessorias),
                                       'posicao' : (acessoria_match.start(), acessoria_match.end())})

    acessorias = remove_overlap(acessorias)
    acessorias = sorted(acessorias, key=lambda x: x['posicao'])

    conectivos_encontrados = []

    padrao = '|'.join("\\b{}\\b ".format(s) for s in conectivos)

    for conectivo_match in re.finditer(padrao, texto[:posicao_principais], re.IGNORECASE):
        conectivo = conectivo_match.group(0)
        if conectivo:
            conectivos_encontrados.append({'conectivo': conectivo[:-1],
                                        'posicao' : (conectivo_match.start(), conectivo_match.end())})

    conectivos_encontrados = sorted(conectivos_encontrados, key=lambda x: x['posicao'])

    if len(acessorias) == 0 or len(conectivos_encontrados) == 0:
        conectivos_encontrados = []
        acessorias = []

    grupo_principais = retorna_sigla_padronizada(grupo_principais, siglas_principais)

    return padroniza_nomeclatura_jurisprudencia(acessorias, conectivos_encontrados, grupo_principais, (grupos.start("principais"), grupos.end("principais"))), grupos.group()


def busca_jurisprudencia(texto):
    siglas_principais = get_siglas_principais()
    siglas_acessorias = get_siglas_acessorias()
    conectivos = get_conectivos()
    estados = get_estados_brasileiros()[1]
    tribunais_superiores = get_tribunais_federais()
    tribunais_estaduais = get_tribunais_estaduais()
    tribunais = tribunais_superiores + tribunais_estaduais

    padrao_acessorias = "|".join(f"(?P<acessorias_{index}>{sigla}|{'|'.join(siglas_acessorias[sigla])})" for index, sigla in enumerate(siglas_acessorias))
    padrao_principais = "|".join(f"({chave}|{'|'.join(siglas_principais[chave])})" for chave in siglas_principais)
    padrao_conectivos = "|".join(f"(?P<conectivos_{i}>{conectivo})" for i, conectivo in enumerate(conectivos))

    regex = (
            f"("
            f"( {padrao_acessorias}) ({padrao_conectivos}) "
            f")*"
            f"(?P<principais>{padrao_principais})\\b"
            )

    w = r'[A-Za-zÀ-ÄÇ-ÏÒ-ÖÙ-Üà-äç-ïò-öù-ü]'
    bl = r'(?:(?<!{})(?={}))'.format(w, w)
    br = r'(?:(?<={})(?!{}))'.format(w, w)
    padrao_numero = r'(\d[\d\.\n\-/]*\d)'
    padrao_local = r'({})'.format("|".join(map(re.escape, estados)))
    padrao_tribunal_superior = r'({})'.format("|".join(map(re.escape, tribunais_superiores)))
    padrao_tribunal_estadual = r'({})'.format("|".join(tribunais_estaduais))
    sep = r'\D{0,9}'
    sep_curto = r'\D{0,5}'

    jurisprudencias_encontradas = []

    recursos = []
    textos_jurisprudencia = []

    for g in list(re.finditer(regex, texto, re.I)):
        recurso, texto_jurisprudencia = verifica_siglas(g, g.group(), siglas_principais, siglas_acessorias, conectivos)
        recursos.append(recurso)
        textos_jurisprudencia.append(texto_jurisprudencia) # guarda o texto das jurisprudencias

    recurso_sumulas = []

    for padrao_abreviatura, recurso in zip(textos_jurisprudencia, recursos):
        if padrao_abreviatura.lower() in ['súmulas', 'sumulas']:
            recurso_sumulas.append(recurso)
            continue
        #remove o primeiro caractere q é um espaço
        padrao_abreviatura = r'({})'.format(padrao_abreviatura[1:]) if padrao_abreviatura.startswith(' ') else r'({})'.format(padrao_abreviatura[:])

        padrao_1 = r'\b{}?{}\b{}{}{}{}{}\b{}\b'.format(padrao_tribunal_superior, sep, padrao_abreviatura, br, sep, padrao_numero, sep_curto, padrao_local)
        padrao_1_1 = r'\b{}{}\b{}{}{}{}{}\b{}\b'.format(padrao_tribunal_superior, sep, padrao_abreviatura, br, sep, padrao_numero, sep_curto, padrao_local)
        padrao_2 = r'\b{}?{}\b{}{}{}{}{}\b{}\b'.format(padrao_tribunal_superior, sep, padrao_local, br, sep, padrao_numero, sep, padrao_abreviatura)
        padrao_3 = r'\b{}?{}\b{}{}\b{}\b{}\b{}\b'.format(padrao_tribunal_superior, sep, padrao_numero, sep, padrao_abreviatura, sep, padrao_local)
        padrao_4 = r'\b{}?{}\b{}\b{}\b{}\b{}\b{}'.format(padrao_tribunal_superior, sep, padrao_local, sep, padrao_abreviatura, sep, padrao_numero)

        padrao_5 = r'\b{}{}{}{}(?:{}\b{}\b)'.format(padrao_abreviatura, br, sep, padrao_numero, sep, padrao_tribunal_estadual)
        padrao_6 = r'\b{}{}{}{}{}\b{}\b'.format(padrao_tribunal_estadual, br, sep, padrao_numero, sep, padrao_abreviatura)
        padrao_7 = r'\b{}{}\b{}\b{}\b{}\b'.format(padrao_numero, sep, padrao_abreviatura, sep, padrao_tribunal_estadual)
        padrao_8 = r'\b{}\b{}\b{}\b{}\b{}'.format(padrao_tribunal_estadual, sep, padrao_abreviatura, sep, padrao_numero)

        padrao_9 = r'\b{}{}{}{}(?:{}\b{}\b)'.format(padrao_abreviatura, br, sep, padrao_numero, sep, padrao_tribunal_superior)
        padrao_10 = r'\b{}{}{}{}{}\b{}\b'.format(padrao_tribunal_superior, br, sep, padrao_numero, sep, padrao_abreviatura)
        padrao_11 = r'\b{}{}\b{}\b{}\b{}\b'.format(padrao_numero, sep, padrao_abreviatura, sep, padrao_tribunal_superior)
        padrao_12 = r'\b{}\b{}\b{}\b{}\b{}'.format(padrao_tribunal_superior, sep, padrao_abreviatura, sep, padrao_numero)
        
        #tipo_padrao, tribunal, número, local
        padroes = [(padrao_1_1, 0, 2, 3),
                    (padrao_1, 0, 2, 3),
                    (padrao_2, 0, 2, 1),
                    (padrao_3, 0, 1, 3),
                    (padrao_4, 0, 3, 1),
                    (padrao_5, 2, 1, None),
                    (padrao_6, 0, 1, None),
                    (padrao_7, 2, 0, None),
                    (padrao_8, 0, 2, None),
                    (padrao_9, 2, 1, None),
                    (padrao_10, 0, 1, None),
                    (padrao_11, 2, 0, None),
                    (padrao_12, 0, 2, None)]

        for padrao, id_tribunal, id_numero, id_local in padroes:
            for m in re.finditer(padrao, texto, flags=re.I):
                tribunal = m.groups()[id_tribunal] if id_tribunal is not None else None
                numero = None
                if m.groups()[id_numero] is not None:
                    if m.groups()[id_numero].isdigit():
                        numero = str(int(m.groups()[id_numero]))
                    elif m.groups()[id_numero].replace('-', '').replace('.', '').isdigit():
                        numero = m.groups()[id_numero]
                local = m.groups()[id_local] if id_local is not None else None

                jurisprudencias_encontradas.append(get_dados_padronizados(m.start(), m.end(), tribunal, recurso['tipo_recurso'], numero, local))
                

    # sumulas
    for recurso in recurso_sumulas:
        padrao = r'({})'.format('S[uú]mula')
        padrao_numeros = r'(\d+(?:[,\se\n]+\d+)*)'
        padrao_tribunal = r'({})'.format("|".join(tribunais))

        padrao_multiplas_sumulas = r'{}{}{}{}{}{}'.format(bl, padrao, sep, padrao_numeros, sep, padrao_tribunal)

        for m in re.finditer(padrao_multiplas_sumulas, texto, flags=re.I):
            tipo_jurisprudencia = recurso['tipo_recurso']
            tribunal = m.groups()[2].upper() if m.groups()[2] is not None else m.groups()[2]
            padrao_numero_interno = r'(\d+)'
            for n in re.finditer(padrao_numero_interno, m.groups()[1]):
                numero = n.groups()[0]
                jurisprudencias_encontradas.append(get_dados_padronizados(m.start(), m.end(), tribunal, tipo_jurisprudencia, numero, local=None))

    return verifica_sobreposicao_jurisprudencia(jurisprudencias_encontradas)
    
### JURISPRUDENCIA ###

### BUSCA JURI ###

def busca_juri(texto):
    return valida_kgl(busca_jurisprudencia(texto))

### BUSCA JURI ###


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
                distancia = abs(posicao_artigo[0] - posicao_dispositivo[0])
                
                
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
    
    url = 'http://localhost:5000/?'
    url += 'tipo={}&'.format(idx_tipo)
    url += 'lei={}&'.format(numero)
    url += 'ano={}&'.format(data)
    url += 'artigo={}&'.format(artigo)
    url += 'complemento={}&'.format(argumento_artigo)
    url += 'paragrafo={}&'.format(paragrafo)
    url += 'inciso={}&'.format(inciso)
    url += 'alinea={}&'.format(alinea)
    url += 'item={}'.format(item)
    
    consulta = eval(requests.get(url).content.decode())
    dispositivos = []
    
    if consulta:
        for dispositivo in consulta:   
            lei = list(dispositivo.keys())[0]
            dispositivos.append({'dispositivo': (flag, tipo, lei),
                                 'ementa': list(dispositivo.values())[0]})
            
    return dispositivos

def ConsultaArtigo(legislacao, d):
    #texto_bruto = legislacao[0][0]
    artigo = legislacao[0][1][0]
    argumento_artigo = legislacao[0][1][1]
    paragrafo = legislacao[0][1][2]
    inciso = legislacao[0][1][3]
    alinea = legislacao[0][1][4]
    item = legislacao[0][1][5]
    
    split = str(legislacao[1][1][0]).split('_')
    tipo = int(split[0])
    numero = split[1]
    data = split[2]
    
    flag_indireta = legislacao[0][3]
    
    if (len(artigo) > 3) and '.' not in artigo:
        artigo = re.sub(r'(\d{1,2})(?=(\d{3})+(?!\d))',
                        r'\1.',
                        artigo)
    
    tupla = (tipo, numero, data, artigo, argumento_artigo, paragrafo, inciso, alinea, item)

    if tupla in d:
        artigos = []
        artigos.append({'artigo': tupla[3:],
                        'texto_artigo': d[tupla]['texto_artigo'],
                        'jurisprudencias': d[tupla]['jurisprudencias'],
                        'flag_indireta': flag_indireta})
    else:
        data = data if data else 0
        artigo = artigo if artigo else '0'
        argumento_artigo = argumento_artigo if argumento_artigo else '0'
        paragrafo = paragrafo if paragrafo else '0'
        inciso = inciso if inciso else '0'
        alinea = alinea if alinea else '0'
        item = item if item else '0'
        
        url = 'http://localhost:5000/?'
        url += 'tipo={}&'.format(tipo)
        url += 'lei={}&'.format(numero)
        url += 'ano={}&'.format(int(data.split('-')[0]))
        url += 'artigo={}&'.format(artigo)
        url += 'complemento={}&'.format(argumento_artigo)
        url += 'paragrafo={}&'.format(paragrafo)
        url += 'inciso={}&'.format(inciso)
        url += 'alinea={}&'.format(alinea)
        url += 'item={}'.format(item)

        consulta = eval(requests.get(url).content.decode())

        artigos = []
        if consulta is not None:

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

def ConsultaGCL(legislacao, d=[]):  
    if len(legislacao) >= 3:
        sugestoes = ConsultaDispositivo(legislacao)           
    else:
        sugestoes = ConsultaArtigo(legislacao, d) 
    
    
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
                elif s[0] == 1:
                    sugestoes_padronizadas_dispositivos.append('{}'.format(PadronizaNomeLei(texto_bruto_dispositivo)))
                else:
                    sugestoes_padronizadas_dispositivos.append('{} n° {}/{}'.format(s[1],
                                                                                    s[2].split('_')[1],
                                                                                    s[2].split('_')[2].split('-')[0]))
            
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
    
    jurisprudencias_texto = busca_juri(texto)

    return {'extensao':{'artigos_e_dispositivos': dado_saida_json,
                        'jurisprudencias_texto': jurisprudencias_texto}}
### AILA ###

### MOCK DATA ###
'''
lista_artigos_jurisprudencias = [(3, '3.689', date(1941, 10, 3), '158'),
                                 (3, '3.689', date(1941, 10, 3), '386'),
                                 (3, '3.689', date(1941, 10, 3), '387'),
                                 (3, '3.689', date(1941, 10, 3), '403'),
                                 (3, '3.689', date(1941, 10, 3), '404'),
                                 (3, '2.848', date(1940, 12, 7), '13'),
                                 (3, '2.848', date(1940, 12, 7), '16'),
                                 (3, '2.848', date(1940, 12, 7), '32'),
                                 (3, '2.848', date(1940, 12, 7), '42'),
                                 (3, '2.848', date(1940, 12, 7), '63')]

jurisprudencias = {}
for artigo in lista_artigos_jurisprudencias:
    url = 'http://gcl:5000/?'
    url += 'tipo={}&'.format(artigo[0])
    url += 'lei={}&'.format(artigo[1])
    url += 'data={}&'.format(artigo[2].strftime('%d/%m/%Y'))
    url += 'artigo={}&'.format(artigo[3])
    url += 'complemento={}&'.format('0')
    url += 'paragrafo={}&'.format('0')
    url += 'inciso={}&'.format('0')
    url += 'alinea={}&'.format('0')
    url += 'item={}'.format('0')
    
    consulta = eval(requests.get(url).content.decode())
    jurisprudencias[artigo] = list(consulta[0].values())[0][1]

d = {}

d_00 = {(3, '3.689', date(1941, 10, 3), '158', None, None, None, None, None): {'artigo': ('158', None, None, None, None, None),
                                                             'texto_artigo': 'Art. 158. Quando a infração deixar vestígios, será indispensável o exame de corpo de delito, direto ou indireto, não podendo supri-lo a confissão do acusado.',
                                                             'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '158')]},
        (3, '3.689', date(1941, 10, 3), '158', None, None, 'I', None, None): {'artigo': ('158', None, None, 'I', None, None),
                                                          'texto_artigo': 'I - violência doméstica e familiar contra mulher;   (Incluído dada pela Lei nº 13.721, de 2018)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '158')]},
        (3, '3.689', date(1941, 10, 3), '158', None, None, 'II', None, None): {'artigo': ('158', None, None, 'II', None, None),
                                                          'texto_artigo': 'II - violência contra criança, adolescente, idoso ou pessoa com deficiência.   (Incluído dada pela Lei nº 13.721, de 2018)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '158')]}}
d.update(d_00)

d_01 = {(3, '3.689', date(1941, 10, 3), '386', None, None, None, None, None): {'artigo': ('386', None, None, None, None, None),
                                                             'texto_artigo': 'Art. 386.  O juiz absolverá o réu, mencionando a causa na parte dispositiva, desde que reconheça:',
                                                             'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, None, 'I', None, None): {'artigo': ('386', None, None, 'I', None, None),
                                                          'texto_artigo': 'I - estar provada a inexistência do fato;',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, None, 'II', None, None): {'artigo': ('386', None, None, 'II', None, None),
                                                          'texto_artigo': 'II - não haver prova da existência do fato;',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, None, 'III', None, None): {'artigo': ('386', None, None, 'III', None, None),
                                                          'texto_artigo': 'III - não constituir o fato infração penal;',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, None, 'IV', None, None): {'artigo': ('386', None, None, 'IV', None, None),
                                                          'texto_artigo': 'IV -  estar provado que o réu não concorreu para a infração penal;           (Redação dada pela Lei nº 11.690, de 2008)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, None, 'V', None, None): {'artigo': ('386', None, None, 'V', None, None),
                                                          'texto_artigo': 'V - não existir prova de ter o réu concorrido para a infração penal;          (Redação dada pela Lei nº 11.690, de 2008)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, None, 'VI', None, None): {'artigo': ('386', None, None, 'VI', None, None),
                                                          'texto_artigo': 'VI - existirem circunstâncias que excluam o crime ou isentem o réu de pena (arts. 20, 21, 22, 23, 26 e § 1º do art. 28, todos do Código Penal), ou mesmo se houver fundada dúvida sobre sua existência;            (Redação dada pela Lei nº 11.690, de 2008)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, None, 'VII', None, None): {'artigo': ('386', None, None, 'VII', None, None),
                                                          'texto_artigo': 'VII - não existir prova suficiente para a condenação.          (Incluído pela Lei nº 11.690, de 2008)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, 'unico', None, None, None): {'artigo': ('386', None, 'unico', None, None, None),
                                                                'texto_artigo': 'Parágrafo único.  Na sentença absolutória, o juiz:',
                                                                'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, 'unico', 'I', None, None): {'artigo': ('386', None, 'unico', 'I', None, None),
                                                             'texto_artigo': 'I - mandará, se for o caso, pôr o réu em liberdade;',
                                                             'jurisprudencia': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, 'unico', 'II', None, None): {'artigo': ('386', None, 'unico', 'II', None, None),
                                                             'texto_artigo': 'II - ordenará a cessação das medidas cautelares e provisoriamente aplicadas;         (Redação dada pela Lei nº 11.690, de 2008)',
                                                             'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]},
        (3, '3.689', date(1941, 10, 3), '386', None, 'unico', 'III', None, None): {'artigo': ('386', None, 'unico', 'III', None, None),
                                                             'texto_artigo': 'III - aplicará medida de segurança, se cabível.',
                                                             'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '386')]}}
d.update(d_01)

d_02 = {(3, '3.689', date(1941, 10, 3), '387', None, None, None, None, None): {'artigo': ('387', None, None, None, None, None),
                                                             'texto_artigo': 'Art. 387.  O juiz, ao proferir sentença condenatória:             (Vide Lei nº 11.719, de 2008)',
                                                             'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '387')]},
        (3, '3.689', date(1941, 10, 3), '387', None, None, 'I', None, None): {'artigo': ('387', None, None, 'I', None, None),
                                                          'texto_artigo': 'I - mencionará as circunstâncias agravantes ou atenuantes definidas no Código Penal, e cuja existência reconhecer;',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '387')]},
        (3, '3.689', date(1941, 10, 3), '387', None, None, 'II', None, None): {'artigo': ('387', None, None, 'II', None, None),
                                                          'texto_artigo': 'II - mencionará as outras circunstâncias apuradas e tudo o mais que deva ser levado em conta na aplicação da pena, de acordo com o disposto nos arts. 59 e 60 do Decreto-Lei no 2.848, de 7 de dezembro de 1940 - Código Penal;           (Redação dada pela Lei nº 11.719, de 2008).',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '387')]},
        (3, '3.689', date(1941, 10, 3), '387', None, None, 'III', None, None): {'artigo': ('387', None, None, 'III', None, None),
                                                          'texto_artigo': 'III - aplicará as penas de acordo com essas conclusões;           (Redação dada pela Lei nº 11.719, de 2008).',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '387')]},
        (3, '3.689', date(1941, 10, 3), '387', None, None, 'IV', None, None): {'artigo': ('387', None, None, 'IV', None, None),
                                                          'texto_artigo': 'IV - fixará valor mínimo para reparação dos danos causados pela infração, considerando os prejuízos sofridos pelo ofendido;           (Redação dada pela Lei nº 11.719, de 2008).',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '387')]},
        (3, '3.689', date(1941, 10, 3), '387', None, None, 'V', None, None): {'artigo': ('387', None, None, 'V', None, None),
                                                          'texto_artigo': 'V - atenderá, quanto à aplicação provisória de interdições de direitos e medidas de segurança, ao disposto no Título Xl deste Livro;',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '387')]},
        (3, '3.689', date(1941, 10, 3), '387', None, None, 'VI', None, None): {'artigo': ('387', None, None, 'VI', None, None),
                                                          'texto_artigo': 'VI - determinará se a sentença deverá ser publicada na íntegra ou em resumo e designará o jornal em que será feita a publicação (art. 73, § 1o, do Código Penal).',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '387')]},
        (3, '3.689', date(1941, 10, 3), '387', None, 1, None, None, None): {'artigo': ('387', None, 1, None, None, None),
                                                          'texto_artigo': '§ 1o  O juiz decidirá, fundamentadamente, sobre a manutenção ou, se for o caso, a imposição de prisão preventiva ou de outra medida cautelar, sem prejuízo do conhecimento de apelação que vier a ser interposta. (Incluído pela Lei nº 12.736, de 2012)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '387')]},
        (3, '3.689', date(1941, 10, 3), '387', None, 2, None, None, None): {'artigo': ('387', None, 2, None, None, None),
                                                          'texto_artigo': '§ 2o  O tempo de prisão provisória, de prisão administrativa ou de internação, no Brasil ou no estrangeiro, será computado para fins de determinação do regime inicial de pena privativa de liberdade.            (Incluído pela Lei nº 12.736, de 2012)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '387')]}}
d.update(d_02)

d_03 = {(3, '3.689', date(1941, 10, 3), '403', None, None, None, None, None): {'artigo': ('403', None, None, None, None, None),
                                                             'texto_artigo': 'Art. 403. Não havendo requerimento de diligências, ou sendo indeferido, serão oferecidas alegações finais orais por 20 (vinte) minutos, respectivamente, pela acusação e pela defesa, prorrogáveis por mais 10 (dez), proferindo o juiz, a seguir, sentença. (Redação dada pela Lei no 11.719, de 2008)',
                                                             'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '403')]},
        (3, '3.689', date(1941, 10, 3), '403', None, 1, None, None, None): {'artigo': ('403', None, 1, None, None, None),
                                                          'texto_artigo': '§ 1o Havendo mais de um acusado, o tempo previsto para a defesa de cada um será individual. (Incluído pela Lei no 11.719, de 2008)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '403')]},
        (3, '3.689', date(1941, 10, 3), '403', None, 2, None, None, None): {'artigo': ('403', None, 2, None, None, None),
                                                          'texto_artigo': '§ § 2o Ao assistente do Ministério Público, após a manifestação desse, serão concedidos 10 (dez) minutos, prorrogando-se por igual período o tempo de manifestação da defesa. (Incluído pela Lei no 11.719, de 2008)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '403')]},
        (3, '3.689', date(1941, 10, 3), '403', None, 3, None, None, None): {'artigo': ('403', None, 3, None, None, None),
                                                          'texto_artigo': '§ 3o O juiz poderá, considerada a complexidade do caso ou o número de acusados, conceder às partes o prazo de 5 (cinco) dias sucessivamente para a apresentação de memoriais. Nesse caso, terá o prazo de 10 (dez) dias para proferir a sentença. (Incluído pela Lei no 11.719, de 2008)',
                                                          'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '403')]}}
d.update(d_03)

d_04 = {(3, '3.689', date(1941, 10, 3), '404', None, None, None, None, None): {'artigo': ('404', None, None, None, None, None),
                                                             'texto_artigo': 'Art. 404. Ordenado diligência considerada imprescindível, de ofício ou a requerimento da parte, a audiência será concluída sem as alegações finais. (Redação dada pela Lei no 11.719, de 2008)',
                                                             'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '404')]},
        (3, '3.689', date(1941, 10, 3), '404', None, 'unico', None, None, None): {'artigo': ('404', None, 'unico', None, None, None),
                                                                'texto_artigo': 'Parágrafo único. Realizada, em seguida, a diligência determinada, as partes apresentarão, no prazo sucessivo de 5 (cinco) dias, suas alegações finais, por memorial, e, no prazo de 10 (dez) dias, o juiz proferirá a sentença. (Incluído pela Lei no 11.719, de 2008)',
                                                                'jurisprudencias': jurisprudencias[(3, '3.689', date(1941, 10, 3), '404')]}}
d.update(d_04)

d_05 = {(3, '2.848', date(1940, 12, 7), '14', None, None, None, None, None): {'artigo': ('14', None, None, None, None, None),
                                                            'texto_artigo': 'Art. 14 - Diz-se o crime: (Redação dada pela Lei nº 7.209, de 11.7.1984)',
                                                            'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '13')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '14', None, None, 'I', None, None): {'artigo': ('14', None, None, 'I', None, None),
                                                         'texto_artigo': 'I - consumado, quando nele se reúnem todos os elementos de sua definição legal; (Incluído pela Lei nº 7.209, de 11.7.1984)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '13')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '14', None, None, 'II', None, None): {'artigo': ('14', None, None, 'II', None, None),
                                                         'texto_artigo': 'II - tentado, quando, iniciada a execução, não se consuma por circunstâncias alheias à vontade do agente. (Incluído pela Lei nº 7.209, de 11.7.1984)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '13')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '14', None, 'unico', None, None, None): {'artigo': ('14', None, 'unico', None, None, None),
                                                               'texto_artigo': 'Parágrafo único - Salvo disposição em contrário, pune-se a tentativa com a pena correspondente ao crime consumado, diminuída de um a dois terços.(Incluído pela Lei nº 7.209, de 11.7.1984)',
                                                               'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '13')]}} # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
d.update(d_05)

d_06 = {(3, '2.848', date(1940, 12, 7), '17', None, None, None, None, None): {'artigo': ('17', None, None, None, None, None),
                                                            'texto_artigo': 'Art. 17 - Não se pune a tentativa quando, por ineficácia absoluta do meio ou por absoluta impropriedade do objeto, é impossível consumar-se o crime. (Redação dada pela Lei no 7.209, de 11.7.1984)',
                                                            'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '16')]}} # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
d.update(d_06)


d_07 = {(3, '2.848', date(1940, 12, 7), '33', None, None, None, None, None): {'artigo': ('33', None, None, None, None, None),
                                                            'texto_artigo': 'Art. 33 - A pena de reclusão deve ser cumprida em regime fechado, semi-aberto ou aberto. A de detenção, em regime semi-aberto, ou aberto, salvo necessidade de transferência a regime fechado. (Redação dada pela Lei nº 7.209, de 11.7.1984)',
                                                            'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '33', None, '1', None, None, None): {'artigo': ('33', None, 1, None, None, None),
                                                         'texto_artigo': '§ 1º - Considera-se: (Redação dada pela Lei nº 7.209, de 11.7.1984)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo        
        (3, '2.848', date(1940, 12, 7), '33', None, '1', None, None, 'a', None): {'artigo': ('33', None, 1, None, None, 'a', None),
                                                              'texto_artigo': 'a) regime fechado a execução da pena em estabelecimento de segurança máxima ou média;',
                                                              'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '33', None, '1', None, None, 'b', None): {'artigo': ('33', None, 1, None, None, 'b', None),
                                                              'texto_artigo': 'b) regime semi-aberto a execução da pena em colônia agrícola, industrial ou estabelecimento similar;',
                                                              'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '33', None, '1', None, None, 'c', None): {'artigo': ('33', None, 1, None, None, 'c', None),
                                                              'texto_artigo': 'c) regime aberto a execução da pena em casa de albergado ou estabelecimento adequado.',
                                                              'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '33', None, '2', None, None, None): {'artigo': ('33', None, 2, None, None, None),
                                                         'texto_artigo': '§ 2º - As penas privativas de liberdade deverão ser executadas em forma progressiva, segundo o mérito do condenado, observados os seguintes critérios e ressalvadas as hipóteses de transferência a regime mais rigoroso: (Redação dada pela Lei nº 7.209, de 11.7.1984)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '33', None, '2', None, None, 'a', None): {'artigo': ('33', None, 2, None, None, 'a', None),
                                                              'texto_artigo': 'a) o condenado a pena superior a 8 (oito) anos deverá começar a cumpri-la em regime fechado;',
                                                              'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '33', None, '2', None, None, 'b', None): {'artigo': ('33', None, 2, None, None, 'b', None),
                                                              'texto_artigo': 'b) o condenado não reincidente, cuja pena seja superior a 4 (quatro) anos e não exceda a 8 (oito), poderá, desde o princípio, cumpri-la em regime semi-aberto;',
                                                              'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '33', None, '2', None, None, 'c', None): {'artigo': ('33', None, 2, None, None, 'c', None),
                                                              'texto_artigo': 'c) o condenado não reincidente, cuja pena seja igual ou inferior a 4 (quatro) anos, poderá, desde o início, cumpri-la em regime aberto.',
                                                              'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '33', None, '3', None, None, None): {'artigo': ('33', None, 3, None, None, None),
                                                         'texto_artigo': '§ 3º - A determinação do regime inicial de cumprimento da pena far-se-á com observância dos critérios previstos no art. 59 deste Código.(Redação dada pela Lei nº 7.209, de 11.7.1984)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '33', None, '4', None, None, None): {'artigo': ('33', None, 4, None, None, None),
                                                         'texto_artigo': '§ 4o O condenado por crime contra a administração pública terá a progressão de regime do cumprimento da pena condicionada à reparação do dano que causou, ou à devolução do produto do ilícito praticado, com os acréscimos legais. (Incluído pela Lei nº 10.763, de 12.11.2003)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '32')]}} # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
d.update(d_07)

d_08 = {(3, '2.848', date(1940, 12, 7), '44', None, None, None, None, None): {'artigo': ('44', None, None, None, None, None),
                                                            'texto_artigo': 'Art. 44. As penas restritivas de direitos são autônomas e substituem as privativas de liberdade, quando: (Redação dada pela Lei n° 9.714, de 1998)',
                                                            'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '42')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '44', None, None, 'I', None, None): {'artigo': ('44', None, None, 'I', None, None),
                                                         'texto_artigo': 'I aplicada pena privativa de liberdade não superior a quatro anos e o crime não for cometido com violência ou grave ameaça à pessoa ou, qualquer que seja a pena aplicada, se o crime for culposo;(Redação dada pela Lei n° 9.714, de 1998)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '42')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '44', None, None, 'II', None, None): {'artigo': ('44', None, None, 'II', None, None),
                                                         'texto_artigo': 'II o réu não for reincidente em crime doloso; (Redação dada pela Lei n° 9.714, de 1998)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '42')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '44', None, None, 'III', None, None): {'artigo': ('44', None, None, 'III', None, None),
                                                         'texto_artigo': 'III a culpabilidade, os antecedentes, a conduta social e a personalidade do condenado, bem como os motivos e as circunstâncias indicarem que essa substituição seja suficiente. (Redação dada pela Lei n° 9.714, de 1998)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '42')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '44', None, '1', None, None, None): {'artigo': ('44', None, 1, None, None, None),
                                                         'texto_artigo': '§ 1° (VETADO) (Incluído pela Lei n° 9.714, de 1998)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '42')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '44', None, '2', None, None, None): {'artigo': ('44', None, 2, None, None, None),
                                                         'texto_artigo': '§ 2° Na condenação igual ou inferior a um ano, a substituição pode ser feita por multa ou por uma pena restritiva de direitos; se superior a um ano, a pena privativa de liberdade pode ser substituída por uma pena restritiva de direitos e multa ou por duas restritivas de direitos. (Incluído pela Lei n° 9.714, de 1998)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '42')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '44', None, '3', None, None, None): {'artigo': ('44', None, 3, None, None, None),
                                                         'texto_artigo': '§ 3° Se o condenado for reincidente, o juiz poderá aplicar a substituição, desde que, em face de condenação anterior, a medida seja socialmente recomendável e a reincidência não se tenha operado em virtude da prática do mesmo crime. (Incluído pela Lei n° 9.714, de 1998)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '42')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '44', None, '4', None, None, None): {'artigo': ('44', None, 4, None, None, None),
                                                         'texto_artigo': '§ 4° A pena restritiva de direitos converte-se em privativa de liberdade quando ocorrer o descumprimento injustificado da restrição imposta. No cálculo da pena privativa de liberdade a executar será deduzido o tempo cumprido da pena restritiva de direitos, respeitado o saldo mínimo de trinta dias de detenção ou reclusão. (Incluído pela Lei n° 9.714, de 1998)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '42')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '44', None, '5', None, None, None): {'artigo': ('44', None, 5, None, None, None),
                                                         'texto_artigo': '§ 5° Sobrevindo condenação a pena privativa de liberdade, por outro crime, o juiz da execução penal decidirá sobre a conversão, podendo deixar de aplicá-la se for possível ao condenado cumprir a pena substitutiva anterior. (Incluído pela Lei n° 9.714, de 1998)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '42')]}} # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
d.update(d_08)

d_09 = {(3, '2.848', date(1940, 12, 7), '65', None, None, None, None, None): {'artigo': ('65', None, None, None, None, None),
                                                            'texto_artigo': 'Art. 65 - São circunstâncias que sempre atenuam a pena: (Redação dada pela Lei nº 7.209, de 11.7.1984)',
                                                            'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '63')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '65', None, None, 'I', None, None): {'artigo': ('65', None, None, 'I', None, None),
                                                         'texto_artigo': ' I - ser o agente menor de 21 (vinte e um), na data do fato, ou maior de 70 (setenta) anos, na data da sentença; (Redação dada pela Lei nº 7.209, de 11.7.1984)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '63')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '65', None, None, 'II', None, None): {'artigo': ('65', None, None, 'II', None, None),
                                                         'texto_artigo': 'II - o desconhecimento da lei; (Redação dada pela Lei nº 7.209, de 11.7.1984)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '63')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '65', None, None, 'III', None, None): {'artigo': ('65', None, None, 'III', None, None),
                                                         'texto_artigo': 'III - ter o agente:(Redação dada spela Lei nº 7.209, de 11.7.1984)',
                                                         'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '63')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '65', None, None, 'III', 'a', None): {'artigo': ('65', None, None, 'III', 'a', None),
                                                        'texto_artigo': 'a) cometido o crime por motivo de relevante valor social ou moral;',
                                                        'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '63')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '65', None, None, 'III', 'b', None): {'artigo': ('65', None, None, 'III', 'b', None),
                                                        'texto_artigo': 'b) procurado, por sua espontânea vontade e com eficiência, logo após o crime, evitar-lhe ou minorar-lhe as conseqüências, ou ter, antes do julgamento, reparado o dano;',
                                                        'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '63')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '65', None, None, 'III', 'c', None): {'artigo': ('65', None, None, 'III', 'c', None),
                                                        'texto_artigo': 'c) cometido o crime sob coação a que podia resistir, ou em cumprimento de ordem de autoridade superior, ou sob a influência de violenta emoção, provocada por ato injusto da vítima;',
                                                        'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '63')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '65', None, None, 'III', 'd', None): {'artigo': ('65', None, None, 'III', 'd', None),
                                                        'texto_artigo': 'd) confessado espontaneamente, perante a autoridade, a autoria do crime;',
                                                        'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '63')]}, # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
        (3, '2.848', date(1940, 12, 7), '65', None, None, 'III', 'e', None): {'artigo': ('65', None, None, 'III', 'e', None),
                                                        'texto_artigo': 'e) cometido o crime sob a influência de multidão em tumulto, se não o provocou.',
                                                        'jurisprudencias': jurisprudencias[(3, '2.848', date(1940, 12, 7), '63')]}} # Erro no GCL, jurisprudencia trocada nos artigos daquele codigo
d.update(d_09)'''
### MOCK DATA ###