from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        t1 = []
        t2 = []
        t3 = []
        p1 = self.kb.kb_ask(parse_input("fact: (on ?X peg1)"))
        if p1:
            for bindings in p1:
                for binding in bindings.bindings:
                    t1.append(binding.constant.element)
        p2 = self.kb.kb_ask(parse_input("fact: (on ?X peg2)"))
        if p2:
            for bindings in p2:
                for binding in bindings.bindings:
                    t2.append(binding.constant.element)
        p3 = self.kb.kb_ask(parse_input("fact: (on ?X peg3)"))
        if p3:
            for bindings in p3:
                for binding in bindings.bindings:
                    t3.append(binding.constant.element)
        gameState = [t1, t2, t3]

        index = 0
        while index < 3:
            L = len(gameState[index])
            ind = 0
            while ind < L:
                if gameState[index][ind] == 'disk1':
                    gameState[index][ind] = 1
                elif gameState[index][ind] == 'disk2':
                    gameState[index][ind] = 2
                elif gameState[index][ind] == 'disk3':
                    gameState[index][ind] = 3
                elif gameState[index][ind] == 'disk4':
                    gameState[index][ind] = 4
                elif gameState[index][ind] == 'disk5':
                    gameState[index][ind] = 5
                ind = ind+1
            index = index+1

        gameState[0].sort()
        gameState[1].sort()
        gameState[2].sort()
        tuple0 = tuple(gameState[0])
        tuple1 = tuple(gameState[1])
        tuple2 = tuple(gameState[2])
        gameStateT = (tuple0, tuple1, tuple2)
        return gameStateT

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        moved = str(movable_statement.terms[0])
        askthing = "fact: (onDisk " + moved + " ?X)"
        below = self.kb.kb_ask(parse_input(askthing))
        t1 = []
        if below:
            for bindings in below:
                for binding in bindings.bindings:
                    t1.append(binding.constant.element)
            oldState = ["onDisk", movable_statement.terms[0], t1[0]]
            f2 = Fact(Statement(oldState))
            self.kb.kb_retract(f2)
            newState = ["top", t1[0], movable_statement.terms[1]]
            f1 = Fact(Statement(newState))
            self.kb.kb_assert(f1)
        else:
            newState = ["empty", movable_statement.terms[1]]
            f1 = Fact(Statement(newState))
            self.kb.kb_assert(f1)

        oldState = ["on", movable_statement.terms[0], movable_statement.terms[1]]
        f2 = Fact(Statement(oldState))
        self.kb.kb_retract(f2)
        oldState = ["top", movable_statement.terms[0], movable_statement.terms[1]]
        f2 = Fact(Statement(oldState))
        self.kb.kb_retract(f2)
        oldState = ["empty", movable_statement.terms[2]]
        f2 = Fact(Statement(oldState))
        self.kb.kb_retract(f2)

        newpeg = str(movable_statement.terms[2])
        askthing = "fact: (top ?x " + newpeg + ")"
        below = self.kb.kb_ask(parse_input(askthing))
        t1 = []
        if below:
            for bindings in below:
                for binding in bindings.bindings:
                    t1.append(binding.constant.element)
            oldState = ["top", t1[0], movable_statement.terms[2]]
            f2 = Fact(Statement(oldState))
            self.kb.kb_retract(f2)
            newState = ["onDisk", movable_statement.terms[0], t1[0]]
            f1 = Fact(Statement(newState))
            self.kb.kb_assert(f1)

        newState = ["on", movable_statement.terms[0], movable_statement.terms[2]]
        f1 = Fact(Statement(newState))
        self.kb.kb_assert(f1)
        newState = ["top", movable_statement.terms[0], movable_statement.terms[2]]
        f1 = Fact(Statement(newState))
        self.kb.kb_assert(f1)

        self.getGameState()
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        rr1 = []
        rr2 = []
        rr3 = []
        cc1 = []
        cc2 = []
        cc3 = []
        r1 = self.kb.kb_ask(parse_input("fact: (Y ?w pos1)"))
        if r1:
            for bindings in r1:
                for binding in bindings.bindings:
                    rr1.append(binding.constant.element)
        r2 = self.kb.kb_ask(parse_input("fact: (Y ?w pos2)"))
        if r2:
            for bindings in r2:
                for binding in bindings.bindings:
                    rr2.append(binding.constant.element)
        r3 = self.kb.kb_ask(parse_input("fact: (Y ?w pos3)"))
        if r3:
            for bindings in r3:
                for binding in bindings.bindings:
                    rr3.append(binding.constant.element)
        c1 = self.kb.kb_ask(parse_input("fact: (X ?w pos1)"))
        if c1:
            for bindings in c1:
                for binding in bindings.bindings:
                    cc1.append(binding.constant.element)
        c2 = self.kb.kb_ask(parse_input("fact: (X ?w pos2)"))
        if c2:
            for bindings in c2:
                for binding in bindings.bindings:
                    cc2.append(binding.constant.element)
        c3 = self.kb.kb_ask(parse_input("fact: (X ?w pos3)"))
        if c3:
            for bindings in c3:
                for binding in bindings.bindings:
                    cc3.append(binding.constant.element)

        row1 = []
        row2 = []
        row3 = []
        stoploop = False
        index = 0
        while index < 3:
            ind = 0
            while ind < 3:
                if rr1[index] == cc1[ind]:
                    row1.append(rr1[index])
                    stoploop = True
                    break
                ind = ind + 1
            if stoploop:
                break
            index = index + 1
        stoploop = False
        index = 0
        while index < 3:
            ind = 0
            while ind < 3:
                if rr1[index] == cc2[ind]:
                    row1.append(rr1[index])
                    stoploop = True
                    break
                ind = ind + 1
            if stoploop:
                break
            index = index + 1
        stoploop = False
        index = 0
        while index < 3:
            ind = 0
            while ind < 3:
                if rr1[index] == cc3[ind]:
                    row1.append(rr1[index])
                    stoploop = True
                    break
                ind = ind + 1
            if stoploop:
                break
            index = index + 1
        stoploop = False
        index = 0
        while index < 3:
            ind = 0
            while ind < 3:
                if rr2[index] == cc1[ind]:
                    row2.append(rr2[index])
                    stoploop = True
                    break
                ind = ind + 1
            if stoploop:
                break
            index = index + 1
        stoploop = False
        index = 0
        while index < 3:
            ind = 0
            while ind < 3:
                if rr2[index] == cc2[ind]:
                    row2.append(rr2[index])
                    stoploop = True
                    break
                ind = ind + 1
            if stoploop:
                break
            index = index + 1
        stoploop = False
        index = 0
        while index < 3:
            ind = 0
            while ind < 3:
                if rr2[index] == cc3[ind]:
                    row2.append(rr2[index])
                    stoploop = True
                    break
                ind = ind + 1
            if stoploop:
                break
            index = index + 1
        stoploop = False
        index = 0
        while index < 3:
            ind = 0
            while ind < 3:
                if rr3[index] == cc1[ind]:
                    row3.append(rr3[index])
                    stoploop = True
                    break
                ind = ind + 1
            if stoploop:
                break
            index = index + 1
        stoploop = False
        index = 0
        while index < 3:
            ind = 0
            while ind < 3:
                if rr3[index] == cc2[ind]:
                    row3.append(rr3[index])
                    stoploop = True
                    break
                ind = ind + 1
            if stoploop:
                break
            index = index + 1
        stoploop = False
        index = 0
        while index < 3:
            ind = 0
            while ind < 3:
                if rr3[index] == cc3[ind]:
                    row3.append(rr3[index])
                    stoploop = True
                    break
                ind = ind + 1
            if stoploop:
                break
            index = index + 1

        gameState = [row1, row2, row3]
        index = 0
        while index < 3:
            ind = 0
            while ind < 3:
                if gameState[index][ind] == 'tile1':
                    gameState[index][ind] = 1
                elif gameState[index][ind] == 'tile2':
                    gameState[index][ind] = 2
                elif gameState[index][ind] == 'tile3':
                    gameState[index][ind] = 3
                elif gameState[index][ind] == 'tile4':
                    gameState[index][ind] = 4
                elif gameState[index][ind] == 'tile5':
                    gameState[index][ind] = 5
                elif gameState[index][ind] == 'tile6':
                    gameState[index][ind] = 6
                elif gameState[index][ind] == 'tile7':
                    gameState[index][ind] = 7
                elif gameState[index][ind] == 'tile8':
                    gameState[index][ind] = 8
                elif gameState[index][ind] == 'empty':
                    gameState[index][ind] = -1
                ind = ind + 1
            index = index + 1

        tuple0 = tuple(gameState[0])
        tuple1 = tuple(gameState[1])
        tuple2 = tuple(gameState[2])
        gameStateT = (tuple0, tuple1, tuple2)
        return gameStateT


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        emptyConstant = Constant('empty')
        emptyTerm = Term(emptyConstant)

        if movable_statement.terms[1].term.element != movable_statement.terms[3].term.element:
            oldStateX = ["X", movable_statement.terms[0], movable_statement.terms[1]]
            ffX = Fact(Statement(oldStateX))
            self.kb.kb_retract(ffX)
        if movable_statement.terms[2].term.element != movable_statement.terms[4].term.element:
            oldStateY = ["Y", movable_statement.terms[0], movable_statement.terms[2]]
            ffY = Fact(Statement(oldStateY))
            self.kb.kb_retract(ffY)
        if movable_statement.terms[1].term.element != movable_statement.terms[3].term.element:
            oldStateX = ["X", emptyTerm, movable_statement.terms[3]]
            ffX = Fact(Statement(oldStateX))
            self.kb.kb_retract(ffX)
        if movable_statement.terms[2].term.element != movable_statement.terms[4].term.element:
            oldStateY = ["Y", emptyTerm, movable_statement.terms[4]]
            ffY = Fact(Statement(oldStateY))
            self.kb.kb_retract(ffY)

        if movable_statement.terms[1].term.element != movable_statement.terms[3].term.element:
            newStateX = ["X", movable_statement.terms[0], movable_statement.terms[3]]
            fX = Fact(Statement(newStateX))
            self.kb.kb_assert(fX)
        if movable_statement.terms[2].term.element != movable_statement.terms[4].term.element:
            newStateY = ["Y", movable_statement.terms[0], movable_statement.terms[4]]
            fY = Fact(Statement(newStateY))
            self.kb.kb_assert(fY)
        if movable_statement.terms[1].term.element != movable_statement.terms[3].term.element:
            newStateX = ["X", emptyTerm, movable_statement.terms[1]]
            fX = Fact(Statement(newStateX))
            self.kb.kb_assert(fX)
        if movable_statement.terms[2].term.element != movable_statement.terms[4].term.element:
            newStateY = ["Y", emptyTerm, movable_statement.terms[2]]
            fY = Fact(Statement(newStateY))
            self.kb.kb_assert(fY)

        self.getGameState()
        pass


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
