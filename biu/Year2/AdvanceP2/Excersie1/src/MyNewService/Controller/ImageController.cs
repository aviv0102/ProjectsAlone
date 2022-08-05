/* aviv shisman 206558157
 * nadav gross 206844920
 */
using ImageService.Commands;
using ImageService.Infrastructure;
using ImageService.Infrastructure.Enums;
using ImageService.Modal;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/* the imageController
 * activates commands and connects between the image modal to the handler/server
 */
namespace ImageService.Controller
{
	public class ImageController : IImageController
	{   
        //members:
		private IImageServiceModal m_modal;                      
		private Dictionary<int, ICommand> commands;

		public ImageController(IImageServiceModal modal)
		{
			m_modal = modal;                    
			commands = new Dictionary<int, ICommand>();
			
            // adding newFile command to the dictionary
			NewFileCommand nfc = new NewFileCommand(modal);
			commands.Add(0, nfc);
		}

        //execute the command using the dictionary 
		public string ExecuteCommand(int commandID, string[] args, out bool result)
		{
			if (!commands.ContainsKey(commandID))
			{
                throw new Exception(" command not found");
				
			}
			ICommand command = commands[commandID];
			command.Execute(args, out bool r);

            result = r;
			return result.ToString();
		}
	}
}