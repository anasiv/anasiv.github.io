#!/usr/bin/env python3
import socket, sys
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")
    
def main():
    
    proxy_host = 'www.google.com'
    proxy_port = 80
    proxy_payload = f'GET / HTTP/1.0\r\nHost: {proxy_host}\r\n\r\n'
        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            # create a new socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_to_google:
                
                remote_ip = get_remote_ip(proxy_host)
                s_to_google.connect((remote_ip , proxy_port))
                
                p = Process(target=handle_echo, args=(s_to_google, addr, conn))
                p.daemon = True
                p.start()                
                
            conn.close()

def handle_echo(s_to_google, addr, conn):
    #recieve data, wait a bit, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    s_to_google.sendall(full_data)
    s_to_google.shutdown(socket.SHUT_WR)
    
    data = s_to_google.recv(BUFFER_SIZE)
    conn.send(data)    
    
if __name__ == "__main__":
    main()
