import pygame as pg
import random
import pygame as pg

class Bullet:
    damage = 100

    def __init__(self, player_position_x, player_position_y, acceleration_y, velocity_y, velocity_x, sprite_path, sound_path=None, is_bomb=False) -> None:

        self.size = (20, 20)
        self.position_x = player_position_x
        self.position_y = player_position_y
        self.velocity_y = velocity_y
        self.acceleration_y = acceleration_y
        self.sprite_path = sprite_path
        self.is_bomb = is_bomb
        self.is_missile = False
        
        if self.is_bomb:
            self.velocity_x = velocity_x *.2
            self.sound_path = 'Assets/Sound/bomb1.mp3'
        else:
            self.velocity_x = velocity_x *.1
            self.sound_path = 'Assets/Sound/shoot.wav'

        if type(sound_path) == None:
            self.sound_path = sound_path
        self.fire_sound(self.sound_path)

    def fire_sound(self, sound_path):
        sound = pg.mixer.Sound(sound_path)
        sound.play()


    def draw(self, game):
        image= pg.image.load(self.sprite_path).convert_alpha()
        image = pg.transform.scale(image, self.size)
        if self.is_bomb:
            image = pg.transform.flip(image, False, True)
        self.mask_collider = pg.mask.from_surface(image)
        self.image = game.screen.blit(image, (self.position_x, self.position_y))
        #pg.draw.rect(game.screen,'red', (self.position_x, self.position_y, self.size[0], self.size[1]) )
    
    def get_mask_collider(self):
        return self.mask_collider
    
    def remove(self, game, enemie_bullet):
        if not enemie_bullet:
            game.player.bullets.remove(self)
        else:
            for bullet in game.bullets:
                
                if bullet == self:
                    game.bullets.remove(self)

    def update_position(self):

        self.velocity_y += self.acceleration_y
        self.position_y += self.velocity_y
        self.position_x += self.velocity_x

    