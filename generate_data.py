"""
Generate synthetic smart city data for the BI dashboard.
Run this once to create the CSV files the dashboard reads.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Config ──
DISTRICTS = ["Central", "Riverside", "Northgate", "Eastfield", "Harbour", "Greenpark"]
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2026, 3, 31)
days = (END_DATE - START_DATE).days


# ── 1. Parking Transactions ──
def generate_parking():
    records = []
    for day_offset in range(days):
        date = START_DATE + timedelta(days=day_offset)
        weekday = date.weekday()
        for district in DISTRICTS:
            base = {"Central": 220, "Riverside": 150, "Northgate": 130,
                    "Eastfield": 100, "Harbour": 180, "Greenpark": 90}[district]
            # weekday boost
            if weekday < 5:
                base = int(base * 1.2)
            # seasonal pattern
            month_factor = 1 + 0.15 * np.sin(2 * np.pi * (date.month - 3) / 12)
            daily_txns = int(base * month_factor + np.random.normal(0, base * 0.15))
            daily_txns = max(daily_txns, 20)
            revenue = round(daily_txns * np.random.uniform(2.5, 5.5), 2)
            violations = max(0, int(np.random.normal(daily_txns * 0.08, daily_txns * 0.03)))
            records.append({
                "date": date.strftime("%Y-%m-%d"),
                "district": district,
                "transactions": daily_txns,
                "revenue_gbp": revenue,
                "violations": violations,
                "avg_duration_mins": round(np.random.normal(95, 25), 1),
                "occupancy_pct": round(min(99, max(15, np.random.normal(72, 15))), 1),
            })
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(OUTPUT_DIR, "parking_transactions.csv"), index=False)
    print(f"Parking: {len(df)} rows")
    return df


# ── 2. IoT Sensor Readings ──
def generate_sensors():
    records = []
    sensor_types = ["air_quality", "noise_level", "temperature", "humidity", "traffic_flow"]
    for day_offset in range(0, days, 1):
        date = START_DATE + timedelta(days=day_offset)
        for district in DISTRICTS:
            for sensor in sensor_types:
                hour_readings = []
                for hour in [8, 12, 16, 20]:
                    if sensor == "air_quality":
                        value = round(np.random.normal(45, 18), 1)  # AQI
                    elif sensor == "noise_level":
                        value = round(np.random.normal(62, 12), 1)  # dB
                    elif sensor == "temperature":
                        seasonal = 10 + 8 * np.sin(2 * np.pi * (date.month - 1) / 12)
                        value = round(seasonal + np.random.normal(0, 3), 1)
                    elif sensor == "humidity":
                        value = round(np.random.normal(65, 15), 1)
                    else:  # traffic_flow
                        base_flow = 800 if hour in [8, 16] else 400
                        value = max(50, int(np.random.normal(base_flow, 150)))
                    records.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "hour": hour,
                        "district": district,
                        "sensor_type": sensor,
                        "value": value,
                        "status": np.random.choice(["normal", "warning", "critical"],
                                                     p=[0.88, 0.09, 0.03]),
                    })
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(OUTPUT_DIR, "sensor_readings.csv"), index=False)
    print(f"Sensors: {len(df)} rows")
    return df


# ── 3. Citizen Service Requests ──
def generate_service_requests():
    categories = ["Pothole Repair", "Streetlight Outage", "Noise Complaint",
                   "Illegal Parking", "Waste Collection", "EV Charger Fault",
                   "Air Quality Concern", "Traffic Signal Issue"]
    sentiments = ["frustrated", "neutral", "concerned", "urgent", "satisfied"]
    records = []
    for day_offset in range(days):
        date = START_DATE + timedelta(days=day_offset)
        n_requests = max(1, int(np.random.normal(18, 6)))
        for _ in range(n_requests):
            category = np.random.choice(categories, p=[0.18, 0.12, 0.1, 0.15, 0.15, 0.1, 0.08, 0.12])
            district = np.random.choice(DISTRICTS)
            resolution_days = max(0, int(np.random.exponential(5)))
            records.append({
                "date": date.strftime("%Y-%m-%d"),
                "district": district,
                "category": category,
                "sentiment": np.random.choice(sentiments, p=[0.2, 0.35, 0.25, 0.12, 0.08]),
                "resolution_days": resolution_days,
                "resolved": resolution_days <= 7,
                "source": np.random.choice(["app", "phone", "email", "chatbot", "social_media"],
                                            p=[0.35, 0.2, 0.15, 0.2, 0.1]),
            })
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(OUTPUT_DIR, "service_requests.csv"), index=False)
    print(f"Service Requests: {len(df)} rows")
    return df


# ── 4. Energy Usage ──
def generate_energy():
    records = []
    for day_offset in range(days):
        date = START_DATE + timedelta(days=day_offset)
        for district in DISTRICTS:
            seasonal = 1 + 0.3 * np.cos(2 * np.pi * (date.month - 1) / 12)  # higher in winter
            base = {"Central": 4500, "Riverside": 3200, "Northgate": 2800,
                    "Eastfield": 2500, "Harbour": 3800, "Greenpark": 2000}[district]
            consumption = round(base * seasonal + np.random.normal(0, base * 0.1), 1)
            renewable_pct = round(min(95, max(10, np.random.normal(42, 12))), 1)
            ev_charging_kwh = round(max(0, np.random.normal(350, 120)), 1)
            records.append({
                "date": date.strftime("%Y-%m-%d"),
                "district": district,
                "consumption_kwh": max(500, consumption),
                "renewable_pct": renewable_pct,
                "ev_charging_kwh": ev_charging_kwh,
                "peak_demand_kw": round(consumption * np.random.uniform(0.12, 0.18), 1),
            })
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(OUTPUT_DIR, "energy_usage.csv"), index=False)
    print(f"Energy: {len(df)} rows")
    return df


# ── 5. AI Alerts (simulated agentic BI output) ──
def generate_alerts():
    alert_templates = [
        ("Parking demand spike detected in {district}. Occupancy at {val}%. Recommend dynamic pricing increase.", "parking", "high"),
        ("Air quality index in {district} reached {val} AQI. Threshold exceeded. Recommend citizen advisory.", "environment", "critical"),
        ("EV charging demand in {district} surged {val}% above baseline. Recommend load balancing.", "energy", "high"),
        ("Noise levels in {district} exceeded {val} dB for 3 consecutive hours. Investigate source.", "noise", "medium"),
        ("Streetlight outage cluster detected in {district}. {val} units offline. Maintenance crew dispatched.", "infrastructure", "medium"),
        ("Traffic flow anomaly in {district}. Volume {val}% above prediction. Signal timing adjusted automatically.", "traffic", "low"),
        ("Waste collection delay in {district}. {val} bins at capacity. Route optimisation triggered.", "waste", "medium"),
        ("Citizen complaint volume in {district} up {val}% week-over-week. Sentiment trending negative.", "citizen_services", "high"),
        ("Temperature forecast: {district} expecting {val}\u00b0C. Cooling centres recommended for vulnerable populations.", "climate", "medium"),
        ("Revenue anomaly: {district} parking revenue down {val}% versus forecast. Investigate enforcement.", "finance", "high"),
    ]
    records = []
    for day_offset in range(days):
        date = START_DATE + timedelta(days=day_offset)
        n_alerts = np.random.choice([0, 1, 2, 3, 4], p=[0.1, 0.25, 0.35, 0.2, 0.1])
        for _ in range(n_alerts):
            template, category, severity = alert_templates[np.random.randint(len(alert_templates))]
            district = np.random.choice(DISTRICTS)
            val = np.random.randint(15, 95)
            message = template.format(district=district, val=val)
            action_taken = np.random.choice([True, False], p=[0.6, 0.4])
            records.append({
                "timestamp": f"{date.strftime('%Y-%m-%d')} {np.random.randint(6,22):02d}:{np.random.randint(0,59):02d}",
                "district": district,
                "category": category,
                "severity": severity,
                "message": message,
                "action_taken": action_taken,
                "requires_human_review": severity in ["critical", "high"] and not action_taken,
            })
    df = pd.DataFrame(records)
    df.to_csv(os.path.join(OUTPUT_DIR, "ai_alerts.csv"), index=False)
    print(f"AI Alerts: {len(df)} rows")
    return df


if __name__ == "__main__":
    print("Generating smart city synthetic data...\n")
    generate_parking()
    generate_sensors()
    generate_service_requests()
    generate_energy()
    generate_alerts()
    print(f"\nAll files saved to: {OUTPUT_DIR}")
