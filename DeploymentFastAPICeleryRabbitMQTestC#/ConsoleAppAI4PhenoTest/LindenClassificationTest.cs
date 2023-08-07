using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleAppAI4PhenoTest
{
    #region class LindenClassificationInput
    public class LindenClassificationInput
    {
        public string imageBase64 { get; set; }
        public string filename { get; set; }
        public string jsonBase64ImageROIs { get; set; }
    }
    #endregion

    #region class LindenClassificationOutput
    public class LindenClassificationOutput
    {
        public string task_id { get; set; }
        public string status { get; set; }
        public string filename { get; set; }
        public List<int> isFlowering { get; set; }
        public List<float> isFloweringConfidence { get; set; }
    }
    #endregion

    #region class LindenClassificationWithIndicatorsInput
    public class LindenClassificationWithIndicatorsInput
    {
        public string imageBase64 { get; set; }
        public string filename { get; set; }
        public string jsonBase64ImageROIs { get; set; }
    }
    #endregion

    #region class LindenClassificationWithIndicatorsOutput
    public class LindenClassificationWithIndicatorsOutput
    {
        public string task_id { get; set; }
        public string status { get; set; }
        public string filename { get; set; }
        public List<int> isFlowering { get; set; }
        public List<float> isFloweringConfidence { get; set; }
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

    public class LindenClassificationTest
    {
        private static readonly HttpClient client = new HttpClient();
        private static readonly string baseUrl = "http://10.0.20.50:8888";  // Change to your actual base URL

        #region static Ticket PostLindenClassificationModelgetClassificationLindenCall1()
        public static Ticket PostLindenClassificationModelgetClassificationLindenCall1()
        {
            string fullname = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\Linden_Photos\1\2022-06-19_04.18.34_class_1.jpg";
            string filename = System.IO.Path.GetFileName(fullname);
            string imagejson = ImageConverter.ImageToBase64(fullname);

            //string fullnameAREA = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\example\LindenKlas\via_project_5Aug2023_18h44m_json.json";
            string fullnameAREA = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\linden\LindenClassification\2023-08-05\ODUPP_2022.06.28.05.54.35._json.json";

            string filenameAREA = System.IO.Path.GetFileName(fullnameAREA);
            string imagejsonAREA = ImageConverter.ImageToBase64(fullnameAREA);

            var modelInput = new LindenClassificationInput
            {
                imageBase64 = imagejson,
                filename = filename,
                jsonBase64ImageROIs = imagejsonAREA
            };

            StringContent stringContent = new StringContent(JsonConvert.SerializeObject(modelInput), Encoding.UTF8, "application/json");

            var jsonString = JsonConvert.SerializeObject(modelInput);
            //File.WriteAllText("json.txt", jsonString);

            string url = string.Format("{0}/LindenClassificationModel/get_classification_linden", baseUrl);

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

        #region static Ticket PostLindenClassificationModelgetClassificationLindenCall2()
        public static Ticket PostLindenClassificationModelgetClassificationLindenCall2()
        {
            string fullname = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\example\LindenKlas\2022-06-19_02.48.33_class_1.jpg";
            string filename = System.IO.Path.GetFileName(fullname);
            string imagejson = ImageConverter.ImageToBase64(fullname);

            //string fullnameAREA = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\example\LindenKlas\via_project_5Aug2023_18h44m_json.json";
            string fullnameAREA = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\example\LindenKlas\via_project_6Aug2023_17h46m_json1.json";

            string filenameAREA = System.IO.Path.GetFileName(fullnameAREA);
            string imagejsonAREA = ImageConverter.ImageToBase64(fullnameAREA);

            var modelInput = new LindenClassificationInput
            {
                imageBase64 = imagejson,
                filename = filename,
                jsonBase64ImageROIs = imagejsonAREA
            };

            StringContent stringContent = new StringContent(JsonConvert.SerializeObject(modelInput), Encoding.UTF8, "application/json");

            var jsonString = JsonConvert.SerializeObject(modelInput);
            //File.WriteAllText("json.txt", jsonString);

            string url = string.Format("{0}/LindenClassificationModel/get_classification_linden", baseUrl);

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

        #region static LindenClassificationOutput GetLindenClassificationGetClassificationLindenResult(string task_id)
        public static LindenClassificationOutput GetLindenClassificationGetClassificationLindenResult(string task_id)
        {
            string url = string.Format("{0}/LindenClassificationModel/get_classification_linden_result/{1}", baseUrl, task_id);

            var response = client.GetAsync(url).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            LindenClassificationOutput objLindenClassificationOutput = JsonConvert.DeserializeObject<LindenClassificationOutput>(responseBody);

            Console.WriteLine($"TaskId: {objLindenClassificationOutput.task_id},\n Status: {objLindenClassificationOutput.status}," +
                $"\n filename:{objLindenClassificationOutput.filename},\n IsFlowering:{objLindenClassificationOutput.isFlowering[0]},\n IsFlowering:{objLindenClassificationOutput.isFloweringConfidence[0]}");

            return objLindenClassificationOutput;
        }
        #endregion

        #region static Ticket PostLindenClassificationModelgetClassificationLindenWithIndicatorsCall1()
        public static Ticket PostLindenClassificationModelgetClassificationLindenWithIndicatorsCall1()
        {
            string fullname = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\Linden_Photos\1\2022-06-19_04.18.34_class_1.jpg";
            string filename = System.IO.Path.GetFileName(fullname);
            string imagejson = ImageConverter.ImageToBase64(fullname);

            //string fullnameAREA = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\example\LindenKlas\via_project_5Aug2023_18h44m_json.json";
            string fullnameAREA = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\linden\LindenClassification\2023-08-05\ODUPP_2022.06.28.05.54.35._json.json";

            string filenameAREA = System.IO.Path.GetFileName(fullnameAREA);
            string imagejsonAREA = ImageConverter.ImageToBase64(fullnameAREA);

            var modelInput = new LindenClassificationWithIndicatorsInput
            {
                imageBase64 = imagejson,
                filename = filename,
                jsonBase64ImageROIs = imagejsonAREA
            };

            StringContent stringContent = new StringContent(JsonConvert.SerializeObject(modelInput), Encoding.UTF8, "application/json");

            var jsonString = JsonConvert.SerializeObject(modelInput);
            //File.WriteAllText("json.txt", jsonString);

            string url = string.Format("{0}/LindenClassificationModel/get_classification_linden_with_indicators", baseUrl);

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

        #region static LindenClassificationWithIndicatorsOutput GetLindenClassificationGetClassificationLindenWithIndicatorsResult(string task_id)
        public static LindenClassificationWithIndicatorsOutput GetLindenClassificationGetClassificationLindenWithIndicatorsResult(string task_id)
        {
            string url = string.Format("{0}/LindenClassificationModel/get_classification_linden_with_indicators_result/{1}", baseUrl, task_id);

            var response = client.GetAsync(url).Result;

            if (!response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }

            response.EnsureSuccessStatusCode();
            var responseBody = response.Content.ReadAsStringAsync().Result;

            LindenClassificationWithIndicatorsOutput objLindenClassificationWithIndicatorsOutput = JsonConvert.DeserializeObject<LindenClassificationWithIndicatorsOutput>(responseBody);

            Console.WriteLine($"TaskId: {objLindenClassificationWithIndicatorsOutput.task_id},\n Status: {objLindenClassificationWithIndicatorsOutput.status}," +
                $"\n filename:{objLindenClassificationWithIndicatorsOutput.filename},\n IsFlowering:{objLindenClassificationWithIndicatorsOutput.isFlowering[0]}," +
                $"\n IsFlowering:{objLindenClassificationWithIndicatorsOutput.isFloweringConfidence[0]}");

            Console.WriteLine($"TaskId: {objLindenClassificationWithIndicatorsOutput.task_id}," +
$" Status: {objLindenClassificationWithIndicatorsOutput.status}," +
$" avg_area: {objLindenClassificationWithIndicatorsOutput.avg_area}," +
$" avg_height: {objLindenClassificationWithIndicatorsOutput.avg_height}," +
$" avg_width: {objLindenClassificationWithIndicatorsOutput.avg_width}," +
$" r_av: {objLindenClassificationWithIndicatorsOutput.r_av}," +
$" g_av: {objLindenClassificationWithIndicatorsOutput.g_av}," +
$" number_of_lindens: {objLindenClassificationWithIndicatorsOutput.number_of_lindens}," +
$" filename:{objLindenClassificationWithIndicatorsOutput.filename}");

            return objLindenClassificationWithIndicatorsOutput;
        }
        #endregion
    }
}
