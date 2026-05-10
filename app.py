import os
import io
import warnings
warnings.filterwarnings('ignore')

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Data Intelligence Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --bg: #0a0e1a;
    --surface: #111827;
    --surface2: #1a2234;
    --accent: #6366f1;
    --accent2: #22d3ee;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
    --text: #e2e8f0;
    --muted: #64748b;
    --border: #1e293b;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp { background: var(--bg) !important; }

section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

h1, h2, h3 { color: var(--text) !important; }

.kpi-card {
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 32px rgba(99,102,241,0.2);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.kpi-value {
    font-size: 1.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #e2e8f0, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'JetBrains Mono', monospace;
    word-break: break-all;
}
.kpi-label {
    color: var(--muted);
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 8px;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 24px 0 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}
.section-header h3 { margin: 0; font-size: 1.1rem; font-weight: 600; }
.section-badge {
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    color: white;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
}

.chat-msg-user {
    background: linear-gradient(135deg, var(--accent), #4f46e5);
    color: white;
    padding: 12px 16px;
    border-radius: 16px 16px 4px 16px;
    margin: 8px 0 8px 40px;
    font-size: 0.9rem;
}
.chat-msg-ai {
    background: var(--surface2);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 12px 16px;
    border-radius: 16px 16px 16px 4px;
    margin: 8px 40px 8px 0;
    font-size: 0.9rem;
    line-height: 1.6;
}
.chat-msg-label {
    font-size: 0.7rem;
    color: var(--muted);
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    padding: 8px 20px !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--accent), #4f46e5) !important;
    color: white !important;
}

.stTextInput > div > div, .stTextArea > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
.stButton button {
    background: linear-gradient(135deg, var(--accent), #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: opacity 0.2s;
}
.stButton button:hover { opacity: 0.85 !important; }

[data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

[data-testid="stFileUploader"] {
    background: var(--surface) !important;
    border: 2px dashed var(--accent) !important;
    border-radius: 16px !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

.hero-title {
    background: linear-gradient(135deg, #e2e8f0 0%, #6366f1 50%, #22d3ee 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.2rem;
    font-weight: 700;
    line-height: 1.2;
}
.hero-sub { color: var(--muted); font-size: 1rem; margin-top: 8px; }

.info-box {
    background: var(--surface2);
    border: 1px solid var(--accent);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 12px 0;
    color: var(--text);
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY THEME ─────────────────────────────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Space Grotesk', color='#e2e8f0', size=12),
    colorway=['#6366f1','#22d3ee','#10b981','#f59e0b','#ef4444','#a78bfa','#34d399','#fbbf24'],
    xaxis=dict(gridcolor='#1e293b', linecolor='#1e293b', tickcolor='#64748b'),
    yaxis=dict(gridcolor='#1e293b', linecolor='#1e293b', tickcolor='#64748b'),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#1e293b'),
    margin=dict(t=50, b=40, l=40, r=20),
)

# ─── SAMPLE DATA GENERATOR ────────────────────────────────────────────────────
def generate_sample_data():
    import random
    from datetime import datetime, timedelta
    np.random.seed(42)
    random.seed(42)
    n = 5000
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Beauty', 'Toys', 'Automotive']
    regions = ['North', 'South', 'East', 'West', 'Central']
    channels = ['Website', 'Mobile App', 'Marketplace', 'Social Media']
    payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Wallet']
    customer_segments = ['New', 'Returning', 'VIP', 'At-Risk']
    shipping_status = ['Delivered', 'Shipped', 'Processing', 'Returned', 'Cancelled']
    cat_price_range = {
        'Electronics': (500, 80000), 'Clothing': (200, 5000),
        'Home & Kitchen': (300, 15000), 'Books': (100, 800),
        'Sports': (400, 20000), 'Beauty': (150, 3000),
        'Toys': (200, 4000), 'Automotive': (800, 50000),
    }
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = [start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) for _ in range(n)]
    category_list = [random.choice(categories) for _ in range(n)]
    prices = [round(random.uniform(*cat_price_range[c]), 2) for c in category_list]
    quantities = np.random.choice([1, 2, 3, 4, 5], n, p=[0.5, 0.25, 0.12, 0.08, 0.05])
    discounts = np.random.choice([0, 5, 10, 15, 20, 25], n, p=[0.4, 0.15, 0.2, 0.1, 0.1, 0.05])
    revenue = [round(p * q * (1 - d/100), 2) for p, q, d in zip(prices, quantities, discounts)]
    ratings = np.round(np.clip(np.random.normal(4.0, 0.8, n), 1, 5), 1)
    df = pd.DataFrame({
        'order_id': [f'ORD{100000 + i}' for i in range(n)],
        'order_date': pd.to_datetime(dates),
        'customer_id': [f'CUST{random.randint(1000, 9999)}' for _ in range(n)],
        'customer_segment': [random.choice(customer_segments) for _ in range(n)],
        'category': category_list,
        'product_name': [f'{c} Product {random.randint(1,50)}' for c in category_list],
        'region': [random.choice(regions) for _ in range(n)],
        'channel': [random.choice(channels) for _ in range(n)],
        'payment_method': [random.choice(payment_methods) for _ in range(n)],
        'unit_price': prices,
        'quantity': quantities,
        'discount_pct': discounts,
        'revenue': revenue,
        'shipping_status': [random.choice(shipping_status) for _ in range(n)],
        'rating': ratings,
        'return_flag': [1 if s == 'Returned' else 0 for s in [random.choice(shipping_status) for _ in range(n)]],
        'profit': [round(r * np.random.uniform(0.1, 0.4), 2) for r in revenue],
    })
    return df

# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_uploaded_file(file_bytes, file_name):
    if file_name.lower().endswith('.csv'):
        df = pd.read_csv(io.BytesIO(file_bytes))
    elif file_name.lower().endswith(('.xlsx', '.xls')):
        df = pd.read_excel(io.BytesIO(file_bytes))
    else:
        raise ValueError(f"Unsupported file type: {file_name}")
    return df

def detect_datetime_cols(df):
    dt_cols = []
    for col in df.columns:
        if df[col].dtype == 'object':
            sample = df[col].dropna().head(50)
            try:
                parsed = pd.to_datetime(sample, errors='coerce')
                if parsed.notna().mean() > 0.8:
                    dt_cols.append(col)
            except Exception:
                pass
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            dt_cols.append(col)
    return dt_cols

def prepare_df(df):
    """Parse datetime columns and add helper time cols."""
    dt_cols = detect_datetime_cols(df)
    for col in dt_cols:
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        except Exception:
            pass
    return df, dt_cols

def get_col_groups(df):
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    dt_cols = df.select_dtypes(include='datetime').columns.tolist()
    bool_cols = df.select_dtypes(include='bool').columns.tolist()
    return num_cols, cat_cols, dt_cols, bool_cols

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 Data Intelligence Hub")
    st.markdown("---")

    st.markdown("**🔑 Gemini API Key**")
    api_key_env = os.getenv("GEMINI_API_KEY", "")
    try:
        api_key_secret = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key_secret = ""
    default_key = api_key_env or api_key_secret or st.session_state.get("gemini_key", "")

    api_key_input = st.text_input("", type="password", value=default_key, placeholder="AIza...")
    if api_key_input:
        st.session_state.gemini_key = api_key_input
        st.success("✓ API key set")

    st.markdown("---")
    st.markdown("**📁 Upload Your Data**")
    uploaded = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="Upload any CSV or Excel file to explore it"
    )
    use_sample = st.checkbox("Use built-in e-commerce sample data", value=(uploaded is None))
    st.markdown("---")

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
is_sample = False
if uploaded is not None:
    try:
        raw_df = load_uploaded_file(uploaded.getvalue(), uploaded.name)
        with st.sidebar:
            st.success(f"✓ Loaded **{len(raw_df):,}** rows × **{raw_df.shape[1]}** cols")
        is_sample = False
    except Exception as e:
        st.sidebar.error(f"❌ Failed to load file: {e}")
        raw_df = generate_sample_data()
        is_sample = True
else:
    raw_df = generate_sample_data()
    is_sample = True
    with st.sidebar:
        st.info(f"📊 Sample dataset: {len(raw_df):,} rows")

# Parse dates
raw_df, dt_cols_detected = prepare_df(raw_df)
num_cols, cat_cols, dt_cols, bool_cols = get_col_groups(raw_df)

# ─── SIDEBAR FILTERS ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("**🔧 Filters**")
    active_filters = {}

    # Up to 3 categorical filters
    if cat_cols:
        filter_cats = cat_cols[:3]
        for col in filter_cats:
            unique_vals = sorted(raw_df[col].dropna().unique().tolist())
            if len(unique_vals) <= 50:
                sel = st.multiselect(col, unique_vals, default=unique_vals, key=f"filter_{col}")
                active_filters[col] = sel

    st.markdown("---")
    st.markdown("<small style='color:#64748b'>Built with Streamlit + Gemini AI</small>", unsafe_allow_html=True)

# Apply filters
df = raw_df.copy()
for col, vals in active_filters.items():
    if vals:
        df = df[df[col].isin(vals)]

if df.empty:
    st.warning("⚠️ No data matches the current filters. Please broaden your selection.")
    st.stop()

# ─── REFRESH column groups after filter ───────────────────────────────────────
num_cols, cat_cols, dt_cols, bool_cols = get_col_groups(df)

# ─── HEADER ───────────────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    title = "E-Commerce Intelligence Hub" if is_sample else f"📊 {uploaded.name if uploaded else 'Data'} — Intelligence Hub"
    st.markdown(f'<p class="hero-title">{title}</p>', unsafe_allow_html=True)
    sub = "Power BI Dashboard · Full EDA · Advanced Analytics · AI Analyst" if is_sample else "Universal EDA · Dashboard · Advanced Analytics · AI Analyst"
    st.markdown(f'<p class="hero-sub">{sub}</p>', unsafe_allow_html=True)
with col_h2:
    st.markdown(
        f"<div style='text-align:right;padding-top:20px'>"
        f"<span style='color:#64748b;font-size:0.8rem'>ROWS × COLS</span><br>"
        f"<span style='font-size:1.4rem;font-weight:700;color:#6366f1'>{len(df):,} × {df.shape[1]}</span>"
        f"</div>", unsafe_allow_html=True
    )

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔬 Full EDA", "📈 Advanced Analytics", "🤖 AI Analyst"])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1: DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## 📊 Dashboard Overview")

    # ── KPI Cards (top numeric columns) ──────────────────────────────────────
    kpi_cols = num_cols[:8] if len(num_cols) >= 8 else num_cols
    if kpi_cols:
        n_kpi = min(len(kpi_cols), 4)
        cols_kpi = st.columns(n_kpi)
        for i, col_name in enumerate(kpi_cols[:4]):
            val = df[col_name].sum()
            avg_val = df[col_name].mean()
            with cols_kpi[i]:
                if val >= 1e9:
                    disp = f"{val/1e9:.2f}B"
                elif val >= 1e6:
                    disp = f"{val/1e6:.2f}M"
                elif val >= 1e3:
                    disp = f"{val/1e3:.1f}K"
                else:
                    disp = f"{val:.2f}"
                st.markdown(f"""
                <div class="kpi-card">
                    <div class="kpi-value">{disp}</div>
                    <div class="kpi-label">Total {col_name}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if len(kpi_cols) > 4:
            cols_kpi2 = st.columns(min(len(kpi_cols) - 4, 4))
            for i, col_name in enumerate(kpi_cols[4:8]):
                val = df[col_name].mean()
                if abs(val) >= 1e6:
                    disp = f"{val/1e6:.2f}M"
                elif abs(val) >= 1e3:
                    disp = f"{val/1e3:.1f}K"
                else:
                    disp = f"{val:.3f}"
                with cols_kpi2[i]:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-value">{disp}</div>
                        <div class="kpi-label">Avg {col_name}</div>
                    </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Basic row/col counts
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Total Rows", f"{len(df):,}")
    col_b.metric("Total Columns", df.shape[1])
    col_c.metric("Numeric Columns", len(num_cols))
    col_d.metric("Categorical Columns", len(cat_cols))

    st.markdown("---")

    # ── Time-series chart (if datetime column exists) ──────────────────────
    if dt_cols and num_cols:
        st.markdown('<div class="section-header"><h3>📅 Time Series</h3><span class="section-badge">Trend</span></div>', unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            ts_date_col = st.selectbox("Date column", dt_cols, key="dash_ts_date")
        with c2:
            ts_val_col = st.selectbox("Value column", num_cols, key="dash_ts_val")

        ts_df = df[[ts_date_col, ts_val_col]].dropna()
        ts_df = ts_df.set_index(ts_date_col).resample('ME')[ts_val_col].sum().reset_index()
        fig = px.area(ts_df, x=ts_date_col, y=ts_val_col,
                      color_discrete_sequence=['#6366f1'],
                      title=f"Monthly {ts_val_col} Trend")
        fig.update_traces(mode='lines+markers', line_width=2.5, marker_size=5)
        fig.update_layout(**PLOTLY_THEME, height=300)
        st.plotly_chart(fig, use_container_width=True)

    # ── Categorical bar charts ──────────────────────────────────────────────
    if cat_cols and num_cols:
        st.markdown('<div class="section-header"><h3>📊 Category Breakdown</h3></div>', unsafe_allow_html=True)
        num_chart_cats = min(len(cat_cols), 3)
        chart_cols = st.columns(num_chart_cats)
        for i, cc in enumerate(cat_cols[:3]):
            with chart_cols[i]:
                top_n = df.groupby(cc)[num_cols[0]].sum().sort_values(ascending=False).head(10).reset_index()
                fig = px.bar(top_n, x=cc, y=num_cols[0], color=num_cols[0],
                             color_continuous_scale='Viridis',
                             title=f"{num_cols[0]} by {cc}")
                fig.update_layout(**PLOTLY_THEME, height=280, coloraxis_showscale=False,
                                  xaxis_tickangle=-20)
                st.plotly_chart(fig, use_container_width=True)

    # ── Distribution of top numeric col ────────────────────────────────────
    if num_cols:
        st.markdown('<div class="section-header"><h3>📈 Numeric Distributions</h3></div>', unsafe_allow_html=True)
        dist_cols = num_cols[:4]
        d_cols = st.columns(len(dist_cols))
        for i, nc in enumerate(dist_cols):
            with d_cols[i]:
                fig = px.histogram(df, x=nc, nbins=30, color_discrete_sequence=['#6366f1'],
                                   title=nc)
                fig.update_layout(**PLOTLY_THEME, height=220)
                st.plotly_chart(fig, use_container_width=True)

    # ── Data preview ────────────────────────────────────────────────────────
    st.markdown('<div class="section-header"><h3>📋 Data Preview</h3></div>', unsafe_allow_html=True)
    st.dataframe(df.head(50), use_container_width=True, height=350)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2: FULL EDA
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## 🔬 Exploratory Data Analysis")

    # Dataset Overview
    st.markdown("### 📋 Dataset Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{df.shape[0]:,}")
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", int(df.isnull().sum().sum()))
    c4.metric("Duplicate Rows", int(df.duplicated().sum()))

    with st.expander("📄 Raw Data Preview (first 100 rows)"):
        st.dataframe(df.head(100), use_container_width=True)

    with st.expander("📊 Descriptive Statistics"):
        if num_cols:
            st.dataframe(df[num_cols].describe().T.round(3), use_container_width=True)
        else:
            st.info("No numeric columns found.")

    with st.expander("🔍 Column Info: Data Types & Missing Values"):
        dtype_df = pd.DataFrame({
            'Column': df.columns,
            'DType': df.dtypes.astype(str).values,
            'Non-Null': df.notnull().sum().values,
            'Null Count': df.isnull().sum().values,
            'Null %': (df.isnull().sum() / len(df) * 100).round(2).values,
            'Unique Values': df.nunique().values
        })
        st.dataframe(dtype_df, use_container_width=True)

    st.markdown("---")

    # ── Univariate: Numerical ──────────────────────────────────────────────
    if num_cols:
        st.markdown("### 📊 Univariate Analysis — Numerical")
        sel_num = st.selectbox("Select numerical column", num_cols, key="eda_num")
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(df, x=sel_num, nbins=40, color_discrete_sequence=['#6366f1'],
                               marginal='box', title=f'Distribution of {sel_num}')
            fig.update_layout(**PLOTLY_THEME, height=350)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.violin(df, y=sel_num, color_discrete_sequence=['#22d3ee'],
                            box=True, points='outliers', title=f'Violin Plot: {sel_num}')
            fig.update_layout(**PLOTLY_THEME, height=350)
            st.plotly_chart(fig, use_container_width=True)

        # Stats summary
        col_stats = df[sel_num].describe()
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Mean", f"{col_stats['mean']:.4g}")
        s2.metric("Median", f"{df[sel_num].median():.4g}")
        s3.metric("Std Dev", f"{col_stats['std']:.4g}")
        s4.metric("Skewness", f"{df[sel_num].skew():.3f}")

    # ── Univariate: Categorical ────────────────────────────────────────────
    if cat_cols:
        st.markdown("### 📊 Univariate Analysis — Categorical")
        sel_cat = st.selectbox("Select categorical column", cat_cols, key="eda_cat")
        cat_counts = df[sel_cat].value_counts().reset_index()
        cat_counts.columns = [sel_cat, 'count']
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(cat_counts.head(20), x=sel_cat, y='count', color='count',
                         color_continuous_scale='Viridis', title=f'Value Counts: {sel_cat}')
            fig.update_layout(**PLOTLY_THEME, height=350, coloraxis_showscale=False, xaxis_tickangle=-20)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.pie(cat_counts.head(15), names=sel_cat, values='count', hole=0.4,
                         title=f'Share: {sel_cat}')
            fig.update_layout(**PLOTLY_THEME, height=350)
            st.plotly_chart(fig, use_container_width=True)

    # ── Bivariate Analysis ─────────────────────────────────────────────────
    if len(num_cols) >= 2:
        st.markdown("### 🔗 Bivariate Analysis")
        c1, c2, c3 = st.columns(3)
        with c1:
            x_col = st.selectbox("X axis", num_cols, key="biv_x")
        with c2:
            y_col = st.selectbox("Y axis", num_cols, index=min(1, len(num_cols)-1), key="biv_y")
        with c3:
            color_col = st.selectbox("Color by (optional)", ['None'] + cat_cols, key="biv_c")

        sample_size = min(2000, len(df))
        scatter_df = df.sample(sample_size, random_state=42) if len(df) > sample_size else df
        fig = px.scatter(scatter_df, x=x_col, y=y_col,
                         color=None if color_col == 'None' else color_col,
                         trendline='ols' if color_col == 'None' else None,
                         opacity=0.6, title=f'{x_col} vs {y_col}',
                         color_discrete_sequence=['#6366f1','#22d3ee','#10b981','#f59e0b','#ef4444'])
        fig.update_layout(**PLOTLY_THEME, height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Box by category
        if cat_cols and num_cols:
            st.markdown("#### Box Plot: Numeric by Category")
            bc1, bc2 = st.columns(2)
            with bc1:
                box_cat = st.selectbox("Category column", cat_cols, key="box_cat")
            with bc2:
                box_num = st.selectbox("Numeric column", num_cols, key="box_num")
            fig = px.box(df, x=box_cat, y=box_num, color=box_cat,
                         title=f'{box_num} by {box_cat}', points='outliers')
            fig.update_layout(**PLOTLY_THEME, height=400, showlegend=False, xaxis_tickangle=-20)
            st.plotly_chart(fig, use_container_width=True)

    # ── Correlation Heatmap ────────────────────────────────────────────────
    if len(num_cols) >= 2:
        st.markdown("### 🌡️ Correlation Heatmap")
        corr = df[num_cols].corr()
        fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='RdBu_r',
                        aspect='auto', title='Numeric Feature Correlation Matrix', zmin=-1, zmax=1)
        fig.update_layout(**PLOTLY_THEME, height=max(350, len(num_cols) * 40))
        st.plotly_chart(fig, use_container_width=True)

    # ── Outlier Detection ──────────────────────────────────────────────────
    if num_cols:
        st.markdown("### 🚨 Outlier Detection (IQR Method)")
        outlier_col = st.selectbox("Detect outliers in", num_cols, key='out_col')
        Q1 = df[outlier_col].quantile(0.25)
        Q3 = df[outlier_col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[outlier_col] < Q1 - 1.5*IQR) | (df[outlier_col] > Q3 + 1.5*IQR)]
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Outliers", len(outliers))
        c2.metric("Outlier %", f"{len(outliers)/len(df)*100:.2f}%")
        c3.metric("IQR Range", f"{Q1:.3g} – {Q3:.3g}")
        fig = go.Figure()
        fig.add_trace(go.Box(y=df[outlier_col], name=outlier_col,
                              marker_color='#6366f1', boxpoints='outliers',
                              jitter=0.3, pointpos=-1.8))
        fig.update_layout(**PLOTLY_THEME, height=350, title=f'Box Plot with Outliers: {outlier_col}')
        st.plotly_chart(fig, use_container_width=True)

    # ── Time Series ────────────────────────────────────────────────────────
    if dt_cols and num_cols:
        st.markdown("### 📅 Time Series Analysis")
        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            ts_date = st.selectbox("Date column", dt_cols, key='ts_date')
        with tc2:
            ts_metric = st.selectbox("Metric", num_cols, key='ts_metric')
        with tc3:
            ts_freq = st.selectbox("Frequency", ['D','W','ME','QE','YE'], index=2, key='ts_freq')

        ts = df[[ts_date, ts_metric]].dropna()
        ts = ts.set_index(ts_date).resample(ts_freq)[ts_metric].sum().reset_index()
        fig = px.line(ts, x=ts_date, y=ts_metric,
                      title=f'{ts_metric} over Time ({ts_freq})',
                      color_discrete_sequence=['#6366f1'])
        fig.update_traces(line_width=2)
        if len(ts) >= 4:
            fig.add_traces(go.Scatter(
                x=ts[ts_date], y=ts[ts_metric].rolling(min(4, len(ts))).mean(),
                mode='lines', name='Rolling Avg',
                line=dict(color='#22d3ee', width=2, dash='dot')
            ))
        fig.update_layout(**PLOTLY_THEME, height=350)
        st.plotly_chart(fig, use_container_width=True)

    # ── Missing value heatmap ──────────────────────────────────────────────
    if df.isnull().sum().sum() > 0:
        st.markdown("### 🕳️ Missing Value Pattern")
        missing = df.isnull().astype(int)
        sample_miss = missing.sample(min(200, len(missing)), random_state=42)
        fig = px.imshow(sample_miss.T, color_continuous_scale='Blues',
                        title='Missing Values Heatmap (sample of 200 rows)', aspect='auto')
        fig.update_layout(**PLOTLY_THEME, height=max(200, df.shape[1]*20))
        st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3: ADVANCED ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## 📈 Advanced Analytics")

    # ── Pivot Heatmap (cat × cat or cat × num) ────────────────────────────
    if len(cat_cols) >= 2 and num_cols:
        st.markdown("### 🧩 Pivot Heatmap")
        p1, p2, p3 = st.columns(3)
        with p1:
            piv_row = st.selectbox("Row (Category)", cat_cols, key='piv_row')
        with p2:
            remaining_cats = [c for c in cat_cols if c != piv_row]
            piv_col_sel = st.selectbox("Column (Category)", remaining_cats, key='piv_col')
        with p3:
            piv_val = st.selectbox("Value (Numeric)", num_cols, key='piv_val')

        try:
            pivot = df.pivot_table(values=piv_val, index=piv_row,
                                   columns=piv_col_sel, aggfunc='sum').fillna(0)
            fig = px.imshow(pivot.round(2), text_auto='.2s',
                            color_continuous_scale='Blues', aspect='auto',
                            title=f'{piv_val}: {piv_row} × {piv_col_sel}')
            fig.update_layout(**PLOTLY_THEME, height=max(300, len(pivot)*30 + 100))
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not build pivot: {e}")

    # ── Distribution comparison ────────────────────────────────────────────
    if cat_cols and num_cols:
        st.markdown("### 📦 Distribution Comparison by Group")
        dc1, dc2 = st.columns(2)
        with dc1:
            dist_cat = st.selectbox("Group by", cat_cols, key='dist_cat')
        with dc2:
            dist_num = st.selectbox("Metric", num_cols, key='dist_num')

        fig = px.box(df, x=dist_cat, y=dist_num, color=dist_cat,
                     title=f'{dist_num} distribution by {dist_cat}', points='outliers')
        fig.update_layout(**PLOTLY_THEME, height=400, showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(fig, use_container_width=True)

        # Violin
        fig2 = px.violin(df, x=dist_cat, y=dist_num, color=dist_cat,
                          box=True, title=f'Violin: {dist_num} by {dist_cat}')
        fig2.update_layout(**PLOTLY_THEME, height=380, showlegend=False, xaxis_tickangle=-20)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Grouped Aggregations ───────────────────────────────────────────────
    if cat_cols and num_cols:
        st.markdown("### 📊 Grouped Aggregation Table")
        ga1, ga2, ga3 = st.columns(3)
        with ga1:
            grp_col = st.selectbox("Group by", cat_cols, key='grp_col')
        with ga2:
            agg_col = st.selectbox("Aggregate", num_cols, key='agg_col')
        with ga3:
            agg_func = st.selectbox("Function", ['sum', 'mean', 'median', 'count', 'std', 'min', 'max'], key='agg_func')

        grp_df = df.groupby(grp_col)[agg_col].agg(agg_func).reset_index()
        grp_df.columns = [grp_col, f'{agg_func}_{agg_col}']
        grp_df = grp_df.sort_values(f'{agg_func}_{agg_col}', ascending=False)

        c1, c2 = st.columns([1, 1])
        with c1:
            st.dataframe(grp_df, use_container_width=True)
        with c2:
            fig = px.bar(grp_df.head(20), x=grp_col, y=f'{agg_func}_{agg_col}',
                         color=f'{agg_func}_{agg_col}', color_continuous_scale='Viridis',
                         title=f'{agg_func.title()} of {agg_col} by {grp_col}')
            fig.update_layout(**PLOTLY_THEME, height=350, coloraxis_showscale=False, xaxis_tickangle=-20)
            st.plotly_chart(fig, use_container_width=True)

    # ── Time-based growth (QoQ / MoM) ─────────────────────────────────────
    if dt_cols and num_cols:
        st.markdown("### 📆 Period-over-Period Growth")
        g1, g2 = st.columns(2)
        with g1:
            growth_date = st.selectbox("Date column", dt_cols, key='growth_date')
        with g2:
            growth_val = st.selectbox("Value column", num_cols, key='growth_val')

        period_df = df[[growth_date, growth_val]].dropna()
        period_df = period_df.set_index(growth_date).resample('ME')[growth_val].sum().reset_index()
        period_df['growth_pct'] = period_df[growth_val].pct_change() * 100

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=period_df[growth_date], y=period_df[growth_val],
                              name=growth_val, marker_color='#6366f1'), secondary_y=False)
        fig.add_trace(go.Scatter(x=period_df[growth_date], y=period_df['growth_pct'],
                                  mode='lines+markers', name='MoM Growth %',
                                  line=dict(color='#22d3ee', width=2.5),
                                  marker=dict(size=7)), secondary_y=True)
        fig.update_layout(**PLOTLY_THEME, height=380, title='Monthly Value & Growth Rate')
        fig.update_yaxes(title_text=growth_val, secondary_y=False)
        fig.update_yaxes(title_text="Growth %", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    # ── Scatter matrix ─────────────────────────────────────────────────────
    if len(num_cols) >= 3:
        st.markdown("### 🔭 Scatter Matrix (Pair Plot)")
        max_cols_scatter = min(5, len(num_cols))
        scatter_cols = st.multiselect("Select columns (2–5)", num_cols,
                                       default=num_cols[:min(4, len(num_cols))],
                                       key='scatter_matrix')
        if len(scatter_cols) >= 2:
            color_opt = st.selectbox("Color by", ['None'] + cat_cols, key='sm_color')
            sample_sm = df.sample(min(1000, len(df)), random_state=42)
            fig = px.scatter_matrix(
                sample_sm,
                dimensions=scatter_cols,
                color=None if color_opt == 'None' else color_opt,
                opacity=0.5,
                title='Scatter Matrix',
                color_discrete_sequence=['#6366f1','#22d3ee','#10b981','#f59e0b','#ef4444']
            )
            fig.update_layout(**PLOTLY_THEME, height=600)
            st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4: AI ANALYST (Gemini)
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## 🤖 AI Data Analyst — Powered by Gemini")
    st.markdown("Ask anything about your dataset. Gemini will analyze it in real-time.")

    # Build a generic dataset context
    def build_data_context(df):
        num_cols_ctx, cat_cols_ctx, dt_cols_ctx, _ = get_col_groups(df)
        ctx = {
            "shape": f"{df.shape[0]} rows × {df.shape[1]} columns",
            "columns": df.columns.tolist(),
            "numeric_columns": num_cols_ctx,
            "categorical_columns": cat_cols_ctx,
            "datetime_columns": dt_cols_ctx,
            "missing_values": int(df.isnull().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "sample_rows": df.head(5).to_dict(orient='records'),
        }
        if num_cols_ctx:
            ctx["numeric_stats"] = df[num_cols_ctx].describe().to_dict()
        if cat_cols_ctx:
            ctx["categorical_value_counts"] = {
                col: df[col].value_counts().head(10).to_dict()
                for col in cat_cols_ctx[:5]
            }
        return ctx

    ctx = build_data_context(df)

    file_name_for_prompt = uploaded.name if uploaded else "sample e-commerce dataset"
    SYSTEM_PROMPT = f"""You are an expert data analyst. The user has uploaded a dataset called '{file_name_for_prompt}'.

DATASET OVERVIEW:
- Shape: {ctx['shape']}
- Columns: {ctx['columns']}
- Numeric columns: {ctx['numeric_columns']}
- Categorical columns: {ctx['categorical_columns']}
- DateTime columns: {ctx['datetime_columns']}
- Missing values: {ctx['missing_values']}
- Duplicate rows: {ctx['duplicate_rows']}

SAMPLE DATA (first 5 rows):
{ctx['sample_rows']}

NUMERIC STATS:
{ctx.get('numeric_stats', 'N/A')}

CATEGORICAL VALUE COUNTS (top 10 each):
{ctx.get('categorical_value_counts', 'N/A')}

Your job:
- Provide clear, structured, actionable insights
- Use bullet points and numbers where helpful
- Suggest visualizations, patterns, anomalies, or next-steps when relevant
- Be concise but thorough
- If asked for recommendations, give specific ones based on the data context above"""

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Quick question buttons
    st.markdown("**💡 Quick Questions:**")
    quick_qs = [
        "Give me an overview of this dataset",
        "What are the key patterns and trends?",
        "Are there data quality issues I should know about?",
        "What are the most important columns and why?",
        "What analysis would you recommend for this data?",
    ]
    q_cols1 = st.columns(3)
    for i, q in enumerate(quick_qs[:3]):
        if q_cols1[i].button(q, key=f"quick_{i}", use_container_width=True):
            st.session_state.pending_query = q

    q_cols2 = st.columns(2)
    for i, q in enumerate(quick_qs[3:]):
        if q_cols2[i].button(q, key=f"quick2_{i}", use_container_width=True):
            st.session_state.pending_query = q

    st.markdown("---")

    # Chat display
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f"""
                <div style='margin: 12px 0'>
                    <div class='chat-msg-label'>YOU</div>
                    <div class='chat-msg-user'>{msg['content']}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='margin: 12px 0'>
                    <div class='chat-msg-label'>GEMINI</div>
                    <div class='chat-msg-ai'>{msg['content']}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align:center;padding:40px;color:#64748b;background:var(--surface);border-radius:16px;'>
            <div style='font-size:2.5rem;margin-bottom:12px'>🤖</div>
            <div style='font-size:1rem'>Ask Gemini anything about your data</div>
            <div style='font-size:0.8rem;margin-top:8px'>Use the quick questions above or type your own</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Input
    user_input = st.text_area(
        "💬 Your question:",
        height=80,
        value=st.session_state.pop("pending_query", ""),
        placeholder="e.g. What are the top-performing categories? Which columns have the most outliers?"
    )

    col_a, col_b, col_c = st.columns([2, 1, 1])
    send_btn = col_a.button("🚀 Ask Gemini", use_container_width=True)
    clear_btn = col_b.button("🗑️ Clear Chat", use_container_width=True)
    export_btn = col_c.button("📋 Export Chat", use_container_width=True)

    if clear_btn:
        st.session_state.chat_history = []
        st.rerun()

    if export_btn and st.session_state.chat_history:
        chat_text = "\n\n".join([
            f"{'USER' if m['role']=='user' else 'GEMINI'}: {m['content']}"
            for m in st.session_state.chat_history
        ])
        st.download_button("⬇️ Download Chat", chat_text, "chat_export.txt", "text/plain")

    if send_btn and user_input.strip():
        key_to_use = st.session_state.get("gemini_key", "")
        if not key_to_use:
            st.error("⚠️ Please enter your Gemini API key in the sidebar.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
            with st.spinner("Gemini is analyzing your data..."):
                try:
                    genai.configure(api_key=key_to_use)
                    model = genai.GenerativeModel(
                        model_name="gemini-2.0-flash",
                        system_instruction=SYSTEM_PROMPT,
                    )
                    # Build Gemini-format history (all but the last user message)
                    gemini_history = []
                    for m in st.session_state.chat_history[:-1]:
                        role = "user" if m["role"] == "user" else "model"
                        gemini_history.append({"role": role, "parts": [m["content"]]})

                    chat = model.start_chat(history=gemini_history)
                    response = chat.send_message(user_input.strip())
                    answer = response.text
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    st.rerun()
                except Exception as e:
                    err = str(e)
                    if "API_KEY" in err.upper() or "401" in err or "403" in err:
                        st.error("❌ Invalid API key. Please check your Gemini API key.")
                    else:
                        st.error(f"❌ Error: {err}")
                    st.session_state.chat_history.pop()
