using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Web;
using WebApplication1.Models;
using System.Web.Mvc;

namespace WebApplication1.Controllers
{
    public class HomeController : Controller
    {

        public ActionResult Index(Student student)
        {
            return View(student);
        }

        public ActionResult About()
        {
            ViewBag.Message = "Your application description page.";

            return View();
        }

        public ActionResult Contact()
        {
            
            ViewBag.Message = "Your contact page.";

            return View();
        }
        public ActionResult Model_01()
        {
            return View();
        }
        public ActionResult Test(string value1)
        {
            var n = value1;
            var types = n.GetType();
            ViewData["Value"] = value1;
            return View("index");
        }
        public ActionResult ModelValidate_01()
        {

            return View();
        }
        [HttpPost]
        public ActionResult ModelValidate_01(Models.ModelValidate_01_UI user)
        {
            try
            {
                if (!ModelState.IsValid)
                {
                    return View("ModelValidate_01", user);
                }
                return View("ModelValidate_01_Result", user);
            }
            catch
            {
                return View();
            }
        }
        public ActionResult ModelValidate_02()
        {
            
            return View();
        }
        [HttpPost]
        public ActionResult ModelValidate_02(Models.Member_Tb member)
        {
            Forum_DBEntities db = new Forum_DBEntities();
            if (!ModelState.IsValid)
            {
                return View("ModelValidate_02", member);
            }
            Member_Tb member_Tb = new Member_Tb();
            member_Tb.NO = member.NO;
            member_Tb.Name = member.Name;
            member_Tb.Account = "test";
            member_Tb.Password = "123456";
            member_Tb.Email = member.Email;
            member_Tb.IsAdmin = false;
            member_Tb.AuthCode = "123456789";

            db.Member_Tb.Add(member_Tb);
            db.SaveChanges();
            return RedirectToAction("ModelValidate_02_RE",member_Tb);
        }
        public ActionResult ModelValidate_02_RE(Models.Member_Tb member_Tb)
        {
            return View(member_Tb);
        }
    }
}