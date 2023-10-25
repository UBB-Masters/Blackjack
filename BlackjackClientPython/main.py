import socket

# Define the server's IP address and port
server_ip = '10.152.0.236'  # Replace with the actual server IP address
server_port = 9999  # Use the same port as the server

# Create a socket to connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

# Send a single "ping" to the server to establish the connection
client.send("ping".encode())

# Receive and display the response (pong)
response = client.recv(1024).decode()
print("Received:", response)

if response == "pong":
    # Connection is established, proceed with further interactions
    print("Connection established. Proceed with the interaction.")
