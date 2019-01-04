using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace WebApplication1.Controllers
{
    public class StudentController : Controller
    {
        // GET: Student
        [ActionName("Default")]
        public string Index()
        {
            return "Index";
        }
    }
}