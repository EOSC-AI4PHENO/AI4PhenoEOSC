using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ConsoleAppTestRestAPI
{

    public class output
    {
        public string name { get; set; }
        public string datatype { get; set; }
        public List<int> shape { get; set; }
        public List<double> data { get; set; }
    }

    public class Root
    {
        public string model_name { get; set; }
        public string model_version { get; set; }
        public List<output> outputs { get; set; }

        public Root()
        {
            outputs = new List<output>();
        }
    }
}