import pygame as pg


class BombExplosion(pg.sprite.Sprite):
    def __init__(self, position, speed) -> None:
        pg.sprite.Sprite.__init__(self)
        self.sprites = []
        self.position = position
        self.speed = speed
        self.size = (40,40)

        for i in range(0,2):
            image = pg.image.load(f'Assets/Bomb_explosion/bomb_explosion_{i}.png')
            image = pg.transform.scale(image, self.size)
            self.sprites.append(image)
            

        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.position['x'], self.position['y']]
        
    
    def update(self):
        self.current_sprite += self.speed
        

        if self.current_sprite >= len(self.sprites):
            self.kill()
        else:
            self.image = self.sprites[int(self.current_sprite)]

        
