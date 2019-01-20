#!/usr/bin/python

import numpy as np
from tronproblem import TronProblem
import random, Queue, math
from implemented_adversarial import alpha_beta_cutoff


class StudentBot():
    """ Write your student bot here"""
    survival= False

    W = '#'  # character for wall
    B = 'x'  # character for Barrier
    S = ' '  # character for space
    P = '*'  # character for powerup.

    def heur2(self, state):
        score = self.bfs2(state, self.player)
        # scale score down so the sigmoid function is more responsive
        return self.sigmoid(score / 200.0)

    def bfs2(self, state, play_num):  # a bounded search of how many tiles are accessible
        board = state.board
        origin = state.player_locs[play_num]
        visited = set()
        Q = Queue.Queue()
        Q.put(origin)
        visited.add(origin)
        while not Q.empty():
            curr = Q.get()
            valid_moves = list(TronProblem.get_safe_actions(board, curr))
            for direction in valid_moves:
                neighbor = TronProblem.move(curr, direction)
                if neighbor not in visited:
                    visited.add(neighbor)
                    Q.put(neighbor)
        return len(visited)

    def sigmoid(self, x):
        # a function that maps any real number to a value between 0 and 1
        return 1 / (1 + math.exp(-x))

    def survive(self,asp):

        order = ['U', 'D', 'L', 'R']
        random.shuffle(order)


        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board,loc))
        if not possibilities:
            return 'U'
        decision = possibilities[0]
        for move in order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            if len(TronProblem.get_safe_actions(board,next_loc)) < 3:
                decision = move
                break
        return decision

    def flatten(self, board):
        maxrow = len(board)
        maxcol = len(board[0])
        grid = np.zeros((maxrow, maxcol))
        for i in range(maxrow):
            for j in range(maxcol):
                if board[i][j]==StudentBot.S or board[i][j]==StudentBot.P:
                    continue
                else :
                    grid[i, j]= -1

        return grid

    # return a ndarray
    # play_num is the player to optimize, state's ptm does not have to equal to play_num
    def bfs(self,state,play_num): #a bounded search of how many tiles are accessible
        board = state.board
        grid = self.flatten(board)
        origin = state.player_locs[play_num]
        visited = {}
        Q = Queue.Queue()
        Q.put(origin)
        visited[origin]=0
        while not Q.empty():
            curr = Q.get()
            d = visited[curr]
            valid_moves = list(TronProblem.get_safe_actions(board,curr))
            for direction in valid_moves:

                neighbor = TronProblem.move(curr,direction)
                if neighbor in visited:
                    continue
                rn, cn =neighbor
                if grid[rn, cn]==-1:
                    continue


                if grid[rn, cn]==0 or d < grid[rn, cn]:
                    grid[rn, cn]= d+ 1

                visited[neighbor]= d+1
                Q.put(neighbor)
        return grid

    def heur(self, state):

        #start_time = timeit.default_timer()

        num_players=len(state.player_locs)

        next_ptm = (self.player + 1) % num_players

        head=state.player_locs[self.player]
        # head = player.segments[0].topleft
        ophead=state.player_locs[next_ptm]
        # ophead = opponent.segments[0].topleft

        myReach=self.bfs(state, self.player)
        theirReach=self.bfs(state, next_ptm)

        self.overlap = False
        myScore = 0
        theirScore = 0

        board = state.board
        maxrow = len(board)
        maxcol = len(board[0])

        for i in range(maxrow):
            for j in range(maxcol):
                adding = 1
                if myReach[i, j]==-1:
                    continue
                if board[i][j] == StudentBot.P:
                    adding=3
                if myReach[i, j] != 0 and theirReach[i, j]!=0:
                    if myReach[i, j] < theirReach[i, j]:
                        myScore+=adding
                    elif myReach[i, j] > theirReach[i, j]:
                        theirScore += adding
                elif myReach[i, j] !=0 and theirReach[i, j]==0 :
                    myScore+=adding
                    self.overlap=True

                elif myReach[i, j] ==0 and theirReach[i, j]!=0 :
                    theirScore+=adding
                    self.overlap = True

        score= myScore - theirScore
        # if not self.overlap and score <= 0:
        #     self.survival=True


        # score = self.bfs(state, self.player)
        # # scale score down so the sigmoid function is more responsive
        return self.sigmoid(score/100.0)
    def decide(self,asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        
        To get started, you can get the current 
        state by calling asp.get_start_state()
        """

        start = asp.get_start_state()
        self.player = start.player_to_move()
        if self.survival:
            #return self.survive(asp)
            return alpha_beta_cutoff(asp, 3, self.heur)

        self.heur(start)

        if self.overlap:
            self.survival=True
            #return self.survive(asp)

        return alpha_beta_cutoff(asp, 3, self.heur)

    def cleanup(self):
        """
        This function will be called in between
        games during grading. You can use it
        to reset any variables your bot uses during the game
        (for example, you could use this function to reset a 
        turns_elapsed counter to zero). If you don't need it,
        feel free to leave it as "pass"
        """
        self.survival=False



class RandBot():
    """Moves in a random (safe) direction"""
    def decide(self,asp):
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board,loc))
        if possibilities:
            return random.choice(possibilities)
        return 'U'

    def cleanup(self):
        pass


class WallBot():
    """Hugs the wall"""
    def __init__(self):
        order = ['U','D','L','R']
        random.shuffle(order)
        self.order = order

    def cleanup(self):
        order = ['U','D','L','R']
        random.shuffle(order)
        self.order = order
        
    def decide(self,asp):
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board,loc))
        if not possibilities:
            return 'U'
        decision = possibilities[0]
        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            if len(TronProblem.get_safe_actions(board,next_loc)) < 3:
                decision = move
                break
        return decision


class TABot1():
    """a bot that tries to leave itself as much space as possible"""
    def decide(self,asp):
        start = asp.get_start_state()
        self.player = start.player_to_move()
        return alpha_beta_cutoff(asp,3,self.heur)
        
    def sigmoid(self,x):
        #a function that maps any real number to a value between 0 and 1
        return 1 / (1 + math.exp(-x))
        
    def heur(self,state):
        score = self.bfs(state,self.player)
        #scale score down so the sigmoid function is more responsive
        return self.sigmoid(score/200.0)
        
    def bfs(self,state,play_num): #a bounded search of how many tiles are accessible
        board = state.board
        origin = state.player_locs[play_num]
        visited = set()
        Q = Queue.Queue()
        Q.put(origin)
        visited.add(origin)
        while not Q.empty():
            curr = Q.get()
            valid_moves = list(TronProblem.get_safe_actions(board,curr))
            for direction in valid_moves:
                neighbor = TronProblem.move(curr,direction)
                if neighbor not in visited:
                    visited.add(neighbor)
                    Q.put(neighbor)
        return len(visited)

    def cleanup(self):
        pass
