##       Satvik Golechha        ##
##       2017A7PS0117P          ##
##                              ##
  ##############################

import tkinter          # for GUI
import random           # for filling dirt randomly
import copy as cp       # for deep, shallow copying of state lists
import sys              # inbuilt python methods
import time             # for running times of bfs/ids
RS = 4                 # room size
rest_pos = [(0,0)]      # rest positions
dp = 20                 # dust percentage

class state():
    def __init__(self,room,location,cost,path):
                        # a list of lists, tells position of dirt
        self.room = cp.deepcopy(room)    
                        # a tuple, denoting the current location of the vaccuum cleaner
        self.location = cp.copy(location)
                        # cost incurred since the start state
        self.cost = cost
                        # the path of actions which drove to this state
        self.path = path

#   amount of memory taken by a single node
def node_size(state):
    mem = 0
    temp = 0
    for elem in state.room:
        temp += sys.getsizeof(elem)
    mem += temp
    mem += sys.getsizeof(state.location)
    mem += sys.getsizeof(state.cost)
    mem += sys.getsizeof(state.path)
    return mem

#   the set of all possible actions
actions = {
    0: 'MR',
    1: 'ML',
    2: 'MU',
    3: 'MD',
    4: 'S',
    #5: 'N',
}

def print_state(st):
    print(f"Room Size: {RS}")
    print(f"Location of VC: {st.location}")
    print(f"Current Cost: {st.cost}")
    for row in st.room:
        print(*row)

def next_state(st, action):
    new = state(st.room,st.location,st.cost,st.path)
    if action[0] == 'M':
        new.cost += 2
    elif action == 'S':
        new.cost += 1
    
    if action == 'S':
        new.room[st.location[0]][st.location[1]] = 0
    elif action == 'MU':
        new.location = (max(0,new.location[0]-1), new.location[1])
    elif action == 'MD':
        new.location = (min(RS-1,new.location[0]+1), new.location[1])
    elif action == 'MR':
        new.location = (new.location[0], min(RS-1,new.location[1]+1))
    elif action == 'ML':
        new.location = (new.location[0], max(0,new.location[1]-1))
    
    new.path += (action+', ')

    return new

    

#   returns a room with dirt on 'p' percent randomly chosen points
def dirt_generator(p):
    room = []
    for i in range(RS):
        room.append([0 for _ in range(RS)])
    if not p:
        return room
    positions = [i for i in range(RS*RS)]
    random.shuffle(positions)
    num_dirt = (p * RS**2) // 100
    dirt_pos = positions[0:num_dirt+1]
    for pos in dirt_pos:
        column = pos % RS
        row = pos // RS
        room[row][column] = 1
    return room

def goal_test(state):
    if state.room == dirt_generator(0):
        return True
    return False

def hashh(state):
    id = 0
    for i in range(RS**2):
        column = i % RS
        row = i // RS
        id = ( id * 2 + st.room[row][column] ) % 100007
    return id

explored = [[] for _ in range(100007)]
frontier = []

def not_explored(st):
    for item in explored[hashh(st)]:
        if item.room == st.room and item.location == st.location:
            return False
    #print("explored")
    return True

def breadth_first_search(state):
    t1 = time.time()
    max_queue = 0
    print()
    print("Performing breadth first search")
    nodes = 0
    frontier.append(state)
    while frontier.__len__()!=0:
        new_state = frontier.pop(0)
        nodes += 1  
        explored[hashh(new_state)].append(new_state)
        if goal_test(new_state):
            t2 = time.time()
            print(f"R1: Number of nodes generated = {nodes}")
            print(f"R2: Size of a node = {node_size(new_state)} bytes")
            print(f"R3: Max size of auxillary queue = {max_queue}")
            print(f"G1: Action Path = {new_state.path}")
            print(f"R4: Total Cost = {new_state.cost}")
            print(f"R5: Total time taken = {round(t2-t1,2)} seconds")
            print()
            return new_state
        for y in range(5):
            future_state = next_state(new_state,actions[y])
            if future_state not in frontier and not_explored(future_state):
                frontier.append(future_state)
                max_queue = frontier.__len__() if max_queue < frontier.__len__() else max_queue
    return None

def not_explored_depth(ED, st):
    for item in ED[hashh(st)]:
        if item.room == st.room and item.location == st.location:
            return False
    return True

dls_nodes = 0
max_stack = 0

def depth_limited_search(ED, state, limit):
    global dls_nodes
    dls_nodes += 1
    global max_stack
    max_stack += 1
    if limit < 0:
        #print("limit reached")
        return None
    if goal_test(state):
        return state
    ED[hashh(state)].append(state)
    for y in range(5):
        future_state = next_state(state,actions[y])
        if not_explored_depth(ED, future_state):
            #print(future_state.path)
            result = depth_limited_search(ED, future_state, limit-1)
            if result != None:
                return result       
    return None

def iterative_deepening_search(st):
    print("Performing iterative deepening search")
    t3 = time.time()
    depth = 0
    while True:
        global max_stack
        max_stack = 0
        ED = [[] for _ in range(100007)]
        depth += 1
        #print(f"Trying depth = {depth}")
        temp_st = state(st.room, st.location, st.cost, st.path)
        result = depth_limited_search(ED, temp_st, depth)
        if result != None:
            t4 = time.time()
            print(f"R6: Number of nodes generated = {dls_nodes}")
            print(f"R7: Size of a node = {node_size(result)} bytes")
            print(f"R8: Max size of auxillary stack = {max_stack}")
            print(f"G2: Action Path = {result.path}")
            print(f"R9: Total Cost = {result.cost}")
            print(f"R10: Total time taken = {round(t4-t3,2)} seconds")
            return result       

if __name__ == "__main__":
    st = state(dirt_generator(dp),(0,0),0,'')
    print_state(st)
    stt1 = breadth_first_search(st)
    stt2 = iterative_deepening_search(st)
