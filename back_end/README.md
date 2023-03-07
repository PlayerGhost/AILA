Serviço GCL
-----------

Serviço de consulta de legislações escrito em flask. Nesta versão o Serviço GCL (Grafo de Conhecimento Legal) consulta um arquivo pickle (.dic)
contendo objetos da classe "Legis" descritas no arquivo `Legis_Class.py`.

Entrada: 
	- Requisição - GET

	- URL - http://localhost:5000/?tipo=<X>&lei=<X>&ano=<X>&artigo=<X>&complemento=<X>&paragrafo=<X>&inciso=<X>&alinea=<X>&item=<X>
		onde <X> são as variáveis da requisição.

Saída:
	- Lista de dicionários em que a chave é a referência da legislação no GCL e o valor pode ser a ementa de uma lei ou o texto da legislação e as jusriprudências que atuam sobre ele.
-----------

Serviço AILA
-----------

Serviço de reconhecimento de citações legais em um texto, também escrito em flask. Através de RegEx e modelos matemáticos o Serviço AILA procura uma lei ou um par Artigo + Lei e
realiza a consulta no Serviço GCL.

Entrada:
	- Texto

Saída:
	- Dicionário contendo um lista de sub-dicionários. Os sub-dicionários possuem a seguinte estrutura:
		
		|Chave          |Valor                                                 |
		|---------------|------------------------------------------------------|
		|tipo           |Tipo de entidade.                                     |
		|marcador       |Parte do texto identificada como entidade.            |
		|posicao        |Posição da entidade no texto de entrada.              |
		|sugestao       |Sugestões de padronização ou o texto da lei.          |
		|jurisprudencias|Lista de jusriprudências que atuam sobre a legislacao.|