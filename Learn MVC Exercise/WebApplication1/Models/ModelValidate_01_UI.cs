using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.ComponentModel.DataAnnotations;

namespace WebApplication1.Models
{
    public class ModelValidate_01_UI
    {
        [Required(ErrorMessage = "請輸入ID")]
        public int ID { get; set; }
        [Required(ErrorMessage = "請輸入姓名")]
        public string Name { get; set; }
        [Required(ErrorMessage = "請輸入年齡")]
        [Range(1, 120, ErrorMessage = "輸入範圍在1~120之間")]
        public int Age { get; set; }
        [Required(ErrorMessage = "請輸入性別")]
        [RegularExpression("^[男|女]$", ErrorMessage = "請輸入性別,男或女")]
        public string Sex { get; set; }

    }
}