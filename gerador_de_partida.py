from random import randrange
from collections import Counter


def menus(*texto, color='menu'):
    """Padroniza os separadores, menus e listas de opções.
    :param texto: não coloque nada para apenas uma linha divisória, coloque
    apenas um item para obter um letreiro mais chamativo, adicione mais de um item para
    lista de opções numeradas.
    :return: retorna o texto, ou textos, inseridos já formatados ou uma linha divisória
    caso parâmetro vazio."""
    if len(texto) == 0:
        print('=' * 40)
    elif len(texto) == 1:
        if color == 'menu':
            print('\033[31m~~' * 20)
            print(f' \033[1:30:45m  {texto[0]}'.center((len(texto) + 3)), '\033[m')
            print('\033[31m~~' * 20, '\033[m')
        elif color == 'negativa':
            print('\033[31m~~' * 20)
            print(f'\033[7:31:40m   {texto[0]}'.center((len(texto) + 3)), '\033[m')
            print('\033[31m~~' * 20, '\033[m')
        elif color == 'positiva':
            print('\033[31m~~' * 20)
            print(f'\033[7:32:40m   {texto[0]}'.center((len(texto) + 3)), '\033[m')
            print('\033[31m~~' * 20, '\033[m')
    else:
        for a in range(0, 20):
            print(f'\033[7:36m[{a+1:^3}]\033[m - \033[1:34m', texto[a], ' \033[m')


def atualizar_quadros():
    """Atualiza a matriz(matrizQ) contendo os quadros do jogo, pegando os dados das linhas em matrizH. Deve
    ser chamado quando se necessita atualizar estas variáveis"""
    global matrizQ
    matrizQ = []
    n1 = 0
    n2 = 3
    v1 = 0
    v2 = 3
    while True:
        quadro = []
        for qua_v in range(v1, v2):
            for qua_h in range(n1, n2):
                quadro.append(matrizH[qua_v][qua_h])
        matrizQ.append(quadro)
        n1 = n1 + 3
        n2 = n2 + 3
        if n1 == 9 and n2 == 12 and v1 == 0 and v2 == 3:
            n1 = 0
            n2 = 3
            v1 = 3
            v2 = 6
        if n1 == 9 and n2 == 12 and v1 == 3 and v2 == 6:
            n1 = 0
            n2 = 3
            v1 = 6
            v2 = 9
        if n2 == 12:
            break


def pedir_nums_impedidos(posi_coluna, posi_linha):
    """Retorna uma lista com os números que não podem ser jogados conforme as posições
    horizontal, vertical atuais e nos quadros da matriz"""
    um = posi_linha
    dois = posi_coluna
    n2 = []
    for vtt in range(0, 9):
        if matrizV[um][vtt] not in n2:
            n2.append(matrizH[um][vtt])

    for htt in range(0, 9):
        if matrizH[htt][dois] not in n2:
            n2.append(matrizV[dois][htt])
    qua = 0
    if dois < 3 and um < 3:
        qua = 0
    elif dois < 6 and um < 3:
        qua = 1
    elif dois < 9 and um < 3:
        qua = 2
    elif dois < 3 and um < 6:
        qua = 3
    elif dois < 6 and um < 6:
        qua = 4
    elif dois < 9 and um < 6:
        qua = 5
    elif dois < 3 and um < 9:
        qua = 6
    elif dois < 6 and um < 9:
        qua = 7
    elif dois < 9 and um < 9:
        qua = 8
    for quadra in range(0, 9):
        if matrizQ[qua][quadra] not in n2:
            n2.append(matrizQ[qua][quadra])
    else:
        n2.remove(0)
        return n2


def pedir_um_numero(posi_coluna, posi_linha):
    """Retorna um número válido de um jogo Sudoku ou um número em branco caso exceda o
    limite de tentativas definido pelo usuário nas configurações. Esta função utiliza a função pedir_nums_impedidos.
    (o conceito de 'em branco' nesta aplicação é estar preenchida com zeros).
    :param posi_coluna: A posição horizontal na matriz, a partir da qual será pedido o número válido.
    :param posi_linha: A posição vertical na matriz, a partir da qual receberá o número."""
    # ---------------------------------------------------------------
    # 1. Pega todos os números possíveis, retira os impedidos e manda o restante pro próximo bloco.
    todos_os_numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    numeros_impedidos = pedir_nums_impedidos(posi_coluna, posi_linha)
    numeros_permitidos = []
    for n in range(0, len(todos_os_numeros)):
        if todos_os_numeros[n] not in numeros_impedidos:
            numeros_permitidos.append(todos_os_numeros[n])
    if debug:
        menus()
        print(f'Aplicando um número. Posição: Hor.:{posi_coluna+1}, Ver.:{posi_linha+1}.')
        print(f'Lista dos números impedidos: {numeros_impedidos}.')
        print(f'Lista dos números permitidos: {numeros_permitidos}.')
    # ---------------------------------------------------------------
    # 2. Pega os números permitidos e sorteia aleatoriamente para retornar para a função requisitante.
    if len(numeros_permitidos) > 0:
        sorteio = randrange(0, len(numeros_permitidos))
        numero_sorteado = numeros_permitidos[sorteio]
        matriz_recebe_numero(posi_coluna, posi_linha, numero_sorteado)
        if debug:
            print(f'Número sorteado: \033[1:42m {numero_sorteado} \033[m.')
            print()
            mostrar_debug(posi_coluna, quo=True)
        return numero_sorteado
    else:
        # ---------------------------------------------------------------
        # 2.1 Quando nenhum número é possível, retorna o número 0, para posterior invalidação da linha.
        if debug:
            print(f'Nenhum número permitido: {numeros_permitidos}, pulando.')
            mostrar_debug(posi_coluna, quo=True)
        return 0


def pedir_coluna(posi_coluna):
    """Retorna uma linha vertical preenchida e válida de um jogo Sudoku ou uma linha em branco caso exceda o
    limite de tentativas definido pelo usuário nas configurações. Esta função utiliza a função pedir_um_numero.
    (o conceito de 'em branco' nesta aplicação é estar preenchida com zeros).
    :param posi_coluna: indica a posição horizontal ou vertical onde a lista se iniciará, e finalizará
    sempre na posição 9.
    :return: retorna a lista. Exemplo: [7, 5, 1, 8, 9, 3, 4, 6, 2]. Retorna false se não conseguiu formar a linha."""
    # Na linha acima define-se a quantidade de tentativas em cada linha antes de desistir da matriz toda e partir pra
    # outra matriz (começar do zero).
    # ---------------------------------------------------------------
    global tentativas_pedir_coluna
    count2 = 0
    while count2 < por_coluna:
        if debug:
            menus(f'Tentativa {count2+1} de {por_coluna} de criar a COLUNA[{posi_coluna + 1}] válida.')
            print()
        matriz_limpa_coluna(posi_coluna)
        lin = []
        for pos in range(0, 9):
            n = pedir_um_numero(posi_coluna, pos)
            if n != 0:
                lin.append(n)
            else:
                if debug:
                    menus(f'Sem saída; cancelada a COLUNA[{posi_coluna + 1}], na tentativa {count2+1}.',
                          color='negativa')
                count2 += 1
                tentativas_pedir_coluna += 1
                if count2 == por_coluna:
                    if debug:
                        menus(f'Criar COLUNA[{posi_coluna + 1}] alcançou o limite de {count2} tentativas.',
                              color='negativa')
                    return [0, 0, 0, 0, 0, 0, 0, 0, 0]
                else:
                    break
        if 0 not in lin and len(lin) == 9:
            if debug:
                menus(f'COLUNA[{posi_coluna + 1}] criada com sucesso! em {count2+1} tentativa(s).',
                      color='positiva')
            matriz_limpa_coluna(posi_coluna)
            return lin


def pedir_3_quadrados(comeca_posi):
    """Retorna 3 linhas verticais preenchidas e válidas de um jogo Sudoku ou três linhas em branco caso exceda o
    limite de tentativas definido pelo usuário nas configurações. Esta função utiliza a função pedir_linha.
    (o conceito de 'em branco' nesta aplicação é estar preenchida com zeros)"""
    global tentativas_pedir_3_quadrados
    count2 = 0
    while count2 < por_3_quadros_vertical:
        if debug:
            menus(f'Tentativa {count2+1} de {por_3_quadros_vertical} de criar TRÊS '
                  f'QUADRADOS_Vert.[{int((comeca_posi / 3) + 1)}] válidos.')
        for limpa in range(comeca_posi, comeca_posi + 3):
            matriz_limpa_coluna(limpa)
        tre_lins = []
        count1 = 0
        tem_z = False
        while count1 < 3:
            lin = pedir_coluna(comeca_posi + count1)
            if 0 in lin:
                if debug:
                    menus(f'Sem saída; cancelados os TRÊS '
                          f'QUADRADOS_Vert.[{int((comeca_posi / 3) + 1)}] na tentativa {count2+1}.',
                          color='negativa')
                count2 += 1
                tentativas_pedir_3_quadrados += 1
                if count2 == por_3_quadros_vertical:
                    if debug:
                        menus(f'TRÊS QUADRADOS_V[{int((comeca_posi / 3) + 1)}] alcançou o limite de {count2} '
                              f'tentativas.', color='negativa')
                    return [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
                else:
                    break
            else:
                matriz_recebe_coluna(comeca_posi + count1, lin)
                tre_lins.append(lin)
                count1 += 1
                tentativas_pedir_3_quadrados += 1
            if count1 == 3 and len(tre_lins) == 3:
                # ---------------------------------------------------------------
                # Limpar a matriz já que consegui as três linha para retornar ao requisitante
                for limpa in range(comeca_posi, comeca_posi + 3):
                    matriz_limpa_coluna(limpa)
                if debug:
                    menus(f'TRÊS QUADRADOS_V[{int((comeca_posi / 3) + 1)}] criados com sucesso! em {count2+1} '
                          f'tentativa(s).', color='positiva')
                return tre_lins


def matriz_recebe_coluna(posi_coluna, lis):
    """Aplica uma lista na matriz de um jogo Sudoku conforme os parâmetros de posição.
    :param posi_coluna: A posição na matriz, a partir da qual será aplicada a lista.
    :param lis: A lista contendo 9 números."""
    a_partir = 0
    for m in range(a_partir, 9):
        matrizH[m][posi_coluna] = lis[m]
    for m in range(a_partir, 9):
        matrizV[posi_coluna][m] = lis[m]
    atualizar_quadros()


def matriz_limpa_coluna(posi_coluna):
    """Apaga uma lista na matriz de um jogo Sudoku conforme os parâmetros de posição (o conceito de apagar nesta
    aplicação é transformar em zeros).
    :param posi_coluna: A posição na matriz, a partir da qual será apagada a lista."""
    lis = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    a_partir = 0
    for m in range(a_partir, 9):
        matrizH[m][posi_coluna] = lis[m]
    for g in range(a_partir, 9):
        matrizV[posi_coluna][g] = lis[g]
    atualizar_quadros()


def matriz_recebe_numero(posi_coluna, posi_linha, num_sorteado):
    """Aplica um número nas listas matrizH e matrizV de um jogo Sudoku conforme os parâmetros de posição.
    :param posi_coluna: A posição na matriz, a partir da qual será apagado o número.
    :param posi_linha: A posição da lista na matriz, a partir da qual receberá o número.
    :param num_sorteado: O número a ser aplicado."""
    matrizH[posi_linha][posi_coluna] = num_sorteado
    matrizV[posi_coluna][posi_linha] = num_sorteado
    atualizar_quadros()


def testar_partida_gerada():
    """Testa se cada linha da matrizH global contém 9 vezes cada número de 1 a 9, depois testa a matrizV e a matrizQ,
    se sim, o jogo/matriz é válido(a) e retornará True, caso não válido, retorna False."""
    tem_0 = False
    for c in range(0, 9):
        for n in range(0, 9):
            if matrizV[c][n] == 0:
                tem_0 = True
    if tem_0 is False:
        if debug:
            menus()
            menus('Teste Final')
        count2 = 0
        for coluna in range(0, 9):
            num_valores_c = len(Counter(matrizV[coluna]).keys())
            count2 += num_valores_c
            if debug:
                print(f'Coluna: {coluna} / Nums. diferentes: {num_valores_c} / count2: {count2}')
        # ---------------------------------------------------------------
        if debug:
            print()
        count2 = 0
        for linha in range(0, 9):
            num_valores_l = len(Counter(matrizH[linha]).keys())
            count2 += num_valores_l
            if debug:
                print(f'Linha: {linha} / Nums. diferentes: {num_valores_l} / count2: {count2}')
        # ---------------------------------------------------------------
        if debug:
            print()
        count3 = 0
        for quadro in range(0, 9):
            num_valores_l = len(Counter(matrizQ[quadro]).keys())
            count3 += num_valores_l
            if debug:
                print(f'Quadro: {quadro} / Nums. diferentes: {num_valores_l} / count2: {count3}')
        # ---------------------------------------------------------------
        if count2 == count2 == count3 == 81:
            if debug:
                menus(f'Teste: Sucesso! Existem 9 números distintos em cada coluna.', color='positiva')
                menus()
            return True
        else:
            if debug:
                menus(f'Teste: Erro; Não Existem 9 números distintos em cada coluna pedida.', color='negativa')
            return False
    else:
        if debug:
            menus(f'Teste: Erro; Tem espaços em branco.', color='negativa')
            menus()
        return False


def gerar_partida_valida(matriz='V'):
    """Retorna 3 linhas verticais preenchidas e válidas de um jogo Sudoku ou três linhas em branco caso exceda o
        limite de tentativas definido pelo usuário nas configurações. Esta função utiliza a função pedir_linha.
        (o conceito de 'em branco' nesta aplicação é estar preenchida com zeros)"""
    # Gerar partida:
    global tentativas_matriz
    while True:
        # ---------------------------------------------------------------
        # Primeiro limpa tudo:
        for l in range(0, 9):
            matriz_limpa_coluna(l)
        # ---------------------------------------------------------------
        if debug:
            menus(f'Tentativa {tentativas_matriz + 1} de criar uma MATRIZ Sudoku válida.')
        for u in range(0, 9, 3):
            y = pedir_3_quadrados(u)
            for t in range(0, 3):
                matriz_recebe_coluna(u + t, y[t])
        if teste is True:
            if testar_partida_gerada() is True:
                if debug:
                    menus(f'MATRIZ criada com sucesso! em {tentativas_matriz + 1} tentativa(s).', color='positiva')
                if matriz == 'V':
                    return matrizV
                elif matriz == 'H':
                    return matrizH
                elif matriz == 'Q':
                    return matrizQ
            else:
                if debug:
                    menus(f'Sem saída; cancelada a MATRIZ na tentativa {tentativas_matriz + 1}.',
                          color='negativa')
                tentativas_matriz += 1
        else:
            break


def mostrar_debug(posi_coluna=10, titulo=False, ho=False, ve=False, qu=False, quo=False):
    """Mostra na tela todas as listas horizontais, verticais, todas as listas dos quadros ou os próprios quadros
     já organizados de um jogo Sudoku.
    :param ho: ativar amostra lista horizontal.
    :param ve: ativar amostra lista vertical.
    :param qu: ativar amostra lista dos quadros.
    :param quo: ativar amostra dos quadros."""
    if ho:
        if titulo is True:
            print('MATRIZ DAS LINHAS (H)')
        for horiz_1 in range(0, len(matrizH)):
            print(matrizH[horiz_1])
        if debug:
            print()
    if ve:
        if titulo is True:
            print('MATRIZ DAS COLUNAS (V)')
        for vertic in range(0, len(matrizV)):
            print(matrizV[vertic])
        if debug:
            print()
    if qu:
        if titulo is True:
            print('MATRIZ DOS QUADROS (Q)')
        for vertical in range(0, len(matrizQ)):
            print(matrizQ[vertical])
        if debug:
            print()
    if quo:
        h1 = h2 = h3 = h4 = h5 = h6 = h7 = h8 = h9 = {'cor1': '\033[m'}
        if posi_coluna == 0:
            h1 = {'cor1': '\033[32m'}
        elif posi_coluna == 1:
            h2 = {'cor1': '\033[32m'}
        elif posi_coluna == 2:
            h3 = {'cor1': '\033[32m'}
        elif posi_coluna == 3:
            h4 = {'cor1': '\033[32m'}
        elif posi_coluna == 4:
            h5 = {'cor1': '\033[32m'}
        elif posi_coluna == 5:
            h6 = {'cor1': '\033[32m'}
        elif posi_coluna == 6:
            h7 = {'cor1': '\033[32m'}
        elif posi_coluna == 7:
            h8 = {'cor1': '\033[32m'}
        elif posi_coluna == 8:
            h9 = {'cor1': '\033[32m'}
        elif posi_coluna == 10:
            ''
        limpar = {'limpar': '\033[m'}

        if titulo is True:
            print()
            print('SUDOKU - MATRIZ')
        for qua_v1 in range(0, 9, 3):
            for qua_h1 in range(0, 9, 3):
                print(
                    f'{h1["cor1"]}{matrizQ[qua_v1][qua_h1]:^2}{limpar["limpar"]}'
                    f'{h2["cor1"]}{matrizQ[qua_v1][qua_h1 + 1]:^2}{limpar["limpar"]}'
                    f'{h3["cor1"]}{matrizQ[qua_v1][qua_h1 + 2]:^2}{limpar["limpar"]} '
                    f'{h4["cor1"]}{matrizQ[qua_v1 + 1][qua_h1]:^2}{limpar["limpar"]}'
                    f'{h5["cor1"]}{matrizQ[qua_v1 + 1][qua_h1 + 1]:^2}{limpar["limpar"]}'
                    f'{h6["cor1"]}{matrizQ[qua_v1 + 1][qua_h1 + 2]:^2}{limpar["limpar"]} '
                    f'{h7["cor1"]}{matrizQ[qua_v1 + 2][qua_h1]:^2}{limpar["limpar"]}'
                    f'{h8["cor1"]}{matrizQ[qua_v1 + 2][qua_h1 + 1]:^2}{limpar["limpar"]}'
                    f'{h9["cor1"]}{matrizQ[qua_v1 + 2][qua_h1 + 2]:^2}{limpar["limpar"]} ')
            print()


# ---------------------------------------------------------------
# VARIÁVEIS GLOBAIS
matrizH = [[], [], [], [], [], [], [], [], []]
matrizV = [[], [], [], [], [], [], [], [], []]
matrizQ = [[], [], [], [], [], [], [], [], []]
tentativas_pedir_coluna = 1
tentativas_pedir_3_quadrados = 1
tentativas_matriz = 1
horizontal = []
count = 1
# ---------------------------------------------------------------
# Gerador de zeros em todas as matrizes.
for v in range(0, 9):
    for h in range(0, 9):
        matrizV[h].append(0)
        horizontal.append(0)
        count += 1
    matrizH[v] = horizontal[:]
    horizontal.clear()
atualizar_quadros()
# ---------------------------------------------------------------
# PAINEL DE CONTROLE
# Ative o debug para acompanhar o processo no console:
debug = False
# Ative para mostrar o Sudoku na execução da aplicação:
mostrar = True
# Ativar o teste de matriz:
teste = True
# Defina a quantidade de tentativas:
por_coluna = 12
por_3_quadros_vertical = 6
# ---------------------------------------------------------------
# PROGRAMA/FUNÇÃO PRINCIPAL
# "gerar_partida_valida()" é a função final. Retora uma lista contendo 9 listas, cada uma contendo 9 números
# aleatórios de 1 a 9, estas listas são as linhas/horizontais de cima para baixo de uma partida de Sudoku válida.
# Para retornar as colunas/verticais, da esquerda para a direita digite o parâmetro 'V', ou 'Q' para
# retornar os quadros, de cima para baixo, esquerda para a direita.
gerar_partida_valida()
# ---------------------------------------------------------------
# MOSTRADORES
if debug:
    print()
    menus()
    print(f'Tentativas totais: \n'
          f'Pedir coluna: {tentativas_pedir_coluna}\n'
          f'Pedir 3 quadrados: {tentativas_pedir_3_quadrados}\n'
          f'Pedir matriz: {tentativas_matriz}')
    menus()
    print()
    mostrar_debug(ho=True, ve=True, qu=True, quo=False, titulo=False)
if mostrar:
    mostrar_debug(ho=False, ve=False, qu=False, quo=True, titulo=True)
