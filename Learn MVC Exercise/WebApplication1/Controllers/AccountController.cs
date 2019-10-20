using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using WebApplication1.Models;

namespace WebApplication1.Controllers
{
    public class AccountController : Controller
    {
        // GET: Account
        public ActionResult Model_01()
        {
            return View();
        }
        public ActionResult Login_01(FormCollection form)
        {
            string strLoginName = form["LoginName"];
            string strPassword = form["Password"];
            if (Models.Model_01_UM.Validate(strLoginName, strPassword))
            {
                Session["CurrentUser"] = Models.Model_01_UM.GetUserInfo(strLoginName);
                return RedirectToAction("FormResult");
            }
            ViewBag.MsgErr = "輸入錯誤";
            return View("Model_01"); 
        }
        public ActionResult FormResult()
        {
            return View();
        }
    }  
}