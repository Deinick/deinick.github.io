"""
Search (Chapters 3-4)

The way to use this code is to subclass Problem to create a class of problems,
then create problem instances and solve them with calls to the various search
functions.
"""

import sys
import math
from collections import deque

from utils import *
from agents import *


"""
1- BFS: Breadth first search. Using tree or graph version, whichever makes more sense for the problem
2- DFS: Depth-First search. Again using tree or graph version.
3- UCS: Uniform-Cost-Search. Using the following cost function to optimise the path, from initial to current state.
4- Greedy: Uses Manhattan distance to the next closest dirty room as heuristic for greedy algorithm. To find the next closest dirty room, use Manhattan distance.
5- A*:  Using A star search.
"""
searchTypes = ['None', 'Reflex', 'BFS', 'DFS', 'UCS', 'Greedy', 'A*']
"""
Cost function used for UCS and A* search. 
-'Step' counts the numbers of steps from start
-'StepTurn' adds number of turns to Step cost
-'StayLeft' favors staying on the left side of the map
-'StayUp' favors staying on the top side of the map
"""
costFunctions = ['Step', 'StepTurn', 'StayLeft', 'StayUp']
heuristics = ['Manhattan', 'Euclid']

class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        pathCost = problem.path_cost(self, self.state, action, next_state)
        next_node = Node(next_state, self, action, pathCost)
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]


    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash Table
        return hash(self.state)



class SearchPlanning(Problem):
    """ The problem of find the next room to clean in a grid of m x n rooms.
    A state is represented by state of the grid cells locations. Each room is specified by index set
    (i, j), i in range(m) and j in range (n). Final goal is to clean all dirty rooms.
    We go by performing sub-goals, each being cleaning the "next" dirty room.
    """

    def __init__(self, env):
        """ Define goal state and initialize a problem
            initial is a pair (i, j) of where the agent is
            goal is next pair(k, l) where map[k][l] is dirty
        """
        self.solution = None
        self.env = env
        self.state = env.agent.location
        super().__init__(self.state)
        self.map = env.things
        self.searchType = env.searchType


    def generateSolution(self):
        """ generate full path and explored nodes from current node to the next goal node based on type of the search chosen"""
        if self.searchType == 'None':
            print("generateSolution: searchType not set or running not clicked!")
            return

        self.env.read_env()
        self.state = self.env.agent.location
        super().__init__(self.state)

        if self.searchType == 'BFS':
            if self.env.args['early'] == False:
                path, explored = breadth_first_search(self)
            else:
                path, explored = breadth_first_earlyExit(self)
        elif self.searchType == 'DFS':
            path, explored = depth_first_search(self)
        elif self.searchType == 'UCS':
            path, explored = uniform_cost_search(self)
        elif self.searchType == 'Greedy':
            path, explored = greedy_search(self, self.h)
        elif self.searchType == 'A*':
            path, explored = astar_search(self, self.h)
        elif self.searchType == 'Reflex':
            path, explored = reflexAgentSearch(self)
        else:
            raise 'NameError'

        if (path != None):
            self.env.set_solution(path)
        else:
            print("There is no solution!\n")

        if (explored != None):
            self.env.display_explored(explored)
            self.env.exploredCount += len(explored)
            self.env.pathCount += len(self.env.path)
            self.env.ExploredCount_label.config(text="ExploredCount: " + str(self.env.exploredCount))
            self.env.PathCount_label.config(text="PathCount: " + str(self.env.pathCount))
        else:
            print("Explored list is empty. It's ok if the search agent is a Reflex Agent.\n")

    def generateNextSolution(self):
        self.generateSolution()

    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only four possible actions
        in any given state of the environment """

        possible_neighbors = self.env.things_near(state)
        possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        for slot in possible_neighbors:
            if isinstance(slot[0], Wall):
                x, y = slot[0].location
                if x == state[0] and y == state[1] + 1:
                    possible_actions.remove('UP')
                if x == state[0] and y == state[1] - 1:
                    possible_actions.remove('DOWN')
                if x == state[0] + 1 and y == state[1]:
                    possible_actions.remove('RIGHT')
                if x == state[0] - 1 and y == state[1]:
                    possible_actions.remove('LEFT')

        return possible_actions

    def result(self, state, action):
        """ Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action for the state """
        self.env.agent.direction = Direction(action.upper())
        new_state = list(state)
        if action == 'RIGHT':
            new_state[0] += 1
        elif action == 'LEFT':
            new_state[0] -= 1
        elif action == 'UP':
            new_state[1] += 1
        elif action == 'DOWN':
            new_state[1] -= 1

        return new_state

    def goal_test(self, state):
        """ Given a state, return True if state is a goal state or False, otherwise """
        return self.env.some_things_at(state, Dirt)

    def path_cost(self, curNode, state1, action, state2):
        """computes accumulated path cost so far to state2. Returns the cost of a solution path that arrives at state2 from
        state1 via action, assuming it costs c to get up to state1. For our problem state is (x, y) coordinate pair.
        Rotation of the agent costs 3 times of basic cost unit for each 90' rotation plus the basic cost. """
        # print("path_cost: to be done by students")
        cost = curNode.path_cost
        if (self.env.costFunc == costFunctions[0]):  # basic stepCount cost
            cost = cost + 1
        elif (self.env.costFunc == costFunctions[1]):  # stepCount plus turn cost
            before=curNode.action
            charges=self.computeTurnCost(before,action)
            cost=cost+1+charges
        elif (self.env.costFunc == costFunctions[2]):  # cost function to encourage staying left of grid
            x,_=state2
            cost=cost+x
        else:  # means self.env.costFunc == costFunctions[3]. cost function to encourage stay at the top half of the grid
            _,y=state2
            cost=cost+y

        #print("Path-Cost: loc1: ", state1, ", loc2: ", state2, "= ", "curCost=", curNode.path_cost, "newCost=", cost)
        return cost

    def computeTurnCost(self, action1, action):
        """computes turn cost as the number of 90' rotations away from current direction given by action1"""
        if not action1 or not action:
            return 0
        direction=['LEFT','UP','RIGHT','DOWN']
        action1=direction.index(action1)
        action=direction.index(action)
        result=action1-action
        if result<0:
            result=result *(-1)
        tur=min(result,4-result)
        return tur*3


    def findMinManhattanDist2DirtyRoom(self, pos):
        """Find a dirty room among all dirty rooms which has minimum Manhattan distance to pos
        hint: use distance_manhattan() function in utils.py"""
        min_dist=float('inf')
        for dirt in self.env.dirtyRooms:
            dist=distance_manhattan(pos, dirt)
            if dist<min_dist:
                min_dist=dist
        return min_dist

    def findMinEuclidDist2DirtyRoom(self, pos):
        """Find a dirty room among all dirty rooms which has minimum Manhattan distance to pos
                hint: use distance_manhattan() function in utils.py"""
        min_dist=float('inf')
        for dirt in self.env.dirtyRooms:
            dist=distance_euclid(pos, dirt)
            if dist<min_dist:
                min_dist=dist
        return min_dist

    def h(self, node):
        """ Return the heuristic value for a given node.
        For this problem use minimum Manhattan or Euclid
        distance to a dirty room, among all the dirty rooms.
        """
        if self.env.args['heuristic'] == 'Manhattan':
            heur = self.findMinManhattanDist2DirtyRoom(node.state)
        else:  ## means Euclid distance
            heur = self.findMinEuclidDist2DirtyRoom(node.state)
        #print("node: ", node.state, ", heur: ", heur)
        return heur

# ______________________________________________________________________________
# Uninformed Search algorithms
def breadth_first_search(problem):
    node=Node(problem.initial)
    if problem.goal_test(node.state):
        return node.solution(), []
    frontier=deque([node])
    explored=set()
    while frontier:
        another_node=frontier.popleft()
        if problem.goal_test(another_node.state):
            return another_node, explored
        explored.add(tuple(another_node.state))
        for action in problem.actions(another_node.state):
            child=problem.result(another_node.state, action)
            child_node=Node(child,another_node,action)
            if tuple(child) not in explored and child_node not in frontier:
                frontier.append(child_node)
            if problem.goal_test(child_node.state):
                return child_node, explored
            explored.add(tuple(child_node.state))
    return None, []



def breadth_first_earlyExit(problem):
    first_node=Node(problem.initial)
    frontier=deque([first_node])
    explored=set()
    while frontier:
        node=frontier.popleft()
        if problem.goal_test(node.state):
            return node, explored
        explored.add(tuple(node.state))
        for action in problem.actions(node.state):
            child_state=problem.result(node.state,action) #we retrieve the child node from the node itslef in advance
            if tuple(child_state) not in explored:
                if all(n.state != child_state for n in frontier):
                    child_node=Node(child_state, node, action)
                    if problem.goal_test(child_state):
                        return child_node,explored
                    frontier.append(child_node)
    return None, explored


def depth_first_search(problem):
    first_node=Node(problem.initial)
    if problem.goal_test(first_node.state):
        return first_node.solution(), []
    frontier= [first_node]
    explored=set()
    while frontier:
        node=frontier.pop()
        if problem.goal_test(node.state):
            return node, explored
        explored.add(tuple(node.state))
        for action in problem.actions(node.state):
            child=problem.result(node.state,action)
            if tuple(child) not in explored:
                if all(n.state != child for n in frontier):
                    child_node=Node(child, node,action)
                    frontier.append(child_node)
    return None, []

def reflexAgentSearch(problem):
    """returns a path to next cell neighboring current location based on a typical reflex agent.
    A reflex agent senses the immediate neighboring cells and it finds a dirty one, move there, otherwise
    move randomly to one of the available left, right, and forward cells."""
    current_state=problem.env.agent.location
    possible_actions=problem.actions(current_state)
    for action in possible_actions:
        next_state=problem.result(current_state, action)
        if problem.env.some_things_at(next_state, Dirt):
            node=Node(next_state, parent=Node(current_state), action=action, path_cost=1)
            return node, [current_state]
    if possible_actions:
        random_action=random.choice(possible_actions)
        next_state=problem.result(current_state, random_action)
        node=Node(next_state, parent=Node(current_state), action=random_action, path_cost=1)
        return node,[current_state]
    return None,[current_state]

def uniform_cost_search(problem):
    first_node_state=Node(problem.initial)
    frontier=PriorityQueue(order='min', f=lambda node: node.path_cost)
    frontier.append(first_node_state)
    explored=set()
    while frontier:
        first_node=frontier.pop()
        if problem.goal_test(first_node.state):
            return first_node, explored
        explored.add(tuple(first_node.state))
        for action in problem.actions(first_node.state):
            child_state=problem.result(first_node.state,action)
            child_cost=problem.path_cost(first_node,first_node.state,action,child_state)
            child_node=Node(child_state,first_node,action,child_cost)
            if tuple(child_state) not in explored:
                if child_node not in frontier:
                    frontier.append(child_node)
            else:
                for exist, exist_node in frontier.heap:
                    if exist_node.state == child_state and child_node.path_cost < exist_node.path_cost:
                        frontier.remove(exist_node)
                        frontier.append(child_node)
                        break

    return None, explored

# ______________________________________________________________________________
# Informed (Heuristic) Searches

def greedy_search(problem, h):
    first_node_state = Node(problem.initial)
    frontier=PriorityQueue(order='min', f=lambda node: problem.h(node))
    frontier.append(first_node_state)
    explored=set()
    while frontier:
        first_node=frontier.pop()
        if problem.goal_test(first_node.state):
            return first_node, explored
        explored.add(tuple(first_node.state))
        for action in problem.actions(first_node.state):
            child_state = problem.result(first_node.state, action)
            child_cost = problem.path_cost(first_node, first_node.state, action, child_state)
            child_node = Node(child_state, first_node, action, child_cost)
            if tuple(child_state) not in explored:
                if child_node not in frontier:
                    frontier.append(child_node)
            else:
                for exist, exist_node in frontier.heap:
                    if exist_node.state==child_state and child_node.path_cost<exist_node.path_cost:
                        frontier.remove(exist_node)
                        frontier.append(child_node)
                        break

    return None, explored

def astar_search(problem, h):
    first_node_state = Node(problem.initial)
    frontier = PriorityQueue(order='min', f=lambda node: node.path_cost + problem.h(node))
    frontier.append(first_node_state)
    explored = set()
    while frontier:
        first_node=frontier.pop()
        if problem.goal_test(first_node.state):
            return first_node, explored
        explored.add(tuple(first_node.state))
        for action in problem.actions(first_node.state):
            child_state=problem.result(first_node.state, action)
            child_cost=problem.path_cost(first_node, first_node.state, action, child_state)
            child_node=Node(child_state, first_node, action, child_cost)
            if tuple(child_state) not in explored:
                if child_node not in frontier:
                    frontier.append(child_node)
            else:
                for exist, exist_node in frontier.heap:
                    if exist_node.state == child_state and child_node.path_cost < exist_node.path_cost:
                        frontier.remove(exist_node)
                        frontier.append(child_node)
                        break

    return None, explored

# ______________________________________________________________________________
# ______________________________________________________________________________

