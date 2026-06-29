# Home Credit 信用違約風險 — 簡報產出

依附件 `spec.md`（訓練流程規格書）與 `Home_Credit_2024…xlsx`（465 欄特徵字典）製作的專案介紹／可行性評估簡報，並提供以 **gws（Google Workspace CLI）** 推送成 **Google Slides** 的腳本。

## 檔案

| 檔案 | 說明 |
|---|---|
| `build_slides.py` | **單一資料來源**：13 張投影片內容。產生 `.pptx` 與 `batch_update.json`。 |
| `home_credit_slides.pptx` | 可立即檢視的本機簡報（13 張）。 |
| `batch_update.json` | Google Slides API `batchUpdate` 請求（52 個 request）。 |
| `create_slides.sh` | 用 gws 建立簡報並寫入內容。 |
| `deck_title.txt` | 簡報標題。 |

## 為什麼附 .pptx 而非直接產出 Google Slides？

本次執行環境（雲端沙箱）**未安裝 gws，且無法進行 Google OAuth**（Google API 不在出口代理允許清單、`gws auth login` 需互動式瀏覽器）。因此無法在此直接推送到你的 Google Slides。已改為：

1. 產生內容完全相同的 `.pptx` 供你立即檢視；
2. 附上 `create_slides.sh`，在**你本機已認證的 gws** 上一鍵生成 Google Slides。

## 在本機產出 Google Slides

```bash
npm install -g @googleworkspace/cli   # 安裝 gws
gws auth login                        # 瀏覽器 OAuth（需 Slides 權限）
cd home-credit-slides
python3 build_slides.py               # 產生 batch_update.json
bash create_slides.sh                 # 建立並填入 Google Slides，輸出可開啟連結
```

> gws 將 Discovery 的 path/query 參數對應到 `--params`、request body 對應到 `--json`。
> 若旗標與你的版本不同，先用 `gws slides presentations --help` 與
> `gws schema slides.presentations.batchUpdate` 確認再微調 `create_slides.sh`。

---

## 內容重點

### 資料集辨識（重要）
附件特徵字典的欄位命名（`_1115A`、`_319D`、`_368M`、`_943P`…）屬於 **2024「Home Credit – Credit Risk Model Stability」** 競賽：主鍵 `case_id`、含 `WEEK_NUM`、評分採自訂 **gini 穩定度**。
而 `spec.md` 描述的是 **2018「Home Credit Default Risk」**（主鍵 `SK_ID_CURR`、多張 csv、AUC 評分）。
兩者 Pipeline 高度相通，本簡報以 2024 實際資料為準、沿用規格書流程架構。

### 特徵字典統計（465 欄）
後綴即型別線索：`L` 一般 187、`A` 金額 102、`M` 遮罩類別 63、`D` 日期 57、`P` 逾期天數 33、`T` 其他 22。

### 可行性結論
資料完備、公開 baseline 成熟、單機 + LightGBM 即具競爭力、商業價值高（可解釋風險因子）。
主要挑戰為**類別不平衡（違約約 3%）**、**多表數 GB 的記憶體／聚合**、以及**時間穩定度要求**——皆有成熟對策，專案**高度可行**。

### 演算法
Logistic Regression（基準）→ LightGBM（主力，原生支援缺失值／類別）→ XGBoost/CatBoost（備援/集成）；以時間感知 CV + Optuna 調參，並偏向較強正則化以換取跨時間穩健。
