import random

COLUNA_MAXIMA     = 56
LINHA_MAXIMA      = 19

# CONSTANTES DE IMPRESSÃO NA TELA
CANHAO            = 'A'
NAVE              = 'V'
LASER_CANHAO      = '^'
LASER_NAVE        = '.'
EXPLOSAO          = '*'

# CONSTANTES DE AÇÕES DE MOVIMENTAÇÃO DOS OBJETOS NO JOGO
ATIRA             = 3  # para tecla 'l' quando movimentar o canhão
ESQUERDA          = -1 # para tecla 'e' quando movimentar o canhão
DIREITA           = 1  # para tecla 'd' quando movimentar o canhão
BAIXO             = -2

# CONSTANTES DE RESULTADO DO JOGO
VENCEU            = True
PERDEU            = False

# CONSTANTES DOS PONTOS RELACIONADOS A LASERS OU NAVES DESTRUÍDAS
PONTOS_ACERTOU_LASER     = 1
PONTOS_ACERTOU_NAVE      = 3

# OUTRAS CONSTANTES: SEMENTE DO GERADOR DE NÚMEROS ALEATÓRIOS E
# VALORES USADOS NA FUNÇÃO QUE MOVIMENTA AS NAVES
SEMENTE           = 0
ATINGIU_ESQUERDA  = -1
ATINGIU_DIREITA   = 1
ATINGIU_EMBAIXO   = -2

# FUNÇÃO PRINCIPAL QUE SÓ LÊ A QUANTIDADE DE INIMIGOS DO TECLADO,
# PASSA O CONTROLE PARA A FUNÇÃO REAL DO JOGO E RECEBE COMO RETORNO A PONTUAÇÃO DO JOGADOR PARA IMPRIMIR NA TELA COM O RESULTADO DO JOGO
def main():
    random.seed(SEMENTE)
    
    quantidadeNaves = int(input("Digite o numero de naves (inteiro maior que 1 e menor que %d): " %(COLUNA_MAXIMA-3)))
    
    resultado = joga(quantidadeNaves)
    
    if resultado[0] == VENCEU:
        print(">>> CONGRATULATIONS! Você venceu!")
    else:
        print(">>> GAME OVER! Você perdeu!")
    
    print(">>> Pontuação:",resultado[1]) 


def imprimeMatriz(matriz): 
    for linha in matriz:
        print('|',end="")
        for posicao in linha:
            print(posicao, end="")
        print('|',end="")
        print("")

def criaElementos(quantidadeNaves, matriz):

    if ((quantidadeNaves%2)==0):
        for i in range(0,quantidadeNaves,2):
            matriz[0][i]=NAVE
            matriz[1][i]=NAVE
    elif(quantidadeNaves==1):
        matriz[0][0]='V'
    else:
        for i in range(0,quantidadeNaves,2):
            matriz[0][i]=NAVE
        for i in range(0,quantidadeNaves-2,2):
            matriz[1][i]=NAVE
    matriz[19][28]=CANHAO

# Mover o canhão do jogador.
def moveCanhao(direcao, matriz):
    #Procurar o canhao para move-lo
    for i in range(len(matriz[19])):
        DIREITA=1
        ESQUERDA=-1
        if (matriz[19][i]=='A'):
            if (direcao==1): #Caso a nave vá para a direita
                if (i==56): #Caso seja a Borda direita da matriz
                    if (matriz[19][0]!=' '): #Caso haja colisão
                        matriz[19][0]='*'
                        matriz[19][i]=' '
                        return True
                    else:
                        matriz[19][0]=CANHAO
                        matriz[19][i]=' '
                        return False
                else: #Caso não seja a borda
                    if (matriz[19][i+1]!=' '): #Caso haja colisão
                        matriz[19][i+1]='*'
                        matriz[19][i]=' '
                        return True
                    else:    
                        matriz[19][i+1]=CANHAO
                        matriz[19][i]=' '
                        return False
            elif (direcao==-1): #Caso a nave vá para a esquerda
                if (i==0): #Caso seja a Borda esquerda da matriz
                    if (matriz[19][56]!=' '): #Caso haja colisão
                        matriz[19][56]='*'
                        matriz[19][0]=' '
                        return True
                    else:
                        matriz[19][56]=CANHAO
                        matriz[19][i]=' '
                        return False
                else: #Caso não seja a borda
                    if (matriz[19][i-1]!=' '): #Caso haja colisão
                        matriz[19][i-1]='*'
                        matriz[19][i]=' '
                        return True
                    else:    
                        matriz[19][i-1]=CANHAO
                        matriz[19][i]=' '
                        return False
            direcao+=10

# Mover as naves.
def moveNaves(direcao, matriz):
    ATINGIU_ESQUERDA  = -1
    ATINGIU_DIREITA   = 1
    ATINGIU_EMBAIXO   = -2

    navesdestruidas=0
    atingiu=0
    if (direcao==1):
        for i in range (20):
            for j in range (56,-1,-1):
                if (matriz[i][j]=='V'): #Acha a Nave
                    if (matriz[i][j+1]=='^'): #Colisao Nave tiro
                        matriz[i][j+1]=' '
                        matriz[i][j]=' '
                        navesdestruidas+=1
                    else:
                        matriz[i][j+1]='V'
                        matriz[i][j]=' '
                        if ((j+1)==56):
                            atingiu=ATINGIU_DIREITA
    
    if (direcao==-1):
        for i in range(20):
            for j in range (57):
                if (matriz[i][j]=='V'): #Acha a Nave
                    if (matriz[i][j-1]=='^'): #Colisao Nave tiro
                        matriz[i][j-1]=' '
                        matriz[i][j]=' '
                        navesdestruidas+=1
                    else:
                        matriz[i][j-1]='V'
                        matriz[i][j]=' '
                        if ((j-1)==0):
                            atingiu=ATINGIU_ESQUERDA

    if (direcao==-2):
        for i in range(19,-1,-1):
            for j in range (57):
                if (matriz[i][j]=='V'): #Acha a Nave
                    if (matriz[i+1][j]=='^'): #Colisao Nave tiro
                        matriz[i+1][j]=' '
                        matriz[i][j]=' '
                        navesdestruidas+=1
                    else:
                        matriz[i+1][j]='V'
                        matriz[i][j]=' '
                        if ((i+1)==19):
                            atingiu=ATINGIU_EMBAIXO
    
    for i in range(20):
        for j in range(57):
            if (matriz[i][j]=='*'): #Verifica se o Canhao foi destruido
                destruido=True
            else:
                destruido=False

    return [destruido , atingiu , navesdestruidas]


# Laser pelo canhão do jogador.
def emiteLaserCanhao(matriz):
    navAtingidas=lasAtingidos=0
    for i in range(20):
        for j in range(57):
            if (matriz[i][j]=='A'): #Acha o Canhao
                if (matriz[i-1][j]=='.'): #Colisao entre tiro e laser
                    matriz[i-1][j]=' '
                    lasAtingidos+=1
                elif (matriz[i-1][j]=='V'): #Colisao entre Nave e tiro
                    matriz[i-1][j]=' '
                    navAtingidas+=1
                else: #Tiro
                    matriz[i-1][j]='^'
    return [navAtingidas, lasAtingidos]


# Lasers pelas naves.
def emiteLasersNaves(matriz):
    destruido=False
    tirosDestruidos=0
    for i in range(19, -1, -1):
        for j in range(57):
            if (matriz[i][j]=='V'): #Acha as naves
                if (matriz[i+1][j]!='V'):
                    if (random.randint(0,1)==1):
                        if (matriz[i+1][j]=='A'):
                            matriz[i+1][j]='*'
                            destruido=True
                        elif (matriz[i+1][j]=='^'):
                            tirosDestruidos+=1
                            matriz[i+1][j]=' '
                        elif (matriz[i+1][j]==' '):
                            matriz[i+1][j]='.'
    
    return [destruido , tirosDestruidos]


# Mover lasers do jogador.
def moveLasersCanhao(matriz):
    navhit=lashit=0
    for i in range(20):
        for j in range(57):
            if (matriz[i][j]=='^'): #Achar os tiros
                if((i-1) >= 0):
                    if (matriz[i-1][j]=='.'): #Colisao com laser
                        matriz[i][j]=' '
                        matriz[i-1][j]=' '
                        lashit+=1
                    elif (matriz[i-1][j]=='V'): #Colisao com Naves
                        matriz[i][j]=' '
                        matriz[i-1][j]=' '
                        navhit+=1
                    else:
                        matriz[i][j]=' '
                        matriz[i-1][j]='^'
                else:
                    matriz[i][j]=' '
    return [navhit, lashit]


# Mover lasers das naves.
def moveLasersNaves(matriz):
    destruido=False
    tiroshit=0
    for i in range(19,0,-1):
        for j in range(57):
            if (matriz[i][j]=='.'): #Acha os lasers
                if((i+1)<=19):
                    if (matriz[i+1][j]=='^'): #Colisao com tiros
                        matriz[i+1][j]=' '
                        matriz[i][j]=' '
                        tiroshit+=1
                    elif (matriz[i+1][j]=='A'): #Colisao com o Canhao
                        matriz[i][j]=' '
                        matriz[i+1][j]='*'
                        destruido=True
                    else:
                        matriz[i][j]=' '
                        matriz[i+1][j]='.'
                else:
                    matriz[i][j]=' '
                    

    return [destruido, tiroshit]

def joga(quantidadeNaves):
    # Criação da matriz que manterá o estado do jogo.
    matriz = []
    for i in range(LINHA_MAXIMA+1):
        matriz.append([' ']*(COLUNA_MAXIMA+1))
    criaElementos(quantidadeNaves,matriz)
    
    # Loop do jogo
    ATIRA         = 3  # para tecla 'l' quando movimentar o canhão
    ESQUERDA      = -1 # para tecla 'e' quando movimentar o canhão
    DIREITA       = 1  # para tecla 'd' quando movimentar o canhão
    BAIXO         = -2
    VENCEU        = True
    PERDEU        = False
    resultado     = VENCEU
    fimDeJogo     = False
    pontos        = 0
    rodada        = 1
    direcaoNaves  = DIREITA
    PONTOS_ACERTOU_LASER     = 1
    PONTOS_ACERTOU_NAVE      = 3


    while not fimDeJogo:
        # complete o loop seguindo a ordem das ações explicada no
        # enunciado e no docstring desta função acima.
        
        # Remover. Está aqui apenas para não causar loop infinito
        hit=moveLasersCanhao(matriz) #movimentacao dos tiros do canhao
        pontos+=(hit[0]*PONTOS_ACERTOU_NAVE)+(hit[1]*PONTOS_ACERTOU_LASER) #Conta a pontuacao
        naves=0
        for i in range(LINHA_MAXIMA+1): #verifica se há naves
            for j in range(COLUNA_MAXIMA+1):
                if (matriz[i][j]=='V'):
                    naves+=1
        if (naves==0):
            fimDeJogo=True

        if (not fimDeJogo):
            imprimeMatriz(matriz)

        if (not fimDeJogo): #movimentacao do canhao
            direcao = input("'e' para esquerda, 'd' para direita e 'l' para emitir laser: ")
            if (direcao=='e') or (direcao=='d'):
                if (direcao=='e'):
                    lado=-1
                elif (direcao=='d'):
                    lado=1
                fimDeJogo=moveCanhao(lado, matriz)
                if (fimDeJogo):
                    resultado=PERDEU

            else:
                hit=emiteLaserCanhao(matriz)
                pontos+=(hit[0]*PONTOS_ACERTOU_NAVE)+(hit[1]*PONTOS_ACERTOU_LASER) #Conta a pontuacao
                naves=0
                for i in range(LINHA_MAXIMA+1): #verifica se há naves
                    for j in range(COLUNA_MAXIMA+1):
                        if (matriz[i][j]=='V'):
                            naves+=1
                if (naves==0):
                    fimDeJogo=True

        if (not fimDeJogo): #movimentacao dos lasers das naves
            hit=moveLasersNaves(matriz)
            pontos+=(hit[1]*PONTOS_ACERTOU_LASER) #Conta a pontuacao
            fimDeJogo=hit[0]
            if (fimDeJogo):
                    resultado=PERDEU

        if (not fimDeJogo): #Naves emitirem o laser ou nao
            hit=emiteLasersNaves(matriz)
            pontos+=(hit[1]*PONTOS_ACERTOU_LASER) #Conta a pontuacao
            fimDeJogo=hit[0]
            if (fimDeJogo):
                    resultado=PERDEU

        if (not fimDeJogo): #move as naves
            if (rodada%2==0):
                hit=moveNaves(direcaoNaves, matriz)
                pontos+=(hit[2]*PONTOS_ACERTOU_NAVE) #Conta a pontuacao
                fimDeJogo=hit[0]
                if (fimDeJogo) or (hit[1]==BAIXO):
                    resultado=PERDEU
                    fimDeJogo=True
                if (direcaoNaves==BAIXO):
                    for i in range(20):
                        if (matriz[i][0]=='V'):
                            direcaoNaves=DIREITA
                        elif (matriz[i][56]=='V'):
                            direcaoNaves=ESQUERDA
                if (hit[1]==ESQUERDA) or (hit[1]==DIREITA):
                    direcaoNaves=BAIXO
        rodada+=1

    imprimeMatriz(matriz)
    return [resultado, pontos]

main()