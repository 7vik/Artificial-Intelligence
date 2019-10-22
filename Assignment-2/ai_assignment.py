########################################
########    Satvik Golechha     ########
########    2017A7PS0117P       ########
########################################

import random
import copy
import sys
import math
from tkinter import *
from tkinter import messagebox

# creating the GUI window
w = Tk()

# setting up the war-field: these values should be changed for different configurations
ro,co = 7, 7
war_field = [[0 for c in range(co)] for r in range(ro)]
mines = 9

class MinesFoundMessage(Exception):
    '''
        - dummy exception class
        - to display the messagebox when all mines are found
        - exception handling used as a construct
    '''
    pass

def best_move(st):
    '''
        - Input: a state 'st'
        - Output: best next state for hill climbing
        - Algorithm: Check all possible actions, and return the one with the maximum heuristic
        - if no best move, raises the exception
    '''

    max_t = 0
    flag = 0
    for r in range(ro):
        for c in range(co):
            t_st = state(st.vf)
            t = next_state(t_st, r, c).h() - st.h()
            if t > max_t:
                flag = 1
                max_t = t
                r_max, c_max = r, c 
    if flag:
        return r_max, c_max
    else:
        raise MinesFoundMessage

def next_state(new_st,r,c):
    '''
        - Input: state (contains visible_field, no of mines, h1, h2) and r,c to click
        - Returns: new state with click on cell
        - Algorithm for observation:
        ************** WRONG IMPLEMENTATION (GIVES CONCAVE AREAS TOO) ********************
    '''
    global wf

        # if it's out of bounds, do nothing and return
    if r < 0 or r == ro or c < 0 or c == co:
        return new_st

    else:
        # if clicked on observed, do nothing and return 
        if new_st.vf[r][c] != -1:
            return new_st
        
        # clicked on unobserved
        else:

            # if it's a mine, open it and explode the mine and return: local minimum reached
            if wf[r][c] == 9:
                return new_st

            # if it's a number, open it and return
            elif wf[r][c] != 0:
                new_st.vf[r][c] = wf[r][c]
                return new_st

            # if it's an empty cell, open it and recursively call click on TBLR cells
            else:
                new_st.vf[r][c] = 0
                next_state(new_st, r+1,c)
                next_state(new_st, r-1,c)
                next_state(new_st, r,c+1)
                next_state(new_st, r,c-1)
                #next_state(new_st, r+1,c+1)
                next_state(new_st, r-1,c-1)
                #next_state(new_st, r-1,c+1)
                next_state(new_st, r+1,c-1)
    return new_st


def hill_climbing():
    ''' 
        - The Hill Climbing Search Algorithm
        - Runs each time Hill Climbing is clicked on the GUI
        - calls best_move and next_state
    '''
    try:
        global new, f
        r,c = best_move(new)
        new = next_state(new,r,c)
        new.show()
    except MinesFoundMessage as e:
        messagebox.showinfo("All Mines Found", "Local or Global Optimum Reached!")
        sys.exit()


def load_images():
    ''' 
        - helper function to load images
    '''
    mine = PhotoImage(file = "mine.png")
    flag = PhotoImage(file = "flag.png")
    hidden = PhotoImage(file = "closed.png")
    zero = PhotoImage(file = "0.png")
    one = PhotoImage(file = "1.png")
    two = PhotoImage(file = "2.png")
    three = PhotoImage(file = "3.png")
    four = PhotoImage(file = "4.png")
    five = PhotoImage(file = "5.png")
    six = PhotoImage(file = "6.png")
    seven = PhotoImage(file = "7.png")
    eight = PhotoImage(file = "8.png")

    return [zero, one, two, three, four, five, six, seven, eight, hidden]


def schedule(t):
    '''
        - stock schedule function
        - returns a temperature for simulated annealing
        - inputs iteration (time) t
        - can be changed to play around with SA
    '''
    return (10 - t) + 1/t 


def goal_test(st):
    '''
        - tests if number of mines has been found
        - to help simulated annealing not get stuck
        - returns true iff number of unopened == mines
    '''
    global mines
    mines_found = 0
    for r in range(ro):
        for c in range(co):
            if st.vf[r][c] == -1:
                mines_found += 1
    if mines_found == mines:
        raise MinesFoundMessage


def simulated_annealing(st, T):
    ''' 
        - inputs temperature and state
        - The Hill Climbing Search Algorithm
        - Runs each time Simulated Annealing is clicked on the GUI
    '''
    r, c = 0, 0
    while st.vf[r][c] != -1:
            r = random.randint(0,ro-1)
            c = random.randint(0,co-1)

    t_st = state(st.vf)
    delta_e = next_state(t_st,r,c).h() - st.h()
    p = random.random()
    sim = math.exp(delta_e/T)
    if delta_e > 0:
        new = next_state(st,r,c)
        new.show()    
    elif p < sim:
        new = next_state(st,r,c)
        new.show()
    goal_test(new)
    return new

# temperature / iteration for simulated annealing
temp = 0

def meta_sa():
    ''' 
        - support function to run simulated annealing
        - as actually called when clicked on GUI
        - handles the exception
    '''
    global new, temp
    try:
        temp += 1
        new = simulated_annealing(new, temp)
    except MinesFoundMessage as e:
        messagebox.showinfo("All Mines Found", "Local or Global Optimum Reached!")
        sys.exit()

# loading the images
images = load_images()


# setting up the two buttons for HC and SA and the frame
l1 = Label(w,text=f"Number of Mines = {mines}")
l1.pack()
b1 = Button(w,text="Hill Climbing", command=hill_climbing, bg="blue", fg="green")
b1.pack()
b2 = Button(w,text="Simulated Annealing", command=meta_sa, bg="red", fg="purple")
b2.pack()
f = Frame(w)
f.pack()

class state():
    '''
        - Class to instantiate each state
        - state is defined as a rows*columns-tuple which tells whether each cell is
                * unobserved = -1
                * observed empty = 0
                * observed radar = {1,2,3,4,5,6,7,8}
                * observed mine = value zero
        - h() gives a heuristic value for the state as a number
        - show() shows the state on the GUI
    '''

    def __init__(self, vf):
        self.vf = copy.deepcopy(vf)

    def h(self):
        '''
            - Heuristic Approximator #1 (default)
            - Algorithm:
                Returns the number of states currently opened
                does not use information of mines
                Admissible heuristic since it will never overestimate the path
                tie-breaking is done through left-to-right manner
        '''
        value = 0
        for r in range(ro):
            for c in range(co):
                if self.vf[r][c] != -1:
                    value += 1
        return value

    def h2(self):
        '''
            - Heuristic Approximator #2 (used when called through HC)
            - Algorithm:
                Returns the sum of number of states currently opened
                does not use information of mines
                Admissible heuristic since it will never overestimate the path
        '''
        value = 0
        for r in range(ro):
            for c in range(co):
                if self.vf[r][c] != -1:
                    value += self.vf[r][c]
        return value

    def show(self):
        global f
        for i in range(ro):
            for j in range(co):
                bn = Button(f, image=images[self.vf[i][j]]).grid(row=i+1, column=j)


def start_state(rows, columns):
    '''
        - input: number of rows and columns
        - output: state with matrix of given params filled with -1 (hidden)
    '''
    matrix = [[-1 for c in range(columns)] for r in range(rows)]
    return state(matrix)

# the start state
new = start_state(ro,co)

def view_field(wf):
    '''
        - Temporary method to view any warfield,
        - It's mines, the numbers, etc
        - to be replaced by GUI in the final version
    '''
    for row in wf:
        print(*row)


def fill_wf(wf, mines):
    '''
        - Input: A field 
        - adds mines randomly to a given empty warfield
        - Returns: A new field, with numbers from 0-8 denoting the number of surr. mines
    '''

    for i in range(mines):
        while True:
            row = random.randint(0, ro-1)
            col = random.randint(0, co-1)
            if wf[row][col] != 9:
                break
        wf[row][col] = 9

    for r in range(ro):
        for c in range(co):
            if wf[r][c] == 9:
                # left
                if c != 0:
                    if wf[r][c-1] != 9:
                        wf[r][c-1] += 1
                # right
                if c != co-1:
                    if wf[r][c+1] != 9:
                        wf[r][c+1] += 1
                # up
                if r != 0:
                    if wf[r-1][c] != 9:
                        wf[r-1][c] += 1
                # down
                if r != ro-1:
                    if wf[r+1][c] != 9:
                        wf[r+1][c] += 1
                # top-right
                if r!=0 and c!=co-1:
                    if wf[r-1][c+1] != 9:
                        wf[r-1][c+1] += 1
                # top-left
                if r!=0 and c!=0:
                    if wf[r-1][c-1] != 9:
                        wf[r-1][c-1] += 1
                # down-right
                if r!=ro-1 and c!=co-1:
                    if wf[r+1][c+1] != 9:
                        wf[r+1][c+1] += 1
                # down-left
                if r!=ro-1 and c != 0:
                    if wf[r+1][c-1] != 9:
                        wf[r+1][c-1] += 1

    return wf

# initiation calls
wf = fill_wf(war_field, mines)
#view_field(wf)
new.show()
w.mainloop()