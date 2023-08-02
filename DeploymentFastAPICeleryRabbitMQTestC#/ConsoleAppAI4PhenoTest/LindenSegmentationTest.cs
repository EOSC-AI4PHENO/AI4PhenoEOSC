using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.IO;


namespace ConsoleAppAI4PhenoTest
{
    #region class AutomaticLindenSegmentationInput
    public class AutomaticLindenSegmentationInput
    {
        public string imageBase64 { get; set; }
        public string filename { get; set; }
        public string jsonBase64ImageROIs { get; set; }
    }
    #endregion

    #region class AutomaticLindenSegmentationOutput
    public class AutomaticLindenSegmentationOutput
    {
        public string task_id { get; set; }
        public string status { get; set; }
        public string filename { get; set; }
        public string jsonBase64LindenROIs { get; set; }
    }
    #endregion

    public class LindenSegmentationTest
    {
        private static readonly HttpClient client = new HttpClient();
        private static readonly string baseUrl = "http://10.0.20.50:8888";  // Change to your actual base URL

        #region static Ticket PostLindenSegmentationGetLindenAutomaticRoisCall()
        public static Ticket PostLindenSegmentationGetLindenAutomaticRoisCall()
        {
            string fullname = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\linden\Mask-RCNN-linden\linden_dataset\linden\test\2022-06-19_04.48.36_class_1.jpg";
            string filename = System.IO.Path.GetFileName(fullname);
            string imagejson = ImageConverter.ImageToBase64(fullname);

            //string fullnameAREA = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\VGGBartek\via_project_30Jul2023_20h54m_jsonTEST.json";
            //string filenameAREA = System.IO.Path.GetFileName(fullnameAREA);
            //string imagejsonAREA = ImageConverter.ImageToBase64(fullnameAREA);

            var modelInput = new AutomaticAppleSegmentationInput
            {
                imageBase64 = imagejson,
                filename = filename
                //jsonBase64ImageROIs = imagejsonAREA
            };

            StringContent stringContent = new StringContent(JsonConvert.SerializeObject(modelInput), Encoding.UTF8, "application/json");

            var jsonString = JsonConvert.SerializeObject(modelInput);
            //File.WriteAllText("json.txt", jsonString);

            string url = string.Format("{0}/AutomaticLindenSegmentationModel/get_linden_automatic_rois", baseUrl);

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

        #region static AutomaticAppleSegmentationOutput GetAppleSegmentationGetAppleAutomaticRoisCallResult(string task_id)
        public static AutomaticAppleSegmentationOutput GetAppleSegmentationGetAppleAutomaticRoisCallResult(string task_id)
        {
            string url = string.Format("{0}/AutomaticAppleSegmentationModel/get_apple_automatic_rois_result/{1}", baseUrl, task_id);

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

            return objAutomaticAppleSegmentationOutput;
        }
        #endregion
    }
}
