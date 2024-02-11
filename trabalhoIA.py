# Boardclasse que representa o tabuleiro do jogo, bem como funções para obter o estado do tabuleiro a partir 
# de argumentos de linha de comando, verificar se o jogo acabou, obter uma lista de ações possíveis para um determinado 
# tabuleiro, aplicar uma ação a um placa e retornar a placa resultante e avaliar o estado da placa. O bloco de código 
# também define uma minimaxfunção com poda alfa-beta, bem como uma best_actionfunção 
# que utiliza minimaxpara determinar a melhor ação para uma determinada placa.
import sys

class Board:
    def __init__(self, board_str, players, life1, life2, bullets1, bullets2):
        self.width = 5
        self.height = 5
        self.board = [list(map(int, board_str[i:i+5])) for i in range(0, 25, 5)]
        self.players = players
        self.life1 = life1
        self.life2 = life2
        self.bullets1 = bullets1
        self.bullets2 = bullets2
        self.player1 = (0, (0, 0))
        self.player2 = (0, (0, 0))
        for i, p in enumerate(players):
            if p == 1:
                self.player1 = (p, (i // self.width, i % self.width))
            elif p == 2:
                self.player2 = (p, (i // self.width, i % self.width))

    def __str__(self):
        return '\n'.join(''.join(str(x) for x in row) for row in self.board)

# Função auxiliar para obter o estado da placa a partir de argumentos de linha de comando
def get_board(args):
    board_str = args[1]
    players = [int(x) for x in args[2:4]]
    life1, life2 = int(args[4]), int(args[5])
    bullets1, bullets2 = int(args[6]), int(args[7])
    return Board(board_str, players, life1, life2, bullets1, bullets2)

# Função auxiliar para checar se o jogo finalizou 
def terminal_test(board):
    return board.life1 == 0 or board.life2 == 0

# Função auxiliar para ver as ações possíveis em um determinado quadro
def actions(board):
    possible_actions = []
    if board.players[0] == 1:
        # Player 1 can move or attack
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = board.player1[1]
            if 0 <= nx + dx < board.width and 0 <= ny + dy < board.height:
                if board.board[ny + dy][nx + dx] == 0:
                    possible_actions.append((dx, dy))
                elif board.board[ny + dy][nx + dx] == 2:
                    possible_actions.append(('attack', dx, dy))
    else:
        # Jogador 2 pode mover ou defender
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = board.player2[1]
            if 0 <= nx + dx < board.width and 0 <= ny + dy < board.height:
                if board.board[ny + dy][nx + dx] == 0:
                    possible_actions.append((dx, dy))
                elif board.board[ny + dy][nx + dx] == 1:
                    possible_actions.append(('defend', dx, dy))
    return possible_actions

# Função auxiliar para realizar uma ação no tabuleiro e retornar o tabuleiro resultante
def result(board, action): 
    if action[0] == 'attack': 
        dx, dy = action[1:] 
        nx, ny = board.player1[1] 
        if 0 <= nx + dx < board.width and 0 <= ny + dy < board.height: 
            if board.board[ny + dy][nx + dx] == 2:
                board.life2 -= 1 
                board.board[ny + dy][nx + dx] = 0 
                board.player1 = (1, (nx + dx, ny + dy)) 
                return board 
            elif action[0] == 'defend': 
                dx, dy = action[1:] nx, ny = board.player2[1] 
                if 0 <= nx + dx < board.width and 0 <= ny + dy < board.height: 
                    if board.board[ny + dy][nx + dx] == 1: 
                        board.board[ny + dy][nx + dx] = 0 
                        board.player2 = (2, (nx + dx, ny + dy)) 
                        return board 
                    else: dx, dy = action nx, ny = board.player1[1] 
                    if board.players[0] == 1
                    else:
                        player2[1] 
                        if 0 <= nx + dx < board.width and 0 <= ny + dy < board.height: 
                            if board.board[ny + dy][nx + dx] == 0: 
                                board.board[ny + dy][nx + dx] = board.players[0] 
                                board.board[ny][ny] = 0 
                                if board.players[0] == 1: 
                                    board.player1 = (1, (nx + dx, ny + dy)) 
                                else:
                                    board.player2 = (2, (nx + dx, ny + dy)) 
                                return board
#Função auxiliar para avaliar o estado do quadro
def evaluate(board): 
    if board.life1 == 0: 
        return -1 
    elif board.life2 == 0: 
        return 1 
    return 0
#Função auxiliar para gerar estados sucessores
def successors(board): 
    successors = [] 
    for action in actions(board): 
        new_board = result(board, action) 
        successors.append((new_board, action)) 
        return successors
# Função minimax recursiva com profundidade limitada e poda alfa-beta
def minimax(board, depth, maximizing_player, alpha, beta): 
    if depth == 0 or terminal_test(board): 
        return evaluate(board)
    if maximizing_player: 
        max_eval = float('-inf') 
        for new_board, action in successors(board): 
            eval = minimax(new_board, depth - 1, False, alpha, beta) 
            max_eval = max(max_eval, eval) 
            alpha = max(alpha, eval) 
            if beta <= alpha: break 
        return max_eval
    else: 
        min_eval = float('inf') 
        for new_board, action in successors(board): 
            eval = minimax(new_board, depth - 1, True, alpha, beta) 
            min_eval = min(min_eval, eval) 
            beta = min(beta, eval) 
            if beta <= alpha: break 
        return min_eval
#  best_action que recebe um boardobjeto e um inteiro depth e retorna a melhor ação para aquela placa de acordo 
# com o algoritmo minimax com poda alfa-beta. A função percorre todas as ações possíveis para o jogador atual, 
# calcula o valor minimax para cada estado do tabuleiro resultante e atualiza best_evalde best_actionacordo.
def best_action(board, depth):
    best_eval = float('-inf') 
    best_action = None 
    for new_board, action in successors(board): 
        eval = minimax(new_board, depth, False, float('-inf'), float('inf')) 
        if eval > best_eval: 
            best_eval = eval 
            best_action = action 
    return best_action

# A main função obtém o estado e a profundidade do quadro a partir dos argumentos da linha de comando, 
# chama best_actionpara obter a melhor ação e imprime-a.
def main(): 
    board = get_board(sys.argv) 
    depth = int(sys.argv[3]) 
    best_action = best_action(board, depth) 
    print(best_action)

if __name__ == '__main__': 
    main()