
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        if self.currentState.state == self.victoryCondition:
            return True

        self.visited[self.currentState] = True
        if self.gm.getMovables():
            i = 0
            while i < len(self.gm.getMovables()):
                movable = self.gm.getMovables()[i]
                self.gm.makeMove(movable)
                self.currentState.children.append(GameState(self.gm.getGameState(), self.currentState.depth+1, movable))
                self.currentState.children[len(self.currentState.children)-1].parent = self.currentState
                self.gm.reverseMove(movable)
                i = i+1
            for child in self.currentState.children:
                if child not in self.visited.keys() or not self.visited[child]:
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child
                    return False
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return False
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    q = []
    tbc = 0

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        if self.currentState.state == self.victoryCondition:
            self.q.clear()
            self.tbc = 0
            return True

        if self.currentState.depth == 0:
            self.q.append(self.currentState)
        if self.gm.getMovables():
            i = 0
            while i < len(self.gm.getMovables()):
                movable = self.gm.getMovables()[i]
                self.gm.makeMove(movable)
                newGameState = GameState(self.gm.getGameState(), self.currentState.depth + 1, movable)
                isNewState = True
                for a_state in self.q:
                    if a_state == newGameState:
                        isNewState = False
                        break
                if isNewState:
                    self.q.append(GameState(self.gm.getGameState(), self.currentState.depth + 1, movable))
                    self.q[len(self.q) - 1].parent = self.currentState
                self.gm.reverseMove(movable)
                i = i + 1
        self.tbc = self.tbc + 1
        while not self.currentState == self.q[0]:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
        if self.tbc < len(self.q):
            pathM = []
            pathS = []
            endState = self.q[self.tbc]
            pathS.append(endState)
            pathM.append(endState.requiredMovable)
            while not endState == self.q[0]:
                endState = endState.parent
                pathS.append(endState)
                pathM.append(endState.requiredMovable)
            pathS.reverse()
            pathM.reverse()
            i = 1
            while not self.currentState == self.q[self.tbc]:
                self.gm.makeMove(pathM[i])
                self.currentState = pathS[i]
                i = i+1
            return False
