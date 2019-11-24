from graphics import *
class Button:

    def __init__(self, rect: Rectangle, text: Text, item, function):
        self.rect = rect
        self.text = text
        self.item = item
        self.func = function

    def draw(self, window: GraphWin):
        self.rect.draw(window)
        self.text.draw(window)

    def is_pressed(self, click: Point):
        return self.rect.getP1().x < click.x < self.rect.getP2().x and \
               self.rect.getP1().y < click.y < self.rect.getP2().y
