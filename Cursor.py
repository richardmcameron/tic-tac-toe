import arcade
class Cursor:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.color = arcade.color.GRAY
        self.r = 5
        self.w = self.r*2
        self.h = self.r*2
        self.showing = True
        self.rect = None
        self.colliding = False

    def draw(self):
        if self.showing:
            arcade.draw_circle_filled(self.x, self.y, self.r, arcade.color.WHITE)
            arcade.draw_circle_outline(self.x, self.y, self.r, arcade.color.NEON_GREEN)

            arcade.draw_rectangle_outline(self.rect[0], self.rect[1], self.rect[2], self.rect[3], arcade.color.NEON_GREEN)

    def update(self, x, y):

        self.rect = [self.x, self.y, self.w, self.h]

        self.x = x
        self.y = y