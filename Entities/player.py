import pygame as pg
from .Bullet import Bullet
from math import fabs, floor

class Player:
    max_ammo = 3
    def __init__(self, context, position_dic, player_size) -> None:
        self.player_size = player_size
        self.context = context
        self.position_dic = position_dic
        self.life = 100
        self.bullets = []
        self.player_ammo = 3

        self.max_velocity ={ 
            'x': 1.5,
            'y': 0}

        self.velocity = {
            'x': 0.0,
            'y': 0
        }

        self.acceleration_increaser = .1
        self.acceleration = {
            'x':0.0,
            'y':0
        }

    def check_movement(self, keys):


        if keys[pg.K_a]:
            self.move_left()
        elif keys[pg.K_d]:
            self.move_right()
        else:
            self.stop_player()


    def move_left(self):
        if self.velocity['x'] > - self.max_velocity['x']:
            self.acceleration['x'] = -self.acceleration_increaser
            self.velocity['x'] += self.acceleration['x']

    def move_right(self):
        if self.velocity['x'] < self.max_velocity['x']:
            self.acceleration['x'] = self.acceleration_increaser
            self.velocity['x'] += self.acceleration['x']

    def stop_player(self):

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


    def update(self):
        self.velocity['x'] += self.acceleration['x']
        self.position_dic['x'] += self.velocity['x']
        self.draw()
        self.remove_bullet()
        self.draw_bullets()
        self.detect_collison()

    def shoot(self):
        if self.player_ammo >0:
            self.bullets.append(Bullet(self.position_dic['x']+ self.player_size[1]/2, \
                                       self.position_dic['y'], -.1,-5,self.velocity['x'], 'Assets/bullet.png'))
            self.player_ammo -= 1


    def remove_bullet(self):
        for bullet in self.bullets:
            if bullet.position_y <= - bullet.size[1]:
                self.bullets.remove(bullet)
    def draw_bullets(self):
        for bullet in self.bullets:
            bullet.draw(self.context)
            bullet.update_position()

    def detect_collison(self):
        for enemie in self.context.enemies:
            for bullet in enemie.bullets:
                offset = (bullet.position_x - self.position_dic['x'], bullet.position_y - self.position_dic['y'])

                overlap = self.mask_collider.overlap(bullet.get_mask_collider(), offset)
                if overlap:
                    Bullet.damage = 10
                    if bullet.is_bomb:
                        Bullet.damage = 20
                    self.life -= Bullet.damage
                    bullet.remove(self.context, enemie_bullet=True)
                    sound = pg.mixer.Sound('Assets/Sound/damage.mp3')
                    sound.play()

                    if self.life <=0:
                        self.context.game_over()




    def draw(self):
        #self.box_collider.draw(self.game,self.position)
        image = pg.image.load('Assets/ship_player.png')
        image = pg.transform.scale(image, self.player_size)
        self.mask_collider = pg.mask.from_surface(image)
        self.image = self.context.screen.blit(image, (self.position_dic['x'], self.position_dic['y']))