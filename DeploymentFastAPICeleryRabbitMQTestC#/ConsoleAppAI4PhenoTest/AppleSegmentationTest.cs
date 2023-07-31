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

    #region class AutomaticAppleSegmentationWithIndicatorsOutput
    public class AutomaticAppleSegmentationWithIndicatorsOutput
    {
        public string task_id { get; set; }
        public string status { get; set; }
        public string filename { get; set; }
        public string jsonBase64AppleROIs { get; set; }
        public float r_av { get; set; }
        public float g_av { get; set; }
        public float b_av { get; set; }
        public float r_sd { get; set; }
        public float g_sd { get; set; }
        public float b_sd { get; set; }
        public float bri_av { get; set; }
        public float bri_sd { get; set; }
        public float gi_av { get; set; }
        public float gei_av { get; set; }
        public float gei_sd { get; set; }
        public float ri_av { get; set; }
        public float ri_sd { get; set; }
        public float bi_av { get; set; }
        public float bi_sd { get; set; }
        public float avg_width { get; set; }
        public float avg_height { get; set; }
        public float avg_area { get; set; }
        public int number_of_apples { get; set; }
    }
    #endregion

    public class AppleSegmentationTest
    {
        private static readonly HttpClient client = new HttpClient();
        private static readonly string baseUrl = "http://10.0.20.50:8888";  // Change to your actual base URL

        #region static Ticket PostAppleSegmentationGetAppleAutomaticRoisCall()
        public static Ticket PostAppleSegmentationGetAppleAutomaticRoisCall()
        {
            string fullname = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\VGGBartek\20220914_1207_0700F136_PIC_150_CAM_2.xml.pi.jpg";
            string filename = System.IO.Path.GetFileName(fullname);
            string imagejson = ImageConverter.ImageToBase64(fullname);

            string fullnameAREA = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\VGGBartek\via_project_30Jul2023_20h54m_jsonTEST.json";
            string filenameAREA = System.IO.Path.GetFileName(fullnameAREA);
            string imagejsonAREA = ImageConverter.ImageToBase64(fullnameAREA);

            var modelInput = new AutomaticAppleSegmentationInput
            {
                imageBase64 = imagejson,
                filename = filename,
                jsonBase64ImageROIs= imagejsonAREA
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
            filename= System.IO.Path.ChangeExtension(filename, "json");

            // Write JSON string to a file
            File.WriteAllText(filename, jsonText);

            return objAutomaticAppleSegmentationOutput;
        }
        #endregion

        #region static Ticket PostAppleSegmentationGetAppleAutomaticRoisWithIndicatorsCall()
        public static Ticket PostAppleSegmentationGetAppleAutomaticRoisWithIndicatorsCall()
        {
            string fullname = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\VGGBartek\20220914_1207_0700F136_PIC_150_CAM_2.xml.pi.jpg";
            string filename = System.IO.Path.GetFileName(fullname);
            string imagejson = ImageConverter.ImageToBase64(fullname);

            string fullnameAREA = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\VGGBartek\via_project_30Jul2023_20h54m_jsonTEST.json";
            string filenameAREA = System.IO.Path.GetFileName(fullnameAREA);
            string imagejsonAREA = ImageConverter.ImageToBase64(fullnameAREA);

            var modelInput = new AutomaticAppleSegmentationInput
            {
                imageBase64 = imagejson,
                filename = filename
                //jsonBase64ImageROIs = imagejsonAREA
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

        #region static AutomaticAppleSegmentationWithIndicatorsOutput GetAppleSegmentationGetAppleAutomaticRoisWithIndicatorsCallResult(string task_id)
        public static AutomaticAppleSegmentationWithIndicatorsOutput GetAppleSegmentationGetAppleAutomaticRoisWithIndicatorsCallResult(string task_id)
        {
            string url = string.Format("{0}/AutomaticAppleSegmentationModel/get_apple_automatic_rois_with_indicators_result/{1}", baseUrl, task_id);

            var response = client.GetAsync(url).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            AutomaticAppleSegmentationWithIndicatorsOutput objAutomaticAppleSegmentationWithIndicatorsOutput = JsonConvert.DeserializeObject<AutomaticAppleSegmentationWithIndicatorsOutput>(responseBody);

            Console.WriteLine($"TaskId: {objAutomaticAppleSegmentationWithIndicatorsOutput.task_id}," +
                $" Status: {objAutomaticAppleSegmentationWithIndicatorsOutput.status}," +
                $" avg_area: {objAutomaticAppleSegmentationWithIndicatorsOutput.avg_area}," +
                $" avg_height: {objAutomaticAppleSegmentationWithIndicatorsOutput.avg_height}," +
                $" avg_width: {objAutomaticAppleSegmentationWithIndicatorsOutput.avg_width}," +
                $" r_av: {objAutomaticAppleSegmentationWithIndicatorsOutput.r_av}," +
                $" g_av: {objAutomaticAppleSegmentationWithIndicatorsOutput.g_av}," +
                $" filename:{objAutomaticAppleSegmentationWithIndicatorsOutput.filename}");


            // Decode the Base64 string
            byte[] base64EncodedBytes = Convert.FromBase64String(objAutomaticAppleSegmentationWithIndicatorsOutput.jsonBase64AppleROIs);
            string jsonText = Encoding.UTF8.GetString(base64EncodedBytes);

            // Path to save the JSON file
            string filename = objAutomaticAppleSegmentationWithIndicatorsOutput.filename;
            filename = System.IO.Path.ChangeExtension(filename, "json");

            // Write JSON string to a file
            File.WriteAllText(filename, jsonText);

            return objAutomaticAppleSegmentationWithIndicatorsOutput;
        }
        #endregion
    }
}
