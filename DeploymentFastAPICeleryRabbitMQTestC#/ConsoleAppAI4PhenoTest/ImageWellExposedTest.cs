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
    #region class SunriseSunsetInput
    public class SunriseSunsetInput
    {
        public float lat { get; set; }
        public float lon { get; set; }
        public DateTime UTCdate { get; set; }
    }
    #endregion

    #region class Ticket
    public class Ticket
    {
        public string task_id { get; set; }
        public string Status { get; set; }
    }
    #endregion

    #region class SunriseSunsetOutput
    public class SunriseSunsetOutput
    {
        public string task_id { get; set; }
        public string status { get; set; }
        public DateTime UTCsunrise { get; set; }
        public DateTime UTCsunset { get; set; }
    }
    #endregion

    #region class ImageWellExposedInput
    public class ImageWellExposedInput
    {
        public string imageBase64 { get; set; }
        public string filename { get; set; }
        public double lat { get; set; }
        public double lon { get; set; }
        public DateTime UTCdate { get; set; }
    }
    #endregion

    #region class ImageWellExposedOutput
    public class ImageWellExposedOutput
    {
        public string task_id { get; set; }
        public string status { get; set; }
        public bool WellExposedStatusFlag { get; set; }
        public string WellExposedStatusDesc { get; set; }
        public string filename { get; set; }

    }
    #endregion

    public class ImageWellExposedTest
    {
        private static readonly HttpClient client = new HttpClient();
        private static readonly string baseUrl = "http://10.0.20.50:8888";  // Change to your actual base URL

        #region static Ticket PostSunriseSunsetCall()
        public static Ticket PostSunriseSunsetCall()
        {
            var modelInput = new SunriseSunsetInput
            {
                lat = 52.2297f,
                lon = 21.0122f,
                UTCdate = DateTime.UtcNow
            };

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

            Console.WriteLine($"TaskId: {objTaskTicket.task_id}, Status: {objTaskTicket.Status}");

            return objTaskTicket;
        }
        #endregion

        #region static SunriseSunsetOutput GetSunriseSunsetCallResult(string task_id)
        public static SunriseSunsetOutput GetSunriseSunsetCallResult(string task_id)
        {
            string url = string.Format("{0}/ImageWellExposedModel/get_sunrise_sunset_result/{1}", baseUrl, task_id);

            var response = client.GetAsync(url).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            SunriseSunsetOutput objSunriseSunsetOutput = JsonConvert.DeserializeObject<SunriseSunsetOutput>(responseBody);

            Console.WriteLine($"TaskId: {objSunriseSunsetOutput.task_id}, Status: {objSunriseSunsetOutput.status}, UTCsunrise: {objSunriseSunsetOutput.UTCsunrise}, UTCsunset: {objSunriseSunsetOutput.UTCsunset}");


            return objSunriseSunsetOutput;
        }
        #endregion

        #region static Ticket PostisImageWellExposedByHistoCall()
        public static Ticket PostisImageWellExposedByHistoCall()
        {
            string fullname = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\linden\LindenClassification\Linden_Photos_ROI\0\2022-01-01_00.06.40_class_0_ROI.jpg";

            string filename = System.IO.Path.GetFileName(fullname);

            string imagejson = ImageConverter.ImageToBase64(fullname);

            var modelInput = new ImageWellExposedInput
            {
                imageBase64 = imagejson,
                filename = filename,
                lat = 52.2297f,
                lon = 21.0122f,
                //UTCdate = DateTime.UtcNow
                UTCdate = new DateTime(2022,01,01,00,06,40)
            };

            StringContent stringContent = new StringContent(JsonConvert.SerializeObject(modelInput), Encoding.UTF8, "application/json");

            var jsonString = JsonConvert.SerializeObject(modelInput);
            //File.WriteAllText("json.txt", jsonString);

            string url = string.Format("{0}/ImageWellExposedModel/is_Image_WellExposedByHisto", baseUrl);

            var response = client.PostAsync(url, stringContent).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            Ticket objTaskTicket = JsonConvert.DeserializeObject<Ticket>(responseBody);

            Console.WriteLine($"TaskId: {objTaskTicket.task_id}, Status: {objTaskTicket.Status}");

            return objTaskTicket;
        }
        #endregion

        #region static ImageWellExposedOutput GetisImageWellExposedByHistoCallResult(string task_id)
        public static ImageWellExposedOutput GetisImageWellExposedByHistoCallResult(string task_id)
        {
            string url = string.Format("{0}/ImageWellExposedModel/is_Image_WellExposedByHisto_result/{1}", baseUrl, task_id);

            var response = client.GetAsync(url).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            ImageWellExposedOutput objImageWellExposedOutput = JsonConvert.DeserializeObject<ImageWellExposedOutput>(responseBody);

            Console.WriteLine($"TaskId: {objImageWellExposedOutput.task_id}, Status: {objImageWellExposedOutput.status}, isWellExposed: {objImageWellExposedOutput.WellExposedStatusFlag}, isWellExposedText: {objImageWellExposedOutput.WellExposedStatusDesc},filename:{objImageWellExposedOutput.filename}");

            return objImageWellExposedOutput;
        }
        #endregion
    }

}
