import Item
import Player
import Room


def move(room: Room):
    print(room.name)


def examine(item: Item):
    print(item.name)


def interact(player: Player, item: Item):
    print(item.name, player.clues)

def pick_up(player: Player, item: Item):
    if item.holdable:
        player.held_obj = item
    return item.
