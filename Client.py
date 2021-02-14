import arcade, socket, json, math, traceback
from Board import Board
from CollisionCircle import Button, Popup
from Cursor import Cursor

WIDTH, HEIGHT, NAME = 800, 800, 'Tic Tac Toe'

class Game(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, NAME)

        arcade.set_background_color(arcade.color.WHITE)

        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.PORT = 5050
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'

        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.setblocking(1)
            self.client.connect(self.ADDR)
        except:
            pass

        self.board_draw = Board()
        self.board = {'7': ' ' , '8': ' ' , '9': ' ' ,
            '4': ' ' , '5': ' ' , '6': ' ' ,
            '1': ' ' , '2': ' ' , '3': ' '}

        self.button_list = []
        self.popup_list = []
        self.cursor = Cursor()

        self.client_ID = None

        self.my_turn = False
        self.game_over = False

        #SERVER REQUEST BOOLS
        self.board_request = False
        self.ID_request = False

        self.player_2 = False
        self.request_reset = False
        self.reset_state = False
        self.clear_state = False

        self.winner = None

        self.popup = Popup(WIDTH/2, HEIGHT/2 - HEIGHT/4, 1)
        self.game_over_popup = Popup(WIDTH/2, HEIGHT/2 - HEIGHT/4, 2)
        self.restart_popup = Popup(WIDTH/2, HEIGHT/2 - HEIGHT/2.5, 3)
        self.popup_list.append(self.restart_popup)

        for x in range(1, 10):
            button = Button(x)
            self.button_list.append(button)

    def col_circle_square(self, tx, ty, tr, cx, cy, cr):
        dx = tx - cx
        dy = ty - cy
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < tr + cr:
            return True

    def detect_collision(self, rect1, rect2):
        if (rect1[0] < rect2[0] + rect2[2]
                and rect1[0] + rect1[2] > rect2[0]
                and rect1[1] < rect2[1] + rect2[3]
                and rect1[1] + rect1[3] > rect2[1]):
            return True

    def decode_board(self, msg):
        utf_json = msg.decode(self.FORMAT)
        json_list = json.loads(utf_json)
        return json_list

    def clear_board(self):
        for x in self.board:
            if self.board[str(x)] == 'X' or self.board[str(x)] == 'O':
                self.board[str(x)] = " "

    def clear_game(self):
        try:
            if self.clear_state:
                msg = '!c'
                self.client.send(msg.encode(self.FORMAT))

                reply = self.client.recv(16)
                reply_decode = reply.decode(self.FORMAT)

                if reply_decode == '!r':
                    self.clear_board()
                    self.game_over = False
                    self.clear_state = False
                    if self.client_ID == 2:
                        self.my_turn = False



        except Exception as e:
            print(e)

    def check_win(self):
        print('2')
        try:
            if not self.clear_state:
                msg = '!w'
                self.client.send(msg.encode(self.FORMAT))
                reply = self.client.recv(128)
                reply_decode = reply.decode(self.FORMAT)

                if reply_decode == 'X':
                    self.winner = 'X'
                    self.game_over = True
                elif reply_decode == 'O':
                    self.winner = 'O'
                    self.game_over = True
                elif reply_decode == '!p':
                    self.game_over = False
                elif reply_decode == '!o':
                        self.game_over = True


        except Exception as e:
            print(e)

    def player_2_connected(self):
        try:
            if self.client_ID == 1:
                if not self.player_2:
                    msg = '!p'
                    self.client.send(msg.encode(self.FORMAT))

                    reply = self.client.recv(2)
                    if reply.decode(self.FORMAT) == '!t':
                        self.player_2 = True
                    else:
                        self.player_2 = False
            elif self.client_ID == 2:
                self.player_2 = True

        except Exception as e:
            print(e)

    def send_board_request(self):
        print('4')
        try:
            if not self.board_request:
                msg = '!board'
                request = msg.encode(self.FORMAT)
                self.client.send(request)

                new_msg = self.client.recv(92)
                utf_string = new_msg.decode(self.FORMAT)
                json_list = json.loads(utf_string)

                self.board = json_list[0]
                self.board_request = True

        except:
            traceback.print_exc()

    def send_ID_request(self):
        try:
            if not self.client_ID:
                msg = '!ID'
                request = msg.encode(self.FORMAT)
                self.client.send(request)

                new_msg = self.client.recv(6)
                message = new_msg.decode(self.FORMAT)
                self.client_ID = int(message)

        except Exception as e:
            pass

    def request_turn(self):
        print('6')
        try:
           if not self.my_turn:
               if self.client_ID:
                   if self.client_ID == 1:
                       msg = '!t1'
                   else:
                       msg = '!t2'

                   self.client.send(msg.encode(self.FORMAT))
                   reply = self.client.recv(2)
                   decoded_reply = reply.decode(self.FORMAT)

                   if decoded_reply == '!t':
                       self.my_turn = True
                       self.board_request = False
                   else:
                       self.my_turn = False

                   self.check_win()


        except Exception as e:
            print(e)

    def on_draw(self):
        arcade.start_render()

        self.board_draw.draw()

        for button in self.button_list:
            button.draw()

        self.cursor.draw()

        if self.client_ID == 1:
            if not self.my_turn or not self.player_2:
                if not self.game_over:
                    self.popup.draw()
        elif self.client_ID == 2:
            if not self.my_turn:
                if not self.game_over:
                    self.popup.draw()

        if self.game_over:
            self.game_over_popup.draw()
            self.restart_popup.draw()

        arcade.finish_render()

    def update(self, delta_time: float):
        self.cursor.update(self._mouse_x, self._mouse_y)

        self.player_2_connected()
        self.send_ID_request()

        if not self.clear_state:
            self.request_turn()
            self.send_board_request()
        elif self.clear_state:
            self.clear_game()

        for button in self.button_list:
            button.update(self.board)

        self.restart_popup.update(self.cursor)


    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if self.my_turn and not self.game_over:
            if self.player_2:
                if button == 1:
                    c = self.cursor
                    for button in self.button_list:
                        if button.value == button.B:
                            if self.col_circle_square(button.x, button.y, button.r, c.x, c.y, c.r):
                                col_list = []
                                col_list.append(button)
                                if (len(col_list) > 1):
                                    col_list.RemoveRange(0, col_list.count() - 1)

                                com = '!sub'
                                com_encode = com.encode(self.FORMAT)
                                self.client.send(com_encode)
                                msg = str(col_list[0].ID)
                                self.client.send(msg.encode(self.FORMAT))
                                col_list.clear()
                                self.my_turn = False
                                self.board_request = False
        elif self.game_over:
            if self.restart_popup.colliding:
                self.clear_state = True

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        pass
        '''for button in self.button_list:
            if button.dragging:
                button.x, button.y = self.cursor.x, self.cursor.y'''

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass
        '''for button in self.button_list:
            if button.dragging:
                print(button.ID, button.x, button.y)
                button.dragging = False'''

def main():
    window = Game()
    arcade.run()

if __name__ == '__main__':
    main()