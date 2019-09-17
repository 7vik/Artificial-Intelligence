board_size = 4
class n_queens_state(object):

    def __init__(self):
        actions = {}
        virgin = [0 for _ in range(board_size)]
        self.state = virgin

    def is_goal(self):
        for i in range(board_size):
            for j in range(i+1,board_size):
                if self.state[i]==self.state[j] or abs(self.state[i]-self.state[j])==abs(i-j):
                    return False
        return True

    def set_actions(self):
        for i in range(2*board_size):
            tmp = [0 for _ in range(board_size)]
            tmp[i//2] = int(2 * ((i % 2)-0.5))
            self.actions[i] = tmp

    def successor(self, action):
        return list(map(lambda z: max(0,min(board_size-1,z)), [s+a for s,a in zip(self.state,self.actions[action])]))

    def hash(self):
        id = 0
        for i in range(board_size):
            id = id * board_size + self.state[i]
        return id

    def breadth_first_search(self):
        explored = []
        frontier = []
        frontier.append(self.state)
        while frontier.__len__()!=0:
            next_state = frontier.pop(0)
            explored.append(self.hash())
            if self.is_goal():
                return next_state
            for y in range(2*board_size):
                future_state = self.successor(y)
                if future_state not in frontier and self.hash() not in explored:
                    frontier.append(future_state)
        return None

    def solve(self):
        self.set_actions
        print(self.breadth_first_search())

six = n_queens_state()
six.solve()