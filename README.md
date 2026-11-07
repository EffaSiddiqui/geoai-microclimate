# GeoAI Micro-Climate Temperature Prediction

## Problem
Small differences in micro-climate between campus and urban areas matter for planning.
This project predicts the temperature one hour ahead.

## Dataset
Open-Meteo Historical Weather API (reanalysis data, not live sensor data).
Location: Karachi (24.86, 67.01). Period: 2024, hourly.

## Method
- Features: lag values (t-1, t-2, t-3, t-24), rolling means, hour (sin/cos),
  day of week, month, humidity, pressure, cloud cover, wind speed
- Split: time-based (first 9 months for training, last 3 months for testing)
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
The output table is saved to `results/metrics.csv`.

## Limitations
- One location only
- Reanalysis data, not live sensor data
- Software prototype only; edge deployment was not tested
- Short prediction horizon (1 hour)

## Future work
Multiple locations, live IoT sensor data, interactive heatmap.

## AI use disclosure
This project was built with the help of AI tools (code structure and documentation drafting).
The results were verified by running the code.
