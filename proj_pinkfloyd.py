import socket 
import select
import data as dt

LISTEN_PORT = 51
ERROR_NUM = 500
#the password <Magsh1m!m#>
PASSWORD = '698d60ae40ad03bb179010488d33089a757aaa1f8e62e425b097eadab917d8fd'
PASSWORD_MSG = 'Please enter the password: '
LOGIN_MSG = 'You haved connected to the server'
ERROR_PASS = '504#Invalid password!'

OP_1 = '201#List of all album of Pink-Floyd: \n'
OP_2 = '202#List of songs in album '
OP_3 = '203#Length of song '
OP_4 = '204#Lyric of song '
OP_5 = '205#Name of the album: '
OP_6 = '206#Songs names by the word in the name: \n'
OP_7 = '207#Songs names by the word in the lyrics: \n'
OP_8 = '208#Goodbye'
ERROR_MSG = '500#ERROR!'
NOT_FOUND = '502#Not found!'

def opening_and_options() -> str:
    '''
    The func prints the intro and the menu of options
    :return: intro and menu
    :rtype: string
    '''
    return "Welcome to 'Know All About Pink-Floyd'\nHeres the options that we have:\n1 - List of albums.\n2 - List of songs in album.\n3 - Length of song.\n4 - Words in the song.\n5 - Which album the song existing.\n6 - Find the song by the word in the song name.\n7 - Find the song by the word in the lyrics.\n8 - Exit.\n"

def is_exited(client_msg):
    '''
    The func is checking if the client exited from the conversation
    :param client_msg: msg from the client
    :type client_msg: str
    :return: does exited 
    :rtype: bool
    '''
    if client_msg == '':
        return True
    return False

def splitting_msg(client_msg) -> str:
    '''
    The func splits the message from the client
    :param client_msg: the query
    :type client_msg: string
    :return: only the msg without the option
    :rtype: string
    '''
    try:
        client_msg = client_msg.split('#')
        return client_msg[1]
    except Exception:
        ERROR_MSG.split('#')
        return ERROR_MSG[1]

def client_op(client_msg) -> int:
    '''
    The func finds the option of the client
    :param client_msg: the query
    :type client_msg: string
    :retrun: the option
    :rtype: int
    '''
    for i in range(101, 109):
        if (str(i)+'#') in client_msg:
            return i
    return ERROR_NUM

def which_func(op,client_msg) -> str:
    '''
    The func is find the option and returns appropriate message
    :param op: option
    :param client_msg: the msg from the client
    :type op: int
    :type client_msg: string
    :return: the message by the option
    :rtype: string
    '''
    client_msg = splitting_msg(client_msg)
    
    if op == 101:
        return OP_1 + dt.get_all_albums() 
    
    elif op == 102:
        if dt.does_album_in_dict(client_msg) == False:
            return NOT_FOUND
        all_songs = dt.get_all_songs(client_msg)
        if len(all_songs) == 0:
            return NOT_FOUND
        return OP_2 +'"' + client_msg + '"' + ': \n' + all_songs
    
    elif op == 103:
        if dt.does_song_in_dict(client_msg) == False:
            return NOT_FOUND
        song_len = dt.get_song_len(client_msg) 
        if len(song_len) == 0:
            return NOT_FOUND
        return OP_3 +'"' + client_msg + '"' + ': \n' + song_len
    
    elif op == 104:
        if dt.does_song_in_dict(client_msg) == False:
            return NOT_FOUND
        lyrics = dt.get_lyrics(client_msg)
        if len(lyrics) == 0:
            return NOT_FOUND
        return OP_4 + '"' + client_msg + '"' + ': \n' + dt.get_lyrics(client_msg) 
    
    elif op == 105:
        if dt.does_song_in_dict(client_msg) == False:
            return NOT_FOUND
        find_album = dt.find_album(client_msg)
        if len(str(find_album)) == 0:
            return NOT_FOUND
        return OP_5 + str(find_album)
    
    elif op == 106:
        find_name = dt.find_by_name(client_msg)
        if len(find_name) == 0:
            return NOT_FOUND
        return OP_6 + find_name
    
    elif op == 107:
        find_name1 = dt.find_by_lyrics(client_msg)
        if len(find_name1) == 0:
            return NOT_FOUND
        return OP_7 + find_name1
    
    elif op == 108:
        return OP_8
    
    else:
        return ERROR_MSG

def pinkfloyd_server():
    '''
    The server of pink-floyd
    '''
    logged_in = False
    was_error = False

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        server_address = ('', LISTEN_PORT)
        sock.bind(server_address)
        sock.listen(5)
        sockets = [sock]
        while True:
            readable, writable, exceptional = select.select(sockets, [], [])
            for s in readable:
                if s is sock:
                    client_soc, client_address = s.accept()
                    sockets.append(client_soc)

                    #checking the password of the client
                    if logged_in == False:
                        client_soc.sendall(PASSWORD_MSG.encode())
                        client_msg = client_soc.recv(1024).decode()
                        if is_exited(client_msg):
                            continue
                        if client_msg != PASSWORD:
                            client_soc.sendall(ERROR_PASS.encode())
                            exit()
                        else:
                            client_soc.sendall(LOGIN_MSG.encode())
                        logged_in = True
                    
                    #sending server's options
                    if was_error == False:
                        client_soc.sendall(opening_and_options().encode())
                    else:
                        nothing = ' '
                        client_soc.sendall(nothing.encode())

                    client_msg = (client_soc.recv(1024)).decode()
                    if is_exited(client_msg):
                        continue

                    #checking the option of client and sending appropriate message
                    op = client_op(client_msg)
                    msg = which_func(op, client_msg)

                    #checking if option is exit
                    if OP_8 == msg:
                        client_soc.sendall(msg.encode())
                        exit()
                    
                    #checking if the message from client is erroneous
                    if msg == ERROR_MSG:
                        was_error = True
                    else:
                        was_error = False

                    #sending the message that isn't error
                    client_soc.sendall(msg.encode())

def main():
    pinkfloyd_server()

if __name__ == "__main__":
    main()