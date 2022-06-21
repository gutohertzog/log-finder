"""
abre e busca dentro do arquivo de log.
"""

import os
import sys


def limpa_tela() -> None:
    """
    Função para limpar a tela.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def busca_log() -> list:
    """
    Função para buscar o arquivo .log na pasta onde está o arquivo python.
    Se houver mais de um arquivo, retornará uma lista com todos eles para
    realizar a busca em todos.
    """
    # busca por todos os itens na pasta
    arquivos = os.listdir()

    # separa e retorna apenas os arquivos .log
    logs = [arquivo for arquivo in arquivos if '.log' in arquivo]
    return logs


def busca_em_log(log:str, termo:str, seg:bool = False):
    """
    Função para buscar um termo em um arquivo de log.
    Ao final, vai salvar um novo arquivo com o resultado da busca.
    """
    linhas = []
    with open(log, 'r', encoding='utf-8') as arq:
        linhas =  arq.readlines()

    # verifica é para buscar pelo tempo de resposta
    if seg:
        filtrado = []
        for linha in linhas:
            teste = linha.split(' ')
            # verifica se o último item da lista (o tempo de resposta) é maior
            # ou igual que o tempo especificado
            if int(teste[-1]) >= int(termo):
                filtrado.append(linha)
        termo = 'seg=' + termo
    # passa por cada linha do log procurando pelo termo
    else:
        filtrado = [linha for linha in linhas if termo in linha]

    # se algum registro foi encontrado acima, salva em um arquivo .txt
    if filtrado:
        # remove a extensão .log do nome do arquivo
        log = log.replace('.log','')
        # nome do arquivo onde será salvo o resultado
        nome = termo + '-' + log + '.txt'
        with open(nome, 'w', encoding='utf-8') as arq:
            arq.writelines(filtrado)
        print(f'Arquivo {nome} salvo.\n')
    else:
        print(f'O termo {termo} não foi encontado em {log}.')


def start():
    """
    Função principal do programa.
    """
    logs = busca_log()

    # se nenhum arquivo .log foi encontrado, encerra o programa
    if len(logs) == 0:
        print('\n\tArquivo Não Encontrado\n')
        print('Nenhum arquivo .log encontrado na pasta.')
        print('Verifique se o arquivo .log está na mesma')
        print('pasta que o arquivo python.')
        return

    # se não for passado nenhum argumento, encerra o programa
    if len(sys.argv) == 1:
        print('\n\tArgumentos Insuficientes\n')
        print('Faltou especificar um ou mais argumentos de busca.')
        print('\nExemplo: python main.py <termo_busca_1> <termo_busca_2> etc')
        return

    # foi encontrado pelo menos um arquivo .log e inserido pelo menos um
    # parâmetro, então está seguro continuar com a busca nos logs
    # separa todos os argumentos a serem buscados
    args = sys.argv[1:]

    # passa por todos os aquivos de logs, um de cada vez
    for log in logs:
        # passa por cada argumento procurando em cada log
        for arg in args:
            # verifica se é para buscar pelo tempo de resposta
            if 'seg=' in arg:
                arg = arg.replace('seg=','')
                try:
                    arg = int(arg)
                except ValueError:
                    print('\nO valor inserido para segundos não é válido!')
                else:
                    busca_em_log(log, str(arg), True)
                finally:
                    continue
            else:
                busca_em_log(log, arg)


if __name__ == "__main__":
    limpa_tela()
    start()
    sys.exit()
