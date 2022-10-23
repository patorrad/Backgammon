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
        moves, scores = self.get_next_ply(state, die1, die2, 1) 
        # return self.get_first_move()
        # return self.get_last_move()
        return self.move_randomly(state.whose_move)

    def get_next_ply(self, state, die1, die2, ply):
        if ply < self.maxPly:
            return self.get_next_ply(state, die1, die2, ply + 1)
        else:
            self.initialize_move_gen_for_state(state, state.whose_move, die1, die2)
            return self.get_all_moves(state.whose_move)

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

    def get_all_moves(self, player):
        """Uses the mover to generate all legal moves."""
        move_list = []
        move_score = []
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
                    move_list.append(m[0])    # Add the move to the list.
                    move_score.append(get_pip_count(m[1].pointLists, player))
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append('p')
        return move_list, move_score

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
