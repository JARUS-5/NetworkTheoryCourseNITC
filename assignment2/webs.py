
import socket

#LOCALHOST, PORT 8001, port arbitrarily chosen
HOST, PORT = '',8001

listen_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM)#Craete a socket
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST,PORT)) #Bind to aforementioned port and host
listen_socket.listen(1) #listen for requests

print(f"Serving http on {PORT}")

while True:
    client_connection, client_address = listen_socket.accept() #wait until request recieved
    print(f"Connection recieved from {client_address}")

    request_data = client_connection.recv(1024) #read request
    print(request_data.decode('utf-8')) 

    http_response = b'HTTP/1.0 200 OK\n\n' #HTTP response header
    f = open('homepage.html','rb') #Open html file to send to client
    http_response += f.read(); #Add html code to response
    print("Printing response \n\n\n", http_response)
    f.close()
    client_connection.sendall(http_response) #Send html page to client
    client_connection.close() 
