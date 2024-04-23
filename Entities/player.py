import pygame as pg
from .Bullet import Bullet

class Player:
    def __init__(self, context, position_dic, player_size) -> None:
        self.player_size = player_size
        self.context = context
        self.position_dic = position_dic

        self.bullets = []

        self.max_velocity ={ 
            'x': 1.5,
            'y': 0}

        self.velocity = {
            'x': 0,
            'y': 0
        }

        self.acceleration_increaser = .1
        self.acceleration = {
            'x':0,
            'y':0
        }

    def check_moviment(self):
        pass 

    def move_left(self):
        if self.velocity['x'] > - self.max_velocity['x']:
            self.acceleration['x'] = -self.acceleration_increaser
            self.velocity['x'] += self.acceleration['x']

    def move_right(self):
        if self.velocity['x'] < self.max_velocity['x']:
            self.acceleration['x'] = self.acceleration_increaser
            self.velocity['x'] += self.acceleration['x']

    def stop_player(self):
        if self.velocity['x'] < 0:
            self.acceleration['x'] = .05
        elif self.velocity['x'] > 0:
            self.acceleration['x'] = -.05
        
        else:
            self.acceleration['x'] = 0

    def update(self):
        self.velocity['x'] += self.acceleration['x']
        self.position_dic['x'] += self.velocity['x']
        self.draw()
        self.draw_bullets()
    
    def shoot(self):
        self.bullets.append(Bullet(self.position_dic['x']+ self.player_size[1]/2, self.position_dic['y']))

    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw(self.context)
            bullet.update_position()

    def draw(self):
        #self.box_collider.draw(self.game,self.position)
        image = pg.image.load('Assets/ship_player.png')
        image = pg.transform.scale(image, self.player_size)
        self.image = self.context.screen.blit(image, (self.position_dic['x'], self.position_dic['y']))