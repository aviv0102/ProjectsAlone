/* aviv shisman 206558157
 * nadav gross 206844920
 */
using ImageService.Modal;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/* the iDriectoryHandler interface
 * has methods listen-activate the handler, close-close the handler and etc
 */ 
namespace ImageService.Controller.Handlers
{
    public interface IDirectoryHandler
    {
		void listen();
		void close();
		string getPath();
    }
}
