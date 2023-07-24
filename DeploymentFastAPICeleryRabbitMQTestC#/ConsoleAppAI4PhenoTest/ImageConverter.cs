using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleAppAI4PhenoTest
{
    public class ImageConverter
    {
        public static string ImageToBase64(string imagePath)
        {
            if (File.Exists(imagePath))
            {
                // Wczytaj obrazek jako tablicę bajtów
                byte[] imageBytes = File.ReadAllBytes(imagePath);

                // Przekształć tablicę bajtów na string w formacie base64
                return Convert.ToBase64String(imageBytes);
            }
            else
            {
                throw new FileNotFoundException("File does not exist.");
            }
        }
    }
}
