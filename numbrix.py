# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 21:
# 97124 Jiaqi Yu
# 89465 Ines Oliveira

import sys
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search

class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id 

    def get_actions(self):
        return self.board.get_actions_board()

    def do_action(self, action):
        return self.board.do_action_board(action)

    def is_goal(self):
    #checks if the board has one sequence 
        return self.board.is_goal_board()
        

class Board:
    """ Representação interna de um tabuleiro de Numbrix. """
    def __init__(self, filename, board):
        self.filename = filename
        self.board_grid = board
        #size of the line and column of the board 
        self.N = len(board)
        #numbers not on the board yet
        self.numbers_list = [] 
    
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        if(row < self.N and col < self.N ):
            return self.board_grid[row][col]
        else:
            raise ValueError('The row or column are out of range.\n')
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        lst = []
        #low position
        if(row == self.N - 1):
            lst.append(None)
        else:
            lst.append(self.get_number(row+1,col))
        #up position
        if(row == 0):
            lst.append(None)
        else:
            lst.append(self.get_number(row-1,col))
        
        return tuple(lst)
    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        lst = []
        #left position
        if(col == 0):
            lst.append(None)
        else:
            lst.append(self.get_number(row,col-1))
        #right position
        if(col == self.N - 1):
            lst.append(None)
        else:
            lst.append(self.get_number(row,col+1))
        
        return tuple(lst)
    
    def to_string(self) -> str:
        s = str()
        for i in range(self.N):
            for j in range(self.N):
                s += str(self.get_number(i,j))
                if (j == self.N-1):
                    s+= '\n'
                else:
                    s+= '\t'
        return s

    def set_numbers_list(self):
        # list with the numbers (from 1 to NxN) that can be used fill the board
        self.numbers_list = list(range(1,self.N*self.N+1))
        for i in range(self.N):
            for j in range(self.N):
                if(self.get_number(i,j) != 0):
                    self.numbers_list.remove(self.get_number(i,j))
        return
    
    def get_actions_board(self):
        actions=[]
        self.set_numbers_list()
        for i in range(self.N):
            for j in range(self.N):
                if(self.get_number(i,j) == 0):
                    for k in range(len(self.numbers_list)):
                        actions.append((i,j,self.numbers_list[k]))
        return actions

    def do_action_board(self, action):
        if action[2] in self.numbers_list:
            if self.board_grid[action[0]][action[1]] not in self.numbers_list:
                self.board_grid[action[0]][action[1]] = action[2]
                self.numbers_list.remove(action[2])
            else:
                raise ValueError('Can not change this position!\n')
        else:
            raise ValueError('The board already has that number!\n')

    def search_number_board(self, number):
        # looks for the line and collumn of the number in the board
        for i in range(self.N):
            for j in range(self.N):
                if(self.get_number(i,j) == number):
                    return [i,j]

        raise ValueError('The number {0} is not on the board\n'.format(number))
                

    def is_goal_board(self):
        #looks for number 1 in the board
        lst = self.search_number_board(1)
        i = lst[0]
        j = lst[1]
        # see if the board has a continuos sequence
        for k in range(1,self.N*self.N):
            adj_horiz = self.adjacent_horizontal_numbers(i, j)
            adj_vert = self.adjacent_vertical_numbers(i, j)
            if( k + 1 == adj_horiz[0]):
                j = j - 1
            elif( k + 1 == adj_horiz[1]):
                j = j + 1
            elif( k + 1 == adj_vert[0]):
                i = i + 1
            elif( k + 1 == adj_vert[1]):
                i = i - 1
            else:
                return False
        return True

    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        file = open(filename, 'r')

        #get the first line of the file (with N)
        N = int(file.readline())
        board=[]
        number=0
        board_index=0

        #for each N line take the numbers and puts them in board
        for k in range(N):
            line = file.readline()
            #print(line)
            board.append([])
            for i in range(len(line)):
                if line[i] != '\t' and line[i] != '\n':
                    number = (number*10) + int(line[i])
                else:
                    board[board_index].append(number)
                    number=0
            board_index+=1 

        file.close()
        #print(board)
        return Board(filename, board)


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.init_state = NumbrixState(board)

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        return state.get_actions()

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        actions = self.actions(state)
        new_state = NumbrixState(state.board)
        if(action in actions):
            new_state.do_action(action)
            return new_state
        else:
            raise ValueError('This action is not possible.\n')

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        return state.is_goal()

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
    


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1], 
    # Usar uma técnica de procura para resolver a instância, 
    # Retirar a solução a partir do nó resultante, 
    # Imprimir para o standard output no formato indicado.

    # Ler o ficheiro de input de sys.argv[1]
    if len(sys.argv) == 2:
	    filename = sys.argv[1]
    else:
	    print("Missing the name of the input file.")

    init_board = Board.parse_instance(filename)

    problem = Numbrix(init_board)

    board = init_board

    # Criar um estado com a configuração inicial:
    s0 = NumbrixState(board)
    print("Initial:\n", s0.board.to_string(), sep="")
    # Aplicar as ações que resolvem a instância
    s1 = problem.result(s0, (0, 0, 21))
    s2 = problem.result(s1, (0, 1, 22))
    s3 = problem.result(s2, (0, 2, 23))
    s4 = problem.result(s3, (0, 3, 24))
    s5 = problem.result(s4, (0, 4, 25))
    s6 = problem.result(s5, (0, 5, 26))

    s8 = problem.result(s6, (1, 0, 20))
    s9 = problem.result(s8, (1, 1, 19))
    s10 = problem.result(s9, (1, 2, 12))
    s11 = problem.result(s10, (1, 4, 28))
    s12 = problem.result(s11, (2, 0, 1))
    s13 = problem.result(s12, (2, 1, 18))
    s14 = problem.result(s13, (2, 2, 13))
    s15 = problem.result(s14, (2, 3, 10))
    s16 = problem.result(s15, (2, 4, 29))
    s17 = problem.result(s16, (3, 0, 2))
    s18 = problem.result(s17, (3, 1, 17))
    s19 = problem.result(s18, (3, 2, 14))
    s20 = problem.result(s19, (3, 3, 9))
    s21 = problem.result(s20, (3, 4, 36))
    s22 = problem.result(s21, (3, 5, 31))
    s23 = problem.result(s22, (4, 0, 3))
    s24 = problem.result(s23, (4, 1, 16))
    s25 = problem.result(s24, (4, 3, 8))
    s26 = problem.result(s25, (4, 5, 32))
    s27 = problem.result(s26, (5, 0, 4))
    s28 = problem.result(s27, (5, 1, 5))
    s29 = problem.result(s28, (5, 2, 6))
    s30 = problem.result(s29, (5, 3, 7))
    s31 = problem.result(s30, (5, 4, 34))
    s32 = problem.result(s31, (5, 5, 33))

    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(s32))
    print("Solution:\n", s32.board.to_string(), sep="")

