/* aviv shisman 206558157
 * nadav gross 206844920
 */
using ImageService.Logging.Modal;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/* the Logging Service Interface
 * Log - notify the logger with message and type of message
 * MessageRecived- create an event if message been recived to logger
 */ 
namespace ImageService.Logging
{
    public interface ILoggingService
    {
        event EventHandler<MessageRecievedEventArgs> MessageRecieved;
        void Log(string message, MessageTypeEnum type);           // Logging the Message
    }
}
