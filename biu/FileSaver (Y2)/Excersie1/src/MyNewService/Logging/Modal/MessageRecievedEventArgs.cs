/* aviv shisman 206558157
 * nadav gross 206844920
 */
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/* we Used this class to notify the logger
 * if message has been recived
 * if we got a message event will be invoked in messagePop(in ImageService)
 */
namespace ImageService.Logging.Modal
{  
   
     public class MessageRecievedEventArgs : EventArgs
    {
		private MessageTypeEnum type;

		public MessageRecievedEventArgs(MessageTypeEnum type, string message)
		{
			this.type = type;
			Message = message;
		}

		public MessageTypeEnum Status { get; set; }
        public string Message { get; set; }
    }
}
