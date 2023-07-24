using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Http;
using Newtonsoft.Json;
using System.IO;

namespace ConsoleAppAI4PhenoTest
{
    public class SunriseSunsetInput
    {
        public float lat { get; set; }
        public float lon { get; set; }
        public DateTime UTCdate { get; set; }
    }

    public class Ticket
    {
        public string task_id { get; set; }
        public string Status { get; set; }
    }

    public class SunriseSunsetOutput
    {
        public string task_id { get; set; }
        public string status { get; set; }
        public List<DateTime> result { get; set; }
    }



    public class ImageWellExposedTest
    {
        private static readonly HttpClient client = new HttpClient();
        private static readonly string baseUrl = "http://10.0.20.50:8888";  // Change to your actual base URL

        public static void GetSunriseSunsetCall()
        {
            var modelInput = new SunriseSunsetInput
            {
                lat = 52.2297f,
                lon = 21.0122f,
                UTCdate = DateTime.UtcNow
            };

            Ticket taskTicket = ScheduleImageWellExposedModelGetSunriseSunset(modelInput);
            Console.WriteLine($"TaskId: {taskTicket.task_id}, Status: {taskTicket.Status}");

            SunriseSunsetOutput objSunriseSunsetOutput=ScheduleImageWellExposedModelGetSunriseSunsetCheckResult(taskTicket.task_id);

            Console.WriteLine($"TaskId: {objSunriseSunsetOutput.task_id}, Status: {objSunriseSunsetOutput.status}, UTCsunrise: {objSunriseSunsetOutput.result[0]}, UTCsunset: {objSunriseSunsetOutput.result[1]}");

        }

        private static Ticket ScheduleImageWellExposedModelGetSunriseSunset(SunriseSunsetInput modelInput)
        {
            StringContent stringContent = new StringContent(JsonConvert.SerializeObject(modelInput), Encoding.UTF8, "application/json");

            var jsonString = JsonConvert.SerializeObject(modelInput);
            File.WriteAllText("json.txt", jsonString);

            string url = string.Format("{0}/ImageWellExposedModel/get_sunrise_sunset", baseUrl);

            var response = client.PostAsync(url, stringContent).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            Ticket objTaskTicket = JsonConvert.DeserializeObject<Ticket>(responseBody);

            return objTaskTicket;

        }

        private static SunriseSunsetOutput ScheduleImageWellExposedModelGetSunriseSunsetCheckResult(string task_id)
        {
            string url = string.Format("{0}/ImageWellExposedModel/result/{1}", baseUrl, task_id);

            var response = client.GetAsync(url).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            SunriseSunsetOutput objSunriseSunsetOutput = JsonConvert.DeserializeObject<SunriseSunsetOutput>(responseBody);

            return objSunriseSunsetOutput;
        }
    }

}
