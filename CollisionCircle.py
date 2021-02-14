import arcade, math, random

class Button:

    def __init__(self, ID):
        self.x = 0
        self.y = 0
        self.r = 60
        self.ID = ID
        self.showing = True
        self.dragging = False
        self.color = arcade.color.NEON_GREEN
        self.X = arcade.load_texture('o.png')
        self.O = arcade.load_texture('x.png')
        self.B = arcade.load_texture('blank.png')
        self.value = self.B

    def col_circle_square(self, tx, ty, tr, cx, cy, cr):
        dx = tx - cx
        dy = ty - cy
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < tr + cr:
            return True

    def draw(self):
        #arcade.draw_circle_outline(self.x, self.y, self.r, self.color)
        #arcade.draw_rectangle_outline(self.x, self.y, self.r * 2, self.r * 2, self.color)

        arcade.draw_texture_rectangle(self.x, self.y, 80, 80, self.value)

    def update(self, board):

        for x in board:
            i = str(x)
            if self.ID == int(x):
                if board[x] == 'X':
                    self.value = self.X
                elif board[x] == 'O':
                    self.value = self.O
                else:
                    self.value = self.B

        if self.x == 0 or self.y == 0:
            if self.ID == 1:
                self.x, self.y = 250, 330

            if self.ID == 2:
                self.x, self.y = 400, 330

            if self.ID == 3:
                self.x, self.y = 550, 330

            if self.ID == 4:
                self.x, self.y = 250, 500

            if self.ID == 5:
                self.x, self.y = 400, 500

            if self.ID == 6:
                self.x, self.y = 550,500

            if self.ID == 7:
                self.x, self.y = 250, 670

            if self.ID == 8:
                self.x, self.y = 400,670

            if self.ID == 9:
                self.x, self.y = 550,670

class Popup:

    def __init__(self, x, y, ID):
        self.x = x
        self.y = y
        self.ID = ID
        self.w = 600
        self.h = 100
        self.rect = None
        self.colliding = False

    def draw(self):
        if self.ID == 1:
            arcade.draw_rectangle_filled(self.x, self.y, self.w, self.h, (128, 128, 128, 240))
            arcade.draw_rectangle_outline(self.x, self.y, self.w, self.h, arcade.color.BLACK)
            arcade.draw_text("Waiting...", self.x - 128, self.y - 48, arcade.color.WHITE, 64)

        if self.ID == 2:
            arcade.draw_rectangle_filled(self.x, self.y, self.w, self.h, (128, 128, 128, 240))
            arcade.draw_rectangle_outline(self.x, self.y, self.w, self.h, arcade.color.BLACK)
            arcade.draw_text("Game Over", self.x - 192, self.y - 48, arcade.color.RED, 64)

        if self.ID == 3:
            arcade.draw_rectangle_filled(self.x, self.y, self.w, self.h, (128, 128, 128, 240))
            arcade.draw_text("Restart?", self.x - 160, self.y - 48, arcade.color.RED, 64)

            if not self.colliding:
                arcade.draw_rectangle_outline(self.x, self.y, self.w, self.h, arcade.color.BLACK)
            elif self.colliding:
                arcade.draw_rectangle_outline(self.x, self.y, self.w, self.h, arcade.color.YELLOW)

            #arcade.draw_rectangle_outline(self.rect[0] + self.w/2, self.rect[1] + self.h/2, self.rect[2], self.rect[3], arcade.color.NEON_GREEN)

    def detect_collision(self, rect1, rect2):
        if (rect1[0] < rect2[0] + rect2[2]
                and rect1[0] + rect1[2] > rect2[0]
                and rect1[1] < rect2[1] + rect2[3]
                and rect1[1] + rect1[3] > rect2[1]):
            return True

    def update(self, cursor):

        self.rect = [self.x - self.w/2, self.y - self.h/2, self.w, self.h]

        if self.ID == 3:
            if self.detect_collision(self.rect, cursor.rect):
                self.colliding = True
            else:
                self.colliding = False
