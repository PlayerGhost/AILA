from anytree.exporter import JsonExporter


class Legis:
    def __init__(self, tipo, legis, data):
        self.tipo = tipo
        self.legis = legis
        self.data = data
        self.dou = ''
        self.link = ''
        self.ementa = ''
        self.localidade = ''
        self.autoridade = ''
        self.texto_struct = None
        self.texto = ''
        self.estado = ''
        self.verificada = False
        self.situacao = ''
        self.edicoes = []
        self.altera = []
        self.e_alterada_por = []
        self.revoga = []
        self.e_revogada_por = []
        self.cita = []
        self.e_citada_por = []
        self.regulamenta = []
        self.e_regulamentada_por = []
        self.catalogo = []
        self.indexacao = []
        self.jurisprudencias = []

    def __str__(self):
        tipos = ['Lei', 'Decreto', 'Lei Complementar', 'Decreto-Lei', 'Lei Delegada',
                 'Medida Provisória AE32', 'Medida Provisória PE32', 'Constituição',
                 'Decreto Legislativo', 'Lei Estadual', 'Lei Complementar Estadual',
                 'Emenda Constitucional', 'Resolução Normativa']
        res = 80 * '-' + '\n'
        lei = '{:s} nº {:s} de {:02d}/{:02d}/{:d}'.format(tipos[self.tipo], self.legis, self.data.day, self.data.month,
                                                          self.data.year)
        res += lei + '{:s}* {:s} * {:s}\n'.format((71 - len(self.estado) - len(lei)) * ' ', self.estado,
                                                  ' V *' if self.verificada else 'NV *')
        if self.tipo == 5 or self.tipo == 6:
            res += 80 * '-' + '\n'
            res += 'SITUAÇÃO: {:s}\n'.format(self.situacao)
            if self.edicoes != []:
                res += 80 * '-' + '\n'
                res += 'Edições {}\n'.format(self.edicoes)
        res += 80 * '-' + '\n'
        res += 'Localidade: {:s}\n'.format(self.localidade)
        res += 80 * '-' + '\n'
        res += 'Autoridade: {:s}\n'.format(self.autoridade)
        res += 80 * '-' + '\n'
        res += 'Texto: {}\n'.format(self.texto)
        res += 80 * '-' + '\n'
        res += 'Texto Estruturado: {}\n'.format(self.texto_struct)
        res += 80 * '-' + '\n'
        if self.dou != '':
            res += '{:s}\n'.format(self.dou)
            res += 80 * '-' + '\n'
        res += 'Link: {:s}\n'.format(self.link)
        res += 80 * '-' + '\n'
        res += 'EMENTA\n{:s}\n'.format(self.ementa)
        res += 80 * '-' + '\n'
        if self.catalogo != []:
            res += 'Catálogo: {}\n'.format(self.catalogo)
            res += 80 * '-' + '\n'
        if self.indexacao != []:
            res += 'Indexação: {}\n'.format(self.indexacao)
            res += 80 * '-' + '\n'
        if self.altera != []:
            res += 'Altera: {}\n'.format(self.altera)
            res += 80 * '-' + '\n'
        if self.e_alterada_por != []:
            res += 'Foi alterada por: {}\n'.format(self.e_alterada_por)
            res += 80 * '-' + '\n'
        if self.revoga != []:
            res += 'Revoga: {}\n'.format(self.revoga)
            res += 80 * '-' + '\n'
        if self.e_revogada_por != []:
            res += 'Foi revogada por: {}\n'.format(self.e_revogada_por)
            res += 80 * '-' + '\n'
        if self.cita != []:
            res += 'Cita: {}\n'.format(self.cita)
            res += 80 * '-' + '\n'
        if self.e_citada_por != []:
            res += 'Foi citada por: {}\n'.format(self.e_citada_por)
            res += 80 * '-' + '\n'
        if self.regulamenta != []:
            res += 'Regulamenta: {}\n'.format(self.regulamenta)
            res += 80 * '-' + '\n'
        if self.e_regulamentada_por != []:
            res += 'Foi regulamentada por: {}\n'.format(self.e_regulamentada_por)
            res += 80 * '-' + '\n'
        return res

    def pre_serialize_key(self, key):
        return (str(key[0]), str(key[1]), self.datetime_to_dict(key[2]))

    def datetime_to_dict(self, date):
        return {"day": str(date.day), "month": str(date.month), "year": str(date.year)}

    def get_as_dict(self):
        exporter = JsonExporter(sort_keys = True)

        return {'tipo': self.tipo, 'legis': self.legis,
                'data': self.datetime_to_dict(self.data),
                'dou': self.dou, 'link': self.link, 'ementa': self.ementa,
                'localidade': self.localidade, 'autoridade': self.autoridade,
                'texto_struct': [exporter.export(struct) for struct in self.texto_struct if struct],
                'texto': self.texto, 'estado': self.estado, 'verificada': self.verificada,
                'situacao': self.situacao, 'edicoes': self.edicoes, 'altera': self.altera,
                'e_alterada_por': [self.pre_serialize_key(key) for key in self.e_alterada_por],
                'revoga': self.revoga, 'e_revogada_por': self.e_revogada_por, 'cita': self.cita,
                'e_citada_por': [self.pre_serialize_key(key) for key in self.e_citada_por],
                'regulamenta': self.regulamenta, 'e_regulamentada_por': self.e_regulamentada_por,
                'catalogo': self.catalogo, 'indexacao': self.indexacao,
                'jurisprudencias': self.jurisprudencias if "jurisprudencias" in self.__dict__.keys() else []}



"""
class Legis:
    def __init__(self, tipo, legis, data, paragrafo):
        self.tipo = tipo
        self.legis = legis
        self.data = data
        self.dou = ''
        self.link = ''
        self.ementa = ''
        self.localidade = ''
        self.autoridade = ''
        self.texto_struct = [None, None]
        self.texto = ''
        self.estado = ''
        self.verificada = False
        self.situacao = ''
        self.edicoes = []
        self.altera = []
        self.e_alterada_por = []
        self.revoga = []
        self.e_revogada_por = []
        self.cita = []
        self.e_citada_por = []
        self.regulamenta = []
        self.e_regulamentada_por = []
        self.catalogo = []
        self.indexacao = []

    def __str__(self):
        tipos = ['Lei', 'Decreto', 'Lei Complementar', 'Decreto-Lei', 'Lei Delegada',
                 'Medida Provisória AE32', 'Medida Provisória PE32', 'Constituição',
                 'Decreto Legislativo', 'Lei Estadual', 'Lei Complementar Estadual',
                 'Emenda Constitucional', 'Resolução Normativa']
        res = 80 * '-' + '\n'
        lei = '{:s} nº {:s} de {:02d}/{:02d}/{:d}'.format(tipos[self.tipo], self.legis, self.data.day, self.data.month,
                                                          self.data.year)
        res += lei + '{:s}* {:s} * {:s}\n'.format((71 - len(self.estado) - len(lei)) * ' ', self.estado,
                                                  ' V *' if self.verificada else 'NV *')
        if self.tipo == 5 or self.tipo == 6:
            res += 80 * '-' + '\n'
            res += 'SITUAÇÃO: {:s}\n'.format(self.situacao)
            if self.edicoes != []:
                res += 80 * '-' + '\n'
                res += 'Edições {}\n'.format(self.edicoes)
        res += 80 * '-' + '\n'
        res += 'Localidade: {:s}\n'.format(self.localidade)
        res += 80 * '-' + '\n'
        res += 'Autoridade: {:s}\n'.format(self.autoridade)
        res += 80 * '-' + '\n'
        res += 'Texto: {}\n'.format(self.texto[:50])
        res += 80 * '-' + '\n'
        res += 'Árvore original: {}\n'.format(self.texto_struct[0])
        res += 80 * '-' + '\n'
        res += 'Árvore atualizada: {}\n'.format(self.texto_struct[1])
        res += 80 * '-' + '\n'
        if self.dou != '':
            res += '{:s}\n'.format(self.dou)
            res += 80 * '-' + '\n'
        res += 'Link: {:s}\n'.format(self.link)
        res += 80 * '-' + '\n'
        res += 'EMENTA\n{:s}\n'.format(self.ementa)
        res += 80 * '-' + '\n'
        if self.catalogo != []:
            res += 'Catálogo: {}\n'.format(self.catalogo)
            res += 80 * '-' + '\n'
        if self.indexacao != []:
            res += 'Indexação: {}\n'.format(self.indexacao)
            res += 80 * '-' + '\n'
        if self.altera != []:
            res += 'Altera: {}\n'.format(self.altera)
            res += 80 * '-' + '\n'
        if self.e_alterada_por != []:
            res += 'Foi alterada por: {}\n'.format(self.e_alterada_por)
            res += 80 * '-' + '\n'
        if self.revoga != []:
            res += 'Revoga: {}\n'.format(self.revoga)
            res += 80 * '-' + '\n'
        if self.e_revogada_por != []:
            res += 'Foi revogada por: {}\n'.format(self.e_revogada_por)
            res += 80 * '-' + '\n'
        if self.cita != []:
            res += 'Cita: {}\n'.format(self.cita)
            res += 80 * '-' + '\n'
        if self.e_citada_por != []:
            res += 'Foi citada por: {}\n'.format(self.e_citada_por)
            res += 80 * '-' + '\n'
        if self.regulamenta != []:
            res += 'Regulamenta: {}\n'.format(self.regulamenta)
            res += 80 * '-' + '\n'
        if self.e_regulamentada_por != []:
            res += 'Foi regulamentada por: {}\n'.format(self.e_regulamentada_por)
            res += 80 * '-' + '\n'
        return res
"""
