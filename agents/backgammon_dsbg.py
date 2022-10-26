'''
Name(s): Paolo Torrado
UW netid(s):patorrad
'''
PAOLO = 'patorrad'
KELLY = 'ployknp'

from cmath import inf
from game_engine import genmoves

GENMOVES_INSTANCE = genmoves.GenMoves()

W = 0
R = 1

class BackgammonPlayer:
    def __init__(self, maxply = 3):
        self.GenMoveInstance = genmoves.GenMoves()
        # feel free to create more instance variables as needed.
        self.maxply = maxply
        self.static_eval = lambda max_player, min_player: max_player - min_player
        self.start_node = None
        self.prune = False
        self.states = 0
        self.cutoffs = 0

    # TODO: return a string containing your UW NETID(s)
    # For students in partnership: UWNETID + " " + UWNETID
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return PAOLO + " " + KELLY

    # If prune==True, then your Move method should use Alpha-Beta Pruning
    # otherwise Minimax
    def useAlphaBetaPruning(self, prune=False):
        # TODO: use the prune flag to indiciate what search alg to use
        self.prune = prune

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        # TODO: return a tuple containig states and cutoff
        return (-1, -1)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. maxply=2 indicates that
    # our search level will go two level deep.
    def setMaxPly(self, maxply=2):
        # TODO: set the max ply
        self.maxply = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        # TODO: update your staticEval function appropriately
        self.static_eval = func

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move.
    # Keep in mind: a player can only pass if the player cannot move any checker with that role
    def move(self, state, die1=1, die2=6):
        self.start_node = Node(state=state)
        self.get_next_ply(die1, die2, 1, self.start_node)
        # return self.last_minimax(self.start_node)
        # self.minimax(self.start_node, 1)
        self.start_node.get_move()
        return self.start_node.move

    # def last_minimax(self, node, ply):
    #     # return node.descendants[node.get_max()].move
    #     if (ply % 2) == False:
    #         node.move = node.descendants[node.get_max()].move
    #     else: 
    #         node.move = node.descendants[node.get_min()].move

    # def minimax(self, node, ply):
    #     if ply >= self.maxply:
    #         ply += 1
    #         self.last_minimax(node, ply)
    #     else: 
    #         ply += 1
    #         for i in range(len(node.descendants)):
    #             self.minimax(node.descendants[i], ply)
    #         if (ply % 2) == False:
    #             node.move = node.descendants[node.get_max()].move
    #         else: 
    #             node.move = node.descendants[node.get_min()].move

    # Hint: Look at game_engine/boardState.py for a board state properties you can use.
    def staticEval(self, state):
        # TODO: return a number for the given state
        # print('static',self.static_eval(get_pip_count(state.pointLists, state.whose_move), get_pip_count(state.pointLists, int(not bool(state.whose_move)))))
        return self.static_eval(get_pip_count(state.pointLists, state.whose_move), get_pip_count(state.pointLists, int(not bool(state.whose_move))))

    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)

    def get_all_moves(self, player, node):
        """Uses the mover to generate all legal moves."""
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    # print(m[1].pretty_print())
                    node.descendants.append(Node(m[0], self.staticEval(m[1]), m[1]))
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            # node.descendants.append('p')
            node.descendants.append(Node(move='p',score=-100, state=node.state))
    
    def get_last_ply(self, die1, die2, node):
        self.initialize_move_gen_for_state(node.state, node.state.whose_move, die1, die2)
        self.get_all_moves(node.state.whose_move, node)

    def get_next_ply(self, die1, die2, ply, node):
        if ply >= self.maxply:
            ply += 1
            self.get_last_ply(die1, die2, node)
            if (ply % 2) == False:
                node.get_max()
            else: 
                node.get_min()
        else:
            self.initialize_move_gen_for_state(node.state, node.state.whose_move, die1, die2)
            self.get_all_moves(node.state.whose_move, node)
            ply += 1
            for i in range(len(node.descendants)):
                self.get_next_ply(die1, die2, ply, node.descendants[i])
            if (ply % 2) == False:
                node.get_max()
            else: 
                node.get_min()

def get_pip_count(board_state, player):
    if player == W:
        a=[(len(e)*(len(board_state)-i)) for i, e in enumerate(board_state) if player in e]
    else:
        a=[(len(e)*(i+1)) for i, e in enumerate(board_state) if player in e]
    # print('pip count', sum(a), 'for', player)
    return sum(a)

class Node:
    def __init__(self, move = None, score = None, state = None, alpha = float(-inf), beta = float(inf)):
        self.move = move
        self.score = score
        self.state = state
        self.descendants = []
        alpha = alpha
        beta = beta

    def get_max(self):
        max = 0
        index = 0
        for i in range(len(self.descendants)):
            if self.descendants[i].score > max: 
                index = i
                max = self.descendants[i].score
        self.score = max

    def get_min(self):
        min = 0
        index = 0
        for i in range(len(self.descendants)):
            if self.descendants[i].score < min: 
                index = i
                min = self.descendants[i].score
        self.score = min

        self.descendants[index]
    
    def get_move(self):
        max = 0
        index = 0
        for i in range(len(self.descendants)):
            if self.descendants[i].score > max: 
                index = i
                max = self.descendants[i].score
        self.move = self.descendants[index].move
