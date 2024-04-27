import pygame as pg
from time import sleep
class Item:
    def __init__(self,context, velocity,acceleration, position, effect_time, effect, item_asset, size) -> None:
        self.context = context
        self.velocity = velocity
        self.acceleration = acceleration
        self.position = position
        self.effect_time = pg.time.get_ticks()+ effect_time * context.second
        self.effect = effect
        self.item_asset = item_asset
        self.size = size
        
        self.time = pg.time.get_ticks()
        self.is_active = False
        self.is_picked = False
        self.draw()
        

    def draw(self):
        image= pg.image.load(self.item_asset).convert_alpha()
        image = pg.transform.scale(image, self.size)
        self.mask_collider = pg.mask.from_surface(image)
        self.image = self.context.screen.blit(image, (self.position['x'], self.position['y']))

    def check_is_picked(self):
        offset = (self.context.player.position_dic['x'] - self.position['x'], \
                  self.context.player.position_dic['y'] - self.position['y'])
        overlap = self.mask_collider.overlap(self.context.player.get_mask_collider(), offset)
        if overlap:
            self.is_picked = True 
            self.add_effect()
            
            return self.is_picked

    def check_is_active(self):
        if self.is_picked:
            if pg.time.get_ticks() < self.effect_time:
                self.is_active = True 
                return self.is_active
            else:
                self.is_active = False
                return self.is_active
        
    
    def update(self):
        self.velocity['y'] += self.acceleration['y']
        self.position['y'] += self.velocity['y']
        self.check_is_active()
        self.check_is_picked()
        self.remove_if_is_picked()
        self.draw()


    def remove_if_is_picked(self):
        if self.is_picked:
            self.context.itens.remove(self)


    
    def add_effect(self):
        self.effect()
    
        