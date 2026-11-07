# GeoAI Micro-Climate Temperature Prediction

## Problem
Campus aur urban areas mein micro-climate ke chhote farq planning ke liye ahem hain.
Ye project agle ghante ka temperature predict karta hai.

## Dataset
Open-Meteo Historical Weather API (reanalysis data, live sensor data nahi).
Location: Karachi (24.86, 67.01). Period: 2024, hourly.

## Method
- Features: lag values (t-1, t-2, t-3, t-24), rolling means, hour (sin/cos),
  day of week, month, humidity, pressure, cloud cover, wind speed
- Split: time-based (pehle 9 mahine train, aakhir ke 3 mahine test)
- Models: Persistence, Linear Regression, Random Forest

## Results (test set)

| Model             | MAE   | RMSE  | R2    |
|-------------------|-------|-------|-------|
| Persistence       | 0.787 | 1.045 | 0.960 |
| Linear Regression | 0.772 | 0.988 | 0.964 |
| Random Forest     | 0.572 | 0.782 | 0.977 |

Test rows: 2207 | Train rows: 6552

## How to run
```bash
pip install -r requirements.txt
python main.py
```
Output table `results/metrics.csv` mein save hota hai.

## Limitations
- Sirf ek location
- Reanalysis data, live sensor nahi
- Sirf software prototype, edge deployment test nahi kiya gaya
- Short prediction horizon (1 hour)

## Future work
Multiple locations, live IoT sensor data, interactive heatmap.

## AI use disclosure
Ye project AI tools ki madad se bana hai (code structure aur documentation drafting).
Results ka verification code ko khud run karke kiya gaya hai.
