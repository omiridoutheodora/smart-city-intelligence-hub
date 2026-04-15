# 🏙️ Smart City Intelligence Hub

A Streamlit dashboard demonstrating the evolution of Business Intelligence from static reporting to AI-driven urban intelligence. Built as a companion piece to the report: *The Dashboard Is Dead: How AI Is Reshaping BI for Smart Cities*.

## Quick Setup (3 steps)

### 1. Install dependencies
```bash
cd smart_city_dashboard
pip install -r requirements.txt
```

### 2. Generate synthetic city data
```bash
python generate_data.py
```
This creates 5 CSV files in the `data/` folder: parking transactions, sensor readings, service requests, energy usage, and AI alerts.

### 3. Run the dashboard
```bash
streamlit run app.py
```
The dashboard will open in your browser at `http://localhost:8501`.

## Optional: Enable Natural Language Querying (Section 3)

The NLQ feature uses Claude's API. To enable it:

1. Get an API key from [console.anthropic.com](https://console.anthropic.com)
2. Set it as an environment variable:
```bash
export ANTHROPIC_API_KEY="your-key-here"
```
3. Restart the dashboard

Without the API key, Section 3 falls back to keyword-based responses (still works, just less flexible).

## Dashboard Structure

| Section | What It Shows | BI Evolution Stage |
|---------|--------------|-------------------|
| Section 1 | KPI cards, bar charts, static metrics | Traditional BI (rearview mirror) |
| Section 2 | Interactive filters, sensor monitoring, drill-downs | AI-Enhanced BI (dynamic exploration) |
| Section 3 | Natural language question input | NLQ-Powered BI (conversational) |
| Section 4 | Automated alerts with auto-action badges | Agentic BI (autonomous intelligence) |

## Tech Stack
- **Streamlit** — dashboard framework
- **Plotly** — interactive charts
- **Pandas/NumPy** — data processing
- **Anthropic API** — natural language querying (optional)
