using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

class BlackjackServer
{
    private const int Port = 9999;
    private const int MaxPlayers = 2;
    
    static void HandleClient(object clientObj)
    {
        TcpClient client = (TcpClient)clientObj;
        NetworkStream stream = client.GetStream();
        
        byte[] buffer = new byte[1024];
        int bytesRead = stream.Read(buffer, 0, buffer.Length);
        
        string receivedData = Encoding.ASCII.GetString(buffer, 0, bytesRead);
        try
        {
            object gameResult = CustomDeserialize(receivedData);
            Console.WriteLine("Dealer's Score: " + ((object[])gameResult)[0]);
            Console.WriteLine("Winning Players: " + string.Join(", ", ((object[])gameResult)[1]));
        }
        catch (Exception e)
        {
            Console.WriteLine("Error receiving and processing the game result: " + e.Message);
        }
        client.Close();
    }

    static object CustomDeserialize(string data)
    {
        // Implement your custom deserialization logic here
        // For instance, convert received data back to objects
        // This method should mirror Python's pickle.loads
        // Return deserialized objects
        // Example: For simplicity, assuming incoming data is a string, you can split and convert it into an object
        return data.Split(',');
    }

    static void Main()
    {
        TcpListener server = new TcpListener(IPAddress.Any, Port);
        server.Start();
        
        Console.WriteLine("Server is waiting for player connections...");
        int playerCount = 0;

        while (playerCount < MaxPlayers)
        {
            TcpClient client = server.AcceptTcpClient();
            playerCount++;

            string playerID = playerCount == 1 ? "Player 1" : (playerCount == 2 ? "Player 2" : "Spectator");
            IPEndPoint clientEndPoint = (IPEndPoint)client.Client.RemoteEndPoint;
            Console.WriteLine("Connected to " + playerID + " at address " + clientEndPoint.Address + ":" + clientEndPoint.Port);

            NetworkStream stream = client.GetStream();
            byte[] playerData = Encoding.ASCII.GetBytes(playerID + '\n');
            stream.Write(playerData, 0, playerData.Length);

            Thread clientThread = new Thread(new ParameterizedThreadStart(HandleClient));
            clientThread.Start(client);
        }

        server.Stop();
    }
}
