import json 

class Simples:
  def __init__(self, chave, texto):
    self.chave = chave
    self.texto = texto

def gravarToken(char, texto, line, indice):
  return {
    "grupo": char,
    "texto": texto,
    "local": {
      "linha": line,
      "indice": indice
    } 
  }
    
def analisadorLexico(programa):
# TODO: implementar essa funcao
  tokens = []
  erros = []

  indice = 0
  line = 1

  textoToken = ""
  
  operadorDiferente = False
  quaseOperadorDiferente = False
  atribuicao = False
  quaseAtribuicao = False
  comentario = False
  quaseComentario = False
  indiceToken = 0

  simples = [
    Simples(':', "dois-pontos"),
    Simples(')', "fecha-parenteses"),
    Simples('(', "abre-parenteses"),
    Simples('{', "abre-chaves"),
    Simples('}', "fecha-chaves"),
    Simples('<', "operador-menor"),
    Simples(',', "virgula"),
    Simples('+', "operador-mais")
  ]

  for c in programa:
    # Comentario
    if c == '-' and not comentario:
      if quaseComentario:
          comentario = True
          quaseComentario = False
      else:
          indiceToken = indice
          textoToken += c
          quaseComentario = True
    elif comentario and c == '\n':
      comentario = False
      tokens.append(gravarToken("comentario", textoToken, line, indiceToken))
    elif comentario:
      textoToken += c
    else:
        grupo = ''

        # Operador Diferente
        if c == '!':
          if quaseOperadorDiferente == False:
            indiceToken = indice
            textoToken = c
            quaseOperadorDiferente = True
          else: 
            quaseOperadorDiferente = False
        elif quaseOperadorDiferente and c == '=':
            operadorDiferente = True
            grupo = "operador-diferente"
            quaseOperadorDiferente = False
        else: 
            operadorDiferente = False
            
        # Atribuicao
        if c == ':':
          if quaseAtribuicao:
              atribuicao = True
              grupo = "atribuicao"
              quaseAtribuicao = False
          else:
              indiceToken = indice
              textoToken = c
              quaseAtribuicao = True
        else: 
          quaseAtribuicao = False

        if atribuicao or operadorDiferente:
            print ('1')
            textoToken += c
            tokens.append(gravarToken(grupo, textoToken, line, indiceToken))
            atribuicao = False
        else:
          for simple in simples:
            if simple.chave == c:
              textoToken = c
              tokens.append(gravarToken(simple.texto, textoToken, line, indice))

    # Quebra-linha
    if c == '\n':
      textoToken = c
      tokens.append(gravarToken("quebra-linha", textoToken, line, indice))
      line += 1
      indice = 0
    else:
      indice += 1

  return {"tokens":tokens,"erros":erros}

# ALERTA: Nao modificar o codigo fonte apos esse aviso

def testaAnalisadorLexico(programa, teste):
  # Caso o resultado nao seja igual ao teste
  # ambos sao mostrados e a execucao termina  
  resultado = json.dumps(analisadorLexico(programa), indent=2)
  teste = json.dumps(teste, indent=2)
  if resultado != teste:
    # Mostra o teste e o resultado lado a lado  
    resultadoLinhas = resultado.split('\n')
    testeLinhas = teste.split('\n')
    if len(resultadoLinhas) > len(testeLinhas):
      testeLinhas.extend(
        [' '] * (len(resultadoLinhas)-len(testeLinhas))
      )
    elif len(resultadoLinhas) < len(testeLinhas):
      resultadoLinhas.extend(
        [' '] * (len(testeLinhas)-len(resultadoLinhas))
      )
    linhasEmPares = enumerate(zip(testeLinhas, resultadoLinhas))
    maiorTextoNaLista = str(len(max(testeLinhas, key=len)))
    maiorIndice = str(len(str(len(testeLinhas))))
    titule = '{:<'+maiorIndice+'} + {:<'+maiorTextoNaLista+'} + {}'
    objeto = '{:<'+maiorIndice+'} | {:<'+maiorTextoNaLista+'} | {}'
    print(titule.format('', 'teste', 'resultado'))
    print(objeto.format('', '', ''))
    for indice, (esquerda, direita) in linhasEmPares:
      print(objeto.format(indice, esquerda, direita))
    # Termina a execucao
    print("\n): falha :(")
    quit()

# Programa que passdo para a funcao analisadorLexico
programa = """-- funcao inicial

inicio:Funcao(valor:Logica,item:Texto):Numero::{
}

tiposDeVariaveis:Funcao::{
  textoVar:Texto::'#'exemplo##'
  numeroVar:Numero::1234
  logicoVar:Logico::Sim
}

tiposDeFluxoDeControle:Funcao:Logico::{
  resultado:Logico::Nao

  se(1 = 2){
    resultado::Nao
  } se nao se('a' != 'a'){
    resultado::Nao
  } se nao @ {
    resultado::Sim
  }

  contador:Numero::0
  enquanto(contador < 10){
    contador::contador + 'a'
  }

  retorna resultado
}"""

# Resultado esperado da execucao da funcao analisadorLexico
# passando paea ela o programa anterior
teste = {
  "tokens":[
    # Comentario    
    {
      "grupo":"comentario", "texto": "-- funcao inicial", 
      "local":{"linha":1,"indice":0}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":1,"indice":17}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":2,"indice":0}
    },
    # Funcao inicio
    {
      "grupo":"identificador", "texto": "inicio", 
      "local":{"linha":3,"indice":0}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":3,"indice":6}
    },
    {
      "grupo":"reservado", "texto": "Funcao", 
      "local":{"linha":3,"indice":7}
    },
    {
      "grupo":"abre-parenteses", "texto": "(", 
      "local":{"linha":3,"indice":13}
    },
    {
      "grupo":"identificador", "texto": "valor", 
      "local":{"linha":3,"indice":14}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":3,"indice":19}
    },
    {
      "grupo":"reservado", "texto": "Logica", 
      "local":{"linha":3,"indice":20}
    },
    {
      "grupo":"virgula", "texto": ",", 
      "local":{"linha":3,"indice":26}
    },
    {
      "grupo":"identificador", "texto": "item", 
      "local":{"linha":3,"indice":27}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":3,"indice":31}
    },
    {
      "grupo":"reservado", "texto": "Texto", 
      "local":{"linha":3,"indice":32}
    },
    {
      "grupo":"fecha-parenteses", "texto": ")", 
      "local":{"linha":3,"indice":37}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":3,"indice":38}
    },
    {
      "grupo":"reservado", "texto": "Numero", 
      "local":{"linha":3,"indice":39}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":3,"indice":45}
    },
    {
      "grupo":"abre-chaves", "texto": "{", 
      "local":{"linha":3,"indice":47}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":3,"indice":48}
    },
    {
      "grupo":"fecha-chaves", "texto": "}", 
      "local":{"linha":4,"indice":0}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":4,"indice":1}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":5,"indice":0}
    },
    # Funcao tiposDeVariaveis
    {
      "grupo":"identificador", "texto": "tiposDeVariaveis", 
      "local":{"linha":6,"indice":0}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":6,"indice":16}
    },
    {
      "grupo":"reservado", "texto": "Funcao", 
      "local":{"linha":6,"indice":17}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":6,"indice":23}
    },
    {
      "grupo":"abre-chaves", "texto": "{", 
      "local":{"linha":6,"indice":25}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":6,"indice":26}
    },
    # textoVar:Texto::'#'exemplo##'
    {
      "grupo":"identificador", "texto": "textoVar", 
      "local":{"linha":7,"indice":2}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":7,"indice":10}
    },
    {
      "grupo":"reservado", "texto": "Texto", 
      "local":{"linha":7,"indice":11}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":7,"indice":16}
    },
    {
      "grupo":"texto", "texto": "'#'exemplo##'", 
      "local":{"linha":7,"indice":18}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":7,"indice":31}
    },
    # numeroVar:Numero::1234
    {
      "grupo":"identificador", "texto": "numeroVar", 
      "local":{"linha":8,"indice":2}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":8,"indice":11}
    },
    {
      "grupo":"reservado", "texto": "Numero", 
      "local":{"linha":8,"indice":12}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":8,"indice":18}
    },
    {
      "grupo":"numero", "texto": "1234", 
      "local":{"linha":8,"indice":20}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":8,"indice":24}
    },
    # logicoVar:Logico::Sim
    {
      "grupo":"identificador", "texto": "logicoVar", 
      "local":{"linha":9,"indice":2}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":9,"indice":11}
    },
    {
      "grupo":"reservado", "texto": "Logico", 
      "local":{"linha":9,"indice":12}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":9,"indice":18}
    },
    {
      "grupo":"logico", "texto": "Sim", 
      "local":{"linha":9,"indice":20}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":9,"indice":23}
    },
    # Fecha Funcao
    {
      "grupo":"fecha-chaves", "texto": "}", 
      "local":{"linha":10,"indice":0}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":10,"indice":1}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":11,"indice":0}
    },
    # Funcao tiposDeFluxoDeControle
    {
      "grupo":"identificador", "texto": "tiposDeFluxoDeControle", 
      "local":{"linha":12,"indice":0}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":12,"indice":22}
    },
    {
      "grupo":"reservado", "texto": "Funcao", 
      "local":{"linha":12,"indice":23}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":12,"indice":29}
    },
    {
      "grupo":"reservado", "texto": "Logico", 
      "local":{"linha":12,"indice":30}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":12,"indice":36}
    },
    {
      "grupo":"abre-chaves", "texto": "{", 
      "local":{"linha":12,"indice":38}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":12,"indice":39}
    },
    # resultado:Logico::Nao
    {
      "grupo":"identificador", "texto": "resultado", 
      "local":{"linha":13,"indice":2}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":13,"indice":11}
    },
    {
      "grupo":"reservado", "texto": "Logico", 
      "local":{"linha":13,"indice":12}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":13,"indice":18}
    },
    {
      "grupo":"logico", "texto": "Nao", 
      "local":{"linha":13,"indice":20}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":13,"indice":23}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":14,"indice":0}
    },
    # se(1 = 2){
    {
      "grupo":"reservado", "texto": "se", 
      "local":{"linha":15,"indice":2}
    },
    {
      "grupo":"abre-parenteses", "texto": "(", 
      "local":{"linha":15,"indice":4}
    },
    {
      "grupo":"numero", "texto": "1", 
      "local":{"linha":15,"indice":5}
    },
    {
      "grupo":"operador-igual", "texto": "=", 
      "local":{"linha":15,"indice":7}
    },
    {
      "grupo":"numero", "texto": "2", 
      "local":{"linha":15,"indice":9}
    },
    {
      "grupo":"fecha-parenteses", "texto": ")", 
      "local":{"linha":15,"indice":10}
    },
    {
      "grupo":"abre-chaves", "texto": "{",
      "local":{"linha":15,"indice":11}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":15,"indice":12}
    },
    {
      "grupo":"identificador", "texto": "resultado", 
      "local":{"linha":16,"indice":4}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":16,"indice":13}
    },
    {
      "grupo":"logico", "texto": "Nao", 
      "local":{"linha":16,"indice":15}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":16,"indice":18}
    },
    # } se nao se('a' != 'a'){
    {
      "grupo":"fecha-chaves", "texto": "}",
      "local":{"linha":17,"indice":2}
    },
    {
      "grupo":"reservado", "texto": "se nao se", 
      "local":{"linha":17,"indice":4}
    },
    {
      "grupo":"abre-parenteses", "texto": "(", 
      "local":{"linha":17,"indice":13}
    },
    {
      "grupo":"texto", "texto": "'a'", 
      "local":{"linha":17,"indice":15}
    },
    {
      "grupo":"operador-diferente", "texto": "!=", 
      "local":{"linha":17,"indice":18}
    },
    {
      "grupo":"texto", "texto": "'a'", 
      "local":{"linha":17,"indice":21}
    },
    {
      "grupo":"fecha-parenteses", "texto": ")", 
      "local":{"linha":17,"indice":24}
    },
    {
      "grupo":"abre-chaves", "texto": "{",
      "local":{"linha":17,"indice":25}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":17,"indice":26}
    },
    {
      "grupo":"identificador", "texto": "resultado", 
      "local":{"linha":18,"indice":4}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":18,"indice":13}
    },
    {
      "grupo":"logico", "texto": "Nao", 
      "local":{"linha":18,"indice":15}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":18,"indice":18}
    },
    # } se nao @ {
    {
      "grupo":"fecha-chaves", "texto": "}",
      "local":{"linha":19,"indice":2}
    },
    {
      "grupo":"reservado", "texto": "se nao", 
      "local":{"linha":19,"indice":4}
    },
    {
      "grupo":"desconhecido", "texto": "@", 
      "local":{"linha":19,"indice":11}
    },
    {
      "grupo":"abre-chaves", "texto": "{",
      "local":{"linha":19,"indice":13}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":19,"indice":14}
    },
    {
      "grupo":"identificador", "texto": "resultado", 
      "local":{"linha":20,"indice":4}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":20,"indice":13}
    },
    {
      "grupo":"logico", "texto": "Sim", 
      "local":{"linha":20,"indice":15}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":20,"indice":18}
    },
    {
      "grupo":"fecha-chaves", "texto": "}", 
      "local":{"linha":21,"indice":2}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":21,"indice":3}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":22,"indice":0}
    },
    # contador:Numero::0
    {
      "grupo":"identificador", "texto": "contador", 
      "local":{"linha":23,"indice":2}
    },
    {
      "grupo":"dois-pontos", "texto": ":", 
      "local":{"linha":23,"indice":10}
    },
    {
      "grupo":"reservado", "texto": "Numero", 
      "local":{"linha":23,"indice":11}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":23,"indice":17}
    },
    {
      "grupo":"numero", "texto": "0", 
      "local":{"linha":23,"indice":19}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":23,"indice":20}
    },
    # enquanto(contador < 10){
    {
      "grupo":"reservado", "texto": "enquanto", 
      "local":{"linha":24,"indice":2}
    },
    {
      "grupo":"abre-parenteses", "texto": "(", 
      "local":{"linha":24,"indice":10}
    },
    {
      "grupo":"identificador", "texto": "contador", 
      "local":{"linha":24,"indice":11}
    },
    {
      "grupo":"operador-menor", "texto": "<", 
      "local":{"linha":24,"indice":20}
    },
    {
      "grupo":"numero", "texto": "10", 
      "local":{"linha":24,"indice":22}
    },
    {
      "grupo":"fecha-parenteses", "texto": ")", 
      "local":{"linha":24,"indice":24}
    },
    {
      "grupo":"abre-chaves", "texto": "{",
      "local":{"linha":24,"indice":25}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":24,"indice":26}
    },
    {
      "grupo":"identificador", "texto": "contador", 
      "local":{"linha":25,"indice":4}
    },
    {
      "grupo":"atribuicao", "texto": "::", 
      "local":{"linha":25,"indice":12}
    },
    {
      "grupo":"identificador", "texto": "contador", 
      "local":{"linha":25,"indice":14}
    },
    {
      "grupo":"operador-mais", "texto": "+", 
      "local":{"linha":25,"indice":23}
    },
    {
      "grupo":"texto", "texto": "'a'", 
      "local":{"linha":25,"indice":25}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":25,"indice":28}
    },
    {
      "grupo":"fecha-chaves", "texto": "}", 
      "local":{"linha":26,"indice":2}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":26,"indice":3}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":27,"indice":0}
    },
    # Fecha Funcao
    {
      "grupo":"reservado", "texto": "retorna", 
      "local":{"linha":28,"indice":2}
    },    
    {
      "grupo":"identificador", "texto": "resultado", 
      "local":{"linha":28,"indice":10}
    },
    {
      "grupo":"quebra-linha", "texto": "\n", 
      "local":{"linha":28,"indice":19}
    },
    {
      "grupo":"fecha-chaves", "texto": "}", 
      "local":{"linha":29,"indice":0}
    }
  ], "erros":[
    {
      "texto":"simbolo, @, desconhecido",
      "local":{"linha":19,"indice":11}
    }
  ]
}

# Execucao do teste que valida a funcao analisadorLexico
testaAnalisadorLexico(programa, teste)

print("(: sucesso :)")