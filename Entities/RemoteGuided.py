from .Bullet import Bullet


class RemoteGuided(Bullet):
    def __init__(self, player_position_x, player_position_y, acceleration_y, velocity_y, velocity_x, sprite_path, sound_path=None, is_bomb=False, context=None) -> None:
        super().__init__(player_position_x, player_position_y, acceleration_y, velocity_y, velocity_x, sprite_path, sound_path, is_bomb)
        self.context = context
        self.acceleration_x = .1
    
    def update_position(self):
        if self.position_x < self.context.player.position_dic['x'] :
            self.velocity_x  += self.acceleration_
        else:
            self.velocity_x -= self.acceleration_x   

        self.velocity_y += self.acceleration_y
        self.position_y += self.velocity_y
        self.position_x += self.velocity_x