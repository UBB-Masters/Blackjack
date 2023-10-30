package org.example;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class BlackjackServer {
    private static final int MAX_PLAYERS = 2; // Maximum number of players

    public static void main(String[] args) {
        int playerCount = 0;
        ServerSocket serverSocket = null;
        try {
            serverSocket = new ServerSocket(9999); // Listening port
            System.out.println("Server is waiting for player connections...");

            while (playerCount < MAX_PLAYERS) {
                Socket client = serverSocket.accept();
                playerCount++;

                String playerID = "Spectator"; // If more than two players connect
                if (playerCount == 1) {
                    playerID = "Player 1";
                } else if (playerCount == 2) {
                    playerID = "Player 2";
                }

                System.out.println("Connected to " + playerID + " at address " + client.getRemoteSocketAddress());

                BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
                String playerIDData = in.readLine(); // Read the player ID sent by the client
                String gameResultData = in.readLine(); // Read the game result sent by the client

                System.out.println(playerIDData + ": " + gameResultData);

                Thread clientThread = new Thread(new HandleClient(client, playerIDData, gameResultData));
                clientThread.start();
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (serverSocket != null) {
                    serverSocket.close();
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}

class HandleClient implements Runnable {
    private final Socket client;
    private final String playerID;
    private final String gameResult;

    public HandleClient(Socket client, String playerID, String gameResult) {
        this.client = client;
        this.playerID = playerID;
        this.gameResult = gameResult;
    }

    @Override
    public void run() {
        try {
            System.out.println(playerID + ": " + gameResult);

            client.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}

