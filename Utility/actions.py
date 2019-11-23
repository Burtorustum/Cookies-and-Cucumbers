from Utility import Item, Player, Room


def move(room: Room):
    print(room.name)


def examine(item: Item):
    print(item.name)


def interact(player: Player, item: Item):
    print(item.name, player.clues)

def pick_up(player: Player, item: Item):
    if item.holdable:
        player.held_obj = item
    return item.pickup_text

def drop(player: Player):
    if player.is_holding_obj()
