import random

import pygame as pg
from math import fabs, floor
from time import sleep
from Entities.Bullet import Bullet

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
        self.can_turn = True
        self.can_fire = True
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
        image= pg.transform.flip(image, False, True)
        image = pg.transform.scale(image, self.enemy_size)
        self.mask_collider = pg.mask.from_surface(image)

        self.image = self.context.screen.blit(image, (self.position_dic['x'], self.position_dic['y']))


    def check_movement(self):
        if self.is_in_corners():
            self.can_turn = not self.can_turn
            if self.get_corner() == 'Left':
                self.is_going_left = False
                self.is_going_right = True
            else:
                self.is_going_left = True
                self.is_going_right = False

            #print(f'Can turn: {self.can_turn} Left: {self.is_going_left} Right: {self.is_going_right}')


        if self.is_going_left:
            self.move_left()
        elif self.is_going_right:
            self.move_right()

    def check_fire(self):
        interval = random.randint(60,100)

        if self.can_fire and len(self.bullets) <1:
            if self.context.player.position_dic['x'] - interval <= self.position_dic['x'] <= self.context.player.position_dic['x'] + interval:
                self.shoot()


        if not self.context.player.position_dic['x'] - interval <= self.position_dic['x'] <= self.context.player.position_dic['x'] + interval:
            self.can_fire = True
    def shoot(self):
        self.bullets.append(Bullet(self.position_dic['x'] + self.enemy_size[1] / 2,\
                                   self.position_dic['y'], .1, 5, self.velocity['x'],'Assets/bullet2.png'))

    def update(self):
        self.velocity['x'] += self.acceleration['x']
        self.position_dic['x'] += self.velocity['x']
        self.check_movement()
        self.check_fire()
        self.draw_bullets()
        self.remove_bullet()
    def is_in_corners(self):
        if self.can_turn:
            if (self.position_dic['x'] < self.enemy_size[0]/2) or (self.position_dic['x'] > self.context.WINDOW_WIDTH - self.enemy_size[0] * 3):
                self.can_turn = not self.can_turn
                from time import sleep
                #print(f'Can turn: {self.can_turn} Left: {self.is_going_left} Right: {self.is_going_right}')

                return True

        return False

    def get_corner(self):
        if (self.position_dic['x'] < self.enemy_size[0]) :
            return 'Left'
        else:
            return 'Right'
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
                self.acceleration['x'] = self.acceleration_increaser/2
                self.velocity['x'] += self.acceleration['x']
            elif self.is_moving_right():
                self.acceleration['x'] = - self.acceleration_increaser/2
                self.acceleration['x'] = self.acceleration['x']

    def remove(self):
        self.context.enemies.remove(self)
    def detect_collison(self):
        for bullet in self.context.player.bullets:
            offset = (bullet.position_x - self.position_dic['x'], bullet.position_y - self.position_dic['y'])
            overlap = self.mask_collider.overlap(bullet.get_mask_collider(), offset)
            if overlap:

                self.life -= Bullet.damage
                if self.life <=0:
                    bullet.remove(self.context)
                    self.remove()

    def remove_bullet(self):
        for bullet in self.bullets:
            if bullet.position_y > self.context.WINDOW_HEIGHT:
                self.bullets.remove(bullet)

    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw(self.context)
            bullet.update_position()
    def is_moving_right(self):
        if self.velocity['x'] > 0:
            return True
        return False
    def is_moving_left(self):
        if self.velocity['x'] < 0:
            return True
        return False
