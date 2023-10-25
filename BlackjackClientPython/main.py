import socket

# Define the server's IP address and port
server_ip = '10.152.0.236'  # Replace with the actual server IP address
server_port = 9999  # Use the same port as the server

# Create a socket to connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

# Implement the handshake mechanism
client.send("ping".encode())
response = client.recv(1024).decode()

if response == "pong":
    print("Connection established. Proceed with the interaction.")
else:
    print("Connection failed.")
    client.close()
