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
    def __init__(self, posicao, tem_doce=False):
        self.posicao = posicao
        self.tem_doce = tem_doce


def cria_mapa():
    mapa = []
    for linha in POSICOES:
        linha_nos = []
        for posicao in linha:
            tem_doce = random.random() < 0.4
            linha_nos.append(No(posicao, tem_doce))
        mapa.append(linha_nos)

    return mapa


def exibir_mapa(mapa):
    print("\nEstado do mapa:")
    for linha in mapa:
        linha_str = ""
        for no in linha:
            if no.tem_doce:
                linha_str += "🍬"
            else:
                linha_str += "⬛"
        print(linha_str)
    print("\n🍬 = doce | ⬛ = Vazio\n")


class Agente:
    def __init__(self, posicao_inicial, mapa, nome_agente):
        self.posicao = posicao_inicial
        self.mapa = mapa
        self.coletas = 0
        self.nome_agente = nome_agente

    def posicao_atual(self):
        linha, coluna = self.posicao
        return self.mapa[linha][coluna]

    def nova_posicao(self, direcao):
        linha, coluna = self.posicao

        if direcao == 'cima' and linha > 0:
            return (linha - 1, coluna)
        elif direcao == 'baixo' and linha < 5:
            return (linha + 1, coluna)
        elif direcao == 'esquerda' and coluna > 0:
            return (linha, coluna - 1)
        elif direcao == 'direita' and coluna < 5:
            return (linha, coluna + 1)

    def mover(self):
        direcoes = ["cima", "baixo", 'esquerda', "direita"]
        random.shuffle(direcoes)
        for direcao in direcoes:
            nova_posicao = self.nova_posicao(direcao)
            if nova_posicao:
                self.posicao = nova_posicao
                break

    def procurar_doce(self):
        no = self.posicao_atual()
        if no.tem_doce:
            print(
                f"\nDoce encontrado por {self.nome_agente} em {no.posicao}!!!\n")
            no.tem_doce = False
            self.coletas += 1


def agente_em_acao(posicao_inicial, nome):
    mapa = cria_mapa()
    exibir_mapa(mapa)
    agente = Agente(posicao_inicial=posicao_inicial,
                    mapa=mapa, nome_agente=nome)

    for rodada in range(1, 20):
        agente.procurar_doce()
        agente.mover()
        print(f"{rodada}: {nome} tem {agente.coletas} doces.")

    exibir_mapa(mapa)
    return {
        "nome": nome,
        "coletas": agente.coletas
    }

def competicao(posicao_inicial1, posicao_inicial2, nome1, nome2):
    agente1 = agente_em_acao(posicao_inicial1, nome1)

    agente2 = agente_em_acao(posicao_inicial2, nome2)

    if agente1["coletas"] > agente2["coletas"]:
        print(f"jogador {agente1} vencedor!")
    elif agente1["coletas"] < agente2["coletas"]:
        print(f"jogador {agente2} vencedor!")
    else:
        print("Empate!")

    return agente1, agente2