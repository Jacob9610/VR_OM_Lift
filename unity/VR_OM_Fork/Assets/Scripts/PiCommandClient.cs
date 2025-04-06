using System.Net.Sockets;
using System.Text;
using UnityEngine;

public class PiCommandClient
{
    private string host = "10.143.230.242"; // Pi IP
    private int port = 8000;

    public void SendCommand(string json)
    {
        try
        {
            using TcpClient client = new TcpClient(host, port);
            using NetworkStream stream = client.GetStream();
            byte[] data = Encoding.UTF8.GetBytes(json);
            stream.Write(data, 0, data.Length);
        }
        catch (SocketException e)
        {
            Debug.LogWarning($"Socket error: {e.Message}");
        }
    }
}
