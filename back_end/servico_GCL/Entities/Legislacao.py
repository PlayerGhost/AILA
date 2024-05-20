import json

from anytree.exporter import JsonExporter

class Legislacao:
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

    def chave_to_str(self, chave):
        nom_tipo = ('Lei', 'Decreto', 'Lei Complementar', 'Decreto-Lei',
                    'Lei Delegada', 'Medida Provisória AE32', 'Medida Provisória PE32',
                    'Constituição', 'Decreto Legislativo', 'Lei Estadual', 'Lei Complementar Estadual',
                    'Emenda Constitucional')
        nom_mes = ('', 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
                   'agosto', 'setembro', 'outubro', 'novembro', 'dezembro')
        return "{:s} nº {:s}, de {:2d} de {:s} de {:d}".format(nom_tipo[chave[0]], chave[1], chave[2].day,
                                                               nom_mes[chave[2].month], chave[2].year)

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
            # res += str(self.catalogo)
            res += 'Catálogo: '
            res += '{:s}'.format(self.catalogo[0])
            for i in range(1, len(self.catalogo)):
                res += ', ' + self.catalogo[i]
            res += '\n' + 80 * '-' + '\n'
        if self.indexacao != []:
            res += 'Indexacao: '
            res += '{:s}'.format(self.indexacao[0])
            for i in range(1, len(self.indexacao)):
                res += ', ' + self.indexacao[i]
            res += '\n' + 80 * '-' + '\n'
        if self.altera != []:
            res += 'Altera:\n'
            for chave in sorted(self.altera, key = lambda cha: cha[2].year):
                res += '    {}\n'.format(self.chave_to_str(chave))
            res += 80 * '-' + '\n'
        if self.e_alterada_por != []:
            res += 'Alterada por:\n'
            for chave in sorted(self.e_alterada_por, key = lambda cha: cha[2].year):
                res += '    {}\n'.format(self.chave_to_str(chave))
            res += 80 * '-' + '\n'
        if self.revoga != []:
            res += 'Revoga:\n'
            for chave in sorted(self.revoga, key = lambda cha: cha[2].year):
                res += '    {}\n'.format(self.chave_to_str(chave))
            res += 80 * '-' + '\n'
        if self.e_revogada_por != []:
            res += 'Revogada por:\n'
            for chave in sorted(self.e_revogada_por, key = lambda cha: cha[2].year):
                res += '    {}\n'.format(self.chave_to_str(chave))
            res += 80 * '-' + '\n'
        if self.cita != []:
            res += 'Cita:\n'
            for chave in sorted(self.cita, key = lambda cha: cha[2].year):
                res += '    {}\n'.format(self.chave_to_str(chave))
            res += 80 * '-' + '\n'
        if self.e_citada_por != []:
            res += 'Citada por:\n'
            for chave in sorted(self.e_citada_por, key = lambda cha: cha[2].year):
                res += '    {}\n'.format(self.chave_to_str(chave))
            res += 80 * '-' + '\n'
        if self.regulamenta != []:
            res += 'Regulamenta:\n'
            for chave in sorted(self.regulamenta, key = lambda cha: cha[2].year):
                res += '    {}\n'.format(self.chave_to_str(chave))
            res += 80 * '-' + '\n'
        if self.e_regulamentada_por != []:
            res += 'Regulamentada por:\n'
            for chave in sorted(self.e_regulamentada_por, key = lambda cha: cha[2].year):
                res += '    {}\n'.format(self.chave_to_str(chave))
            res += 80 * '-' + '\n'
        return res

    def pre_serialize_date_key_list(self, list):
        return [f"{k[0]}_{k[1]}_{k[2].year}-{k[2].month}-{k[2].day}" for k in list]

    def get_as_dict(self):
        exporter = JsonExporter(sort_keys = True)

        return {
            #       'tipo': self.tipo, 'legis': self.legis,
            # 'data': self.datetime_to_dict(self.data),
            'dou': self.dou, 'link': self.link, 'ementa': self.ementa,
            'localidade': self.localidade, 'autoridade': self.autoridade,
            # 'texto_struct': [json.loads(exporter.export(struct)) for struct in self.texto_struct if
            #                  struct] if self.texto_struct else [],
            'texto': self.texto, 'estado': self.estado, 'verificada': self.verificada,
            'situacao': self.situacao, 'edicoes': self.edicoes,
            'altera': self.pre_serialize_date_key_list(self.altera),
            'e_alterada_por': self.pre_serialize_date_key_list(self.e_alterada_por),
            'revoga': self.pre_serialize_date_key_list(self.revoga),
            'e_revogada_por': self.pre_serialize_date_key_list(self.e_revogada_por),
            'cita': self.pre_serialize_date_key_list(self.cita),
            'e_citada_por': self.pre_serialize_date_key_list(self.e_citada_por),
            'regulamenta': self.pre_serialize_date_key_list(self.regulamenta),
            'e_regulamentada_por': self.pre_serialize_date_key_list(self.e_regulamentada_por),
            'catalogo': self.catalogo, 'indexacao': self.indexacao,
            'jurisprudencias': self.jurisprudencias if "jurisprudencias" in self.__dict__.keys() else []}