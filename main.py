import pygame as pg 
import sys
from Entities.player import Player
from time import sleep
from Debug import  terminal
from Entities.Enemies.Enemy import Enemy

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
        self.time = pg.time.get_ticks()
        self.clock = pg.time.Clock()

        self.enemies = [
            Enemy(context=self,life=100, position_dic={'x': self.CENTER[0], 'y':30}, enemy_size = (60,50), \
                  sprite_list=['Assets/basic_enemy.png'],bullet_sprite='Assets/bullet.png',\
                  acceleration_increaser=0.2, max_velocity={'x':1.5,'y':0})
        ]
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type== pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.shoot()

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw()

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update()

    def check_player_movements(self):

        self.player.check_movement(keys=pg.key.get_pressed())
    
    def run(self):
        while True:
            self.screen.fill((34, 57, 94))
            self.check_events()
            self.check_player_movements()

            self.player.update()
            self.draw_enemies()
            self.update_enemies()
            terminal.clear_terminal()
            print(f'Acceleration: {self.player.acceleration["x"]}')
            print(f'Velocity: {self.player.velocity["x"]}')
            print(self.enemies[0].position_dic['x'])
            self.time = pg.time.get_ticks()
            #sleep(.1)

            pg.display.flip()
            self.clock.tick(60)



if __name__ == '__main__':
    game = Game()
    game.run()

            
