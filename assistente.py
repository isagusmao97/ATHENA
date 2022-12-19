import speech_recognition as sr
from nltk import word_tokenize, corpus
import json

IDIOMA_CORPUS = "portuguese"
IDIOMA_FALA = "pt-BR"
CAMINHO_CONFIGURACAO = "config.json"

def iniciar():
    global reconhecedor 
    global palavras_de_parada
    global nome_assistente
    global acoes


    with open(CAMINHO_CONFIGURACAO, "r") as arquivo_configuracao:
        configuracao = json.load(arquivo_configuracao)

        nome_assistente = configuracao["nome"]
        acoes = configuracao["acoes"]
        arquivo_configuracao.close()


    reconhecedor = sr.Recognizer()
    palavras_de_parada = set(corpus.stopwords.words(IDIOMA_CORPUS))

def escutar_comando():
    global reconhecedor

    comando = None

    with sr.Microphone() as fonte_audio:
        reconhecedor.adjust_for_ambient_noise(fonte_audio)

        print("Fale algo...")
        fala  = reconhecedor.listen(fonte_audio, timeout=5)

        try:
            comando = reconhecedor.recognize_google(fala, language=IDIOMA_FALA)
        except sr.UnknownValueError:
            pass    

    return comando 

def eliminar_palavras_de_paradas(tokens):
    global palavras_de_parada
    global nome_assistente

    tokens_filtrados = []
    for token in tokens:
        if token not in palavras_de_parada:
            tokens_filtrados.append(token)

    return tokens_filtrados

def tokenizar_comando(comando):
    acao = None
    objeto = None

    tokens = word_tokenize(comando, IDIOMA_CORPUS)

    if tokens:
        tokens = eliminar_palavras_de_paradas(tokens)
        if len(tokens) >= 3:
            if nome_assistente == tokens[0]:
                acao = tokens[1].lower()
                objeto = tokens[2].lower() 
        else: 
            print('Quantidade insuficiente de comandos!')

    return acao, objeto

def validar_comando(acao, objeto):
    global acoes

    valido = False
    resposta = []

    if acao and objeto:
        for acaoCadastrada in acoes:
            # nome = f'{acao} {objeto}'
            # if nome == acaoCadastrada["nome"]:
            if acao in acaoCadastrada["nome"]:
                # if objeto in acaoCadastrada["objetos"]:
                valido = True
                resposta = acaoCadastrada["objetos"]
            break  

    return valido, resposta

def executar_comando(acao, objeto, resposta):
    nome_comando = f'{acao} {objeto}'
    print("vou executar o comando", nome_comando, resposta)

if __name__ == "__main__":
    iniciar()

    continuar = True
    while continuar:
        try:
            comando = escutar_comando()
            if comando:
                acao, objeto = tokenizar_comando(comando)
                valido, resposta = validar_comando(acao, objeto)
                if valido:
                    executar_comando(acao, objeto, resposta)
                else:
                    print("Desculpe, pode repetir por favor?")

        except KeyboardInterrupt:
            print("Até a próxima!")
            continuar = False