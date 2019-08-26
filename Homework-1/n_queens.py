class n_queens():

    def __init__(self, board_size):
        board_size = board_size
        actions = {}

    def new_state(self):
        return [0 for _ in range(self.board_size)]

    def is_goal(self, state):
        for i in range(board_size):
            for j in range(i+1,board_size):
                if state[i]==state[j] or abs(state[i]-state[j])==abs(i-j):
                    return False
        return True

    def set_actions(self):
        for i in range(2*board_size):
            tmp = [0 for _ in range(board_size)]
            tmp[i//2] = int(2 * ((i % 2)-0.5))
            self.actions[i] = tmp

    def successor(self, state, action):
        return list(map(lambda z: max(0,min(board_size-1,z)), [s+a for s,a in zip(state,self.actions[action])]))

    def hash(self, state):
        id = 0
        for i in range(board_size):
            id = id * board_size + state[i]
        return id

    def breadth_first_search(self, state):
        explored = []
        frontier = []
        frontier.append(state)
        while frontier.__len__()!=0:
            next_state = frontier.pop(0)
            explored.append(self.hash(next_state))
            if self.is_goal(next_state):
                return next_state
            for y in range(2*board_size):
                future_state = self.successor(next_state,y)
                if future_state not in frontier and self.hash(future_state) not in explored:
                    frontier.append(future_state)
        return None

    def solve(self):
        self.set_actions
        print(self.breadth_first_search(self.new_state()))

six = n_queens(4)
six.solve()