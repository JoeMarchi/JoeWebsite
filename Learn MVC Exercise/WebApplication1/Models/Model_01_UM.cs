using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication1.Models
{
    public class Model_01_UM
    {
        public static bool Validate(string strUserID,string strPassword)
        {
            return strUserID == "admin" && strPassword == "admin";


            
        }
        public static Model_01_UI GetUserInfo(string strUserID)
        {
            return new Model_01_UI()
            {
                UserID = "admin",
                Password = "admin",
                UserName = "劉騏瑋"
            };
        }
    }
}