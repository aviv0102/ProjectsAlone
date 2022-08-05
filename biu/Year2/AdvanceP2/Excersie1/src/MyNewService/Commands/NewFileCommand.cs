/* aviv shisman 206558157
 * nadav gross 206844920
 */
using ImageService.Infrastructure;
using ImageService.Modal;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/* the command that the handler uses to move the file from the directory we follow
 * implements the icommand interface
 */
namespace ImageService.Commands
{
    public class NewFileCommand : ICommand
    {   
        //members:
        private IImageServiceModal m_modal;

        //constructor:
        public NewFileCommand(IImageServiceModal modal)
        {
            m_modal = modal;            
        }

        //execute the command using the image modal
        public string Execute(string[] args, out bool result)
        {
			// The String Will Return the New Path if result = true, and will return the error message
			try
			{
				if (args.Length == 0)
				{
					throw new Exception("the array is not in the right length");
				}
				else if (File.Exists(args[0]))
				{
					m_modal.AddFile(args[0],args[1], out result);

				}
				result = true;
				return result.ToString();
			}
			catch (Exception e)
			{
				result = false;
				return e.ToString();
			}
        }
    }
}
