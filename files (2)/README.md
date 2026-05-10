# 📊 Data Intelligence Hub

An AI-powered universal data analytics platform — upload **any CSV or Excel file** and get instant EDA, dashboards, advanced analytics, and Gemini AI insights.

---

## 🚀 Deploy to Streamlit Cloud (Free)

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2 — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
2. Click **"New app"**
3. Select your repository, branch (`main`), and set **Main file path** to `app.py`
4. Click **"Advanced settings"** → **"Secrets"** and paste:

```toml
GEMINI_API_KEY = "AIza-your-key-here"
```

5. Click **"Deploy"** — live in ~2 minutes ✅

> Get your free Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## ⚡ Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Gemini API key
echo "GEMINI_API_KEY=AIza-your-key-here" > .env

# 3. Run
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## 📁 Required File Structure

```
your-repo/
├── app.py                        ← Main app (required)
├── requirements.txt              ← Dependencies (required)
├── .streamlit/
│   └── config.toml               ← Theme & server config (required)
├── .gitignore                    ← Keeps secrets out of GitHub
└── README.md
```

> ⚠️ **Never push `.streamlit/secrets.toml` to GitHub.** It's already in `.gitignore`.

---

## 📊 Features

| Tab | What you get |
|-----|-------------|
| **Dashboard** | KPI cards, time-series, category charts, distributions, data preview |
| **Full EDA** | Dataset overview, stats, univariate/bivariate analysis, correlation heatmap, outlier detection, time series |
| **Advanced Analytics** | Pivot heatmap, group aggregations, period-over-period growth, scatter matrix |
| **AI Analyst** | Chat with Gemini about your data — context-aware, conversation history, quick questions |

---

## 🛠️ Tech Stack

Streamlit · Plotly · Pandas · NumPy · SciPy · Google Gemini (`gemini-2.0-flash`)
