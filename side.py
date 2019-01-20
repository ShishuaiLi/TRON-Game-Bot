def heur(self, state):
    # start_time = timeit.default_timer()

    num_players = len(state.player_locs)

    next_ptm = (self.player + 1) % num_players

    head = state.player_locs[self.player]
    # head = player.segments[0].topleft
    ophead = state.player_locs[next_ptm]
    # ophead = opponent.segments[0].topleft

    myReach = self.bfs(state, self.player)
    theirReach = self.bfs(state, next_ptm)

    self.overlap = False
    myScore = 0
    theirScore = 0

    board = state.board
    maxrow = len(board)
    maxcol = len(board[0])

    for i in range(maxrow):
        for j in range(maxcol):
            if myReach[i, j] == -1:
                continue
            if myReach[i, j] != 0 and myReach[i, j] < theirReach[i, j]:
                self.overlap = True
                if board[i][j] == StudentBot.P:
                    myScore += 3
                else:
                    myScore += 1
            elif myReach[i, j] > theirReach[i, j] and theirReach[i, j] != 0:
                self.overlap = True
                if board[i][j] == StudentBot.P:
                    theirScore += 3
                else:
                    theirScore += 1

    score = myScore - theirScore
    if not self.overlap and score <= 0:
        self.survival = True

    # score = self.bfs(state, self.player)
    # # scale score down so the sigmoid function is more responsive
    return self.sigmoid(score / 100.0)




    def heur(self, state):
        player_costs = self.dijkstra(state, head)

        op_costs = self.dijkstra(state, ophead)

        pcount = 0
        opcount = 0
        board = state.board
        maxcost = len(board) + len(board[0])
        for r in range(len(board)):
            for c in range(len(board[0])):
                if player_costs[r, c] < op_costs[r, c] and player_costs[r, c] <= maxcost:
                    pcount += 1
                if op_costs[r, c] < player_costs[r, c] and op_costs[r, c] <= maxcost:
                    opcount += 1

        v = (pcount - opcount) / float(len(board) * len(board[0]))
        # print "Heuristic val: " + str(v)
        #print str(timeit.default_timer() - start_time)
        return


    def grid_neighbors(self, board, row, col):
        maxrow = len(board)
        maxcol = len(board[0])
        l = []
        if (row + 1 < maxrow):
            l += [(row + 1, col)]
        if (row > 0):
            l += [(row - 1, col)]
        if (col + 1 < maxcol):
            l += [(row, col + 1)]
        if (col > 0):
            l += [(row, col - 1)]
        return l


    def dijkstra(self, state, head):
        hr, hc = head
        board = state.board
        dists = np.zeros((len(board), len(board[0])))
        # dists = np.zeros((GAME_ROWS, GAME_COLS))
        dists[:] = np.inf
        visited = np.zeros((len(board), len(board[0])))
        # visited = np.zeros((GAME_ROWS, GAME_COLS))
        dists[hr, hc] = 0.0
        ns = self.grid_neighbors(board, hr, hc)
        q = Queue.Queue()
        for n in ns:
            r, c = n
            dists[r, c] = 1
            q.put(n)

        while q.qsize() != 0:
            cr, cc = q.get()
            ndist = dists[cr, cc] + 1
            for n in self.grid_neighbors(board, cr, cc):
                nr, nc = n
                if (board[nr][nc] != StudentBot.S and board[nr][nc] != StudentBot.P):
                    continue
                if ndist < dists[nr, nc]:
                    dists[nr, nc] = ndist
                if visited[nr, nc] == 0:
                    q.put(n)
                    visited[nr, nc] = 1
        return dists


    def sigmoid(self, x):
        # a function that maps any real number to a value between 0 and 1
        return 1 / (1 + math.exp(-x))