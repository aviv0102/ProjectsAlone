/* aviv shisman 206558157
 * nadav gross 206844920
 */
using ImageService.Logging;
using System.IO;
using System.Threading;
using System.Threading.Tasks;

/* the Directory Handler
 * implements IDirectory Handler
 */
namespace ImageService.Controller.Handlers
{
	public class DirectoryHandler : IDirectoryHandler
	{

		//members:
		private string Dirpath;
		private string OutputPath;
		private string ThumbNailPath;
		private FileSystemWatcher watcher;
		private IImageController imageController;
        private ILoggingService log;
        private static Mutex Mymutex = new Mutex();

        //creating the handler and the output directory+thumbnails directory
        public DirectoryHandler(string p,string output, IImageController image,ILoggingService logger)
		{
			Dirpath = p;
			CreateOutPutDir(output);
			watcher = new FileSystemWatcher(Dirpath);
            imageController = image;
            log = logger;
		}

		/* creating a hidden directory in the path
         * if path is not legal printing warning to user
         */
		public void CreateOutPutDir(string path)
		{
			if (Directory.Exists(path))
			{
				//create a directory and making it hidden...
				OutputPath = path + "\\OutputDirectory";
				DirectoryInfo di = Directory.CreateDirectory(OutputPath);
				di.Attributes = FileAttributes.Directory | FileAttributes.Hidden;

				//creating thumbnails directory
				ThumbNailPath = OutputPath + "\\Thumbnails";
				DirectoryInfo d = Directory.CreateDirectory(ThumbNailPath);
			}
			else
			{
				System.Console.WriteLine("Path not exist or wrong format");
				System.Console.WriteLine("check that the path is in the right format for c#");

			}
		}

        //activate the handler
		public void listen()
		{
			watcher.Created += Watcher_Created;
			watcher.Renamed += Watcher_Created;

			watcher.EnableRaisingEvents = true;

		}

        //the method invoked if something was created in the directory
		private void Watcher_Created(object sender, FileSystemEventArgs e)
		{
            Mymutex.WaitOne();

            //if the file created is an image active the new file command 
			if (e.Name.Contains("jpg") || e.Name.Contains("png") || e.Name.Contains("bmp") || e.Name.Contains("gif"))
            {   
                string[] array = { e.FullPath,OutputPath };
                bool result;

                
                //active the new file command(uses the addfile method in imageModal)
                imageController.ExecuteCommand(0, array, out result);

               
                //checking results
                if(result == true)
                {
                    log.Log("Success in adding new file",Logging.Modal.MessageTypeEnum.INFO);

                }
                if(result==false)
                {
                    log.Log("Failure in adding new file", Logging.Modal.MessageTypeEnum.FAIL);
                }
			}
            Mymutex.ReleaseMutex();
		}

        //close the watcher
		public void close()
		{
			watcher.EnableRaisingEvents = false;
            
		}

        //get the path of the directory
		public string getPath()
		{
			return this.Dirpath;
		}


       
    }
	
}
