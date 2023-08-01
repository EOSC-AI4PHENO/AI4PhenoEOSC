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
        public string jsonBase64ImageROI { get; set; }
    }
    #endregion

    #region class LindenClassificationOutput
    public class LindenClassificationOutput
    {
        public string task_id { get; set; }
        public string status { get; set; }
        public string filename { get; set; }
        public bool isflowering { get; set; }
    }
    #endregion

    public class LindenClassificationTest
    {
        private static readonly HttpClient client = new HttpClient();
        private static readonly string baseUrl = "http://10.0.20.50:8888";  // Change to your actual base URL

        #region static Ticket PostLindenClassificationModelgetClassificationLindenCall()
        public static Ticket PostLindenClassificationModelgetClassificationLindenCall()
        {
            string fullname = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\linden\Linden_Photos_Flowering\1\2022-06-19_02.48.33_class_1.jpg";
            string filename = System.IO.Path.GetFileName(fullname);
            string imagejson = ImageConverter.ImageToBase64(fullname);

            string fullnameAREA = @"E:\!DeepTechnology\!Customers\!2023\Seth Software EOSC-AI4Pheno\AI4PhenoEOSC\DeploymentTriton\ClassificationLinden\via_project_1Aug2023_7h29m_json.json";
            string filenameAREA = System.IO.Path.GetFileName(fullnameAREA);
            string imagejsonAREA = ImageConverter.ImageToBase64(fullnameAREA);

            var modelInput = new LindenClassificationInput
            {
                imageBase64 = imagejson,
                filename = filename,
                jsonBase64ImageROI = imagejsonAREA
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
    }
}
