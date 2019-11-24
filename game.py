from graphics import *
import Utility.actions as act
from Utility.Player import Player
from Utility.Room import Room
from Utility.Item import Item
from Instantiations.Bedroom import *


def game_start(player: Player, window: GraphWin):
    update_window(player, window, [])
    click_button(player, window)


def click_button(player: Player, window: GraphWin, cur_item=None):
    buttons = None
    if cur_item is None:  # get the buttons
        buttons = gen_buttons(player, window)
    else:
        buttons = gen_object_buttons(player, window, cur_item)

    click = window.getMouse()
    s = None
    for b in buttons:
        if in_rectangle(click, b[0]):
            if b[3] is Item:
                cur_item = b[3]
                s = b[3].examine_text
            else:
                b[3](player)  # TODO: Not sure what to input here lol
    update_window(player, window, cur_item, s)
    return cur_item


def update_window(player: Player, window: GraphWin, buttons,  cur_item=None, s=None):
    window.delete("all")  # remove all current things in window

    player_notes(player, window)  # redraw the left hand stuff
    context(player, window, s)

    for b in buttons:  # draw the buttons
        for x in b:
            if x is Rectangle or x is Text:
                x.draw(window)

    window.update()
    return buttons


# NOTE: Buttons are just going to be boxes, so each gen_button will just return a bunch of tuples of the form
# (Rectangle, Text, object<or room?>), then can go through the list and for each tuple, draw onto the window.
# then the func that checks for button presses can call the update window button w/ the object of the button.
def gen_buttons(player: Player, window: GraphWin):
    objects = player.cur_room.objects
    # get current room
    # get objects in current room
    # make button for each object in room, that calls specific interact/examine/etc
    buttons = []
    for i in range(len(objects)):
        o = objects[i]
        b = Rectangle(Point(), Point())
    return []


# TODO: TEST GEN OBJECT BUTTONS
# returns a list of tuples (Rectangle, Text, Object related call)
# where the call is either to the object's interact or pickup text gen funcs
def gen_object_buttons(player: Player, window: GraphWin, item: Item):
    diff = 56.25
    left = 537.5
    right = 1112.5
    middle = (right + left) / 2

    interact_box = Rectangle(Point(left, 187.5 + 4 * diff), Point(right, 187.5 + 6 * diff))
    interact_text = Text(Point(middle, (187.5 * 2 + 10 * diff) / 2), "Interact")

    pickup_box = Rectangle(Point(left, 187.5 + 7 * diff), Point(right, 187.5 + 9 * diff))
    pickup_text = Text(Point(middle, (187.5 * 2 + 16 * diff) / 2), "Pickup")

    return [ # (interact_box, interact_text, item.interact()),  # THEY HAVE TO BE FUNC BECAUSE OF INTERACT?
            (pickup_box, pickup_text, item.pickup_text())] # TODO: DO THESE TAKE IN PLAYER OR SOMETHING ELSE?


# TODO: Decide what else goes in here
def player_notes(player: Player, window: GraphWin):
    bar = 250
    left_line = Line(Point(bar, 0), Point(bar, window.getHeight()))
    left_line.setWidth(4)
    left_line.draw(window)

    room_string = "Current Room:\n" + player.cur_room.name
    room_text = Text(Point(bar / 2, 50), room_string)
    room_text.setSize(24)
    room_text.draw(window)

    item_string = "Current Item:\n"
    if player.held_item is None:
        item_string += "None"
    else:
        item_string += player.held_item.name
    item_text = Text(Point(bar / 2, 250), item_string)
    item_text.setSize(24)
    item_text.draw(window)


def context(player: Player, window: GraphWin, cur_item=None):
    bar = window.getHeight() / 4
    top_line = Line(Point(250, bar), Point(window.getWidth(), bar))
    top_line.setWidth(4)
    top_line.draw(window)

    context_string = player.cur_room.description if cur_item is None else cur_item.examine_text
    context_text = Text(Point(window.getWidth() / 2 + 125, window.getHeight() / 15), context_string)
    context_text.setSize(18)
    context_text.draw(window)


def in_rectangle(point: Point, rect: Rectangle):
    return rect.getP1().x < point.x < rect.getP2().x and rect.getP2().y < point.y < rect.getP1().y


def main():
    player = Player()
    player.cur_room = Bedroom

    window = GraphWin("Cucumbers and Cookies", 1400, 750, autoflush=False)

    game_start(player, window)


if __name__ == '__main__':
    main()
