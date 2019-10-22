#################################################################
#########                                               #########
#########               SATVIK GOLECHHA                 #########
#########               2017A7PS0117P                   #########
#########                                               #########
#################################################################


# inbuilt library imports
from tkinter import *
from tkinter import messagebox
import math
import random
import time
import copy

class ColumnFullException(Exception):
    '''
        - dummy exception class
        - to display a messagebox when human clicks on full column
        - exception handling used as a construct
    '''
    pass

class state:
    '''
    - state of the board instantiates this class
    - contains:
        - matrix of cells:
            - 0 for unfilled
            - 1 for machine (green)
            - 2 for human (blue)
        - terminal test function
        - turn = boolean value to tell turn:
            - True for machine
            - False for human
        - utility value for the state (scalar)
        - show displays the board using gui
    '''

    def __init__(self, board=[]):
        # to create a state, takes a matrix as an input
        self.board = copy.deepcopy(board)

    def start(self):
        # sets the board to an empty state
        self.board = []
        for _ in range(4):
            self.board.append([0,0,0,0])

    def terminal_test(self):
        # tests whether the game has ended, and returns a utility based on the winner
        b = self.board
        # for both players (t=1,2 denote the machine and human)
        for t in [1,2]:

            # for each row - horizontal patterns
            for r in range(4):
                if (b[r][0]==t and b[r][1]==t and b[r][2]==t):
                    return True, int(2*(1.5-t))
                elif (b[r][3]==t and b[r][1]==t and b[r][2]==t):
                    return True, int(2*(1.5-t))
            
            # for each column - vertical patterns
            for c in range(4):
                if (b[0][c]==t and b[1][c]==t and b[2][c]==t):
                    return True, int(2*(1.5-t))
                elif (b[1][c]==t and b[2][c]==t and b[3][c]==t):
                    return True, int(2*(1.5-t))

            # main diagonal
            if b[0][1]==t and b[1][2]==t and b[2][3]==t:
                return True, int(2*(1.5-t))
            elif b[0][0]==t and b[1][1]==t and b[2][2]==t:
                return True, int(2*(1.5-t))
            elif b[1][1]==t and b[2][2]==t and b[3][3]==t:
                return True, int(2*(1.5-t))
            elif b[1][0]==t and b[2][1]==t and b[3][2]==t:
                return True, int(2*(1.5-t))
     
            # other diagonal
            if b[2][0]==t and b[1][1]==t and b[0][2]==t:
                return True, int(2*(1.5-t))
            elif b[3][0]==t and b[2][1]==t and b[1][2]==t:
                return True, int(2*(1.5-t))
            elif b[2][1]==t and b[1][2]==t and b[0][3]==t:
                return True, int(2*(1.5-t))
            elif b[3][1]==t and b[2][2]==t and b[1][3]==t:
                return True, int(2*(1.5-t))

        # to check if the game terminates in a draw
        flag = 0
        for c in range(4):
            if b[3][c] == 0:
                flag = 1    

        if flag==0:
            return True, 0

        return False, None

    def show(self, frame, images):
        # to show the game on the GUI using tkinter
        # every state can be shown using st.show()
        for i in range(4):
            j = 0
            b = Button(frame, command = lambda: human_c1(), image=images[(self.board[i][j]-1) % 3]).grid(row=i, column=j)
            j = 1
            b = Button(frame, command = lambda: human_c2(), image=images[(self.board[i][j]-1) % 3]).grid(row=i, column=j)
            j = 2
            b = Button(frame, command = lambda: human_c3(), image=images[(self.board[i][j]-1) % 3]).grid(row=i, column=j)
            j = 3
            b = Button(frame, command = lambda: human_c4(), image=images[(self.board[i][j]-1) % 3]).grid(row=i, column=j)

    def actions(self):
    # should return all possible actions from the current state
    # that is, a list of numbers denoting possible action values
    # action values as defined in next-state
        acts = []
        b = self.board
        for col in range(4):
            if b[3][col]==0:
                acts.append(col)
        return acts

def next_state(st, action, turn):
    '''
    - takes as input:
        - a state (class instance)
        - and an action (a number from {0,1,2,3} to denote the column),
            - since row is decided automatically by game rules
        - and the turn (True for machine, False for human)
    - returns a new state, with action performed
    '''

    new = state(st.board)

    # if human tries a column which is already filled, raise ex
    if turn == False and new.board[3][action] != 0:
        raise ColumnFullException

    else:
        tag = 1 if turn else 2
        flag = 1
        index = -1
        while flag != 0:
            index += 1
            flag = new.board[index][action]
        new.board[index][action] = tag
    return new

def load_images():
    '''
    - helper function to load images
    '''
    green = PhotoImage(file = "green_blob.png")
    blue = PhotoImage(file = "blue_blob.png")
    white = PhotoImage(file = "white_blob.png")
    baseline = PhotoImage(file = "base_line.png")
    return [green, blue, white, baseline]

def minimax(st, turn):
    '''
    - Minimax Algorithm
    - Input: a state, and the turn
    - Output: the best action in the current state and corresponding utility
    - Recursively calls minimax() on each child.
    '''
#    global R1
#   R1 += 1
    global bottom_frame, imgs
    if st.terminal_test()[0]:
        return st.terminal_test()[1], None
    best = -math.inf if turn else math.inf
    for a in st.actions():
        t = next_state(st, a, turn)
        ut, ac = minimax(t, not turn)
        if (turn) and (ut > best):
            best = ut
            act = a
        elif (not turn) and (ut < best):
            best = ut
            act = a
    return best, act

def alpha_beta(st, alpha, beta, turn):
    '''
    - Alpha Beta Pruning Algorithm
    - Input: a state, the alpha and beta values, and the turn
    - Output: the best action in the current state and corresponding utility
    - Recursively calls alpha_beta() on each child.
    '''
#    global R6
#    R6 += 1
    global bottom_frame, imgs
    if st.terminal_test()[0]:
        return st.terminal_test()[1], None
    best = - math.inf if turn else math.inf
    for a in st.actions():
        t = next_state(st, a, turn)
        ut, ac = alpha_beta(t, alpha, beta, not turn)
        if (turn) and (ut > best):
            best = ut
            act = a
            alpha = max(alpha, best)
            if alpha > beta:
                break
        elif (not turn) and (ut < best):
            best = ut
            act = a
            beta = min(beta, best)
            if alpha > beta:
                break
    return best, act

def minimax_move():
    '''
    - Next move function for minimax algorithm
    - calls minimax() on a global state, 
    - gets the best move from minimax() and performs the move
    - on the current state, and then checks if the game is over.
    - if it is, displays a messagebox and exits the game
    '''
    global st, bottom_frame, imgs, l, chance
    if chance == False:
        messagebox.showinfo("Out of Chance", "Please make a human move.")
        return
    if chance == None:
        chance = False
    else:
        chance = not chance
    ut, act = minimax(st, True)
    #print(R1)
    st = next_state(st, act, True)
    st.show(bottom_frame, imgs)
    if st.terminal_test()[0]:
        uti = st.terminal_test()[1]
        if uti == 1:
            messagebox.showinfo("Game Over", "You Lost!")
        elif uti == 0:
            messagebox.showinfo("Game Over", "It was a draw!")
        elif uti == -1:
            messagebox.showinfo("Game Over", "You Won!!")
        sys.exit()

def alpha_beta_prune_move():
    '''
    - Next move function for alpha-beta pruning
    - calls alpha-beta() on a global state, 
    - gets the best move from alpha-beta() and performs the move
    - on the current state, and then checks if the game is over.
    - if it is, displays a messagebox and exits the game
    '''
    global st, bottom_frame, imgs, l
    global chance
    if chance == False:
        messagebox.showinfo("Out of Chance", "Please make a human move.")
        return
    if chance == None:
        chance = False
    else:
        chance = not chance
    ut, act = alpha_beta(st, -math.inf, math.inf, True)
    #print(R6)
    st = next_state(st, act, True)
    st.show(bottom_frame, imgs)
    if st.terminal_test()[0]:
        uti = st.terminal_test()[1]
        if uti == 1:
            messagebox.showinfo("Game Over", "You Lost!")
        elif uti == 0:
            messagebox.showinfo("Game Over", "It was a draw!")
        elif uti == -1:
            messagebox.showinfo("Game Over", "You Won!!")
        sys.exit()

def human_c1():
    global chance
    if chance == True:
        messagebox.showinfo("Out of Chance", "Please allow machine to move.")
        return
    try:
        global st, bottom_frame, imgs, l
        st = next_state(st, 0, False)
        st.show(bottom_frame, imgs)
    except ColumnFullException as e:
        messagebox.showinfo("Column Full", "Please try another column.")
        return
    if chance == None:
        chance = True
    else:
        chance = not chance
    if st.terminal_test()[0]:
        uti = st.terminal_test()[1]
        if uti == 1:
            messagebox.showinfo("Game Over", "You Lost!")
        elif uti == 0:
            messagebox.showinfo("Game Over", "It was a draw!")
        elif uti == -1:
            messagebox.showinfo("Game Over", "You Won!!")
        sys.exit()

def human_c2():
    global chance
    if chance == True:
        messagebox.showinfo("Out of Chance", "Please allow machine to move.")
        return
    try:
        global st, bottom_frame, imgs, l
        st = next_state(st, 1, False)
        st.show(bottom_frame, imgs)
    except ColumnFullException as e:
        messagebox.showinfo("Column Full", "Please try another column.")
        return
    if chance == None:
        chance = True
    else:
        chance = not chance
    if st.terminal_test()[0]:
        uti = st.terminal_test()[1]
        if uti == 1:
            messagebox.showinfo("Game Over", "You Lost!")
        elif uti == 0:
            messagebox.showinfo("Game Over", "It was a draw!")
        elif uti == -1:
            messagebox.showinfo("Game Over", "You Won!!")
        sys.exit()

def human_c3():
    global chance
    if chance == True:
        messagebox.showinfo("Out of Chance", "Please allow machine to move.")
        return
    try:
        global st, bottom_frame, imgs, l
        st = next_state(st, 2, False)
        st.show(bottom_frame, imgs)
    except ColumnFullException as e:
        messagebox.showinfo("Column Full", "Please try another column.")
        return
    if chance == None:
        chance = True
    else:
        chance = not chance
    if st.terminal_test()[0]:
        uti = st.terminal_test()[1]
        if uti == 1:
            messagebox.showinfo("Game Over", "You Lost!")
        elif uti == 0:
            messagebox.showinfo("Game Over", "It was a draw!")
        elif uti == -1:
            messagebox.showinfo("Game Over", "You Won!!")
        sys.exit()

def human_c4():
    global chance
    if chance == True:
        messagebox.showinfo("Out of Chance", "Please allow machine to move.")
        return
    try:
        global st, bottom_frame, imgs, l
        st = next_state(st, 3, False)
        st.show(bottom_frame, imgs)
    except ColumnFullException as e:
        messagebox.showinfo("Column Full", "Please try another column.")
        return
    if chance == None:
        chance = True
    else:
        chance = not chance
    if st.terminal_test()[0]:
        uti = st.terminal_test()[1]
        if uti == 1:
            messagebox.showinfo("Game Over", "You Lost!")
        elif uti == 0:
            messagebox.showinfo("Game Over", "It was a draw!")
        elif uti == -1:
            messagebox.showinfo("Game Over", "You Won!!")
        sys.exit()


def show_values():
    '''
    - display the pre-computer R values as defined in the assignment
    '''
    messagebox.showinfo("Precomputed R Values", "R1 = 6761217\n R2 = 104 bytes + object metadata\n R3 = 26.9 MB\n R4 = 250 seconds\n R5 = 30721 \n R6 = 1571529\n R7 = 0.7675375602\n R8 = 82 seconds\n R9 = Alpha-Beta pruning takes slightly more memory (28.4 MB)\n R10 = 246 seconds\n R11 = 10 (if M plays first)\n R12 = 20 (if M plays first)\n R4 >> R8")

if __name__ == "__main__":

    # global variables to calculate R1 to R12
#    R1 = 0
#    R6 = 0
    # human will decide who will take the first chance 
    chance = None

    # setting up the global state
    st = state()
    st.start()

    # setting up the tkinter gui window and the top and bottom frames
    w = Tk()
    w.title("align3")
    imgs = load_images()
    top_frame = Frame(w)
    top_frame.pack(side=TOP)
    bottom_frame = Frame(w)
    bottom_frame.pack(side=TOP)

    # setting up labels and buttons for human moves
    b = Button(top_frame,text="Precomputed Values", command = lambda: show_values(), bg="red", fg="black")
    b.pack(side=TOP)
    b = Button(top_frame,text="αβ-Pruning Move", command = lambda: alpha_beta_prune_move(), bg="orange", fg="blue")
    b.pack(side=TOP)
    b0 = Button(top_frame,text="Minimax Move", command = lambda: minimax_move(), bg="orange", fg="red")
    b0.pack(side=TOP)
    bbase = Label(top_frame, image=imgs[3])
    bbase.pack(side=TOP)
    # displaying the initial game board
    st.show(bottom_frame, imgs)

    # initiate tkinter gui
    w.mainloop()




# PRECOMPUTED VALUES:
#   R1 = 6761217
#   R2 = 104 bytes + object metadata
#   R3 = 26.9 MB
#   R4 = 250 seconds
#   R5 = 30721 
#   R6 = 1571529
#   R7 = 0.7675375602
#   R8 = 82 seconds
#   R9 = Alpha-Beta pruning takes slightly more memory (28.4 MB)
#   R10 = 246 seconds
#   R11 = 10 (if M plays first)
#   R12 = 20 (if M plays first)
#   R4 >> R8