using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using Newtonsoft.Json;
using System.Drawing;
using System.IO;
using static System.Net.Mime.MediaTypeNames;

namespace ConsoleAppTestRestAPI
{
    public class CallTriton
    {
        public static void CallJarek()
        {
            // Pobieranie losowego obrazka z folderu
            var imagesDir = new DirectoryInfo(@"cifar10_images");
            var randomImageFile = imagesDir.GetFiles().OrderBy(x => Guid.NewGuid()).FirstOrDefault();

            if (randomImageFile == null)
            {
                Console.WriteLine("Brak obrazów w folderze.");
                return;
            }

            var img = (Bitmap)System.Drawing.Image.FromFile(randomImageFile.FullName);

            if (img.Width != 32 || img.Height != 32)
            {
                Console.WriteLine("Obraz musi mieć rozmiar 32x32.");
                return;
            }

            var imageArray = new float[1, 32, 32, 3];

            for (int i = 0; i < img.Width; i++)
            {
                for (int j = 0; j < img.Height; j++)
                {
                    var pixel = img.GetPixel(i, j);

                    // Normalizacja danych
                    imageArray[0, i, j, 0] = pixel.R / 255f;
                    imageArray[0, i, j, 1] = pixel.G / 255f;
                    imageArray[0, i, j, 2] = pixel.B / 255f;
                }
            }

            // URL do serwera Triton
            string tritonUrl = "http://10.0.20.50:8050/v2/models/ExampleCNNModelv1/versions/1/infer";

            // Dane wejściowe do inferencji
            var inferInput = new
            {
                inputs = new[]
                {
                new
                {
                    name = "conv2d_input",
                    shape = new[] {1, 32, 32, 3},
                    datatype = "FP32",
                    data = imageArray
                }
            },
                outputs = new[]
                {
                new
                {
                    name = "dense_1"
                }
            }
            };

            // Wykonanie inferencji
            using (var client = new HttpClient())
            {
                var content = new StringContent(JsonConvert.SerializeObject(inferInput), System.Text.Encoding.UTF8, "application/json");
                var response = client.PostAsync(tritonUrl, content).Result;
                var responseString = response.Content.ReadAsStringAsync().Result;

                Root result = JsonConvert.DeserializeObject<Root>(responseString);

                //Console.WriteLine(result);

                int a = 1;

                // Wyświetlanie wyniku
                double[] prediction = (double[])result.outputs[0].data.ToArray();
                int predictedLabel = Array.IndexOf(prediction, prediction.Max());

                Console.WriteLine($"Prediction: {string.Join(", ", prediction)}");
                Console.WriteLine(randomImageFile.Name);
                Console.WriteLine($"Predicted label: {predictedLabel}");
            }
        }
    }
}
