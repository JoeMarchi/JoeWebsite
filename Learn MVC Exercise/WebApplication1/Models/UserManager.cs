using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication1.Models
{
    public class UserManager
    {
        public static bool Validate(string strUserID,string strPassword)
        {
            return strUserID == "admin" && strPassword == "admin";


            
        }
        public static UserInfo GetUserInfo(string strUserID)
        {
            return new UserInfo()
            {
                UserID = "admin",
                Password = "admin",
                UserName = "劉騏瑋"
            };
        }
    }
}