import pygame as pg 
import sys
from Entities.player import Player
from time import sleep
from Debug import  terminal

class Game:
    def __init__(self, win_size=(400,600)):
        pg.init()

        self.WINDOW_SIZE = win_size
        self.WINDOW_HEIGHT = self.WINDOW_SIZE[1]
        self.WINDOW_WIDTH = self.WINDOW_SIZE[0]

        self.CENTER = (self.WINDOW_WIDTH/2, self.WINDOW_HEIGHT/2)

        PLAYER_INITIAL_POSITION = {'x':self.CENTER[0], 'y': self.CENTER[1]+200}
        self.player = Player(self, PLAYER_INITIAL_POSITION, player_size=(60, 50) )

        self.screen = pg.display.set_mode(win_size)

        self.clock = pg.time.Clock()
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type== pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.shoot()


    def check_player_movements(self):

        self.player.check_movement(keys=pg.key.get_pressed())
    
    def run(self):
        while True:
            self.screen.fill((34, 57, 94))
            self.check_events()
            self.check_player_movements()

            self.player.update()

            terminal.clear_terminal()
            print(f'Acceleration: {self.player.acceleration["x"]}')
            print(f'Velocity: {self.player.velocity["x"]}')
            #sleep(.1)

            pg.display.flip()
            self.clock.tick(60)



if __name__ == '__main__':
    game = Game()
    game.run()

            
