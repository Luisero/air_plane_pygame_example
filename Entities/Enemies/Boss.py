from .Enemy import Enemy
class Boss(Enemy):
    def __init__(self, context, life, position_dic, enemy_size, sprite_list, bullet_sprite, acceleration_increaser, max_velocity):
        super().__init__(context, life, position_dic, enemy_size, sprite_list, bullet_sprite, acceleration_increaser, max_velocity)
        