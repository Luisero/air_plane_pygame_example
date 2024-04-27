from .Item import Item
from Entities.player import Player

class LifeRestoreItem(Item):
    def __init__(self, context, velocity, acceleration, position, effect_time, item_asset, size) -> None:
        effect = self.get_effect()
        self.type = 'Life'
        super().__init__(context, velocity, acceleration, position, effect_time, effect, item_asset, size)

    def get_effect(self):
        def effect():
            self.context.player.life = Player.default_life
        return effect

