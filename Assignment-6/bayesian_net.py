###########################################################################
###########                                                     ###########
###########                 AI Assignment-6                     ###########
###########                 Satvik Golechha                     ###########
###########                 2017A7PS0117P                       ###########
###########                                                     ###########
###########################################################################

# import inbuilt python libraries
from typing import List, Dict, Tuple
from tkinter import *
from tkinter import messagebox

# input file
INPUT_FILE = 'input1.txt'

def driver(nn, q,c, w):
    '''
        - driver method to answer to the query asked
        - calls class method "ask" on the bayesian network "nn"
        - driver is run through the GUI commands
    '''
    t1 = []
    t2 = []
    for v in range(nn.variables.__len__()):
        if q[v].get()==1:
            t1.append(list(nn.variables.keys())[v])
        elif q[v].get()==-1:
            t1.append('~'+list(nn.variables.keys())[v])
        if c[v].get()==1:
            t1.append(list(nn.variables.keys())[v])
        elif c[v].get()==-1:
            t1.append('~'+list(nn.variables.keys())[v])
    b1 = Label(w,text=nn.ask((t1,t2)), bg="white")
    b1.place(x= 150, y = 600 , width=200, height=25)

def exit_a():
    exit(0)

class node(object):
    '''
        - node of the bayesian network
        - holds information about the 
            - name
            - root or not
            - parents
            - children
            - conditional probability tables
        - for each node
        - call is used as a construct to create the node
        - add_child and show are helper functions
    '''

    def __init__(self) -> None:
        self.name: str = None
        self.root: bool = False
        self.parents: List[str] = []
        self.children: List[str] = []
        self.CPT: List[float] = []
    
    def __call__(self, line: str) -> None:
        # convert G >> [O] >> 0.001 0.42 to self.parents and self.CPT
        # order is important
        self.name = line[0]
        self.parents = list(_ for _ in str(line[6:].split(sep=']')[0]).replace(', ', ''))
        if self.parents.__len__():
            self.CPT = [float(n) for n in line.split()[::-1][:2**self.parents.__len__()][::-1]]
        else:
            self.root = True
            self.CPT = [float(line[11:])]
        
    def add_child(self, child: str) -> None:
        self.children.append(child)

    def show(self) -> None:
        print(f'{self.name}, parents {self.parents}, children {self.children}')
        if self.root:
            print("root node")


class BN(object):
    '''
        - the bayesian network class
        - contains all the variables of the network.
        - their stochastic dependancy is set through the node class
        - create sets the net up by creating nodes
        - ask, probability, and direct check are functions to calculate probability
        - show displays the variables using the GUI
    '''

    def __init__(self) -> None:
        self.variables: Dict[str, node] = {}

    def create(self, filename: str) -> None:
        with open(filename, mode='r') as f:
            for line in f:
                if '$$' not in line:
                    self.variables[line[0]] = node()
                    self.variables[line[0]](line)
                    # Soft Assumption: Variables during input have single letter names
        #print(self.variables.keys())
        for key in self.variables.keys():
            #print(key)
            for parent in self.variables[key].parents:
                self.variables[parent].add_child(key)

    def ask(self, query: Tuple[List[str], List[str]]) -> float:
        return self.probability(query[0]+query[1]) / self.probability(query[1])    # bayes theorem
    
    def probability(self, joint: List[str]) -> float:
        frac: float = 1.00
        abs_joint: List[str] = [j[-1] for j in joint] 
        for j in range(joint.__len__()):
            conds: List[str] = []
            for i in range(joint.__len__()):
                if abs_joint[i] in self.variables[joint[j][-1]].parents:
                    conds.append(joint[i])
            #print(f'{joint[j]}: {conds}')
            frac *= self.direct_check(joint[j], conds)
        #print(f'{joint}: {frac}')
        return frac

    def direct_check(self, variable: str, conditions: List[str]) -> float:
        # recursive method
        if self.variables[variable[-1]].parents.__len__() == conditions.__len__():
            # recursion breaks
            if self.variables[variable[-1]].root:
                # root reached
                #print(self.variables[variable[-1]].CPT)
                rootp: float = self.variables[variable[-1]].CPT[0]
                return rootp if variable==variable[-1] else 1-rootp
            else:
                # all parents exi..
                binary_index: str = ''
                for p in self.variables[variable[-1]].parents:
                    # order is important because of this 
                    binary_index += ('1' if p in conditions else '0')
                index: int = int(binary_index, 2)
                prob: float = self.variables[variable[-1]].CPT[index]
                return prob if variable==variable[-1] else 1-prob

        else:
            # recursive enumeration
            for p in self.variables[variable[-1]].parents:
                if p not in [u[-1] for u in conditions]:
                    return self.direct_check(variable, conditions+[p])*self.direct_check(p, []) + self.direct_check(variable, conditions+['~'+p])*self.direct_check('~'+p, [])


    def show(self, w) -> None:
        b1 = Label(w,text="Query Variables", bg="SteelBlue3")
        b1.place(x= 10, y = 30 , width=200, height=25)
        b2 = Label(w,text="Condition Variables", bg="SteelBlue3")
        b2.place(x = 280, y = 30, width=200, height=25)

        #global queries, conditionals

        queries = []
        conditionals = []
        for v in range(nn.variables.__len__()):
            tempq = IntVar()
            tempc = IntVar()
            queries.append(tempq)
            conditionals.append(tempc)

        for v in range(self.variables.__len__()):
            r1 = Radiobutton(w, bg='DarkOliveGreen3', activebackground='gold', text=list(self.variables.keys())[v],indicatoron = 0,width = 20,padx = 20, variable=queries[v], command=temp,value=1)
            r2 = Radiobutton(w, bg='DarkOliveGreen3', activebackground='gold', text='~'+list(self.variables.keys())[v],indicatoron = 0,width = 20,padx = 20, variable=queries[v], command=temp,value=-1)
            r3 = Radiobutton(w, bg='DarkOliveGreen3', activebackground='gold', text=list(self.variables.keys())[v],indicatoron = 0,width = 20,padx = 20, variable=conditionals[v], command=temp,value=1)
            r4 = Radiobutton(w, bg='DarkOliveGreen3', activebackground='gold', text='~'+list(self.variables.keys())[v],indicatoron = 0,width = 20,padx = 20, variable=conditionals[v], command=temp,value=-1)
            r1.place(x= 10, y = 90 + 30*v , width=70, height=25)
            r2.place(x= 80, y = 90 + 30*v, width=70, height=25)
            r3.place(x= 280, y = 90 + 30*v, width=70, height=25)
            r4.place(x= 350, y = 90 + 30*v, width=70, height=25)
        
        b3 = Button(w,text="Answer Query", bg="DarkOliveGreen3", command=lambda: driver(self, queries, conditionals, w))
        b3.place(x = 150, y = 650, width=200, height=25)
        b4 = Button(w,text="Reset", bg="DarkOliveGreen3", command=lambda: self.show(w))
        b4.place(x = 150, y = 700, width=200, height=25)
        b5 = Button(w,text="Exit", bg="DarkOliveGreen3", command=exit_a)
        b5.place(x = 150, y = 750, width=200, height=25)

        #for t in queries:
        #    print(t.get())
             

def temp():
    pass

def markov_blanket(net: BN, node: str) -> List[str]:
    # returns the markov blanket of any node of a BN, which has:
    mb: List[str] = []
    # its parents
    for parent in net.variables[node].parents:
        if parent not in mb:
            mb.append(parent)
    # its children
    for child in net.variables[node].children:
        if child not in mb:
            mb.append(child)
    # its children's parents
    for child in net.variables[node].children:
        for cp in net.variables[child].parents:
            if cp not in mb:
                mb.append(cp)
    return mb

def normalize(distribution: List[float]) -> List[float]:
    '''
        - to normalize any given probablity distribution
        - not used in this implementation
    '''
    s: float = sum(distribution)
    return distribution if s==0.0 else map(lambda z: z/s, distribution)

# create the bayesian network
nn = BN()
# fill it with data (from input file as defined at the top)
nn.create(INPUT_FILE)

# create the GUI window
w = Tk()
w.title('Bayesian Network')
w.geometry("500x3000+30+30")
nn.show(w)
w.mainloop()