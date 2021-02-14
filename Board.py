import arcade

WIDTH, HEIGHT= 800, 800

class Board:

    def draw(self):
        arcade.draw_line(WIDTH/4, HEIGHT - HEIGHT/4, WIDTH - WIDTH/4, HEIGHT - HEIGHT/4, arcade.color.BLACK, 20)
        arcade.draw_line(WIDTH/4, HEIGHT - HEIGHT/2, WIDTH - WIDTH/4, HEIGHT - HEIGHT/2, arcade.color.BLACK, 20)

        arcade.draw_line(WIDTH/2.5, HEIGHT/3, WIDTH/2.5, HEIGHT - HEIGHT/9, arcade.color.BLACK, 20)
        arcade.draw_line(WIDTH - WIDTH/2.5, HEIGHT / 3, WIDTH - WIDTH/2.5, HEIGHT - HEIGHT / 9, arcade.color.BLACK, 20)
