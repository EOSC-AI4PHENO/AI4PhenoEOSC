using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleAppAI4PhenoTest
{
    public class RedisTest
    {
        private static readonly HttpClient client = new HttpClient();
        private static readonly string baseUrl = "http://10.0.20.50:8888";  // Change to your actual base URL

        public static void RemoveResultFromRedis(string task_id)
        {
            string url = string.Format("{0}/Redis/delete_task_from_redis/{1}", baseUrl, task_id);

            var response = client.GetAsync(url).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            AutomaticAppleSegmentationOutput objAutomaticAppleSegmentationOutput = JsonConvert.DeserializeObject<AutomaticAppleSegmentationOutput>(responseBody);

            Console.WriteLine($"TaskId: {objAutomaticAppleSegmentationOutput.task_id}, Status: {objAutomaticAppleSegmentationOutput.status},filename:{objAutomaticAppleSegmentationOutput.filename}");


            // Decode the Base64 string
            byte[] base64EncodedBytes = Convert.FromBase64String(objAutomaticAppleSegmentationOutput.jsonBase64AppleROIs);
            string jsonText = Encoding.UTF8.GetString(base64EncodedBytes);

            // Path to save the JSON file
            string filename = objAutomaticAppleSegmentationOutput.filename;
            filename = System.IO.Path.ChangeExtension(filename, "json");

            // Write JSON string to a file
            File.WriteAllText(filename, jsonText);

        }
    }
}
