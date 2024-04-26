import random

import pygame as pg
import sys
from Entities.player import Player
from time import sleep
from Debug import  terminal
from Entities.Enemies.Enemy import Enemy
from random import randint

class Game:
    def __init__(self, win_size=(400,600)):
        pg.init()

        self.WINDOW_SIZE = win_size
        self.WINDOW_HEIGHT = self.WINDOW_SIZE[1]
        self.WINDOW_WIDTH = self.WINDOW_SIZE[0]

        self.CENTER = (self.WINDOW_WIDTH/2, self.WINDOW_HEIGHT/2)

        self.SKY_SCROLL_SPEED = 1
        self.SKY_MAX_SPEED = 2
        self.SKY_SCROLL_ACCELERATION = .001

        PLAYER_INITIAL_POSITION = {'x':self.CENTER[0], 'y': self.CENTER[1]+200}
        self.player = Player(self, PLAYER_INITIAL_POSITION, player_size=(60, 50) )

        self.screen = pg.display.set_mode(win_size)
        self.time = pg.time.get_ticks()
        self.clock = pg.time.Clock()

        self.enemies = [
            Enemy(context=self,life=100, position_dic={'x': self.WINDOW_WIDTH, 'y':30}, enemy_size = (60,50), \
                  sprite_list=['Assets/basic_enemy.png'],bullet_sprite='Assets/bullet.png',\
                  acceleration_increaser=0.1, max_velocity={'x':.2,'y':0})
        ]

        pg.mixer.init()
        self.sky_images =[]

        self.load_sky_image()

    def load_sky_image(self):
        for i in range(0, 3):
            image = pg.image.load('Assets/sky.png').convert()
            image = pg.transform.scale(image, (self.WINDOW_HEIGHT, self.WINDOW_HEIGHT)  )
            height = image.get_height()
            self.sky_images.append({"image":image,'y':-i*height})


    def game_over(self):
        pg.quit()
        sys.exit()

    def draw_background_sky(self):
        for i,image in enumerate(self.sky_images):

            if image['y'] > self.WINDOW_HEIGHT:
                self.sky_images.insert(0, self.sky_images.pop() )

            if i > 0:
               image['y'] = self.sky_images[i-1]['y']- self.WINDOW_HEIGHT

            image['y'] += self.SKY_SCROLL_SPEED
            if self.SKY_SCROLL_SPEED < self.SKY_MAX_SPEED:
                self.SKY_SCROLL_SPEED += self.SKY_SCROLL_ACCELERATION

        for i in range(3):
            self.screen.blit(self.sky_images[i]['image'], (0, self.sky_images[i]['y']))




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
            enemy.detect_collison()

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update()

    def check_player_movements(self):

        self.player.check_movement(keys=pg.key.get_pressed())

    def add_enemy(self):
        random_positions = [self.WINDOW_WIDTH, -30]
        position = random.choice(random_positions)
        self.enemies.append(
            Enemy(context=self, life=100, position_dic={'x': position+randint(-50,50), 'y': randint(30,60)}, enemy_size=(60, 50), \
                  sprite_list=['Assets/basic_enemy.png'], bullet_sprite='Assets/bullet.png', \
                  acceleration_increaser=0.1, max_velocity={'x': .2, 'y': 0})
        )
    def run(self):
        while True:
            self.screen.fill((34, 57, 94))
            self.draw_background_sky()
            self.check_events()
            self.check_player_movements()

            self.player.update()
            self.draw_enemies()
            self.update_enemies()
            terminal.clear_terminal()
            '''print(f'Acceleration: {self.player.acceleration["x"]}')
            print(f'Velocity: {self.player.velocity["x"]}')
            print(f'\tAcceleration: {self.enemies[0].acceleration["x"]}')
            print(f'\tVelocity: {self.enemies[0].acceleration["x"]}')'''

            if (self.time % 1000) == 0:
                self.add_enemy()

            #print(self.enemies[0].position_dic['x'])
            print(self.player.life)
            self.time = pg.time.get_ticks()
            #sleep(.1)

            pg.display.flip()
            self.clock.tick(60)



if __name__ == '__main__':
    game = Game()
    game.run()

            
