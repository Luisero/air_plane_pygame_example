import random
import math
import pygame as pg
from math import fabs, floor
from time import sleep
from Entities.Bullet import Bullet
from Entities.RemoteGuided import RemoteGuided

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
        self.can_fire = False
        self.has_exploded = False
        self.bullets = []
        self.is_boss = False
        

        self.max_fires= 2
        self.min_fires = 1

        
        if 'enemy3' in self.sprite_list[0]:
            self.max_fires = 6
            self.min_fires = 4
        
       

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

    def check_can_fire(self):
        if self.is_boss:
            self.max_fires= 4
            self.min_fires = 2
        interval = random.randint(60,100)
        if self.context.player.position_dic['x'] - interval <= self.position_dic['x'] <= self.context.player.position_dic['x'] + interval:
            if len(self.bullets)== self.max_fires:
                self.can_fire = False
            else:
                self.can_fire = True
        else:
            if len(self.bullets) == self.max_fires:
                self.bullets = []
            self.can_fire = False
    
    def check_fire(self):
        decide_fire = [True, False, False]

        
        if self.can_fire:
            if random.choice(decide_fire):
                self.shoot()
    

    def shoot(self):
            
        is_bomb = [True, False, False, False]
        if 'enemy2' in self.sprite_list[0]:
           del is_bomb[1:]

        elif 'enemy3' in self.sprite_list[0]:
            del is_bomb[0]


        is_bomb = random.choice(is_bomb)
        is_remote_guided = False
        if self.is_boss and not is_bomb:
            is_remote_guided = [True]
            for i in range(5):
                is_remote_guided.append(False)
        
            is_remote_guided = random.choice(is_remote_guided)

        acceleration_y = .1
        velocity_y = 5
        sprite_path = self.bullet_sprite
        if is_bomb:
            acceleration_y = .2
            velocity_y = -1
            sprite_path = 'Assets/bomb1.png'
        elif is_remote_guided:
            acceleration_y = .1
            velocity_y = 1
            sprite_path = 'Assets/remote_guided.png'
            
            
        
            
        self.bullets.append(1)
        if is_remote_guided:
            
            self.context.bullets.append(
                RemoteGuided(player_position_x=self.position_dic['x']+ self.enemy_size[1] / 2,\
                                   player_position_y=self.position_dic['y'], acceleration_y= acceleration_y, velocity_y = velocity_y, \
                                    velocity_x= self.velocity['x'], sprite_path=sprite_path, is_bomb=is_bomb, context=self.context)
            )
            #self.context.bullets.append(
            #    RemoteGuided(player_position_x=self.position_dic['x']+ self.enemy_size[1],\
            #                       player_position_y=self.position_dic['y'], acceleration_y= acceleration_y, velocity_y = velocity_y, \
            #                        velocity_x= self.velocity['x'], sprite_path=sprite_path, is_bomb=is_bomb, context=self.context)
            #)
            

        else:
            self.context.bullets.append(Bullet(self.position_dic['x'] + self.enemy_size[1] / 2,\
                                    self.position_dic['y'], acceleration_y, velocity_y, self.velocity['x'],sprite_path, is_bomb=is_bomb))
            if self.is_boss:
                self.context.bullets.append(Bullet(self.position_dic['x'] + self.enemy_size[1] ,\
                                    self.position_dic['y'], acceleration_y, velocity_y, self.velocity['x'],sprite_path, is_bomb=is_bomb))
        #    last_index = len(self.context.bullets)-1
         #   self.context.bullets[last_index].size = (30,30)

    def update(self):
        
       
        self.velocity['x'] += self.acceleration['x']
        self.position_dic['x'] += self.velocity['x']
        self.check_movement()
        
        #self.remove_bullet()
        self.check_can_fire()
        self.check_fire()
        
        
    def is_in_danger(self):
        for bullet in self.context.player.bullets:
            distance = math.sqrt((self.position_dic['x']- bullet.position_x)**2 + (self.position_dic['y'] - bullet.position_y)**2)
            print(distance)
            if bullet.position_x - self.enemy_size[0] <= self.position_dic['x'] <= bullet.position_x + self.enemy_size[0] and distance < 70:
                print('Danger')
                
                return True

        return False    
            
        
    def is_in_corners(self):
        if self.can_turn:
            if (self.position_dic['x'] < self.enemy_size[0]/(random.uniform(1, 2))) or (self.position_dic['x'] > self.context.WINDOW_WIDTH - self.enemy_size[0] * 3):
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
        self.context.score +=1
        self.context.enemies.remove(self)
    def detect_collison(self):
        for bullet in self.context.player.bullets:
            offset = (bullet.position_x - self.position_dic['x'], bullet.position_y - self.position_dic['y'])
            overlap = self.mask_collider.overlap(bullet.get_mask_collider(), offset)
            if overlap:
                Bullet.damage = 100
                self.life -= Bullet.damage
                sound = pg.mixer.Sound('Assets/Sound/damage.mp3')
                sound.play()
                if self.life <=0:
                    
                    bullet.remove(self.context, enemie_bullet=False)
                    if not self.has_exploded:
                        
                        self.has_exploded = True
                        if not self.is_boss:
                            self.remove()
                        else:
                            
                            self.context.score += 1
                            self.context.boss_list  = []


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
