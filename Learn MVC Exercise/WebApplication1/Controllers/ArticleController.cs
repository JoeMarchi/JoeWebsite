using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using WebApplication1.Models;

namespace WebApplication1.Controllers
{
    public class ArticleController : Controller
    {
        
        // GET: Article
        public ActionResult List_Table_OrderByDescending_MSSQL()
        {
            Article art = new Article();
            
            return View(art.List_Table_OrderByDescending_MSSQL());
        }
    }
}