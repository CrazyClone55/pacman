import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghost import Ghost

class Controller(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('song.mp3')
        #pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        
    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)  
            if pellet.name == POWERPELLET:
               self.ghost.startFright()  
        
    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup(LEVEL)
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getStartTempNode())
        self.pellets = PelletGroup(LEVEL)
        self.ghost = Ghost(self.nodes.getStartTempNode(), self.pacman)
        self.ghost.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
    
    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)
            
    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.pacman.update(dt)
        self.ghost.update(dt)
        self.pellets.update(dt)
        self.checkPelletEvents()
        self.checkGhostEvents()
        self.checkQuit()
        self.render()            

    def checkGhostEvents(self):
        if self.pacman.collideGhost(self.ghost):
            if self.ghost.mode.current is FRIGHT:
                self.ghost.startSpawn()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update()
        
    def checkQuit(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        
if __name__ == "__main__":
    game = Controller()
    game.startGame()
    while True:
        game.update()