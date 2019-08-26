board_size = 6

def new_state(size):
    return [0 for _ in range(size)]

def is_goal(state):
    size = state.__len__()
    for i in range(size):
        for j in range(i+1,size):
            if state[i]==state[j] or abs(state[i]-state[j])==abs(i-j):
                return False
    return True

actions = {}
for i in range(2*board_size):
    tmp = [0 for _ in range(board_size)]
    tmp[i//2] = int(2 * ((i % 2)-0.5))
    actions[i] = tmp

def successor(state, action):
    return list(map(lambda z: max(0,min(board_size-1,z)), [s+a for s,a in zip(state,actions[action])]))

def hash(state):
    id = 0
    for i in range(board_size):
        id = id * board_size + state[i]
    return id

explored = []
frontier = []

def breadth_first_search(state):
    frontier.append(state)
    while frontier.__len__()!=0:
        next_state = frontier.pop(0)
        explored.append(hash(next_state))
        if is_goal(next_state):
            return next_state
        for y in range(2*board_size):
            future_state = successor(next_state,y)
            if future_state not in frontier and hash(future_state) not in explored:
                frontier.append(future_state)
    return None  

print(breadth_first_search(new_state(board_size)))
