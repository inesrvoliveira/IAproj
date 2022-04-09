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

    def goal_state(self):
        #find the goal state in this stata (that is the init_state)
        return 
        
    # TODO: outros metodos da classe


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """
    def __init__(self, filename, board):
        self.filename = filename
        self.board = board
        self.N = len(board)
    
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        if(row < self.N and col < self.N ):
            return self.board[row][col]
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
                if (j == self.N-1 and i != self.N-1):
                    s+= '\n'
                else:
                    s+= ' '
        return s

    def get_actions(self):
        # list with the numbers (from 1 to NxN) that can be used fill the board
        numbers = list(range(1,self.N*self.N+1))
        actions=[]
        for i in range(self.N):
            for j in range(self.N):
                if(self.get_number(i,j) != 0):
                    numbers.remove(self.get_number(i,j))
        for i in range(self.N):
            for j in range(self.N):
                if(self.get_number(i,j) == 0):
                    for k in range(len(numbers)):
                        actions.append((i,j,numbers[k]))
        return actions

    def do_action(self, action):
        self.board[action[0]][action[1]] = action[2]



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

    # TODO: outros metodos da classe


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.init_state = NumbrixState(board)

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        return state.board.get_actions()

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        actions = self.actions(state)
        new_state = NumbrixState(state.board)
        if(action in actions):
            new_state.board.do_action(action)
            return new_state
        else:
            raise ValueError('This action is not possible.\n')

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        return state == self.init_state.goal_state()

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
    
    # TODO: outros metodos da classe


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
    s1 = problem.result(s0, (2, 2, 1))
    s2 = problem.result(s1, (0, 2, 3))
    s3 = problem.result(s2, (0, 1, 4))
    s4 = problem.result(s3, (1, 1, 5))
    s5 = problem.result(s4, (2, 0, 7))
    s6 = problem.result(s5, (1, 0, 8))
    s7 = problem.result(s6, (0, 0, 9))
    # Verificar se foi atingida a solução
    print("Is goal?", problem.goal_test(s7))
    print("Solution:\n", s7.board.to_string(), sep="")

    pass
