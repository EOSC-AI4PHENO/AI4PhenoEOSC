using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleAppAI4PhenoTest
{
    public class RedisOutput
    {
        public bool statusFlag { get; set; }
    }

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

            RedisOutput objRedisOutput = JsonConvert.DeserializeObject<RedisOutput>(responseBody);

            Console.WriteLine($"Redis output: {objRedisOutput.statusFlag}");
        }
    }
}
