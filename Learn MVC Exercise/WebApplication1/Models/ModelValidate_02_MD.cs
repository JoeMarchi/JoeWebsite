using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel;

namespace WebApplication1.Models
{
    [MetadataType(typeof(Member_Tb_MD))]
    public partial class Member_Tb
    {
        public class Member_Tb_MD
        {
            [DisplayName("用戶編號")]
            [Required(ErrorMessage = "請輸入編號")]
            public int NO { get; set; }
            [DisplayName("用戶姓名")]
            [Required(ErrorMessage ="請輸入姓名")]
            public string Name { get; set; }
            [DisplayName("用戶信箱")]
            [Required(ErrorMessage ="請輸入信箱")]
            public string Email { get; set; }
        }
    }
}