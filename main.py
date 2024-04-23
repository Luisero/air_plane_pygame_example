import pygame as pg 
import sys
from Entities.player import Player
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
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.player.move_left()
        elif keys[pg.K_d]:
            self.player.move_right()
        else:
            self.player.stop_player()
    
    def run(self):
        while True:
            self.screen.fill((34, 57, 94))
            self.check_events()

            self.player.update()
            

            pg.display.flip()
            self.clock.tick(60)



if __name__ == '__main__':
    game = Game()
    game.run()

            
