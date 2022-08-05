using System;
using System.Configuration;
using System.Diagnostics;
using System.Linq;
using System.ServiceProcess;
using System.Runtime.InteropServices;
using ImageService.Server;
using ImageService.Modal;
using ImageService.Controller;
using ImageService.Logging;
using ImageService.Logging.Modal;

namespace MyNewService
{
	public enum ServiceState
	{
		SERVICE_STOPPED = 0x00000001,
		SERVICE_START_PENDING = 0x00000002,
		SERVICE_STOP_PENDING = 0x00000003,
		SERVICE_RUNNING = 0x00000004,
		SERVICE_CONTINUE_PENDING = 0x00000005,
		SERVICE_PAUSE_PENDING = 0x00000006,
		SERVICE_PAUSED = 0x00000007,
	}

	[StructLayout(LayoutKind.Sequential)]
	public struct ServiceStatus
	{
		public int dwServiceType;
		public ServiceState dwCurrentState;
		public int dwControlsAccepted;
		public int dwWin32ExitCode;
		public int dwServiceSpecificExitCode;
		public int dwCheckPoint;
		public int dwWaitHint;
	};

	public partial class ImageService : ServiceBase
	{
		//private System.ComponentModel.IContainer components;
		//private System.Diagnostics.EventLog eventLog1;
		private int eventId = 1;
		private ImageServer server;
        private IImageServiceModal imageServiceModal;
		private ILoggingService loggingService;
		private IImageController imageController;

		public ImageService(string[] args)
		{
			InitializeComponent();
			string eventSourceName = ConfigurationManager.AppSettings.Get("SourceName");
			string logName = ConfigurationManager.AppSettings.Get("LogName");
			if (args.Count() > 0)
			{
				eventSourceName = args[0];
			}
			if (args.Count() > 1)
			{
				logName = args[1];
			}
			eventLog1 = new System.Diagnostics.EventLog();
			if (!System.Diagnostics.EventLog.SourceExists(eventSourceName))
			{
				System.Diagnostics.EventLog.CreateEventSource(eventSourceName, logName);
			}
			eventLog1.Source = eventSourceName;
			eventLog1.Log = logName;
		}

		protected override void OnStart(string[] args)
		{
			// Update the service state to Start Pending.  
			ServiceStatus serviceStatus = new ServiceStatus();
			serviceStatus.dwCurrentState = ServiceState.SERVICE_START_PENDING;
			serviceStatus.dwWaitHint = 100000;
			SetServiceStatus(this.ServiceHandle, ref serviceStatus);
			eventLog1.WriteEntry("Service Starts");
            
        

            // Set up a timer to trigger every minute.  
            System.Timers.Timer timer = new System.Timers.Timer();
			timer.Interval = 60000; // 60 seconds  
			timer.Elapsed += new System.Timers.ElapsedEventHandler(this.OnTimer);
			timer.Start();

			// Update the service state to Running.  
			serviceStatus.dwCurrentState = ServiceState.SERVICE_RUNNING;
			SetServiceStatus(this.ServiceHandle, ref serviceStatus);

            //Logging Service + adding Event in case message been recived
            this.loggingService = new LoggingService();
            loggingService.MessageRecieved += MessagePop;

            //creating all classes
            int size = int.Parse(ConfigurationManager.AppSettings.Get("ThumbnailSize"));
            this.imageServiceModal = new ImageServiceModal(size);
            this.imageController = new ImageController(imageServiceModal);
			this.server = new ImageServer(imageController, loggingService);
           
            //update gui's log:
            //string res = "Service Starts;WARNING";
            //this.server.addLog(res); no need in Java App

            // creating handlers
            string outPut = ConfigurationManager.AppSettings.Get("OutputDir");
            string str = ConfigurationManager.AppSettings.Get("Handler");
            string[] directories = str.Split(';');
            foreach (string dir in directories)
            {
                server.AddHandler(dir, outPut);
            }

            //start server
            this.server.startServer();

        }

        private void MessagePop(object s, MessageRecievedEventArgs e)
        {
            //update gui's log:
            string res = e.Message + ";" + e.Status;
            //this.server.addLog(res); no need in java app
            //update log
            this.eventId++;
            string logS = e.Message + " with status " + e.Status;
            eventLog1.WriteEntry(logS, EventLogEntryType.Information, this.eventId);
        }
		protected override void OnStop()
        {   //update gui's log:
            //string res = "Stopping Service;WARNING";
           // this.server.addLog(res); no need in java app


            eventLog1.WriteEntry("Stopping Service");
            server.close();
		}

		public void OnTimer(object sender, System.Timers.ElapsedEventArgs args)
		{
            //update gui's log:
          //  string res = "still monitoring service;INFO";
          //  this.server.addLog(res); no need in java app

            eventLog1.WriteEntry("still monitoring service", EventLogEntryType.Information, eventId++);
		}

		protected override void OnContinue()
        {  //update gui's log:
          //  string res = "In OnContinue.;INFO";
          //  this.server.addLog(res); no need in java app


            eventLog1.WriteEntry("In OnContinue.");
		}

		[DllImport("advapi32.dll", SetLastError = true)]
		private static extern bool SetServiceStatus(IntPtr handle, ref ServiceStatus serviceStatus);
	}
}
