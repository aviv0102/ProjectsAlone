using ImageService.Infrastructure;
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Text;
using System.Text.RegularExpressions;

/* the ImageServiceModal
 * has methods to create and move file
 */ 
namespace ImageService.Modal
{
    public class ImageServiceModal : IImageServiceModal
    {
        private int thumbnailSize;              // The Size Of The Thumbnail Size


        public ImageServiceModal(int size)
        {
            this.thumbnailSize = size;

        }

        //adding the file from dir to thumbnails dir and outPut dir
		public string AddFile(string path,string outDir, out bool result)
		{
			try
			{   

                //file not exists
				if (!File.Exists(path))
				{
					throw new Exception("path file not exists");
				}

                //taking date taken/created of image
                DateTime d = GetDateTakenFromImage(path);
                //creating the proper directories
                string yearDir= CreateFolder(outDir, d.Year.ToString());
                string monthDir = CreateFolder(yearDir, d.Month.ToString());


                string thumbnails = CreateFolder(outDir, "Thumbnails");
                string thumbyearDir = CreateFolder(thumbnails, d.Year.ToString());
                string thumbmonthDir = CreateFolder(thumbyearDir, d.Month.ToString());

                string name2=Path.GetFileName(path);


                //moving the file to the month dir
                string name = CheckExist(name2, monthDir, thumbnails);

                File.Copy(path, thumbmonthDir + "\\" + name);
				File.Move(path, monthDir+"\\"+name);

                //creating the thumbnail and moving it
                //Image image = Image.FromFile(monthDir + "\\" + name);
               /// Image thumb = image.GetThumbnailImage(120, 120, () => false, IntPtr.Zero);
                //thumb.Save(Path.ChangeExtension(thumbmonthDir+"\\"+name, "thumb"));
                


                result = true;
				return "true";
			}
			catch (Exception e)
			{
				result = false;
				return e.ToString();
			}
		}

        //getting the meta data from the image 
        private static Regex r = new Regex(":");

        //take the date taken or created (if not exist) of image
        public static DateTime GetDateTakenFromImage(string path)
        {
            using (FileStream fs = new FileStream(path, FileMode.Open, FileAccess.Read))
            using (Image myImage = Image.FromStream(fs, false, false))
            {
                PropertyItem propItem = null;
                try
                {
                    propItem = myImage.GetPropertyItem(36867);
                }
                catch { }
                if (propItem != null)
                {
                    string dateTaken = r.Replace(Encoding.UTF8.GetString(propItem.Value), "-", 2);
                    return DateTime.Parse(dateTaken);
                }
                else
                    return new FileInfo(path).LastWriteTime;
            }
        }

        //create a folder
        public string CreateFolder(string path, string name)
		{
			try
			{
				if (!Directory.Exists(path))
				{
					throw new Exception("file not exists");
				}
				string newPath = path + "\\" + name;
				DirectoryInfo dir = Directory.CreateDirectory(newPath);
				return newPath;
			}
			catch (Exception e)
			{
				return e.ToString();
			}
		}
        public string CheckExist(string name,string path1,string path2)
        {
            if (File.Exists(path1+"\\"+name) || File.Exists(path2+"\\"+name))
            {
                string nameW = Path.GetFileNameWithoutExtension(name);
                string exten = Path.GetExtension(name);
                name = nameW + "(1)"+exten;
                return CheckExist(name, path1, path2);
            }

            return name;
        }
	}
}
