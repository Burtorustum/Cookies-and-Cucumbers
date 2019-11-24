from graphics import *
from Utility.Button import Button
import Utility.actions as act
from Utility.Player import Player
from Utility.Room import Room
from Utility.Item import Item
from Instantiations.Bedroom import *


def game_start(player: Player, window: GraphWin):
    update_window(player, window, gen_buttons(player, window))
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
        if b.is_pressed(click):
            cur_item = b.item
            s = b.func(player)
            print("clicked" + str(b))

    update_window(player, window, buttons, s)
    click_button(player, window, cur_item)


def update_window(player: Player, window: GraphWin, buttons, s=None):
    window.delete("all")  # remove all current things in window

    player_notes(player, window)  # redraw the left hand stuff
    context(player, window, s)  # redraw the top stuff

    for b in buttons:  # draw the buttons
        b.draw(window)

    window.update()


def gen_buttons(player: Player, window: GraphWin):
    objects = player.cur_room.objects
    # get current room
    # get objects in current room
    # make button for each object in room, the function for which should be the examine func
    buttons = []
    xdiff = 71.875
    x = 250 + xdiff
    ydiff = 43
    y = 187.5 + ydiff
    for i in range(len(objects)):
        o = objects[i]
        x += 3*xdiff
        if (i+1) % 4 == 0:
            y += 3*ydiff
            x = 250 + xdiff
        rect = Rectangle(Point(x,y), Point(x+2*xdiff, y + 2*ydiff))
        text = Text(Point((2*x + 2*xdiff)/2, (2*y + 2*ydiff)/2), o.name)
        b = Button(rect, text, o, o.get_examine)
        buttons.append(b)
    return buttons


# TODO: TEST GEN OBJECT BUTTONS
# returns a list of tuples (Rectangle, Text, Object related call)
# where the call is either to the object's interact or pickup text gen funcs
def gen_object_buttons(player: Player, window: GraphWin, item: Item):
    diff = 56.25
    left = 537.5
    right = 1112.5
    middle = (right + left) / 2

    interact_box = Rectangle(Point(left, 187.5 + diff), Point(right, 187.5 + 3*diff))
    interact_text = Text(Point(middle, (187.5 * 2 + 10 * diff) / 2), "Interact")

    pickup_box = Rectangle(Point(left, 187.5 + 4*diff), Point(right, 187.5 + 6*diff))
    pickup_text = Text(Point(middle, (187.5 * 2 + 16 * diff) / 2), "Pickup")

    return [Button(interact_box, interact_text, None, item.interact.getText),
            Button(pickup_box, pickup_text, None, act.pick_up(player, item))]


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


def context(player: Player, window: GraphWin, s):
    bar = window.getHeight() / 4
    top_line = Line(Point(250, bar), Point(window.getWidth(), bar))
    top_line.setWidth(4)
    top_line.draw(window)

    if s is None:
        context_string = player.cur_room.description
    else:
        context_string = s

    context_text = Text(Point(window.getWidth() / 2 + 125, window.getHeight() / 15), context_string)
    context_text.setSize(18)
    context_text.draw(window)


def main():
    player = Player()
    player.cur_room = Bedroom

    window = GraphWin("Cucumbers and Cookies", 1400, 750, autoflush=False)

    game_start(player, window)


if __name__ == '__main__':
    main()
