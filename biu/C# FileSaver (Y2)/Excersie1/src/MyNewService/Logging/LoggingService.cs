/* aviv shisman 206558157
 * nadav gross 206844920
 */
using ImageService.Logging.Modal;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/* the LoggingService
 * if a message been recived in Log function invoke the MessageRecivedEvent 
 */
namespace ImageService.Logging
{
    public class LoggingService : ILoggingService
    {   
        public event EventHandler<MessageRecievedEventArgs> MessageRecieved;
        public void Log(string message, MessageTypeEnum type)
        {
			MessageRecieved?.Invoke(this, new MessageRecievedEventArgs(type, message));
		}
	}
}
