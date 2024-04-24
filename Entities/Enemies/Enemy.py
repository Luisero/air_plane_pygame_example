

class Enemy:
    def __init__(self, life, sprite_list, bullet_sprite, acceleration_increaser, max_velocity):
        self.life = life
        self.sprite_list = sprite_list
        self.bullet_sprite  = bullet_sprite
        self.acceleration_increaser = acceleration_increaser
        self.max_velocity = max_velocity

        self.velocity = {
            'x': 0,
            'y': 0
        }

        self.acceleration = {
            'x': 0,
            'y': 0
        }


