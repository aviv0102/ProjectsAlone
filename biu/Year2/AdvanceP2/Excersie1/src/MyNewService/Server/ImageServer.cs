/* aviv shisman 206558157
 * nadav gross 206844920
 */

//using:
using ImageService.Controller;
using ImageService.Controller.Handlers;
using ImageService.Logging;
using MyNewService.Server;
using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Threading.Tasks;

/* the Server
 * has a list of handlers and maintains the handlers
 */
namespace ImageService.Server
{
    public class ImageServer
    {   
        //members:
        private IImageController controller;
        private ILoggingService logging;
        private List<IDirectoryHandler> handlers;
        private List<handleClient> clients;


        //constructor:
        public ImageServer(IImageController c, ILoggingService l)
        {
            handlers = new List<IDirectoryHandler>();
            clients = new List<handleClient>();
            controller = c;
            logging = l;
        }

        //add a handler to the list and activate it.
        public void AddHandler(string path,string output)
        {
            this.logging.Log("Creating handler in : " + path, Logging.Modal.MessageTypeEnum.INFO);
            DirectoryHandler d = new DirectoryHandler(path,output,controller,logging);
            handlers.Add(d);
            d.listen();
        }

        //tcp start:
        public void startServer()
        {
            IPEndPoint ep = new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8000);

            TcpListener serverSocket = new TcpListener(ep);

            serverSocket.Start();
            Console.WriteLine(" >> " + "Server Started");
         
            Task task = new Task(() => {
                while (true)
                {
                    try
                    {   //accapt a client and create handler for it
                        TcpClient clientSocket = serverSocket.AcceptTcpClient();
                        Console.WriteLine(" >> " + "Client No:" + " started!");
                        handleClient client = new handleClient();

                        //listen for any changes from client handler and add it to list(for brodcast)
                        this.clients.Add(client);

                        //start client handler
                        client.startClient(clientSocket,this.handlers);
                    }
                    catch (SocketException)
                    {
                        break;
                    }
                }
                Console.WriteLine("Server stopped");
            });
            task.Start();


            Console.ReadLine();
        }
        //close all handlers
        public void close()
        {
            foreach( DirectoryHandler d in handlers)
            {
                d.close();
            }
           


        }
    }
}