import random

POSICOES = [
    ['A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8'],
    ['A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7'],
    ['A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6'],
    ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5'],
    ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4'],
    ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3'],
    ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2'],
    ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1']
]


class No:
    def __init__(self, posicao, tem_goiabada=False, tem_queijo=False):
        self.posicao = posicao
        self.tem_goiabada = tem_goiabada
        self.tem_queijo = tem_queijo


def cria_mapa():
    mapa = []
    for linha in POSICOES:
        linha_nos = []
        for posicao in linha:
            tem_goiabada = random.random() < 0.3
            tem_queijo = False
            if not tem_goiabada:
                tem_queijo = random.random() < 0.3
            linha_nos.append(No(posicao, tem_goiabada, tem_queijo))
        mapa.append(linha_nos)
    return mapa


def exibir_mapa(mapa):
    print("\nEstado do mapa:")
    for linha in mapa:
        linha_str = ""
        for no in linha:
            if no.tem_goiabada:
                linha_str += "🔴"
            elif no.tem_queijo:
                linha_str += "🧀"
            else:
                linha_str += "⬛"
        print(linha_str)
    print("\n🔴 = Goiabada | 🧀 = Queijo | ⬛ = Vazio\n")


class Agente:
    def __init__(self, posicao_inicial, mapa, nome_agente):
        self.posicao = posicao_inicial
        self.mapa = mapa
        self.nome_agente = nome_agente
        self.coletas = {
            "goiabada": 0,
            "queijo": 0
        }

    def posicao_atual(self):
        linha, coluna = self.posicao
        return self.mapa[linha][coluna]

    def nova_posicao(self, direcao):
        linha, coluna = self.posicao

        if direcao == 'cima' and linha > 0:
            return linha-1, coluna
        elif direcao == 'baixo' and linha < 7:
            return linha+1, coluna
        elif direcao == 'esquerda' and coluna > 0:
            return linha, coluna-1
        elif direcao == 'direita' and coluna < 7:
            return linha, coluna+1

    def mover(self):
        direcoes = ['cima', 'baixo', 'esquerda', 'direita']
        random.shuffle(direcoes)
        for direcao in direcoes:
            nova_posicao = self.nova_posicao(direcao)
            if nova_posicao:
                self.posicao = nova_posicao
                break

    def procurar_goiabada(self):
        no = self.posicao_atual()
        if no.tem_goiabada:
            print(
                f"\nGoiabada encontrada por {self.nome_agente} em {no.posicao}!\n")
            no.tem_goiabada = False
            self.coletas["goiabada"] += 1

    def procurar_queijo(self):
        no = self.posicao_atual()
        if no.tem_queijo:
            print(
                f"\nQuijo encontrado por {self.nome_agente} em {no.posicao}!\n")
            no.tem_queijo = False
            self.coletas["queijo"] += 1


def cooperacao(posicao_inicial1, posicao_inicial2, nome1, nome2):
    mapa = cria_mapa()
    agente1 = Agente(posicao_inicial1, mapa, nome1)
    agente2 = Agente(posicao_inicial2, mapa, nome2)
    exibir_mapa(mapa)
    cont = 0
    while (agente1.coletas["goiabada"] + agente2.coletas["goiabada"] < 10 or agente1.coletas["queijo"] + agente2.coletas["queijo"] < 5) and cont < 50:
        agente1.procurar_goiabada() if (
            agente1.coletas["goiabada"] < 10) else agente1.procurar_queijo()
        agente2.procurar_queijo() if (
            agente2.coletas["queijo"] < 5) else agente2.procurar_goiabada()

        agente1.mover()
        agente2.mover()

        cont += 1
        print(f"Rodada {cont}:")
        print(f"\t{agente1.nome_agente}: {agente1.coletas}")
        print(f"\t{agente2.nome_agente}: {agente2.coletas}")
        print(
            f"Goiabadas: {agente1.coletas["goiabada"]+agente2.coletas["goiabada"]}")
        print(
            f"Queijos: {agente1.coletas["queijo"]+agente2.coletas["queijo"]}\n")

    print("\n***Não conseguiram o objetivo***\n") if agente1.coletas["goiabada"] + \
        agente2.coletas["goiabada"] < 10 or agente1.coletas["queijo"] + agente2.coletas["queijo"] < 5 else print("\n***Conseguiram o objetivo***\n")
    exibir_mapa(mapa)

    return agente1, agente2
