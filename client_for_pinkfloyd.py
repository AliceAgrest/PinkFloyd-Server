import socket
import hashlib

SERVER_IP = '127.0.0.1'
SERVER_PORT = 51

def encrypt_password(hash_s):
    '''
    The func hashing password of the client
    :param hash_s: client password
    :type hash_s: str
    :return: hashed password
    :rtype: str
    '''
    sha_signature = hashlib.sha256(hash_s.encode()).hexdigest()
    return sha_signature

def client_msg():
    '''
    The func is checking if the input wasn't Ctrl-c 
    :return: msg of client or collapsing the program
    :rtype: str
    '''
    try:
        msg = input()
        return msg
    except KeyboardInterrupt:
        #return 'exit'
        exit()

def client():
    '''
    Client for pink-floyd
    '''
    logged_in = False
    while True:
        server_msg = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            server_address = (SERVER_IP, SERVER_PORT)
            try:
                sock.connect(server_address)
            except Exception:
                exit()

            #getting the password message
            if logged_in == False:
                print(sock.recv(1024).decode())
                msg_client = client_msg()
                msg_client = encrypt_password(msg_client)
                sock.sendall(msg_client.encode())
                #sending and checking if valid
                server_msg = sock.recv(1024).decode()
                if 'Invalid' in server_msg:
                    print(server_msg)
                    exit()
                else:
                    print(server_msg)
                logged_in = True

            #getting the menu of the server and sending the option
            print(sock.recv(1024).decode())
            msg_client = client_msg()
            sock.sendall(msg_client.encode())

            #checking if we get a goodbye message
            server_msg = sock.recv(1024).decode()
            print(server_msg)
            if 'Goodbye' in server_msg:
                exit()

def main():
    client()

if __name__ == "__main__":
    main()