"""
Ocean Environmental Data Pipeline (海洋環境資料自動化運算腳本)
示範如何將「公開資料擷取 -> 統計計算與濾波 -> 導出 JSON」自動化
"""

import json
import os
import datetime
import numpy as np

def fetch_ocean_raw_data():
    """
    第一步：資料擷取 (可替換為 requests / httpx 呼叫政府氣象局、NOAA 或浮標 API)
    """
    print("[1/4] 正在從海洋浮標資料庫與公開 API 擷取即時觀測數據...")
    # 此處模擬自 API 獲取的海溫、波高、鹽度時間序列
    now = datetime.datetime.now(datetime.timezone.utc)
    timestamps = [(now - datetime.timedelta(hours=i*2)).strftime("%m/%d %H:00") for i in range(48, -1, -1)]
    
    # 模擬 48 小時原始觀測海溫 (加入高頻雜訊)
    t = np.linspace(0, 4 * np.pi, len(timestamps))
    raw_sst = 25.5 + 0.8 * np.sin(t) + np.random.normal(0, 0.2, len(timestamps))
    raw_wave = 1.2 + 0.5 * np.cos(t * 0.8) + np.random.uniform(0, 0.3, len(timestamps))
    
    return {
        "timestamps": timestamps,
        "raw_sst": raw_sst,
        "raw_wave": raw_wave
    }

def process_numerical_computations(data):
    """
    第二步：數值與統計運算 (利用 NumPy / SciPy 進行平滑濾波、異常值檢測、躍層梯度)
    """
    print("[2/4] 執行數值清洗、高斯平滑濾波 (SMA) 與溫鹽躍層梯度計算...")
    
    # 1. 滾動滑動平均濾波 (SMA-5)
    window_size = 5
    kernel = np.ones(window_size) / window_size
    smoothed_sst = np.convolve(data["raw_sst"], kernel, mode='same')
    
    # 2. 海溫統計指標 (平均值、標準差、氣候距平)
    climatology_mean = 25.0
    current_sst = float(np.round(smoothed_sst[-1], 2))
    anomaly = float(np.round(current_sst - climatology_mean, 2))
    
    # 3. 顯著波高統計計算 (Hs: 前 1/3 最大波高平均)
    sorted_waves = np.sort(data["raw_wave"])
    hs = float(np.round(np.mean(sorted_waves[-int(len(sorted_waves)/3):]), 2))
    
    # 4. CTD 垂直水深剖面 (0~200m) 與躍層梯度計算 (dT/dz)
    depths = np.array([0, 10, 20, 30, 40, 50, 75, 100, 150, 200])
    profile_temp = 26.5 - 0.04 * depths - 4.5 / (1 + np.exp(-(depths - 45) / 10))
    temp_gradients = np.gradient(profile_temp, depths)
    thermocline_depth = float(depths[np.argmin(temp_gradients)]) # 梯度最大處為溫躍層中心
    
    return {
        "metrics": {
            "current_sst": current_sst,
            "sst_anomaly": anomaly,
            "significant_wave_height": hs,
            "thermocline_depth_meters": thermocline_depth,
            "update_time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        "time_series": {
            "timestamps": data["timestamps"],
            "raw_sst": [round(x, 2) for x in data["raw_sst"].tolist()],
            "smoothed_sst": [round(x, 2) for x in smoothed_sst.tolist()],
            "wave_height": [round(x, 2) for x in data["raw_wave"].tolist()]
        },
        "vertical_profile": {
            "depths": depths.tolist(),
            "temperatures": [round(x, 2) for x in profile_temp.tolist()],
            "gradients": [round(x, 3) for x in temp_gradients.tolist()]
        }
    }

def export_json_for_frontend(processed_data, output_path="output/latest_ocean_metrics.json"):
    """
    第三步：導出為靜態 JSON 供前端 ECharts / Leaflet 直接載入
    """
    print(f"[3/4] 導出輕量化靜態 JSON: {output_path} ...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
    print("[4/4] Pipeline 執行完成！已準備好供 GitHub Actions / 靜態網站發布。")

if __name__ == "__main__":
    raw = fetch_ocean_raw_data()
    processed = process_numerical_computations(raw)
    export_json_for_frontend(processed, output_path="output/latest_ocean_metrics.json")
