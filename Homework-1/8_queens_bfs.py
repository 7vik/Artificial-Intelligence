board_size = 8

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

def hashh(state):
    id = 0
    for i in range(board_size):
        id = id * board_size + state[i]
    return id

def hash_index(h):
    return h % 100000007

explored = [[None] for _ in range(100000007)]
frontier = []

def breadth_first_search(state):
    frontier.append(state)
    kkk = 0
    while frontier.__len__()!=0:
        print(f"Checked states: {kkk}")
        next_state = frontier.pop(0)
        explored[hash_index(hashh(next_state))].append(hashh(next_state))
        if is_goal(next_state):
            return next_state
        for y in range(2*board_size):
            future_state = successor(next_state,y)
            if future_state not in frontier and hashh(future_state) not in explored[hash_index(hashh(future_state))]:
                kkk += 1
                frontier.append(future_state)
    return None  

print(breadth_first_search(new_state(board_size)))
