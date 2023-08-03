using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace ConsoleAppAI4PhenoTest
{
    public class klas
    {
        public static void RunStressTest(int ile)
        {
            Random rand = new Random();

            string folder1Path = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\linden\Linden_Photos_Flowering_WellExposed";
            string folder2Path = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\Linden_Photos\0";

            List<string> jpgFilesFolder1 = Directory.GetFiles(folder1Path, "*.jpg").ToList();
            List<string> jpgFilesFolder2 = Directory.GetFiles(folder2Path, "*.jpg").ToList();

            // Jeżeli w każdym folderze jest mniej niż ile plików JPG, wybierz wszystkie
            if (jpgFilesFolder1.Count < ile || jpgFilesFolder2.Count < ile)
            {
                Console.WriteLine("Za mało plików jpg w jednym lub obu folderach");
                return;
            }

            List<string> selectedFilesFolder1 = new List<string>();
            List<string> selectedFilesFolder2 = new List<string>();

            for (int i = 0; i < ile; i++)
            {
                int index1 = rand.Next(jpgFilesFolder1.Count);
                selectedFilesFolder1.Add(jpgFilesFolder1[index1]);
                jpgFilesFolder1.RemoveAt(index1); // Usuwamy wybrany plik, żeby nie został wybrany ponownie

                int index2 = rand.Next(jpgFilesFolder2.Count);
                selectedFilesFolder2.Add(jpgFilesFolder2[index2]);
                jpgFilesFolder2.RemoveAt(index2); // Usuwamy wybrany plik, żeby nie został wybrany ponownie
            }

            // Teraz masz wybrane pliki w selectedFilesFolder1 i selectedFilesFolder2, możesz z nimi zrobić co chcesz
            // Na przykład, możemy je wyświetlić

            Console.WriteLine("Wybrane pliki z folderu 1:");
            //foreach (string file in selectedFilesFolder1)
            for(int  i = 0;i < selectedFilesFolder1.Count;i++) 
            {
                string file= selectedFilesFolder1[i];
                string filename=System.IO.Path.GetFileName(file);
                LindenSegmentationTest.PostLindenSegmentationGetLindenAutomaticRoisCall(file);
                Console.WriteLine(string.Format("{0}.plik:{1}", i, filename));
            }

            Console.WriteLine("Wybrane pliki z folderu 2:");
            //foreach (string file in selectedFilesFolder2)
            for (int i = 0; i < selectedFilesFolder2.Count; i++)
            {
                string file = selectedFilesFolder2[i];
                string filename = System.IO.Path.GetFileName(file);
                LindenSegmentationTest.PostLindenSegmentationGetLindenAutomaticRoisCall(file);
                Console.WriteLine(string.Format("{0}.plik:{1}",i, filename));
            }

        }
    }
}
