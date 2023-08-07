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

    #region class AutomaticLindenSegmentationWithIndicatorsOutput
    public class AutomaticLindenSegmentationWithIndicatorsOutput
    {
        public string task_id { get; set; }
        public string status { get; set; }
        public string filename { get; set; }
        public string jsonBase64LindenROIs { get; set; }
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
        public int number_of_lindens { get; set; }
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

        #region static AutomaticLindenSegmentationOutput GetLindenSegmentationGetLindenAutomaticRoisCallResult(string task_id)
        public static AutomaticLindenSegmentationOutput GetLindenSegmentationGetLindenAutomaticRoisCallResult(string task_id)
        {
            string url = string.Format("{0}/AutomaticLindenSegmentationModel/get_linden_automatic_rois_result/{1}", baseUrl, task_id);

            var response = client.GetAsync(url).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            AutomaticLindenSegmentationOutput objAutomaticLindenSegmentationOutput = JsonConvert.DeserializeObject<AutomaticLindenSegmentationOutput>(responseBody);

            Console.WriteLine($"TaskId: {objAutomaticLindenSegmentationOutput.task_id}, Status: {objAutomaticLindenSegmentationOutput.status},filename:{objAutomaticLindenSegmentationOutput.filename}");


            // Decode the Base64 string
            byte[] base64EncodedBytes = Convert.FromBase64String(objAutomaticLindenSegmentationOutput.jsonBase64LindenROIs);
            string jsonText = Encoding.UTF8.GetString(base64EncodedBytes);

            // Path to save the JSON file
            string filename = objAutomaticLindenSegmentationOutput.filename;
            filename = System.IO.Path.ChangeExtension(filename, "json");

            // Write JSON string to a file
            File.WriteAllText(filename, jsonText);

            return objAutomaticLindenSegmentationOutput;
        }
        #endregion

        #region static Ticket PostLindenSegmentationGetLindenAutomaticRoisCall(string fullname)
        public static Ticket PostLindenSegmentationGetLindenAutomaticRoisCall(string fullname)
        {
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

        #region static Ticket PostLindenSegmentationGetLindenAutomaticRoisWithIndicatorsCall()
        public static Ticket PostLindenSegmentationGetLindenAutomaticRoisWithIndicatorsCall()
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

            string url = string.Format("{0}/AutomaticLindenSegmentationModel/get_linden_automatic_rois_with_indicators", baseUrl);

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

        #region static AutomaticLindenSegmentationWithIndicatorsOutput GetLindenSegmentationGetLindenAutomaticRoisWithIndicatorsCallResult(string task_id)
        public static AutomaticLindenSegmentationWithIndicatorsOutput GetLindenSegmentationGetLindenAutomaticRoisWithIndicatorsCallResult(string task_id)
        {
            string url = string.Format("{0}/AutomaticLindenSegmentationModel/get_linden_automatic_rois_with_indicators_result/{1}", baseUrl, task_id);

            var response = client.GetAsync(url).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            AutomaticLindenSegmentationWithIndicatorsOutput objAutomaticLindenSegmentationWithIndicatorsOutput = JsonConvert.DeserializeObject<AutomaticLindenSegmentationWithIndicatorsOutput>(responseBody);

            Console.WriteLine($"TaskId: {objAutomaticLindenSegmentationWithIndicatorsOutput.task_id}, Status: {objAutomaticLindenSegmentationWithIndicatorsOutput.status},filename:{objAutomaticLindenSegmentationWithIndicatorsOutput.filename}");

            Console.WriteLine($"TaskId: {objAutomaticLindenSegmentationWithIndicatorsOutput.task_id}," +
    $" Status: {objAutomaticLindenSegmentationWithIndicatorsOutput.status}," +
    $" avg_area: {objAutomaticLindenSegmentationWithIndicatorsOutput.avg_area}," +
    $" avg_height: {objAutomaticLindenSegmentationWithIndicatorsOutput.avg_height}," +
    $" avg_width: {objAutomaticLindenSegmentationWithIndicatorsOutput.avg_width}," +
    $" r_av: {objAutomaticLindenSegmentationWithIndicatorsOutput.r_av}," +
    $" g_av: {objAutomaticLindenSegmentationWithIndicatorsOutput.g_av}," +
    $" filename:{objAutomaticLindenSegmentationWithIndicatorsOutput.filename}");


            // Decode the Base64 string
            byte[] base64EncodedBytes = Convert.FromBase64String(objAutomaticLindenSegmentationWithIndicatorsOutput.jsonBase64LindenROIs);
            string jsonText = Encoding.UTF8.GetString(base64EncodedBytes);

            // Path to save the JSON file
            string filename = objAutomaticLindenSegmentationWithIndicatorsOutput.filename;
            filename = System.IO.Path.ChangeExtension(filename, "json");

            // Write JSON string to a file
            File.WriteAllText(filename, jsonText);

            return objAutomaticLindenSegmentationWithIndicatorsOutput;
        }
        #endregion
    }
}
