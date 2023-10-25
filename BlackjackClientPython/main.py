import socket

# Define the server's IP address and port
server_ip = 'YOUR_SERVER_IP'  # Replace with the actual server IP address
server_port = 9999  # Use the same port as the server

# Create a socket to connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

while True:
    # Receive and display server messages
    message = client.recv(1024).decode()
    print(message)

    if 'Welcome' in message:
        # Send player actions (hit, stand, double_down, or quit)
        action = input("Enter your action (hit, stand, double_down, or quit): ")
        client.send(action.encode())

    elif 'Bust' in message or 'Stand' in message:
        # Player turn is done; wait for the other player's turn
        pass
