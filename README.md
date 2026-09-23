# OceanPulse - 海洋環境資料自動化觀測與統計分析平台

> 自動化流程：公開資料擷取 (ETL) $\rightarrow$ 數值/統計運算 (NumPy / SciPy) $\rightarrow$ 繪圖視覺化 (ECharts / Leaflet) $\rightarrow$ GitHub Actions 定期排程更新 $\rightarrow$ 網站展示 (GitHub Pages)

![Status](https://img.shields.io/badge/status-active-emerald.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Frontend](https://img.shields.io/badge/Frontend-TailwindCSS%20%7C%20ECharts%20%7C%20Leaflet-0284c7.svg)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-purple.svg)

---

## 🌟 專案特色

1. **多維海洋指標監測 (KPI Cards)**：海表水溫 (SST) 與氣候距平、顯著波高 (Hs) 與波浪週期、海水鹽度 (SSS)、表層海流 (Current Speed & Direction)、葉綠素 a (Chl-a) 濃度、天文潮位 (Tide)。
2. **海域測站地理分佈地圖 (Leaflet.js)**：互動式標註富貴角、花蓮、東港、澎湖、墾丁等海域浮標測站，支援一鍵切換與平滑縮放。
3. **科學統計與視覺化 (Apache ECharts)**：
   - 72 小時歷史數據與 24 小時預報時序圖（含 12 小時移動平均濾波去噪）。
   - CTD 垂直水深剖面分析（0 ~ 200m 水溫與鹽度剖面、溫躍層 Thermocline 識別）。
   - 16 方位海流與波浪能量分佈極座標玫瑰圖 (Current Rose)。
4. **零伺服器維護成本 (Serverless)**：利用 GitHub Actions 定時執行 Python ETL 腳本，輸出靜態 JSON，並由 GitHub Pages 快速提供展示。

---

## 📂 目錄結構

```text
├── index.html                     # 前端儀表板展示頁面 (Tailwind + ECharts + Leaflet)
├── pipeline/
│   └── update_ocean_data.py       # Python 資料擷取、NumPy/SciPy 統計與濾波計算
├── output/
│   └── latest_ocean_metrics.json  # 計算後的輕量化 JSON 成果 (前端直接讀取)
├── .github/
│   └── workflows/
│       └── update_data.yml        # GitHub Actions 自動定時排程 (每天定時更新)
├── requirements.txt               # Python 依賴套件
└── README.md                      # 專案說明文件
```

---

## 🚀 本地快速啟動

### 1. 檢視前端網頁
直接在瀏覽器開啟 `index.html` 即可瀏覽完整互動儀表板。

### 2. 執行 Python 資料擷取與計算管線
```bash
pip install -r requirements.txt
python pipeline/update_ocean_data.py
```

---

## ⚙️ 啟用 GitHub Pages 免費託管

1. 在 GitHub Repository 頁面點擊 **Settings**。
2. 在左側選單點選 **Pages**。
3. 在 **Build and deployment** 下方的 **Branch** 選擇 `main` 分支並選擇 `/ (root)` 目錄，點擊 **Save**。
4. 稍等約 1 分鐘即可透過 `https://<您的帳號>.github.io/<專案名稱>/` 訪問公開網站！
