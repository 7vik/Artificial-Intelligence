###########################################################################
###########                                                     ###########
###########                 AI Assignment-5                     ###########
###########                 Satvik Golechha                     ###########
###########                 2017A7PS0117P                       ###########
###########                                                     ###########
###########################################################################


class KB:
    def __init__(self):
        self.sentences = []
    
    def add(self, expr):
        self.sentences.append(expr)
        self.sentences.sort()

    
if __name__ == "__main__":
    kb1 = KB()
    kb1.add("human(Marcus)")
    print(kb1.sentences)