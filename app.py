"""
Smart City Intelligence Hub
A Streamlit dashboard demonstrating the evolution of BI from static reporting to AI-driven intelligence.
"""
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Smart City Intelligence Hub",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DISTRICT_COLORS = {
    "Central": "#5f8fd8",
    "Riverside": "#6aa9d8",
    "Northgate": "#67bfb5",
    "Eastfield": "#7cc989",
    "Harbour": "#d8b06a",
    "Greenpark": "#9a85d6",
}
CHART_COLORS = ["#5f8fd8", "#6aa9d8", "#67bfb5", "#7cc989", "#d8b06a"]
MUTED_STATUS_COLORS = {
    "critical": "#d97a7a",
    "warning": "#d8b06a",
    "normal": "#8dc6a1",
}

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    .stApp {
        font-family: 'DM Sans', sans-serif;
        background-color: #f7f9fb;
        color: #0f172a;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .main-header {
        background: #0f766e;
        padding: 2.45rem 2.1rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        border: 1px solid #0b5f59;
        box-shadow: 0 8px 22px rgba(15, 118, 110, 0.14);
        text-align: center;
    }

    .main-header h1 {
        color: #ffffff;
        font-size: 2.45rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.04em;
    }

    .main-header p {
        color: #ccfbf1;
        font-size: 1.08rem;
        margin: 0;
        font-weight: 600;
    }

    .section-header {
        background: #dff3ef;
        border: 1px solid #bfe4dc;
        border-left: 6px solid #2aaea0;
        padding: 1.1rem 1.2rem 1.1rem 1.2rem;
        border-radius: 12px;
        margin: 2.25rem 0 1.15rem 0;
    }

    .section-header h2 {
        color: #0f172a;
        font-size: 1.52rem;
        font-weight: 900;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.02em;
    }

    .section-header .subtitle {
        color: #5f7288;
        font-size: 1.04rem;
        margin: 0.38rem 0 0 0;
        font-weight: 650;
    }

    .kpi-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.15rem 1rem;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        height: 100%;
    }

    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.9rem;
        font-weight: 700;
        color: #0f172a;
        margin: 0.3rem 0;
    }

    .kpi-label {
        color: #64748b;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
    }

    .kpi-delta {
        font-size: 0.78rem;
        margin-top: 0.25rem;
        font-weight: 600;
    }

    .kpi-up { color: #16a34a; }
    .kpi-down { color: #dc2626; }

    .insight-caption {
        color: #475569;
        font-size: 0.84rem;
        margin: 0.15rem 0 0.8rem 0;
    }

    .sidebar-note {
        color: #64748b;
        font-size: 0.8rem;
        line-height: 1.55;
    }

    .alert-card {
        border-radius: 10px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.6rem;
        border: 1px solid #e5e7eb;
        font-size: 0.86rem;
        line-height: 1.5;
    }

    .alert-critical {
        background: #fef2f2;
        color: #b91c1c;
        border-left: 4px solid #ef4444;
    }

    .alert-high {
        background: #fffbeb;
        color: #92400e;
        border-left: 4px solid #f59e0b;
    }

    .alert-medium {
        background: #eff6ff;
        color: #1e3a8a;
        border-left: 4px solid #60a5fa;
    }

    .alert-low {
        background: #f0fdf4;
        color: #166534;
        border-left: 4px solid #22c55e;
    }

    .alert-time {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #64748b;
    }

    .alert-badge {
        display: inline-block;
        padding: 0.12rem 0.45rem;
        border-radius: 999px;
        font-size: 0.66rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-left: 0.45rem;
    }

    .badge-auto {
        background: #dcfce7;
        color: #15803d;
    }

    .badge-review {
        background: #fee2e2;
        color: #b91c1c;
    }

    .alert-severity {
        text-transform: uppercase;
        font-size: 0.68rem;
        font-weight: 700;
        margin-left: 0.45rem;
        letter-spacing: 0.04em;
    }

    .nlq-box {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1.1rem 1.2rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }

    .nlq-example {
        background: #ffffff;
        border: 1px solid #dbeafe;
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        margin: 0.3rem 0;
        color: #475569;
        font-size: 0.82rem;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    [data-testid="stSidebar"] * {
        color: #0f172a;
    }

    .stMultiSelect [data-baseweb="tag"] {
        background-color: #dff3ef !important;
        border: 1px solid #9fd9ce !important;
    }

    .stMultiSelect [data-baseweb="tag"] span {
        color: #0f172a !important;
        font-weight: 600;
    }

    .stMultiSelect [data-baseweb="tag"] svg {
        fill: #2aaea0 !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""",
    unsafe_allow_html=True,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def build_global_benchmark_data() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {"city": "Singapore", "region": "Asia", "lat": 1.3521, "lon": 103.8198, "ai_score": 92, "focus": "mobility optimisation"},
            {"city": "London", "region": "Europe", "lat": 51.5072, "lon": -0.1276, "ai_score": 88, "focus": "urban services"},
            {"city": "Dubai", "region": "Middle East", "lat": 25.2048, "lon": 55.2708, "ai_score": 84, "focus": "digital government"},
            {"city": "New York", "region": "North America", "lat": 40.7128, "lon": -74.0060, "ai_score": 86, "focus": "transport analytics"},
            {"city": "Toronto", "region": "North America", "lat": 43.6532, "lon": -79.3832, "ai_score": 81, "focus": "energy efficiency"},
            {"city": "São Paulo", "region": "South America", "lat": -23.5505, "lon": -46.6333, "ai_score": 73, "focus": "public safety"},
            {"city": "Nairobi", "region": "Africa", "lat": -1.2921, "lon": 36.8219, "ai_score": 69, "focus": "citizen services"},
            {"city": "Sydney", "region": "Oceania", "lat": -33.8688, "lon": 151.2093, "ai_score": 79, "focus": "sustainability"},
        ]
    )


@st.cache_data
def load_data():
    parking = pd.read_csv(os.path.join(DATA_DIR, "parking_transactions.csv"))
    parking["date"] = pd.to_datetime(parking["date"])

    sensors = pd.read_csv(os.path.join(DATA_DIR, "sensor_readings.csv"))
    sensors["date"] = pd.to_datetime(sensors["date"])

    requests = pd.read_csv(os.path.join(DATA_DIR, "service_requests.csv"))
    requests["date"] = pd.to_datetime(requests["date"])

    energy = pd.read_csv(os.path.join(DATA_DIR, "energy_usage.csv"))
    energy["date"] = pd.to_datetime(energy["date"])

    alerts = pd.read_csv(os.path.join(DATA_DIR, "ai_alerts.csv"))
    alerts["timestamp"] = pd.to_datetime(alerts["timestamp"])

    return parking, sensors, requests, energy, alerts


parking, sensors, requests, energy, alerts = load_data()

with st.sidebar:
    st.markdown("### Dashboard Filters")
    st.markdown("---")

    selected_districts = st.multiselect(
        "Urban Zones (generic city model)",
        options=sorted(parking["district"].unique()),
        default=sorted(parking["district"].unique()),
    )
    st.markdown(
        "<p class='sidebar-note'>These zones are fictional placeholders rather than London boroughs or one specific real city. That keeps the dashboard internationally reusable.</p>",
        unsafe_allow_html=True,
    )

    date_range = st.date_input(
        "Date Range",
        value=(parking["date"].min().date(), parking["date"].max().date()),
        min_value=parking["date"].min().date(),
        max_value=parking["date"].max().date(),
    )

    start_date, end_date = (
        (date_range[0], date_range[1])
        if len(date_range) == 2
        else (date_range[0], parking["date"].max().date())
    )

    st.markdown("---")
    st.markdown("**About**")
    st.markdown(
        "<span style='color:#64748b; font-size:0.84rem; line-height:1.65;'>This dashboard demonstrates the evolution of BI from static reporting to AI-driven urban intelligence across generic urban zones rather than one named city. Companion to <em>The Dashboard Is Dead.</em></span>",
        unsafe_allow_html=True,
    )

mask_p = parking["district"].isin(selected_districts) & (parking["date"].dt.date >= start_date) & (parking["date"].dt.date <= end_date)
mask_s = sensors["district"].isin(selected_districts) & (sensors["date"].dt.date >= start_date) & (sensors["date"].dt.date <= end_date)
mask_r = requests["district"].isin(selected_districts) & (requests["date"].dt.date >= start_date) & (requests["date"].dt.date <= end_date)
mask_e = energy["district"].isin(selected_districts) & (energy["date"].dt.date >= start_date) & (energy["date"].dt.date <= end_date)
mask_a = alerts["district"].isin(selected_districts) & (alerts["timestamp"].dt.date >= start_date) & (alerts["timestamp"].dt.date <= end_date)

f_parking = parking[mask_p]
f_sensors = sensors[mask_s]
f_requests = requests[mask_r]
f_energy = energy[mask_e]
f_alerts = alerts[mask_a]

PLOT_LAYOUT = dict(
    template="plotly_white",
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(family="DM Sans", color="#334155", size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    title_font=dict(size=20, color="#0f172a"),
)


def style_figure(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        **PLOT_LAYOUT,
        xaxis=dict(showgrid=True, gridcolor="#e5e7eb", zeroline=False, linecolor="#cbd5e1", title_font=dict(size=13), tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor="#e5e7eb", zeroline=False, linecolor="#cbd5e1", title_font=dict(size=13), tickfont=dict(size=11)),
    )
    return fig


st.markdown(
    '<div class="main-header"><h1>SMART CITY INTELLIGENCE HUB</h1><p>From static dashboards to AI-driven urban intelligence</p></div>',
    unsafe_allow_html=True,
)

# ── SECTION 1: TRADITIONAL BI ──
st.markdown(
    '<div class="section-header"><h2>Section 1: Traditional BI — City Performance Overview</h2><p class="subtitle">Static KPIs and retrospective reporting — the rearview mirror</p></div>',
    unsafe_allow_html=True,
)

total_parking_rev = f_parking["revenue_gbp"].sum()
total_txns = f_parking["transactions"].sum()
avg_occupancy = f_parking["occupancy_pct"].mean()
total_reqs = len(f_requests)
res_rate = f_requests["resolved"].mean() * 100 if len(f_requests) > 0 else 0

for col, label, value, delta, delta_cls in zip(
    st.columns(5),
    ["Parking Revenue", "Total Transactions", "Avg Occupancy", "Service Requests", "Resolution Rate"],
    [
        f"£{total_parking_rev/1e6:.1f}M",
        f"{total_txns/1e6:.2f}M",
        f"{avg_occupancy:.1f}%",
        f"{total_reqs:,}",
        f"{res_rate:.1f}%",
    ],
    [
        "▲ 12.3% vs prior period",
        "▲ 8.1% vs prior period",
        "▼ 2.4% vs prior period",
        "▲ 5.7% vs prior period",
        "▲ 3.2% vs prior period",
    ],
    ["kpi-up", "kpi-up", "kpi-down", "kpi-up", "kpi-up"],
):
    col.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-delta {delta_cls}">{delta}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
c1, c2 = st.columns(2)

with c1:
    mr = f_parking.groupby(f_parking["date"].dt.to_period("M")).agg(revenue=("revenue_gbp", "sum")).reset_index()
    mr["date"] = mr["date"].dt.to_timestamp()

    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=mr["date"],
            y=mr["revenue"],
            mode="lines+markers",
            line=dict(color="#5f8fd8", width=3),
            marker=dict(size=6, color="#5f8fd8"),
            fill="tozeroy",
            fillcolor="rgba(95, 143, 216, 0.08)",
        )
    )
    fig1.update_layout(title="Monthly Parking Revenue", yaxis_title="Revenue (£)")
    style_figure(fig1)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    rc = f_requests.groupby("category").size().reset_index(name="count").sort_values("count", ascending=True)
    fig2 = go.Figure()
    fig2.add_trace(
        go.Bar(
            y=rc["category"],
            x=rc["count"],
            orientation="h",
            marker_color="#6aa9d8",
            opacity=0.9,
        )
    )
    fig2.update_layout(title="Service Requests by Category", xaxis_title="Count")
    style_figure(fig2)
    st.plotly_chart(fig2, use_container_width=True)

# ── SECTION 2: AI-ENHANCED BI ──
st.markdown(
    '<div class="section-header"><h2>Section 2: AI-Enhanced BI — Dynamic Exploration</h2><p class="subtitle">Interactive filtering, drill-down analysis, and real-time sensor monitoring</p></div>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(["Sensor Network", "Energy Analytics", "Request Analysis"])

with tab1:
    sensor_type = st.selectbox("Sensor Type", sorted(f_sensors["sensor_type"].unique()))
    sf = f_sensors[f_sensors["sensor_type"] == sensor_type]

    st.markdown('<p class="insight-caption"><strong>Zone-level sensor patterns and anomalies over time</strong></p>', unsafe_allow_html=True)

    t1c1, t1c2 = st.columns(2)

    with t1c1:
        district_avg = sf.groupby("district")["value"].mean().reset_index().sort_values("value", ascending=False)
        fig_district = go.Figure(
            go.Bar(
                x=district_avg["district"],
                y=district_avg["value"],
                marker_color="#88bdb5",
                opacity=0.92,
            )
        )
        fig_district.update_layout(
            title=f"Average {sensor_type.replace('_', ' ').title()} by Zone",
            showlegend=False,
            yaxis_title="Average value",
            xaxis_title="Zone",
        )
        style_figure(fig_district)
        st.plotly_chart(fig_district, use_container_width=True)

    with t1c2:
        sc = sf.groupby(["district", "status"]).size().reset_index(name="count")
        figs = px.bar(
            sc,
            x="district",
            y="count",
            color="status",
            title="Sensor Status by Zone",
            color_discrete_map=MUTED_STATUS_COLORS,
            barmode="group",
        )
        figs.update_layout(yaxis_title="Count", xaxis_title="Zone")
        style_figure(figs)
        st.plotly_chart(figs, use_container_width=True)

    ds = sf.groupby(["date", "district"]).agg(avg_value=("value", "mean")).reset_index().sort_values(["district", "date"])
    ds["rolling_avg"] = ds.groupby("district")["avg_value"].transform(lambda x: x.rolling(7, min_periods=1).mean())
st.markdown(
    '<p class="insight-caption"><strong>7-day rolling trend highlighting sustained sensor patterns across zones</strong></p>',
    unsafe_allow_html=True,
)

fig3 = px.line(
    ds,
    x="date",
    y="rolling_avg",
    color="district",
    title=f"{sensor_type.replace('_', ' ').title()} — 7-Day Rolling Trend by Zone",
    color_discrete_map=DISTRICT_COLORS,
)

fig3.update_traces(line=dict(width=1.7), opacity=0.8)
fig3.update_layout(yaxis_title="7-day rolling average", xaxis_title="Date")

style_figure(fig3)
st.plotly_chart(fig3, use_container_width=True)

with tab2:
    e1, e2 = st.columns(2)

    with e1:
        me = f_energy.groupby(f_energy["date"].dt.to_period("M")).agg(consumption=("consumption_kwh", "sum")).reset_index()
        me["date"] = me["date"].dt.to_timestamp()
        fig4 = go.Figure()
        fig4.add_trace(
            go.Bar(
                x=me["date"],
                y=me["consumption"],
                marker_color="#8fbfba",
                opacity=0.88,
            )
        )
        fig4.update_layout(title="Monthly Energy Consumption", yaxis_title="kWh")
        style_figure(fig4)
        st.plotly_chart(fig4, use_container_width=True)

    with e2:
        mrn = f_energy.groupby(f_energy["date"].dt.to_period("M"))["renewable_pct"].mean().reset_index()
        mrn["date"] = mrn["date"].dt.to_timestamp()
        fig5 = go.Figure()
        fig5.add_trace(
            go.Scatter(
                x=mrn["date"],
                y=mrn["renewable_pct"],
                mode="lines+markers",
                line=dict(color="#7cc989", width=2.5),
                marker=dict(size=6, color="#7cc989"),
            )
        )
        fig5.update_layout(title="Renewable Energy Share", yaxis_title="%")
        style_figure(fig5)
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown('<p class="insight-caption"><strong>EV charging demand across zones and time</strong></p>', unsafe_allow_html=True)
    evm = f_energy.copy()
    evm["month"] = evm["date"].dt.to_period("M").astype(str)
    evp = evm.groupby(["district", "month"])["ev_charging_kwh"].sum().reset_index().pivot(index="district", columns="month", values="ev_charging_kwh")
    fig_ev = go.Figure(
        data=go.Heatmap(
            z=evp.values,
            x=evp.columns.tolist(),
            y=evp.index.tolist(),
            colorscale=[[0, "#eff6ff"], [0.25, "#dbeafe"], [0.5, "#9cc7e6"], [0.75, "#6aa9d8"], [1, "#5f8fd8"]],
            colorbar=dict(title="kWh"),
        )
    )
    fig_ev.update_layout(title="EV Charging Demand — Heatmap by Zone and Month", xaxis=dict(title="Month", tickangle=-45), yaxis=dict(title=""))
    style_figure(fig_ev)
    st.plotly_chart(fig_ev, use_container_width=True)

with tab3:
    r1, r2 = st.columns(2)

    with r1:
        scc = f_requests.groupby("source").size().reset_index(name="count").sort_values("count", ascending=False)
        fig6 = px.bar(
            scc,
            x="source",
            y="count",
            color="source",
            title="Request Sources",
            color_discrete_sequence=["#7fa6d9", "#8fb5d8", "#8fc8c0", "#9fceb1", "#d4b37a"],
        )
        fig6.update_layout(showlegend=False, xaxis_title="Source", yaxis_title="Count")
        style_figure(fig6)
        st.plotly_chart(fig6, use_container_width=True)

    with r2:
        stc = f_requests.groupby("sentiment").size().reset_index(name="count")
        stc["sentiment"] = pd.Categorical(
            stc["sentiment"],
            categories=["satisfied", "neutral", "concerned", "frustrated", "urgent"],
            ordered=True,
        )
        stc = stc.sort_values("sentiment")
        fig7 = px.bar(
            stc,
            x="sentiment",
            y="count",
            title="Citizen Sentiment Analysis",
            color="sentiment",
            color_discrete_map={
                "frustrated": "#cf8a8a",
                "urgent": "#d4b37a",
                "concerned": "#93b3d1",
                "neutral": "#aeb8c4",
                "satisfied": "#95c3a4",
            },
        )
        fig7.update_layout(showlegend=False, xaxis_title="Sentiment", yaxis_title="Count")
        style_figure(fig7)
        st.plotly_chart(fig7, use_container_width=True)

    rbc = f_requests.groupby("category")["resolution_days"].mean().reset_index().sort_values("resolution_days", ascending=True)
    fig_res = go.Figure()
    fig_res.add_trace(
        go.Bar(
            y=rbc["category"],
            x=rbc["resolution_days"],
            orientation="h",
            marker_color="#a493d8",
            opacity=0.9,
        )
    )
    fig_res.update_layout(title="Average Resolution Time by Category (Days)", xaxis_title="Days")
    style_figure(fig_res)
    st.plotly_chart(fig_res, use_container_width=True)

# ── SECTION 3: NLQ ──
st.markdown(
    '<div class="section-header"><h2>Section 3: Natural Language Querying — Ask Your City</h2><p class="subtitle">Type a question in plain English. No SQL required.</p></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="nlq-box"><p style="color:#475569; font-size:0.85rem; margin:0;">Gartner predicts that by 2026, 40% of analytics queries will use natural language. This section demonstrates that shift. Ask any question about parking, energy, service requests, or sensor data.</p></div>',
    unsafe_allow_html=True,
)
st.markdown("**Example questions:**")
ex1, ex2 = st.columns(2)
with ex1:
    st.markdown(
        '<div class="nlq-example">Which district had the most parking violations?</div><div class="nlq-example">What is the average air quality across all districts?</div>',
        unsafe_allow_html=True,
    )
with ex2:
    st.markdown(
        '<div class="nlq-example">Show me the trend in EV charging demand</div><div class="nlq-example">Which category has the longest resolution time?</div>',
        unsafe_allow_html=True,
    )

user_question = st.text_input(
    "Ask a question about the city data:",
    placeholder="e.g. Which district generates the most parking revenue?",
)
if user_question:
    with st.spinner("Analysing city data..."):
        ps = f_parking.groupby("district").agg(
            total_revenue=("revenue_gbp", "sum"),
            total_transactions=("transactions", "sum"),
            avg_occupancy=("occupancy_pct", "mean"),
            total_violations=("violations", "sum"),
        ).round(2).to_string()
        es = f_energy.groupby("district").agg(
            total_consumption=("consumption_kwh", "sum"),
            avg_renewable_pct=("renewable_pct", "mean"),
            total_ev_charging=("ev_charging_kwh", "sum"),
        ).round(2).to_string()
        rs = f_requests.groupby("category").agg(
            count=("category", "size"),
            avg_resolution_days=("resolution_days", "mean"),
            resolution_rate=("resolved", "mean"),
        ).round(2).to_string()
        ss = f_sensors.groupby(["district", "sensor_type"])["value"].mean().round(2).unstack().to_string()

        try:
            import anthropic

            client = anthropic.Anthropic()
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=500,
                system="You are a smart city analytics assistant. Answer concisely with specific numbers. 2-3 sentences max.",
                messages=[
                    {
                        "role": "user",
                        "content": f"Based on this data, answer: {user_question}\n\nPARKING:\n{ps}\n\nENERGY:\n{es}\n\nREQUESTS:\n{rs}\n\nSENSORS:\n{ss}",
                    }
                ],
            )
            st.success(response.content[0].text)
        except Exception:
            q = user_question.lower()
            if "parking" in q and ("revenue" in q or "most" in q):
                t = f_parking.groupby("district")["revenue_gbp"].sum()
                st.success(f"**{t.idxmax()}** generates the highest parking revenue at **£{t.max():,.0f}**.")
            elif "violation" in q:
                t = f_parking.groupby("district")["violations"].sum()
                st.success(f"**{t.idxmax()}** has the most violations with **{t.max():,}** recorded.")
            elif "air quality" in q or "aqi" in q:
                t = f_sensors[f_sensors["sensor_type"] == "air_quality"].groupby("district")["value"].mean()
                st.success(f"AQI ranges from **{t.min():.1f}** to **{t.max():.1f}**. **{t.idxmax()}** has the highest readings.")
            elif "ev" in q or "charging" in q:
                t = f_energy.groupby("district")["ev_charging_kwh"].sum()
                st.success(f"**{t.idxmax()}** has the highest EV charging demand at **{t.max():,.0f} kWh**.")
            elif "resolution" in q or "longest" in q:
                t = f_requests.groupby("category")["resolution_days"].mean()
                st.success(f"**{t.idxmax()}** has the longest resolution time at **{t.max():.1f} days**.")
            elif "energy" in q or "consumption" in q:
                t = f_energy.groupby("district")["consumption_kwh"].sum()
                st.success(f"**{t.idxmax()}** has the highest energy consumption at **{t.max():,.0f} kWh**.")
            elif "renewable" in q:
                t = f_energy.groupby("district")["renewable_pct"].mean()
                st.success(f"**{t.idxmax()}** leads in renewable energy share at **{t.max():.1f}%**.")
            else:
                st.info("Try asking about parking revenue, violations, air quality, EV charging, energy consumption, or resolution times.")

# ── SECTION 4: AGENTIC BI ──
st.markdown(
    '<div class="section-header"><h2>Section 4: Agentic BI — Automated Intelligence Alerts</h2><p class="subtitle">AI systems that observe, decide, and act — the operational frontier of BI</p></div>',
    unsafe_allow_html=True,
)

total_alerts = len(f_alerts)
critical_alerts = len(f_alerts[f_alerts["severity"] == "critical"])
auto_actions = f_alerts["action_taken"].sum()
human_review = f_alerts["requires_human_review"].sum()

for col, label, value, color in zip(
    st.columns(4),
    ["Total Alerts", "Critical Alerts", "Auto-Actioned", "Needs Human Review"],
    [f"{total_alerts:,}", str(critical_alerts), f"{int(auto_actions):,}", f"{int(human_review):,}"],
    ["#0f172a", "#dc2626", "#16a34a", "#d97706"],
):
    col.markdown(
        f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value" style="color:{color};">{value}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
alert_severity = st.multiselect(
    "Filter by severity:",
    options=["critical", "high", "medium", "low"],
    default=["critical", "high"],
)
recent_alerts = f_alerts[f_alerts["severity"].isin(alert_severity)].sort_values("timestamp", ascending=False).head(12)

for _, a in recent_alerts.iterrows():
    ab = '<span class="alert-badge badge-auto">AUTO-ACTIONED</span>' if a["action_taken"] else ""
    rb = '<span class="alert-badge badge-review">NEEDS REVIEW</span>' if a["requires_human_review"] else ""
    st.markdown(
        f'<div class="alert-card alert-{a["severity"]}"><span class="alert-time">{a["timestamp"]}</span><span class="alert-severity">{a["severity"]}</span>{ab}{rb}<br><span style="margin-top:0.3rem;display:inline-block;">{a["message"]}</span></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)
al1, al2 = st.columns(2)
with al1:
    abc = f_alerts.groupby("category").size().reset_index(name="count").sort_values("count", ascending=True)
    fac = go.Figure()
    fac.add_trace(
        go.Bar(
            y=abc["category"],
            x=abc["count"],
            orientation="h",
            marker_color="#d8b06a",
            opacity=0.9,
        )
    )
    fac.update_layout(title="Alerts by Category")
    style_figure(fac)
    st.plotly_chart(fac, use_container_width=True)
with al2:
    abd = f_alerts.groupby("district").size().reset_index(name="count").sort_values("count", ascending=True)
    fad = go.Figure()
    fad.add_trace(
        go.Bar(
            y=abd["district"],
            x=abd["count"],
            orientation="h",
            marker_color="#5f8fd8",
            opacity=0.9,
        )
    )
    fad.update_layout(title="Alerts by Zone")
    style_figure(fad)
    st.plotly_chart(fad, use_container_width=True)

st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#64748b; font-size:0.78rem;'>Smart City Intelligence Hub — Built with Streamlit  |  Companion to <em>The Dashboard Is Dead: How AI Is Reshaping BI for Smart Cities</em>  |  Business Intelligence Module, Hult International Business School, Spring 2026</p>",
    unsafe_allow_html=True,
)
