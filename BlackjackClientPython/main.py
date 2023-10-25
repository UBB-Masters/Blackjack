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
    # Connection is established, proceed with the interaction
    print("Connection established. Proceed with the game.")

    # Main game loop
    while True:
        # Receive and display the game state from the server
        game_state = client.recv(1024).decode()
        print("Game State:", game_state)

        # Check if it's the player's turn (you can modify this based on your game's logic)
        if "Your Turn" in game_state:
            action = input("Enter your action (hit or stand): ")
            client.send(action.encode())

        # Check if the game is over
        if "Game Over" in game_state:
            print("Game Over. Thank you for playing!")
            break

    # Close the client socket when the game is finished
    client.close()
