from py import process
from pacman import Pacman
from constants import *
from time import process_time

class BFSPacman(Pacman):
    def __init__(self, node):
        Pacman.__init__(self, node)
        self.direction = STOP
        
    def breathFirstSearch(self,startNode, goalNode):
        start_time = process_time()
        self.queue = self.graphSearcher(startNode,goalNode)
        stop_time = process_time()
        print(stop_time, start_time)
        print(stop_time-start_time)
        self.queue.pop(0)
        self.target = self.queue.pop(0)
        self.direction = self.getDirection()
    
        
    def graphSearcher(self, startNode, goalNode):
        queue = []
        self.explored = []
        self.parents = {}
        queue.append(startNode)
        self.parents[startNode] = None
        while queue:
            node = queue.pop(0)
            if node is goalNode:
                return self.givePath(startNode, goalNode)
            self.explored.append(node)
            for v in node.neighbors.values():
                if v not in queue and v not in self.explored and v is not None:
                    self.explored.append(v)
                    queue.append(v)
                    self.parents[v] = node
                    
                
                
    def givePath(self, start, finish):
        stack = []
        first, last = finish, self.parents[finish]
        while last is not start:
            stack.append(first)
            first, last = last, self.parents[last]
        stack.append(first)
        stack.append(last)
        
        queue = []
        while stack:
            queue.append(stack.pop())
        return queue      
            
    def getDirection(self):
        directionIndex = list(self.node.neighbors.values()).index(self.target)
        direction = list(self.node.neighbors.keys())[directionIndex]
        return direction
        
    def update(self, dt):	
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.direction
        
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
               
            if self.queue:
                self.target = self.queue.pop(0)
            else:
                self.target = self.node
            print(self.target.position/16)
            
            if self.target is not self.node:
                # get the direction of the target
                self.direction = self.getDirection()

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()