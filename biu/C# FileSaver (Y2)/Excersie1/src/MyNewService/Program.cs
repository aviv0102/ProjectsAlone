using ImageService.Controller;
using ImageService.Controller.Handlers;
using ImageService.Logging;
using ImageService.Modal;
using ImageService.Server;
using System;
using System.Collections.Generic;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading.Tasks;

namespace MyNewService
{
	static class Program
	{
		/// <summary>
		/// The main entry point for the application.
		/// </summary>
		static void Main(string[] args)
		{
            ServiceBase[] ServicesToRun;
            ServicesToRun = new ServiceBase[]
            {
            	new ImageService(args)
            };

            ServiceBase.Run(ServicesToRun);


            // creating all classes
      


        }
    }
}
