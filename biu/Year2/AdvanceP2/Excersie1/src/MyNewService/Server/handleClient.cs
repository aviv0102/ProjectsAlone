/* aviv shisman 206558157
 * nadav gross 206844920
 */


using ImageService.Controller.Handlers;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Net.Sockets;
using System.Threading;

/* client handler-> takes care of each client connected
 * talk with the client and update server if command was recived(via eventes)
 */
namespace MyNewService.Server
{
    class handleClient
    {   
        //members for the tcp connection
        private TcpClient clientSocket;
        private NetworkStream stream;
        private BinaryReader reader;
        private BinaryWriter writer;
        private List<IDirectoryHandler> handlers;

        //starting the client handler(no con)-> creating thread for each one
        public void startClient(TcpClient inClientSocket, List<IDirectoryHandler> h)

        {   
            this.clientSocket = inClientSocket;
            this.handlers = h;

            Thread ctThread = new Thread(Communicate);
            ctThread.Start();
            
        }

        /* begin communication with client
         * get From him the images and store them on our service
         */
        private void Communicate()
        {
            this.stream = clientSocket.GetStream();
            this.reader = new BinaryReader(stream);
            this.writer = new BinaryWriter(stream);

            bool stop = false;

            //checking connection
            CheckConnectionToApp();
            while (!stop)
            {
                //gettin pic name
                string name= getPictureName();
                if (name == null || name=="") { continue; }
                if (name.Contains("end"))
                {
                    break;
                }
                //getting pic
                byte[] photo = getPicture();
                Console.WriteLine("Got image :" + name);
                
                //move to handler
                string pathOld = this.handlers[0].getPath() + "\\" +name+"1"+".png";
                string path= this.handlers[0].getPath() + "\\" + name  + ".png";
                try
                {
                    File.WriteAllBytes(pathOld, photo);
                    System.IO.File.Move(pathOld, path);
                }
                catch (Exception e)
                {

                }

                Console.WriteLine(" image was moved :" + name);
            }


            Console.ReadLine();

        }
        
        /* get the picture name from client
         * byte by byte, return the extracted from them
         */
        public string getPictureName()
        {
            writer.Write(1);
            List<Byte> byteList = new List<Byte>();
            Byte[] b = new Byte[1];
            do
            {
                stream.Read(b, 0, 1);
                byteList.Add(b[0]);
            } while (stream.DataAvailable);
            return Path.GetFileNameWithoutExtension(System.Text.Encoding.UTF8.GetString(byteList.ToArray()));
        }


        /* get the picture by bytes
         * later will be converted to image itself
         */
        public byte[] getPicture()
        {
            writer.Write(1);
            int i = 0;
            List<Byte> byteList = new List<Byte>();
            Byte[] b = new Byte[1];
            do
            {
                i = stream.Read(b, 0, b.Length);
                byteList.Add(b[0]);
            } while (stream.DataAvailable);
            writer.Write(1);


            return byteList.ToArray();

        }

      
        /*
         * check the connection
         */
        public void CheckConnectionToApp()
        {
            int a = 1,b = 2, c = 3, d = 4;
            writer.Write(a);
            reader.ReadInt32();
            writer.Write(b);
            reader.ReadInt32();
            writer.Write(c);
            reader.ReadInt32();
            writer.Write(d);
            reader.ReadInt32();
        }
        
      


        

    }
}

