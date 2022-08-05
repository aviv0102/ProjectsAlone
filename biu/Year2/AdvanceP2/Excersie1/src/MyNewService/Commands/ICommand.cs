/* aviv shisman 206558157
 * nadav gross 206844920
 */
using ImageService.Infrastructure.Enums;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/* the command Interface
 * each command has execute method
 */
namespace ImageService.Commands
{
    public interface ICommand
    {
        string Execute(string[] args, out bool result);          // The Function That will Execute The 
    }
}
