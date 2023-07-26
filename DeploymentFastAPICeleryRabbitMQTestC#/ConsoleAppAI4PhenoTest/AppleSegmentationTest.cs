using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.IO;

namespace ConsoleAppAI4PhenoTest
{
    #region class AutomaticAppleSegmentationInput
    public class AutomaticAppleSegmentationInput
    {
        public string imageBase64 { get; set; }
        public string filename { get; set; }
        public string jsonBase64ImageROIs { get; set; }
    }
    #endregion

    #region class AutomaticAppleSegmentationOutput
    public class AutomaticAppleSegmentationOutput
    {
        public string task_id { get; set; }
        public string status { get; set; }
        public string filename { get; set; }
        public string jsonBase64AppleROIs { get; set; }
    }
    #endregion

    public class AppleSegmentationTest
    {
        private static readonly HttpClient client = new HttpClient();
        private static readonly string baseUrl = "http://10.0.20.50:8888";  // Change to your actual base URL

        #region static Ticket PostAppleSegmentationGetAppleAutomaticRoisCall()
        public static Ticket PostAppleSegmentationGetAppleAutomaticRoisCall()
        {
            string fullname = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\apple\dataset_2023_07_05_17_28_03\test\20220811_1257_0700F136_PIC_120_CAM_2.xml.pi.jpg";

            string filename = System.IO.Path.GetFileName(fullname);

            string imagejson = ImageConverter.ImageToBase64(fullname);

            var modelInput = new AutomaticAppleSegmentationInput
            {
                imageBase64 = imagejson,
                filename = filename
            };

            StringContent stringContent = new StringContent(JsonConvert.SerializeObject(modelInput), Encoding.UTF8, "application/json");

            var jsonString = JsonConvert.SerializeObject(modelInput);
            //File.WriteAllText("json.txt", jsonString);

            string url = string.Format("{0}/AutomaticAppleSegmentationModel/get_apple_automatic_rois", baseUrl);

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
    }
}
