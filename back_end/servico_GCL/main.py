import re
import json
from roman import toRoman, fromRoman, InvalidRomanNumeralError
from unicodedata import normalize

# Necessário, se não bug. param: Legis_Class = Arquivo .py com a classe Legis. script.py não funciona.
from Entities.Legislacao import Legislacao

def artigo_tree(texto_legis, artigo, arg_artigo, paragrafo, inciso, alinea, item):
    """Função que segue a estrutura do Artigo."""
    match_artigo = re.compile(fr"^Art\.\s? ?{artigo}\ş?(?: º|º|\.|o|°)?.*?(?=^Art\.\s? ?[1-9]\ş?)",
                              re.MULTILINE | re.DOTALL).findall(texto_legis)
    # verifica se o artigo existe
    if len(match_artigo) != 0:
        match_artigo_tree = re.compile(fr"^Art\.\s? ?{artigo}\ş?(?: º|º|\.|o|°)?.*?:", re.MULTILINE).findall(
            match_artigo[0])
        # artigo com tree - Art.1 ... :
        if len(match_artigo_tree) != 0:
            # -------------------------------------------------------------------------------------
            # TODO: Artigos que vigoram algo -> "" (Questionar)
            # match_artigo_update = re.compile(fr"^“.*?(?=”)",
            #                                  re.MULTILINE | re.DOTALL).findall(match_artigo[0])
            # if len(match_artigo_update) != 0:
            #     return "Artigo que Vigora Algo"

            # -------------------------------------------------------------------------------------

            if arg_artigo != '0':
                match_art_comp = re.compile(fr"^Art\.\s? ?{artigo}\-{arg_artigo}.*?(?=^Art\.\s? ?{artigo})",
                                            re.MULTILINE | re.DOTALL).findall(match_artigo[0])
                if len(match_art_comp) != 0:
                    return new_art_tree(artigo, arg_artigo, paragrafo, inciso, alinea, item, match_art_comp, texto_legis)
                else:
                    match_art_comp = re.compile(fr"^Art\.\s? ?{artigo}\-{arg_artigo}.*",
                                                re.MULTILINE | re.DOTALL).findall(match_artigo[0])
                    if len(match_art_comp) != 0:
                        return new_art_tree(artigo, arg_artigo, paragrafo, inciso, alinea, item, match_art_comp, texto_legis)
                    else:
                        return None
            return new_art_tree(artigo, arg_artigo, paragrafo, inciso, alinea, item, match_artigo, texto_legis)

        # artigo sem tree - Art. 1 ... . paragrafo ...
        else:
            match_artigo = re.compile(fr"^Art\.\s? ?{artigo}\ş?(?: º|º|\.|o|°)?.*",
                                      re.MULTILINE | re.DOTALL).findall(match_artigo[0])
            if len(match_artigo) != 0:
                return new_art_tree(artigo, arg_artigo, paragrafo, inciso, alinea, item, match_artigo, texto_legis)
            else:
                return None
    else:
        # Ultimo Artigo
        match_artigo = re.compile(fr"^Art\.\s? ?{artigo}\ş?(?: º|º|\.|o|°)?.*",
                                  re.MULTILINE | re.DOTALL).findall(texto_legis)
        if len(match_artigo) != 0:
            # verifica se tem tree:
            match_artigo_tree = re.compile(fr"^Art\.\s? ?{artigo}\ş?(?: º|º|\.|o|°)?.*?\:", re.MULTILINE).findall(
                match_artigo[0])
            if match_artigo_tree != 0:
                # há tree:
                return new_art_tree(artigo, arg_artigo, paragrafo, inciso, alinea, item, match_artigo, texto_legis)
            else:
                # sem tree:
                match_artigo_notree = re.compile(fr"^Art\.\s? ?{artigo}\ş?(?: º|º|\.|o|°)?.*",
                                                 re.MULTILINE | re.DOTALL).findall(match_artigo[0])
                if len(match_artigo_notree) != 0:
                    return new_art_tree(artigo, arg_artigo, paragrafo, inciso, alinea, item, match_artigo_notree, texto_legis)
                else:
                    return None

        else:
            return None


def paragrafo_tree(paragrafo, inciso, alinea, item, match_artigo):
    """Função que segue a estrutura do paragrafo"""
    match_paragrafo = re.compile(fr"^§\s? ?{paragrafo}\ş?(?: º|º|\.|o)?.*?(?=^§\s? ?)",
                                 re.MULTILINE | re.DOTALL).findall(match_artigo[0])
    # verifica se o paragrafo existe
    if len(match_paragrafo) != 0:
        match_paragrafo_tree = re.compile(fr"^§\s? ?{paragrafo}\ş?(?: º|º|\.|o)?.*?\:", re.MULTILINE).findall(
            match_paragrafo[0])
        # paragrafo com tree
        if len(match_paragrafo_tree) != 0:
            if inciso != '0':
                return inciso_tree(inciso, alinea, item, match_paragrafo)
            else:
                return match_paragrafo_tree[0]

        else:
            if alinea != '0' or item != '0' or inciso != '0':
                return None
            match_paragrafo = re.compile(fr"^§\s? ?{paragrafo}\ş?(?: º|º|\.|o)?.*?(?:\;|\.$|\:|(?=\.§)|\n|(?=\.A)|(?=\.I))",
                                         re.MULTILINE | re.DOTALL).findall(match_artigo[0])
            return match_paragrafo[0]
    else:
        # Ultimo Paragrafo .*?(?=\n)
        match_last_paragrafo = re.compile(fr"^§\s? ?{paragrafo}\ş?(?: º|º|\.|o)?.*",
                                          re.MULTILINE | re.DOTALL).findall(match_artigo[0])
        # verifica se o último parágrafo existe
        if len(match_last_paragrafo) != 0:
            match_paragrafo_tree = re.compile(fr"^§\s? ?{paragrafo}\ş?(?: º|º|\.|o)?.*?\:",
                                              re.MULTILINE).findall(match_last_paragrafo[0])
            # ultimo paragrafo com tree, se existir
            if len(match_paragrafo_tree) != 0:
                if inciso != '0':
                    return inciso_tree(inciso, alinea, item, match_last_paragrafo)
                else:
                    return match_paragrafo_tree[0]
            else:
                if alinea != '0' or item != '0' or inciso != '0':
                    return None

                match_last_paragrafo = re.compile(fr"^§\s? ?{paragrafo}\ş?(?: º|º|\.|o)?.*?(?:\;|\.$|\:|(?=\.§)|\n|(?=\.A)|(?=\.I)|(?=\.C))",
                                                  re.MULTILINE | re.DOTALL).findall(match_last_paragrafo[0])
                return match_last_paragrafo[0]
        else:
            return None


def paragrafo_unico_tree(inciso, alinea, item, match_artigo):
    """Função que segue a estrutura do paragrafo unico"""
    match_paragrafo_unico = re.compile(fr"^Parágrafo\s? ?único\.\s? ?.*", re.MULTILINE | re.DOTALL).findall(
        match_artigo[0])
    if len(match_paragrafo_unico) != 0:
        # tree do paragrafo unico
        match_paragrafo_unico_tree = re.compile(fr"^Parágrafo\s? ?único\.\s? ?(?:.*?(?=\.A)|.*?:)",
                                                re.MULTILINE).findall(match_paragrafo_unico[0])
        if len(match_paragrafo_unico_tree) != 0:
            if inciso != '0':
                match_inciso = re.compile(
                    fr"^{toRoman(int(inciso))}\s? ?[-|–].*?(?=^{toRoman(int(inciso) + 1)})",
                    re.MULTILINE | re.DOTALL).findall(match_paragrafo_unico[0])
                # verifica se o inciso existe
                if len(match_inciso) != 0:
                    match_inciso_tree = re.compile(fr"^{toRoman(int(inciso))}\s? ?[-|–].*?\:",
                                                   re.MULTILINE).findall(match_inciso[0])
                    # inciso com tree
                    if len(match_inciso_tree) != 0:
                        if alinea != '0':
                            match_alinea = re.compile(fr"^{alinea}\).*",
                                                      re.MULTILINE | re.DOTALL).findall(match_inciso[0])
                            if len(match_alinea) != 0:
                                match_alinea_tree = re.compile(fr"^{alinea}\).*?\:",
                                                               re.MULTILINE | re.DOTALL).findall(match_inciso[0])
                                if len(match_alinea_tree) != 0:
                                    if item != '0':
                                        return item_tree(item, match_alinea)
                                    else:
                                        match_alinea = re.compile(fr"^{alinea}\).*?(?:\;|\.$|\:|(?=\.§)|\n|(?=\.A)|(?=\.I))",
                                                                  re.MULTILINE | re.DOTALL).findall(match_inciso[0])
                                        return match_alinea[0]

                                else:
                                    # alinha sem tree
                                    if item != '0':
                                        return None
                                    return match_alinea[0]
                        else:
                            return match_inciso_tree[0]

                    else:
                        if alinea != '0' or item != '0':
                            return None
                        return match_inciso[0]

                else:
                    # Ultimo Inciso de um Paragrafo
                    match_last_inciso = re.compile(fr"^{toRoman(int(inciso))}\s? ?[-|–].*",
                                                   re.MULTILINE | re.DOTALL).findall(
                        match_paragrafo_unico[0])
                    # verifica se o ultimo inciso desse paragrafo existe
                    if len(match_last_inciso) != 0:
                        match_inciso_tree = re.compile(fr"^{toRoman(int(inciso))}\s? ?[-|–].*?\:",
                                                       re.MULTILINE).findall(match_last_inciso[0])
                        # ultimo inciso com tree
                        if len(match_inciso_tree) != 0:
                            match_inciso_tree_verify = re.compile(fr"[a-z].A",
                                                                  re.MULTILINE).findall(match_last_inciso[0])
                            if len(match_inciso_tree_verify) != 0:
                                # inciso com tree falso
                                if alinea != '0' or item != '0':
                                    return None
                                match_last_inciso = re.compile(
                                    fr"^{toRoman(int(inciso))}\s? ?[-|–].*?(?:\;|\.$|\:|(?=\.§)|\n|(?=\.A)|(?=\.I))",
                                    re.MULTILINE | re.DOTALL).findall(match_paragrafo_unico[0])
                                return match_last_inciso[0]
                            if alinea != '0':
                                match_alinea = re.compile(fr"^{alinea}(?:\)).*",
                                                          re.MULTILINE | re.DOTALL).findall(match_last_inciso[0])
                                if len(match_alinea) != 0:
                                    match_alinea_tree = re.compile(fr"^{alinea}\).*?\:",
                                                                   re.MULTILINE | re.DOTALL).findall(match_last_inciso[0])
                                    if len(match_alinea_tree) != 0:
                                        if item != '0':
                                            return item_tree(item, match_alinea)
                                        else:
                                            match_alinea = re.compile(fr"^{alinea}\).*?(?:\;|\.$|\:|(?=\.§)|\n|(?=\.A)|(?=\.I))",
                                                                      re.MULTILINE | re.DOTALL).findall(match_last_inciso[0])
                                            return match_alinea[0]

                                    else:
                                        # alinha sem tree
                                        if item != '0':
                                            return None
                                        return match_alinea[0]
                                else:
                                    return None
                            else:
                                if item != '0':
                                    return item_tree(item, match_last_inciso)
                                else:
                                    return match_inciso_tree[0]
                        else:
                            if alinea != '0' or item != '0':
                                return None
                            match_last_inciso = re.compile(
                                fr"^{toRoman(int(inciso))}\s? ?[-|–].*?(?:\;|\.$|\:|(?=\.§)|\n|(?=\.A)|(?=\.I))",
                                re.MULTILINE | re.DOTALL).findall(match_paragrafo_unico[0])
                            return match_last_inciso[0]
                    else:
                        return None
            else:
                return match_paragrafo_unico_tree[0]
        else:
            if alinea != '0' or item != '0' or inciso != '0':
                return None
            match_paragrafo_unico = re.compile(fr"^Parágrafo\s? ?único\.\s? ?.*?(?:\;|\.$|\:|(?=\.§)|\n|(?=\.A)|(?=\.I))",
                                               re.MULTILINE | re.DOTALL).findall(match_artigo[0])
            return match_paragrafo_unico[0]

    else:
        return None


def inciso_tree(inciso, alinea, item, match_block):
    """Função que segue a estrutura do inciso"""
    match_inciso = re.compile(
        fr"^{toRoman(int(inciso))}\s? ?[-|–].*?(?=^{toRoman(int(inciso) + 1)})",
        re.MULTILINE | re.DOTALL).findall(match_block[0])
    # verifica se inciso existe
    if len(match_inciso) != 0:
        match_inciso_tree = re.compile(fr"^{toRoman(int(inciso))}\s? ?[-|–].*?(?:\;|\.$|\:$|(?=\:a)|(?=\.§)|\n|(?=\.A)|(?=\.a)|(?=\.C)|(?=\.I))",
                                       re.MULTILINE).findall(match_inciso[0])
        # inciso com tree
        if len(match_inciso_tree) != 0:
            if alinea != '0':
                return alinea_tree(alinea, item, match_inciso)
            else:
                if item != '0':
                    return item_tree(item, match_inciso)
                else:
                    return match_inciso_tree[0]
        else:
            if alinea != '0' or item != '0':
                return None
            match_inciso = re.compile(
                fr"^{toRoman(int(inciso))}\s? ?[-|–].*?(?:\;|\.$|\:$|(?=\:a)|(?=\.§)|\n|(?=\.A)|(?=\.a)|(?=\.C)|(?=\.I))",
                re.MULTILINE | re.DOTALL).findall(match_block[0])
            return match_inciso[0]

    else:
        match_last_inciso = re.compile(fr"^{toRoman(int(inciso))}\s? ?[-|–].*",
                                       re.MULTILINE | re.DOTALL).findall(match_block[0])
        # verifica se o ultimo inciso existe
        if len(match_last_inciso) != 0:
            match_inciso_tree = re.compile(fr"^{toRoman(int(inciso))}\s? ?[-|–].*?(?:\:$|(?=\:a|\:A|\)A))",
                                           re.MULTILINE).findall(match_last_inciso[0])
            # ultimo inciso com tree
            if len(match_inciso_tree) != 0:
                if alinea != '0':
                    return alinea_tree(alinea, item, match_last_inciso)
                else:
                    return match_inciso_tree[0]

            else:
                if alinea != '0' or item != '0':
                    return None
                match_last_inciso = re.compile(fr"^{toRoman(int(inciso))}\s? ?[-|–].*?(?:\;|\.$|\:|(?=\:a)(?=\.§)|\n|(?=\.A)|(?=\.I)|(?=\.C)|(?=\.P)|(?=\)A))",
                                               re.MULTILINE | re.DOTALL).findall(match_block[0])
                return match_last_inciso[0]

        else:
            return None


def alinea_tree(alinea, item, match_inciso):
    """Função que segue a estrutura da alínea"""
    match_alinea = re.compile(fr"^{alinea}\).*",
                              re.MULTILINE | re.DOTALL).findall(match_inciso[0])
    if len(match_alinea) != 0:
        match_alinea_tree = re.compile(fr"^{alinea}\).*?:",
                                       re.MULTILINE | re.DOTALL).findall(match_inciso[0])
        if len(match_alinea_tree) != 0:
            if item != '0':
                return item_tree(item, match_alinea)
            else:
                match_alinea = re.compile(fr"^{alinea}\).*?(?:\;|\.$|\:|(?=\.§)|\n|(?=\.A)|(?=\.I))",
                                          re.MULTILINE | re.DOTALL).findall(match_inciso[0])
                return match_alinea[0]
        else:
            if item != '0':
                return None

            match_alinea = re.compile(fr"^{alinea}\).*?(?:\;|\.$|\:|(?=\.§)|\n|(?=\.A)|(?=\.I))",
                                      re.MULTILINE | re.DOTALL).findall(match_inciso[0])
            return match_alinea[0]
    else:
        return None


def item_tree(item, match_block):
    """Função que segue a estrutura do ítem"""
    match_item = re.compile(fr"^{item}\.?\)?.*?(?:\;$|\.$|(?=\:)|(?=\.§)|\n|(?=\.Ar)|(?=\;?\.?I))",
                            re.MULTILINE | re.DOTALL).findall(
        match_block[0])
    if len(match_item) != 0:
        return match_item[0]
    else:
        return None


def new_art_tree(artigo, arg_artigo, paragrafo, inciso, alinea, item, block, whole_txt):
    """Função que reduz repetições no código"""
    if paragrafo == 'unico':
        return paragrafo_unico_tree(inciso, alinea, item, block)
    elif paragrafo != '0':
        return paragrafo_tree(paragrafo, inciso, alinea, item, block)
    elif inciso != '0':
        return inciso_tree(inciso, alinea, item, block)
    elif arg_artigo != '0':
        match_art_comp = re.compile(fr"^Art\.\s? ?{artigo}\-{arg_artigo}.*?(?:\;|\.$|\:|(?=\.§)|\n|(?=\.A)|(?=\.I))",
                                    re.MULTILINE | re.DOTALL).findall(whole_txt)
        if len(match_art_comp) != 0:
            if paragrafo != '0' or alinea != '0' or item != '0' or inciso != '0':
                return None
            return match_art_comp[0]
        else:
            return None
    elif alinea != '0':
        return alinea_tree(alinea, item, block)
    elif item != '0':
        return item_tree(item, block)
    else:
        match_artigo = re.compile(fr"^Art\.\s? ?{artigo}\ş?(?: º|º|\.|o|°)?.*?(?:\n|\:|(?=\.A)|(?=\.I)|(?=\.§)|\.$|(?=\.P))",
                                  re.MULTILINE | re.DOTALL).findall(block[0])
        if len(match_artigo) != 0:
            return match_artigo[0]
        else:
            return None


def busca_norma(tipo, num, ano, arquivo_dic):
    lista_disp = []
    for k in arquivo_dic.keys():
        #separar valores da chave
        valores = k.split('_')
        
        if ano is not None and ano != 0:
            if tipo == int(valores[0]) and num == valores[1] and ano == int(valores[2].split('-')[0]):
                lista_disp.append(k)
        else:
            if tipo == int(valores[0]) and num == valores[1]:
                lista_disp.append(k)
    return lista_disp


def consulta_texto_lei(arquivo_dic, legislacao):

    lista_disp = busca_norma(legislacao[0], legislacao[1], int(str(legislacao[2]).split('-')[0]), arquivo_dic)

    if len(lista_disp) == 0:
        return None

    lista_dict_results = []

    for chave_legis in lista_disp:
        texto_legis = arquivo_dic[chave_legis]['texto']
        if texto_legis == '':
            if arquivo_dic[chave_legis]['ementa'] is None:
                lista_dict_results.append({f'{chave_legis}': 'None'})
            lista_dict_results.append({f'{chave_legis}': normalize('NFKD', arquivo_dic[chave_legis]['ementa'])})
            continue

        artigo = legislacao[3]
        arg_artigo = legislacao[4].upper()
        paragrafo = legislacao[5]
        inciso = legislacao[6]

        # TODO: Provavelmente necessário modificar esta lógica.
        # append_lista_dict_results({f'{chave_legis}': 'None'})
        # continue
        
        if inciso != '0':
            try:
                inciso = fromRoman(inciso.upper())
            except InvalidRomanNumeralError:
                return None

        alinea = legislacao[7]
        item = legislacao[8]

        if artigo != '0':
            if artigo_tree(texto_legis, artigo, arg_artigo, paragrafo, inciso, alinea, item) is None:
                lista_dict_results.append({f'{chave_legis}': 'None'})
            else:
                try:
                    artigo_index = int(artigo.replace('.', '')) - 1
                    if artigo_index < len(arquivo_dic[chave_legis]['jurisprudencias']):
                        lista_dict_results.append({f'{chave_legis}': [normalize('NFKD', artigo_tree(texto_legis, artigo, arg_artigo, paragrafo, inciso, alinea, item)),
                                                                      arquivo_dic[chave_legis]['jurisprudencias'][artigo_index]]})
                    else:
                        lista_dict_results.append({f'{chave_legis}': normalize('NFKD', artigo_tree(texto_legis, artigo, arg_artigo, paragrafo, inciso, alinea, item))})
                except Exception:
                    lista_dict_results.append({f'{chave_legis}': 'None'})

        else:
            if arquivo_dic[chave_legis]['ementa'] is None:
                lista_dict_results.append({f'{chave_legis}': 'None'})
            else:
                lista_dict_results.append({f'{chave_legis}': normalize('NFKD', arquivo_dic[chave_legis]['ementa'])})


    return lista_dict_results

#with open('./legislacoes.json', encoding='utf-8') as file:
 #   dic_leis = json.load(file)

from pickle import load

fp = open('./dicionario_legislacao.dic', 'rb')
dic_leis = load(fp)
fp.close()

#legislacao = (11, "100", date(2019, 6, 26), "1", "0", "0", "iii", "0", "0")

 #legislacao = (11, '113', date(2021, 12, 8), '4', '0', '3', '0', '0', '0')

#legislacao = (2, '179', date(2021, 2, 24), '6', '0', '5', '0', '0', '0')

#legislacao = (0, "10.736", date(2003, 9, 15), "1", "0", "3", "0", "0", "0")

#legislacao = (0, "14.166", date(2021, 6, 10), "6", "0", "7", "Ii", "a", "1")

# legislacao = (0, "14.390", date(2022, 7, 4), "5", "0", "0", "i", "b", "0")

# legislacao = (0, '11.893', date(2008, 12, 29), "2", "0", "0", "i", "0", "0")

# legislacao = (0, '13.096', date(2015, 1, 12), "2", "0", "0", "ii", "0", "0")

# legislacao = (0, '13.587', date(2018, 1, 2), "1", "0", "0", "IiI", "0", "0")

# legislacao = (0, '8.432', date(1992, 6, 11), "1", "0", "0", "IiI", "0", "0")

# legislacao = (0, '12.587', date(2012, 1, 3), "17", "0", "unico", "0", "0", "0")

# legislacao = (0, '8.078', date(1990, 9, 11), "2", "0", "0", "0", "0", "0")

# legislacao = (0, '2.463', date(1955, 4, 22), "1", "0", "0", "0", "0", "0")

# legislacao = (0, '65', date(1947, 8, 14), "1", "0", "0", "0", "0", "0")

# legislacao = (0, '6.949', date(1981, 10, 27), "1", "0", "0", "0", "0", "0")

# legislacao = (1, '301', 0, "0", "0", "0", "0", "0", "0")

#legislacao = (7, "1.988", date(1973, 2, 24), "0", "0", "0", "0", "0", "0")

#resultado = consulta_texto_lei(dic_leis, legislacao)

# Descomentar para rodar na main.
#print(resultado)