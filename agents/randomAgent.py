"""SkeletonAgent.py
This file defines a class BackgammonPlayer.
Instantiating this class creates an "agent"
that implements the introduce method and
the move method, and is capable of making
a legal move, but will not make any
effort to choose a good move.

S. Tanimoto, April 17, 2020.
 The get_all_moves function was updated April 24
so it only includes the pass move 'p' if there are
no other moves.

"""

# Access to the state class is not needed in the
# starter version of this agent.
# from boardState import *

from game_engine import genmoves
import random    # Used in the "move_randomly" method.

W = 0
R = 1

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.maxPly = 2

    def introduce(self):
        return "I\'m random."

    def nickname(self):
        return "Random"

    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)

    def move(self, state, die1, die2):
        # self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
        start_node = Node(state=state)
        self.get_next_ply(die1, die2, 1, start_node) 
        # return self.get_first_move()
        # return self.get_last_move()
        # return self.move_randomly(state.whose_move)
        return random.choice(moves)

    def get_last_ply(self, die1, die2, node):
        self.initialize_move_gen_for_state(node.state, node.state.whose_move, die1, die2)
        return self.get_all_moves(node.state.whose_move, node)

    def get_next_ply(self, die1, die2, ply, node):
        if ply >= self.maxPly:
            ply += 1
            return self.get_last_ply(die1, die2, node)
        else:
            self.initialize_move_gen_for_state(node.state, node.state.whose_move, die1, die2)
            self.get_all_moves(node.state.whose_move, node)
            ply += 1
            for i in range(len(node.descendants)):
                self.get_next_ply(die1, die2, ply, node.descendants[i])
            # return moves, scores, states

    def get_first_move(self):
        """Uses the mover to generate only one move."""
        try:
            m = next(self.move_generator)    # Gets a (move, state) pair.
            # print("next returns: ", m[0])    # Prints out the move.    For debugging.
            print(m[1].pretty_print())
            return m[0]    # Returns the move.
        except StopIteration as e:
            print("Exception generating the next move.")
            print(e)
            return "NO_MOVES"

    def get_last_move(self):
        """Chooses the last of the legal moves."""
        moves = self.get_all_moves()
        if len(moves) == 0:
            return "NO MOVES COULD BE FOUND"
        return moves[-1]

    def get_all_moves(self, player, node):
        """Uses the mover to generate all legal moves."""
        move_list = []
        move_score = []
        move_state = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                print(m[1].pointLists)
                # print(get_pip_count(m[1].pointLists, player))
                
                if m[0] != 'p':
                    any_non_pass_moves = True
                    node.descendants.append(Node(m[0], get_pip_count(m[1].pointLists, player), m[1]))
                    # move_list.append(m[0])    # Add the move to the list.
                    # move_score.append(get_pip_count(m[1].pointLists, player))
                    # move_state.append(m[1])
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            # move_list.append('p')
            node.descendants.append('p')
        #return move_list, move_score, move_state

    def move_randomly(self, player):
        moves, scores = self.get_all_moves(player)
        print(scores)
        if len(moves) == 0:
            return "NO MOVES COULD BE FOUND"
        # return random.choice(moves)
        score = scores.index(min(scores))
        return moves[score]

def get_pip_count(board_state, player):
    a=[(len(e)*(len(board_state)-i)) for i, e in enumerate(board_state) if player in e]
    return sum(a)


class Node:
    def __init__(self, move = None, score = None, state = None):
        self.move = move
        self.score = score
        self.state = state
        self.descendants = []