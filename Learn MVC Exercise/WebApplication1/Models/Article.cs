using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace WebApplication1.Models
{
    
    public class Article
    {
        Forum_DBEntities db = new Forum_DBEntities();
        public List<Article_Tb> List_Table_OrderByDescending_MSSQL()
        {
            return db.Article_Tb.OrderByDescending(p => p.NO_F).ToList();
            
        }
        public List<Article_Tb> List_Table_Where_Contain_MSSQL(string content)
        {
            return db.Article_Tb.Where(p=>p.Title_F.Contains(content)).ToList();
        }
    }
}