# Unemployment Analysis and Prediction in India and Pakistan

This project analyzes unemployment trends in India and Pakistan using data visualization and machine learning. By identifying key socio-economic drivers and forecasting future rates, it provides actionable insights for data-driven economic decision-making.

➡️ **[Live Demo of the Interactive Tableau Dashboard](https://unemployment-analysis-and-prediction-in.onrender.com/)** 

---

### 1. The Business Problem

Unemployment is a critical economic indicator that shapes national policy and social stability. For governments and economists in South Asia, understanding the interplay between population growth, GDP, and inflation is essential, yet often obscured by complex, high-dimensional data.

* **Policymakers** struggle to isolate specific causes of unemployment spikes.
* **Economic Planners** lack precise forecasting tools for future labor market trends.

Our project tackled this problem by building a machine learning pipeline to replace retrospective reporting with **predictive economic intelligence**, empowering stakeholders to anticipate challenges rather than just react to them.

---

### 2. My Technical Approach

To solve this, I developed an end-to-end data science pipeline:

* **Data Collection & Merging:** Aggregated multi-dimensional datasets including Population, Inflation, GDP, and Employment by Sector for India and Pakistan.
* **Data Preprocessing:** Utilized Pandas for extensive cleaning, including handling null values, categorical encoding, and reshaping data from wide to long formats for time-series compatibility.
* **Exploratory Data Analysis (EDA):** Leveraged Seaborn and Matplotlib to visualize historical trends, identifying correlations between economic sectors and unemployment rates.
* **Model Training:** Experimented with multiple regression techniques:
    * *Linear Regression & Lasso* for baseline trends.
    * *Random Forest* for capturing non-linear relationships.
    * *XGBoost* for high-performance gradient boosting.
* **Optimization:** Applied `RandomizedSearchCV` for hyperparameter tuning to prevent overfitting.
* **Visualization:** Designed an interactive **Tableau Dashboard** to communicate findings effectively.

---

### 3. The Solution & Key Findings

The final solution offers a dual-pronged approach to economic analysis:

#### 🧭 **Analysis Dashboard (Tableau)**
* **Historical Trends:** Interactive timelines of unemployment variations over the years.
* **Sector Breakdown:** Visual analysis of employment distribution across Agriculture, Industry, and Services.
* **Regional Comparison:** Direct side-by-side comparison of India and Pakistan's economic indicators.

#### 📊 **Model Performance**
The machine learning models achieved exceptional accuracy in forecasting unemployment rates:

* **Best Model:** XGBoost Regressor
* **Test Set R² Score:** **~0.96** (Explains 96% of the variance in the data)
* **Test RMSE:** Extremely low error rates (e.g., ~0.0003 in normalized scale), indicating precise predictions.

**Key Findings:**
* **GDP & Inflation:** Strong correlation found between GDP growth stability and unemployment reduction.
* **Population Dynamics:** Rapid population changes significantly lag labor force absorption.
* **Model Robustness:** Ensemble methods (Random Forest/XGBoost) significantly outperformed linear baselines in capturing market volatility.

---

### 4. Business Impact

This project transforms raw economic statistics into **accessible decision-support tools**:

✅ **Evidence-Based Policy Making**
Enables governments to simulate how changes in GDP or inflation targets might impact future unemployment.

✅ **Strategic Resource Allocation**
Identifies which sectors (Agriculture vs. Services) are underperforming, guiding targeted investment.

✅ **Regional Benchmarking**
Provides a comparative framework to understand how similar economies react differently to global economic shifts.

---

### 5. Future Enhancements

* **Granular Analysis:** Incorporate state or province-level data to identify localized unemployment hotspots.
* **Real-time Integration:** Connect to live economic APIs (e.g., World Bank API) for automated monthly updates.
* **Deep Learning:** Experiment with LSTM (Long Short-Term Memory) networks for better handling of long-term time-series dependencies.
* **Education Correlation:** Add datasets regarding literacy rates and education quality to analyze the "skills gap."

---

### Author

**Kaung Si Thu**
[kaungsithu.sallius@gmail.com](mailto:kaungsithu.sallius@gmail.com)
