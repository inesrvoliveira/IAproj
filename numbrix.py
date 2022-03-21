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
        
    # TODO: outros metodos da classe


class Board:
    """ Representação interna de um tabuleiro de Numbrix. """

    def __init__(self, filename, board):
        self.filename = filename
        self.board = board
    
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        if(row < len(self.board) and col < len(self.board) ):
            return self.board[row][col]
        else:
            raise ValueError('The row or column are out of range.\n')
    
    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        lst = []
        #low position
        if(row == len(self.board) - 1):
            lst.append(None)
        else:
            lst.append(self.board[row+1][col])
        #up position
        if(row == 0):
            lst.append(None)
        else:
            lst.append(self.board[row-1][col])
        
        return tuple(lst)
    
    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        lst = []
        #left position
        if(col == 0):
            lst.append(None)
        else:
            lst.append(self.board[row][col-1])
        #right position
        if(col == len(self.board) - 1):
            lst.append(None)
        else:
            lst.append(self.board[row][col+1])
        
        return tuple(lst)
    
    def to_string(self) -> str:
        s = str()
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                s += str(self.board[i][j])
                if (j == len(self.board)-1):
                    s+= '\n'
                else:
                    s+= ' '
        return s

    
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
        # TODO
        pass

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        # TODO
        pass

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        # TODO
        pass

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

    #for testing
    board = Board.parse_instance(filename)

    print("Initial:\n", board.to_string(), sep="")

    print(board.adjacent_vertical_numbers(0, 2))
    print(board.adjacent_horizontal_numbers(0, 2))
    pass
