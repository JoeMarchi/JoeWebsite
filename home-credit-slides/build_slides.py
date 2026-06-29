#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Home Credit 信用違約風險 — 簡報內容（單一資料來源）

此檔案同時產生：
  1) home_credit_slides.pptx      — 可立即檢視的本機簡報
  2) batch_update.json            — 供 `gws slides presentations batchUpdate` 推送到 Google Slides 的請求內容

每張投影片以 dict 描述：
  layout: "TITLE"（封面：CENTERED_TITLE + SUBTITLE）或 "TITLE_AND_BODY"
  title : 標題
  body  : 字串（封面副標）或 list[str]（內文條列）
"""
import json, os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
DECK_TITLE = "Home Credit 信用違約風險 — Kaggle 機器學習專案評估"

SLIDES = [
    {
        "layout": "TITLE",
        "title": "Home Credit 信用違約風險",
        "body": "Kaggle 信用評估競賽資料介紹、專案可行性、資料處理與演算法評估\n（資料來源：Home Credit 2024 特徵字典 + 訓練流程規格書）",
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "競賽與資料集介紹",
        "body": [
            "目標：依申請人資料預測貸款是否違約（target：0=正常，1=違約），協助對信用紀錄不足的族群做風險評估。",
            "附件特徵字典共 465 個欄位，採 _<id><型別> 命名（如 amount_1115A、approvaldate_319D），屬於 2024「Credit Risk Model Stability」競賽。",
            "與規格書(spec.md)所述 2018 版差異：2018 以 SK_ID_CURR 為主鍵、多張 csv（bureau、previous_application…）；2024 以 case_id 為主鍵、parquet 多深度表，並新增『模型穩定度』要求。",
            "本簡報以 2024 實際資料為準，沿用規格書的 Pipeline 架構（兩版流程高度相通）。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "資料結構與檔案",
        "body": [
            "主表 base：case_id、date_decision、WEEK_NUM、MONTH、target，定義每筆申請與時間軸。",
            "特徵表依 depth 分層：depth 0（單列／申請當下）、depth 1、depth 2（一對多歷史，需聚合）。",
            "主題涵蓋：聯徵紀錄、過往申請、稅務、存款／簽帳卡金流、分期還款、人口統計等。",
            "串接鍵：以 case_id 將各表 left join 回主表；depth 1/2 需先 groupby(case_id) 聚合為單列。",
            "格式為 parquet、資料量達數 GB，建議用 Polars / DuckDB 做高效聚合。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "特徵字典概覽（465 欄位）",
        "body": [
            "命名後綴即資料型別線索，分布如下：",
            "L 其他/一般轉換 187；A 金額 102；M 遮罩類別 63；D 日期 57；P 逾期天數(DPD) 33；T 其他轉換 22。",
            "金額類(A)：授信額度、攤還金額、存款餘額、扣繳稅額等 → 適合做比率與統計聚合。",
            "日期類(D)：核准日、指派日等 → 轉為距今天數、區間長度等時間特徵。",
            "逾期類(P)：avgdpd、maxdpd 等 → 違約風險最直接訊號。",
            "類別類(M)：地址行政區、帳戶類型等 → 樹模型可原生處理或目標編碼。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "評估指標：Gini 穩定度",
        "body": [
            "主指標為自訂的『gini stability』，不只看單一 AUC，而看跨時間(WEEK_NUM)的表現穩定度。",
            "每週計算 gini = 2×AUC − 1；對各週 gini 擬合線性迴歸取斜率 a。",
            "穩定度 = mean(gini) + 88.0×min(0, a) − 0.5×std(殘差)：效能隨時間下滑或波動都會被重罰。",
            "啟示：模型不能只追求驗證集高分，須具時間泛化力與穩健性（正則化、特徵穩定）。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "專案可行性評估",
        "body": [
            "資料面：標籤明確、特徵豐富(數百~上千)、公開 baseline 與 notebook 成熟 → 高度可行。",
            "挑戰一 類別不平衡：違約僅約 3%，須用 AUC/Gini 為主、佐以 scale_pos_weight。",
            "挑戰二 資料規模：多表數 GB，記憶體與聚合是瓶頸 → Polars/DuckDB、分塊與型別優化。",
            "挑戰三 穩定度要求：須做時間感知驗證，避免過擬合近期資料。",
            "資源：單機(16~32GB RAM) + LightGBM 即可達競爭力；GPU 非必要。",
            "商業價值高：可解釋(SHAP) 的風險因子報告可直接支援授信決策。",
            "結論：技術與資源門檻可控，建議推進，以 LightGBM 為主力先建立穩定 baseline。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "資料處理流程總覽",
        "body": [
            "1. 資料載入：parquet 讀取、以 case_id 對齊、型別優化。",
            "2. EDA：標籤不平衡、缺失率、異常碼、欄位 cardinality 與時間分布。",
            "3. 資料清理：異常值轉 NaN、日期正負號修正、類別缺失處理。",
            "4. 特徵工程：比率、時間、聚合（depth 1/2 的 mean/max/sum/std/last）。",
            "5. 特徵彙整：left join 回主表、移除高缺失/零變異/高共線特徵。",
            "6. 切分→7. 訓練→8. 評估→9. 調參→10. 推論→11. 提交檔。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "資料清理與異常處理",
        "body": [
            "異常碼：將哨兵值（如就業天數的異常極大值）統一轉為 NaN，避免污染分布。",
            "日期欄(_D)：多為相對天數，統一符號並轉為正向『距今天數』。",
            "類別欄(_M)：缺失補 'Unknown' 或保留交由 LightGBM/CatBoost 原生處理。",
            "高缺失(>80%) 與零變異欄位移除；高度共線(|r|>0.95) 擇一保留。",
            "全程固定 random seed，確保可重現性。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "特徵工程與多表彙整",
        "body": [
            "比率特徵：授信/收入、攤還/收入、負債/額度等風險敏感比值。",
            "時間特徵：年齡、年資、合約存續期間、最近一次逾期距今天數。",
            "歷史聚合（依 case_id groupby）：逾期天數的 mean/max/std、繳款準時率、未償餘額統計、申請/核准次數。",
            "depth 2 → depth 1 → base 逐層聚合，控制特徵爆炸與記憶體。",
            "類別編碼：樹模型用 Label/原生處理；必要時用平滑後的目標編碼(避免洩漏)。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "演算法選擇",
        "body": [
            "基準：Logistic Regression（標準化 + L2），建立可解釋下限。",
            "主力：LightGBM（梯度提升樹），原生支援缺失值與類別、訓練快、特徵多時表現佳。",
            "備援：XGBoost、CatBoost（類別特徵強）；可做模型集成。",
            "不平衡處理：scale_pos_weight 或 is_unbalance；以 AUC 早停。",
            "穩定度導向：較強正則化(reg_alpha/lambda)、限制樹深、特徵/樣本抽樣，換取跨時間穩健。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "驗證策略與超參數調整",
        "body": [
            "驗證：依 WEEK_NUM 做時間感知切分 / StratifiedGroupKFold，模擬未來週次、貼近 stability 評分。",
            "另留 holdout（最後一段時間）做最終驗證。",
            "調參工具：Optuna（貝氏搜尋），目標為交叉驗證平均 gini/AUC。",
            "LightGBM 主要參數：num_leaves、max_depth、learning_rate、min_child_samples、feature_fraction、bagging_fraction、reg_alpha、reg_lambda。",
            "以 5-fold 平均分數與標準差評估穩定性。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "預期成果與驗收標準",
        "body": [
            "Pipeline 可從原始檔一鍵執行至產出 submission（case_id, score）。",
            "LightGBM baseline 交叉驗證 AUC 目標 ≥ 0.78（規格書門檻）；持續優化 gini 穩定度。",
            "輸出特徵重要性 / SHAP 報告，提供業務可理解的風險因子。",
            "全流程可重現（固定 seed）、模型序列化保存，支援對測試集推論。",
        ],
    },
    {
        "layout": "TITLE_AND_BODY",
        "title": "風險、下一步與結論",
        "body": [
            "風險：特徵洩漏(時間因果)、近期分布漂移、過擬合單一時段。",
            "下一步：先建 LightGBM baseline → 時間感知 CV → 加聚合特徵 → Optuna 調參 → 監控穩定度。",
            "工程：以 Polars/DuckDB 控管資料量；Pipeline 模組化（loader/cleaning/fe/train/predict）。",
            "結論：資料完備、技術成熟、資源可控，專案高度可行，建議以穩定度為核心目標推進。",
        ],
    },
]


# ---------------------------------------------------------------------------
# 1) 產生 .pptx（本機可立即檢視）
# ---------------------------------------------------------------------------
def build_pptx(path):
    from pptx import Presentation
    from pptx.util import Pt
    prs = Presentation()
    title_layout = prs.slide_layouts[0]   # Title Slide
    body_layout = prs.slide_layouts[1]    # Title and Content
    for s in SLIDES:
        if s["layout"] == "TITLE":
            slide = prs.slides.add_slide(title_layout)
            slide.shapes.title.text = s["title"]
            if slide.placeholders and len(slide.placeholders) > 1:
                slide.placeholders[1].text = s["body"]
        else:
            slide = prs.slides.add_slide(body_layout)
            slide.shapes.title.text = s["title"]
            tf = slide.placeholders[1].text_frame
            tf.clear()
            for i, line in enumerate(s["body"]):
                p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                p.text = line
                p.font.size = Pt(16)
    prs.save(path)
    print("wrote", path, "(", len(SLIDES), "slides )")


# ---------------------------------------------------------------------------
# 2) 產生 Google Slides batchUpdate 請求（供 gws 推送）
#    使用 createSlide + placeholderIdMappings 取得可控的 objectId，
#    再以 insertText 寫入標題/內文，body 套用項目符號。
# ---------------------------------------------------------------------------
def build_batch_requests():
    requests = []
    for idx, s in enumerate(SLIDES):
        sid = f"slide_{idx}"
        if s["layout"] == "TITLE":
            title_id, sub_id = f"{sid}_title", f"{sid}_sub"
            requests.append({"createSlide": {
                "objectId": sid, "insertionIndex": idx,
                "slideLayoutReference": {"predefinedLayout": "TITLE"},
                "placeholderIdMappings": [
                    {"layoutPlaceholder": {"type": "CENTERED_TITLE", "index": 0}, "objectId": title_id},
                    {"layoutPlaceholder": {"type": "SUBTITLE", "index": 0}, "objectId": sub_id},
                ]}})
            requests.append({"insertText": {"objectId": title_id, "text": s["title"]}})
            requests.append({"insertText": {"objectId": sub_id, "text": s["body"]}})
        else:
            title_id, body_id = f"{sid}_title", f"{sid}_body"
            requests.append({"createSlide": {
                "objectId": sid, "insertionIndex": idx,
                "slideLayoutReference": {"predefinedLayout": "TITLE_AND_BODY"},
                "placeholderIdMappings": [
                    {"layoutPlaceholder": {"type": "TITLE", "index": 0}, "objectId": title_id},
                    {"layoutPlaceholder": {"type": "BODY", "index": 0}, "objectId": body_id},
                ]}})
            requests.append({"insertText": {"objectId": title_id, "text": s["title"]}})
            body_text = "\n".join(s["body"])
            requests.append({"insertText": {"objectId": body_id, "text": body_text}})
            requests.append({"createParagraphBullets": {
                "objectId": body_id,
                "textRange": {"type": "ALL"},
                "bulletPreset": "BULLET_DISC_CIRCLE_SQUARE"}})
    # 移除建立簡報時預設的第一張空白投影片（其 id 於執行期由 create_slides.sh 注入）
    requests.append({"deleteObject": {"objectId": "__DEFAULT_SLIDE_ID__"}})
    return {"requests": requests}


if __name__ == "__main__":
    build_pptx(os.path.join(OUT_DIR, "home_credit_slides.pptx"))
    with open(os.path.join(OUT_DIR, "batch_update.json"), "w", encoding="utf-8") as f:
        json.dump(build_batch_requests(), f, ensure_ascii=False, indent=2)
    print("wrote batch_update.json")
    with open(os.path.join(OUT_DIR, "deck_title.txt"), "w", encoding="utf-8") as f:
        f.write(DECK_TITLE)
