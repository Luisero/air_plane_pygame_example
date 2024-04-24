import pygame as pg
from math import fabs, floor

class Enemy:
    def __init__(self, context, life, position_dic,enemy_size, sprite_list, bullet_sprite, acceleration_increaser, max_velocity):
        self.context = context
        self.life = life
        self.position_dic = position_dic
        self.enemy_size = enemy_size
        self.sprite_list = sprite_list
        self.bullet_sprite = bullet_sprite
        self.acceleration_increaser = acceleration_increaser
        self.max_velocity = max_velocity

        self.bullets = []

        self.velocity = {
            'x': 1,
            'y': 0
        }

        self.acceleration = {
            'x': 0,
            'y': 0
        }


        self.is_going_left = True
        self.is_going_right = False
    def draw(self):
        image = pg.image.load(self.sprite_list[0])
        image = pg.transform.scale(image, self.enemy_size)
        self.image = self.context.screen.blit(image, (self.position_dic['x'], self.position_dic['y']))

    def check_movement(self):

        if self.is_in_corners():
            if self.is_going_left:
                self.is_going_left =  not self.is_going_left
                self.is_going_right = not self.is_going_right
            else:
                self.is_going_left = not self.is_going_left
                self.is_going_right = not self.is_going_right


        if self.is_going_left:
            self.move_left()
        elif self.is_going_right:
            self.move_right()
        else:
            self.stop_enemy()


    def update(self):
        self.velocity['x'] += self.acceleration['x']
        self.position_dic['x'] += self.velocity['x']
        self.check_movement()
    def is_in_corners(self):
        if (self.position_dic['x'] < self.enemy_size[0] ) or (self.position_dic['x'] > self.context.WINDOW_WIDTH - self.enemy_size[0] * 2):
            return True
        return False

    def move_left(self):
        if self.velocity['x'] > - self.max_velocity['x']:

            self.acceleration['x'] = -self.acceleration_increaser
            self.velocity['x'] += self.acceleration['x']


    def move_right(self):
        if self.velocity['x'] < self.max_velocity['x']:
            self.acceleration['x'] = self.acceleration_increaser
            self.velocity['x'] += self.acceleration['x']

    def stop_enemy(self):

        if floor(fabs(self.velocity['x'])) == 0:
            pass
        else:
            if self.is_moving_left() :
                self.acceleration['x'] = self.acceleration_increaser
            elif self.is_moving_right():
                self.acceleration['x'] = - self.acceleration_increaser



    def is_moving_right(self):
        if self.velocity['x'] > 0:
            return True
        return False
    def is_moving_left(self):
        if self.velocity['x'] < 0:
            return True
        return False
