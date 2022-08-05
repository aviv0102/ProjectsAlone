/* aviv shisman 206558157
 * nadav gross 206844920
 */
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/*Types of messages to logger
 * INFO- info on system
 * Warning- somthing bad happened
 * FAIL- system will crash...
 */
namespace ImageService.Logging.Modal
{
    public enum MessageTypeEnum : int
    {
        INFO,
        WARNING,
        FAIL
    }
}
