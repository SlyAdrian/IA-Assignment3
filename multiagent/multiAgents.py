# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import Queue, manhattanDistance
from game import Directions
import random, util

from game import Agentº

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """

        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class Node :
    def __init__(self, depth = 0, parent = 0, value = None, moove = None, gameState = None, children = []):
        self.value = value
        self.depth = depth
        self.parent = parent
        self.moove = moove
        self.gameState = gameState
        self.children = children

    def set_value(self, value):
        self.value = value

    def set_gameState(self, gameState):
        self.gameState = gameState

    def set_moove(self, moove):
        self.moove = moove

    def set_children(self, children):
        self.children = children

    def set_parent(self, parent):
        self.parent = parent

    def get_value(self):
        return self.value



class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """



    def evaluationFunction(self, currentGameState, action): 

            # Useful information you can extract from a GameState (pacman.py)
            successorGameState = currentGameState.generatePacmanSuccessor(action)
            newPos = successorGameState.getPacmanPosition()
            newFood = successorGameState.getFood() ## Boolean grid
            newGhostStates = successorGameState.getGhostStates()
            newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] # Grid with the remaining moves being scared for the ghosts
            
            return successorGameState.getScore()
    
    
    def getAction(self, gameState):
        
        depth = 5

        index = depth % gameState.getNumAgents()

        queue = Queue()

        # !TODO : Work in progress name
        otherQueue = Queue()

        queue.push(Node(depth=0, gameState= gameState))

        for i in range (depth) :

            element = queue.pop()

            # Collect legal moves from the element removed from the queue
            legalPacManMoves = element.gameState.getLegalActions(0)
            
            for e in legalPacManMoves :

                node = Node(depth= depth-i, parent= element, gameState= gameState.generateSuccessor(index, e))

                if(node.gameState.isWin()):
                    node.set_value(float('inf'))
                    otherQueue.push(node)

                elif(node.gameState.isLose()):
                    node.set_value(float('-inf'))
                    otherQueue.push(node)

                elif(i == depth-1):
                    node.set_value(self.evaluationFunction(node.gameState, e))
                    otherQueue.push(node)

                else :
                    queue.push(node)

                # Add to element the new child created
                element.children.append(node)

        max = 0

        while (otherQueue.length > 1):
            
            node = otherQueue.pop()

            parent = node.parent

            index = parent.depth % parent.gameState.getNumAgents()

            if(parent.get_value() == None):
                parent.set_value(node.get_value())

            elif(index == 0 and parent.get_value() < node.get_value()):
                parent.set_value(node.get_value())
            
            elif(index != 0 and parent.get_value() > node.get_value()):
                parent.set_value(node.get_value())

            if(parent not in otherQueue):
                otherQueue.push(parent)

            if(otherQueue.length == 1 and node.get_value() > max):
                max = node 
        
        # max = 
            
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
