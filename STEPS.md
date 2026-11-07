# Step-by-Step Guide: GeoAI Micro-Climate

This guide takes you from the start of the project to GitHub. Move to the next step only after the previous one is complete.

---

## Step 1: Open Google Colab
1. Go to `colab.research.google.com` in your browser.
2. Log in with your Google account.
3. Create a **New notebook**.

## Step 2: Run main.py
1. Paste the full code of `main.py` into one cell.
2. Click the Play (▶) button on the cell.
3. The output is a table.
4. Copy these numbers (or download the `results/metrics.csv` file).
5. If you get an error, check your internet connection and run the cell again.

## Step 3: Fill in the numbers in the README
1. Open `README.md`.
2. In the results table, replace each `[ ]` with the number from the output.
3. **Important:** do not round the numbers, and do not change them to look better.
4. If Random Forest does not beat Persistence, still report it. That is a valid result.

## Step 4: Create a GitHub repository
1. Log in to `github.com`.
2. Click **+** at the top right, then **New repository**.
3. Repository name: `geoai-microclimate`
4. Visibility: **Public**
5. Click **Create repository**.

## Step 5: Upload the files
1. On the repository page, click **uploading an existing file**.
2. Drag these files from the project folder:
   - `main.py`
   - `requirements.txt`
   - `README.md`
   - `STEPS.md` (optional, useful for your presentation)
   - `.gitignore`
3. Click **Commit changes**.
4. Copy the repository link (for example, `https://github.com/your-username/geoai-microclimate`) and paste it into the form.

## Step 6: Understand the code
Read the section below before your presentation. If a line is unclear, ask about it.

---

## Line-by-line explanation of the code

### Imports
| Line | Meaning |
|------|---------|
| `os` | Creates the results folder |
| `numpy` | Math calculations (sin, cos, sqrt) |
| `pandas` | Handles data in tables (DataFrame) |
| `requests` | Fetches data from the internet (API call) |
| `RandomForestRegressor` | The Random Forest model |
| `LinearRegression` | The simple straight-line model |
| `mean_absolute_error`, `mean_squared_error`, `r2_score` | Ways to measure how good the model is |

### Settings
| Line | Meaning |
|------|---------|
| `LAT, LON = 24.86, 67.01` | Latitude and longitude of Karachi |
| `URL` | Address of the Open-Meteo historical weather API |
| `VARS` | Which data we want: temperature, humidity, pressure, cloud cover, wind speed |

### `fetch_data()`: get the data
- `requests.get(...)`: sends a request to the API asking for hourly 2024 data.
- `r.raise_for_status()`: if the API returns an error, the program stops here.
- `pd.DataFrame(...)`: converts the JSON response into a table.
- `pd.to_datetime`: converts the time column into a proper date-time format.
- `sort_values` and `drop_duplicates`: sorts by time and removes duplicate rows.
- `interpolate()`: fills missing values using the nearby values.

### `make_features()`: build the model inputs
- **Target** = next hour's temperature (`T.shift(-1)`).
- **Lag features** = temperature 1, 2, 3, and 24 hours earlier (`T.shift(k)`).
- **Rolling mean** = average of the previous 3 and 24 hours.
- **hour_sin, hour_cos** = time of day as a circle. This makes 23:00 and 00:00 appear close together.
- **dow, month** = day of the week and month (seasonal effects).
- `.dropna()`: removes rows that still have empty values.
- **No leakage:** features use only past values, never future ones. Otherwise the model would be cheating.

### `metrics()`: the model score
- **MAE** (Mean Absolute Error): the average size of the error, in degrees. Lower is better.
- **RMSE**: gives large errors more weight. Lower is better.
- **R2**: how much of the variation the model explains. Closer to 1 is better. A value of 0 means no better than the average.

### `main()`: putting it all together
1. Fetch the data and build the features.
2. **Time-based split:** training is 1 January to 30 September, testing is 1 October to 31 December. We do not split randomly, because in a time series the model must not learn from the future.
3. `feature_cols`: all columns used as inputs (everything except time and target).
4. **Persistence:** simply predicts that the next hour will be the same as the current one. This is the simple baseline the AI models must beat.
5. **Linear Regression:** a weighted sum of the inputs. A simple model.
6. **Random Forest:** 200 decision trees, each slightly different. The final prediction is their average. `max_depth=12` stops the trees from becoming too deep (less overfitting). `random_state=42` gives the same result on every run.
7. Prints the table for all three models and saves it to `results/metrics.csv`.

---

## Tips for your presentation
- Start with the **problem**: why micro-climate matters.
- Then the **data**: Open-Meteo reanalysis, not live sensors.
- Then the **split** and **features**: why a time-based split, why lag features.
- Then the **results table**: how the models compare to Persistence.
- End with the **limitations** and **future work**.
- If someone asks something you do not know, say: "That is my understanding, and I can check it." An honest answer is always better.

## Checklist before submission
- [ ] I ran the code myself in Colab and got the output
- [ ] The `[ ]` numbers in the README are filled in and match the output
- [ ] The GitHub repository is **Public**
- [ ] `main.py`, `requirements.txt`, and `README.md` are in the repository
- [ ] I added the repository link to the form
- [ ] I checked the IEEE AI-use disclosure rules and mentioned AI use if required
