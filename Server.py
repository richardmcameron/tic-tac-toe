import socket, json, random, time
from _thread import *

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

client_list = []
dispatch_list = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

board = {'7': ' ' , '8': ' ' , '9': ' ' ,
            '4': ' ' , '5': ' ' , '6': ' ' ,
            '1': ' ' , '2': ' ' , '3': ' '}

board_to_list = [board]
count = [0]
client_turn = [1]

players_request_reset = [False, False]

try:
    print("[BIND ATTEMPT]...")
    server.bind(ADDR)
    print("[BIND SUCCESSFULL]")
except:
    print("[BIND FAILURE]...")

def decode_message():
    pass

def encode_board():
    msg = board_to_list
    msg_json = json.dumps(msg)
    json_utf = msg_json.encode(FORMAT)
    return json_utf

def check_space(space):
    if space == 'X':
        return 'X'
    else:
        return 'O'


def handle_client(conn, addr):
    connected = True

    ID = 1 + len(client_list)
    print('\n')
    print(f'[NEW CONNECTION]...')
    print(f'[CONNECTED] Client: {ID}')
    print('\n')

    client_list.append({'connection': conn, 'ID': ID})

    if ID > 2:
        conn.close()
        print(f'[CLIENT {ID} DISCONNECTED]')
        print('[TOO MANY CONNECTIONS]')

    while connected:

        print('\n')
        print(board)
        print(client_turn)
        print(players_request_reset[0], players_request_reset[1])
        print('\n')

        c = conn.recv(256)
        msg = c.decode(FORMAT)

        if msg == '!p':
            print('!p')
            if len(client_list) > 1:
                msg = '!t'
            else:
                msg = '!f'
            conn.send(msg.encode(FORMAT))

        if msg == '!board':
            print('!board')
            conn.send(encode_board())

        if msg == '!ID':
            print('!ID')
            conn.send(str(ID).encode(FORMAT))

        if msg == '!sub':
            print('!sub')
            if ID == 1:
                c = conn.recv(256)
                dic_index = c.decode(FORMAT)
                board[dic_index] = 'X'
                client_turn[0] = 2

            if ID == 2:
                c = conn.recv(256)
                dic_index = c.decode(FORMAT)
                board[dic_index] = 'O'
                client_turn[0] = 1

        if msg == '!t1':
            print('!t1')
            if client_turn[0] == 1:
                reply = '!t'
            else:
                reply = '!f'

            conn.send(reply.encode(FORMAT))

        if msg == '!t2':
            print('!t2')
            if client_turn[0] == 2:
                reply = '!t'
            else:
                reply = '!f'

            conn.send(reply.encode(FORMAT))

        if msg == '!w':
            print('!w')
            if count == 9:
                reply = '!o'

            elif count[0] < 9:
                if board['7'] == board['8'] == board['9'] != ' ': # across the top
                    reply = check_space(board['7'])
                elif board['4'] == board['5'] == board['6'] != ' ': # across the middle
                    reply = check_space(board['4'])
                elif board['1'] == board['2'] == board['3'] != ' ': # across the bottom
                    reply = check_space(board['1'])
                elif board['1'] == board['4'] == board['7'] != ' ': # down the left side
                    reply = check_space(board['1'])
                elif board['2'] == board['5'] == board['8'] != ' ': # down the middle
                    reply = check_space(board['2'])
                elif board['3'] == board['6'] == board['9'] != ' ': # down the right side
                    reply = check_space(board['3'])
                elif board['7'] == board['5'] == board['3'] != ' ': # diagonal
                    reply = check_space(board['7'])
                elif board['1'] == board['5'] == board['9'] != ' ': # diagonal
                    reply = check_space(board['1'])
                else:
                    reply = '!p'
                conn.send(reply.encode())

        if msg == '!c':

            for x in board:
                if board[str(x)] == 'X' or board[str(x)] == 'O':
                    board[str(x)] = " "

            client_turn[0] = 1

            reply = '!r'
            conn.send(reply.encode(FORMAT))

    conn.close()


def start():
    server.listen(2)
    print(f'[SERVER LISTENING] {SERVER}')
    while True:
        conn, addr = server.accept()
        start_new_thread(handle_client, (conn, addr,))

print("[SERVER STARTING]...")
start()