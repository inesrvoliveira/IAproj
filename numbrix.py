# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 21:
# 97124 Jiaqi Yu
# 89465 Ines Oliveira

import sys
import copy
from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_graph_search, greedy_search, recursive_best_first_search

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
        print("GOAL:")
        print(self.board.is_goal_board())
        print(self.board.to_string())
        return self.board.is_goal_board()
        

class Board:
    """ Representação interna de um tabuleiro de Numbrix. """
    def __init__(self, board):
        self.board_grid = board
        #size of the line and column of the board 
        self.N = len(board)
        #numbers not on the board yet
        self.numbers_list = [] 
        #number on the board
        self.numbers_on_list = []
    
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
                    self.numbers_on_list.append(self.get_number(i,j))
                    self.numbers_list.remove(self.get_number(i,j))
        self.numbers_on_list.sort()
        return
    
    def verify_adj_number(self, row,col, number):
        #verify if the adjacent numbers (horizontal and veritcal) are the previous number or the next number 
        adj_horiz = self.adjacent_vertical_numbers(row,col)
        adj_vert = self.adjacent_horizontal_numbers(row,col)
        if (adj_horiz[0] == number-1 or adj_horiz[0] == number+1 or adj_horiz[1] == number-1 or adj_horiz[1] == number+1 or adj_vert[0] == number-1 or adj_vert[0] == number+1 or adj_vert[1] == number-1 or adj_vert[1] == number+1):
            return True
        else:
            return False

    def get_actions_board(self):
        actions=[]
        first_time = True 
        actions_aux=[]
        self.set_numbers_list()
        for h in self.numbers_list:
            for i in range(self.N):
                for j in range(self.N):
                    if self.get_number(i,j) == 0 and self.verify_adj_number(i,j,h):
                        actions_aux.append((i,j,h))  
            
            if len(actions_aux) < len(actions) or first_time:
                actions = copy.deepcopy(actions_aux) 
                first_time = False   
        print(actions)          
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

        return []
                
    def is_goal_board(self):
        #searches for number 1 in the board
        lst = self.search_number_board(1)
        # if lst [] means that the number is not on the board, so is not goal yet
        if(lst == []):
            return False
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
        return Board(board)


class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = NumbrixState(board)

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
        new_state = copy.deepcopy(NumbrixState(state.board))
        if(action in actions):
            new_state.do_action(action)
            return new_state
        else:
            print("This action is not possible.\n")
            #raise ValueError('This action is not possible.\n')

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        return state.is_goal()

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        board = node.state.board
        board.set_numbers_list()
        smallest_number_played = board.numbers_on_list[0]
        aux0 = board.N * board.N
        aux1 = 0
        j = 0
        x1=0
        x2=0
        y1=0
        y2=0
        for i in range(len(board.numbers_on_list)):
            aux1 = board.numbers_on_list[i] - smallest_number_played
            if (aux0 > aux1):
                aux0 = copy.deepcopy(aux1)
                j = i
        for y in range(board.N):
            for x in range(board.N):
                if board.board_grid[y][x] == smallest_number_played:
                    x1 = x
                    y1 = y
                if board.board_grid[y][x] == board.numbers_on_list[j]:
                    x2 = x
                    y2 = y
        h = ( (x1 - x2)**2 + (y1 - y2)**2 )**2
        return h
    


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

    # Obter o nó solução usando a procura A*:
    goal_node = depth_first_graph_search(problem)
    # Verificar se foi atingida a solução
    #print("Is goal?", problem.goal_test(goal_node.state))
    
    print(goal_node.state.board.to_string(),end="", sep="")

