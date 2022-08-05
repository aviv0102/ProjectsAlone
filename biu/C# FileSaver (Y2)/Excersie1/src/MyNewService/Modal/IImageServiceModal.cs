/* aviv shisman 206558157
 * nadav gross 206844920
 */
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

/* the ImageServiceModal Interface
 */ 
namespace ImageService.Modal
{
    public interface IImageServiceModal
    {
        //add File from dir to thumbnails and outPutDir
        string AddFile(string path,string s, out bool result);
    }
}
